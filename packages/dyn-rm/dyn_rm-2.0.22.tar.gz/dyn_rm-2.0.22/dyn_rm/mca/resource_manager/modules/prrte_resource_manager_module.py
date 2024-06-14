from pmix import *
from time import *
from dyn_rm.hpc_system import *
from threading import *
from dyn_rm.my_pmix import *
from dyn_rm.util import *
from dyn_rm.logger import *
from dyn_rm.mca.mca import *
import argparse 
import asyncio
import os
import json
import subprocess
import tempfile


### TODO: This class does not yet implement the resource manager module interface ###

# Singleton Class
class ResourceManager(MCA):
    
    my_system = None
    dummy_pset_name = None
    output=None
    status = "STARTUP"
    process_managers=dict()
    job_mix = []
    verbosity_level = 0
    event_loop = asyncio.new_event_loop()
    my_pmix = My_PMIx()
    registered_event_handlers = dict()
    start_time = time.time()
    tmpdir = None

    _instance = None
    _lock = Lock()
    _init_called = False

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, verbosity_level = None, outputfile = None, tmpdir=None, logger = None):
        
        with self._lock:
            if not self._init_called:
                super().__init__(parent=None, parent_dir=outputfile, verbosity=verbosity_level, enable_output=True)
                if tmpdir is not None:
                    self.tmpdir = tmpdir
                self._init_called = True
        
        if None != verbosity_level:
            self.verbosity_level = verbosity_level
        if None != outputfile:
            self.output = outputfile
        if None != tmpdir:
            self.tmpdir=tmpdir
        if None != logger:
            self.logger = logger
        #else: 
        #    print("Set default logger Module")self.logger 
        #    self.logger = LoggerModule(None, verbosity_level=4)
    
    def add_job_mix(self, job_file):

        # Using readlines()
        file1 = open(job_file, 'r')
        lines = file1.readlines()

        for line in lines:
            self.job_mix.append(json.loads(line))
        
    # Start the process manager
    def start_process_manager(self, name, hosts, timeout=1):
        
        pid = -1
        if name == "PRRTE":
            v_print("Starting PRRTE", 1, self.verbosity_level)
            filename = None
            if None != self.tmpdir:
                filename = os.path.join(self.tmpdir, "pid")
            else:
                filename = os.path.join(os.getcwd(), "pid")
            # Start PRRTE
            v_print("os.system("+"prterun --report-pid "+filename+" --max-vm-size 4 --daemonize --mca ras timex --host "+hosts+")", 3, self.verbosity_level)
            os.system("prterun --report-pid "+filename+" --max-vm-size 4 --daemonize --mca ras timex --host "+hosts)

            start = time.time()
            # get the pid of the PRRTE Master
            while pid < 0:
                if time.time() - start > timeout:
                    raise Exception("PRRTE startup timed out!") 
                
                try:
                    pid = int(open(filename, 'r').readlines()[0])
                except FileNotFoundError:
                    sleep(0.1)
            try: 
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception:
                pass

        else:
            raise Exception("Process Manager not supported!")
        
        self.process_managers[name] = pid
        return pid

    # Stop the Process Manager
    def stop_process_manager(self, name):

        pid = self.process_managers[name]

        if name == "PRRTE":
            os.system("pterm --pid "+str(pid))

    # Creates a system object with the current state of the system the RM is connected to
    def init_system_from_current_state(self, system_name, scheduling_policy):

        my_system = System(system_name, scheduling_policy, verbosity_level=self.verbosity_level)
        self.my_system = my_system

        node_names = self.my_pmix.query_nodelist()
        jobids = self.my_pmix.query_namespaces()
        pset_names = self.my_pmix.query_psets()

        # Add all known PSet names
        for pset_name in pset_names:
            my_system.add_psets([PSet("no_jobid", pset_name)])
    
        # Setup the systems Node pool
        for node_name in node_names:
            slots = self.my_pmix.query_node_slots(node_name)
            node = Node(node_name, slots)
            my_system.add_nodes([node])
	
        # Setup the jobs in the system
        first_job = True
        for jobid in jobids:
            if jobid == '':
            	continue		
            job = Job(jobid)

            my_system.add_jobs([job])

            nodes = self.my_pmix.get_node_map(jobid)
            ppn = self.my_pmix.get_proc_map(jobid)

            # Insert Procs
            for node, proc_ranks in zip(nodes, ppn):
                job.add_node_names([node])

                for proc_rank in proc_ranks.split(','):
                    proc = Proc(jobid, proc_rank, node)
                    my_system.add_procs([proc])

            
            self.run_component_service(MCALoggerComponent, "LOG", "EVENT", 
                DefaultJobLogger, "JOB_STARTED", job)

            # Set jobids for the jobs PSets
            job_pset_names = self.my_pmix.query_job_psets(jobid)
            
            for pset_name in job_pset_names:
                if first_job:
                    self.dummy_pset_name = pset_name
                    first_job = False
                my_system.pset_assign_to_job(pset_name, jobid)

        self.run_component_service(MCALoggerComponent, "LOG", "EVENTS",
                                    DefaultNodeLogger, "NODE_INIT", 
                                    [node for node in my_system.node_pool.values()]
        )

        # setup the systems PSet memberships 
        for pset_name in pset_names:
            pset_members = self.my_pmix.query_pset_membership(pset_name)

            my_system.pset_set_membership(pset_name, [ Proc.convert_to_procname(member['nspace'], member['rank']) for member in pset_members])  

            self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                                        DefaultSetLogger, "SET_DEFINED", 
                                        my_system.psets[pset_name])

        if self.verbosity_level > 0:
            my_system.print()

        return my_system  

    # EVENT_HANDLERS
    def _register_event_handler(self, event_code, pmix_cbfunc, my_cbfunc):
        id = self.my_pmix.register_event_handler(event_code, pmix_cbfunc)
        self.registered_event_handlers[event_code] = {'cbfunc': my_cbfunc, 'req_id': id}


    def register_event_handlers(self, psetop_defined_handler = None , psetop_finalized_handler = None, psetop_canceled_handler = None, pset_defined_handler = None, job_terminated_handler = None):

        if psetop_defined_handler is None:
            psetop_defined_handler = self._default_psetop_defined_handler
        if psetop_finalized_handler is None:
            psetop_finalized_handler = self._default_psetop_finalized_handler
        if psetop_canceled_handler is None:
            psetop_canceled_handler = self._default_psetop_canceled_handler
        if pset_defined_handler is None:
            pset_defined_handler = self._default_pset_defined_handler
        if job_terminated_handler is None:
            job_terminated_handler = self._default_job_terminated_handler
  
        
        self.event_loop.call_soon_threadsafe(self._register_event_handler, PMIX_EVENT_PSETOP_CANCELED, ResourceManager.setop_canceled_evhandler, psetop_canceled_handler)
        self.event_loop.call_soon_threadsafe(self._register_event_handler, PMIX_PROCESS_SET_DEFINE, ResourceManager.set_defined_evhandler, pset_defined_handler)
        self.event_loop.call_soon_threadsafe(self._register_event_handler, PMIX_EVENT_PSETOP_EXECUTED, ResourceManager.setop_finalized_evhandler, psetop_finalized_handler)
        self.event_loop.call_soon_threadsafe(self._register_event_handler, PMIX_EVENT_PSETOP_DEFINED, ResourceManager.setop_defined_evhandler, psetop_defined_handler)
        self.event_loop.call_soon_threadsafe(self._register_event_handler, PMIX_EVENT_JOB_END, ResourceManager.job_terminated_evhandler, job_terminated_handler)


    def _default_job_terminated_handler(self, info):

        jobid = None
        for item in info:
            if item['key'] == PMIX_EVENT_AFFECTED_PROC.decode("utf-8"):
                jobid = item['value']['nspace']

        if None == jobid:
            return

        job = self.my_system.jobs[jobid]

        self.logger.log_event_direct("JOB", "JOB_TERMINATED", job)
        
        self.my_system.remove_procs([proc_name for proc_name in job.proc_names.keys()])
        self.logger.log_events_direct("NODE", "NODE_OCCUPATION_CHANGED", [self.my_system.node_pool[node_name] for node_name in job.node_names.keys()])
        
        self.my_system.jobs.pop(jobid)

        

        t = localtime()
        current_time = strftime("%H:%M:%S", t)    
        v_print(current_time+": RECEIVED JOB '"+str(jobid)+"' TERMINATED EVENT FROM PRRTE", 3, self.verbosity_level)


    def _default_pset_defined_handler(self, info):

        pset_name = None
        members = None
        for item in info:

            if item['key'] == PMIX_PSET_NAME.decode("utf-8"):
                pset_name = item['value']
            elif item['key'] == PMIX_PSET_MEMBERS.decode("utf-8"):
                members = item['value']['array']
        if None == pset_name or None == members:
            return
        
        if len(members) <= 0:
            jobid = "no_jobid"
        else:
            jobid = members[0]['nspace'].decode("utf-8")   
        pset = PSet(jobid, pset_name)
        proc_names = [Proc.convert_to_procname( member['nspace'].decode("utf-8"), member['rank']) for member in members]
        self.my_system.add_psets([pset])
        self.my_system.pset_set_membership(pset_name, proc_names)


        self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                                    DefaultSetLogger, "SET_DEFINED", pset)

    def _default_psetop_finalized_handler(self, info):
        if info == None:
            return
        setop_id = None
        output_sets = None
        for item in info:
            if item['key'] == PMIX_ALLOC_ID.decode("utf-8"):
                setop_id = item['value']
            elif item['key'] == PMIX_PSETOP_OUTPUT.decode("utf-8"):
                output_sets = item['value'].split(',')
        setop = self.my_system.get_setop(setop_id)
        setop.output = output_sets

        self.run_component_service( MCALoggerComponent, "LOG", "EVENT", 
                                    DefaultSetOpLogger, "SETOP_FINALIZED", setop)

        if setop.op == PMIX_PSETOP_SUB or setop.op == PMIX_PSETOP_SHRINK:
            self.my_system.setop_apply(setop_id)
        else:
            node_map = self.my_pmix.get_node_map(setop.jobid)
            proc_map = self. my_pmix.get_proc_map(setop.jobid)
            self.my_system.setop_apply(setop_id, node_map=node_map, proc_map=proc_map)
        
        self.run_component_service( MCALoggerComponent, "LOG", "EVENT", 
                            DefaultJobLogger, "JOB_RECONFIGURED",
                            self.my_system.jobs[setop.jobid])  
        
        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS", 
                    DefaultNodeLogger, "NODE_OCCUPATION_CHANGED",
                    setop.get_affected_nodes(self.my_system)) 

        t = localtime()
        current_time = strftime("%H:%M:%S", t)    
        v_print(current_time+": RECEIVED SETOP FINALIZATION FROM PRRTE", 1, self.verbosity_level)
        v_print(" "+setop.toString(), 1, self.verbosity_level)


    def _default_psetop_canceled_handler(self, info):
        return

    def _default_psetop_defined_handler(self, info):
        if info == None:
            return

        setop = SetOp.from_info(info)

        if setop == None:
            return

        t = localtime()
        current_time = strftime("%H:%M:%S", t)    
        v_print(current_time+": RECEIVED SETOP FROM PRRTE", 1, self.verbosity_level)
        v_print(" "+setop.toString(), 1, self.verbosity_level)

        self.my_system.setop_assign_to_job(setop.jobid, setop)

        self.logger.log_event_direct("SETOP", "SETOP_RECEIVED", setop)
        self.run_component_service( MCALoggerComponent, "LOG", "EVENT", 
                                    DefaultMCASetOpLogger, "SETOP_RECEIVED", setop)

        if PMIX_PSETOP_CANCEL == setop.op:
            for i in range(len(self.my_system.jobs[setop.jobid].setops)):
                pending_setop = self.my_system.jobs[setop.jobid].setops[i]

                if pending_setop == setop:
                    continue

                if pending_setop.is_unprocessed():
                    for pset in setop.input:
                        if pset in pending_setop.input:
                            pending_setop.op = PMIX_PSETOP_NULL

    def job_terminated_evhandler(evhdlr, status, source, info, results):
        _instance = ResourceManager()
        try:
            handler = _instance.registered_event_handlers[PMIX_EVENT_JOB_END]['cbfunc']
        except KeyError as ke:
            rc = PMIX_ERR_NOT_FOUND
            v_print("Received JOB TERMINATED event, but no event handler was registered", 3, _instance.verbosity_level)
        else:
            rc = PMIX_SUCCESS
            _instance.event_loop.call_soon_threadsafe(handler, info)
        finally:
            return rc, []

    def set_defined_evhandler(evhdlr, status, source, info, results):

        _instance = ResourceManager()
        if _instance.status == 'STARTUP':
            return rc, []
        try:
            handler = _instance.registered_event_handlers[PMIX_PROCESS_SET_DEFINE]['cbfunc']
        except KeyError as ke:
            rc = PMIX_ERR_NOT_FOUND
            v_print("Received PSET_DEFINED event, but no event handler was registered", 3, _instance.verbosity_level)
        else:
            rc = PMIX_SUCCESS
            _instance.event_loop.call_soon_threadsafe(handler, info)
        finally:
            return rc, []

    def setop_defined_evhandler(evhdlr, status, source, info, results):
        _instance = ResourceManager()
        try:
            handler = _instance.registered_event_handlers[PMIX_EVENT_PSETOP_DEFINED]['cbfunc']
        except KeyError as ke:
            rc = PMIX_ERR_NOT_FOUND
            v_print("Received PSETOP_DEFINED event, but no event handler was registered", 3, _instance.verbosity_level)
        else:
            rc = PMIX_SUCCESS
            _instance.event_loop.call_soon_threadsafe(handler, info)
        finally:
            return rc, []

    def setop_finalized_evhandler(evhdlr, status, source, info, results):
        _instance = ResourceManager()
        try:
            handler = _instance.registered_event_handlers[PMIX_EVENT_PSETOP_EXECUTED]['cbfunc']
        except KeyError as ke:
            rc = PMIX_ERR_NOT_FOUND
            v_print("Received PSETOP_FINALIZED event, but no event handler was registered", 3, _instance.verbosity_level)
        else:
            rc = PMIX_SUCCESS
            _instance.event_loop.call_soon_threadsafe(handler, info)
        finally:
            return rc, []

    def setop_canceled_evhandler(evhdlr, status, source, info, results):
        _instance = ResourceManager()
        try:
            handler = _instance.registered_event_handlers[PMIX_EVENT_PSETOP_CANCELED]['cbfunc']
        except KeyError as ke:
            rc = PMIX_ERR_NOT_FOUND
            v_print("Received PSETOP_CANCELED event, but no event handler was registered", 3, _instance.verbosity_level)
        else:
            rc = PMIX_SUCCESS
            _instance.event_loop.call_soon_threadsafe(handler, info)
        finally:
            return rc, []

    def _send_setop_cmds(self, setops):

        for setop in setops:
            info = []
            info.append({'key': 'SETOP_ID', 'value': setop.id, 'val_type': PMIX_SIZE})
            if(len(setop.nodelist) > 0):
                info.append({'key': PMIX_NODE_LIST, 'value': (',').join(setop.nodelist), 'val_type': PMIX_STRING})
            for item in setop.additional_info:
                info.append(item)
            self.my_pmix.notify_event(PMIX_EVENT_PSETOP_GRANTED, PMIX_RANGE_RM, info)

    def start_scheduling_loop(self, interval = 1.0, num_iters = None):
        self.status = 'RUNNING'
        self.event_loop.call_soon_threadsafe(self.event_loop.call_later, interval, self._periodic_sched, interval, 1, num_iters)
        self.event_loop.run_forever()

    
    def _periodic_sched(self, interval, cur_it, max_it):
        #self.my_system.write_output(self.output, cur_it)

        t = localtime()
        current_time = strftime("%H:%M:%S", t)
        v_print("\n\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"+current_time+": DOING PERIODIC SCHEDULING ("+str(cur_it)+"/"+str(max_it)+")\n", 1, self.verbosity_level)
        
        # See if someone "submitted" a job
        _time = time.time()
        for job in self.job_mix:
            if float(job['submission_time']) < _time - self.start_time:
                self.job_mix.remove(job)
                self.submit_job(job['bash_script'])

        # apply the scheduling policy
        results = self.my_system.schedule([])

        v_print("Starting "+str(len(results["jobs_to_start"]))+" jobs and executing "+str(len(results["setops_to_execute"]))+" set operations", 1, self.verbosity_level)
        
        self._spawn_jobs([job[0] for job in results["jobs_to_start"]])
        self._send_setop_cmds(results["setops_to_execute"])

        #if len(jobs_to_start) + len(setops_to_execute) > 0 and self.verbosity_level > 0 or self.verbosity_level > 3:
        if self.verbosity_level > 0:
            self.my_system.print()
        v_print("\nnxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n\n", 1, self.verbosity_level)

        

        cur_it = cur_it + 1
        if (max_it == None or cur_it <= max_it) and (len(self.my_system.jobs) > 0 or len(self.job_mix) > 0 or len(self.my_system.queue) > 0):
            self.event_loop.call_soon_threadsafe(self.event_loop.call_later, interval, self._periodic_sched, interval, cur_it, max_it)
        else:
            self.event_loop.call_soon_threadsafe(self.stop_scheduling_loop)

    def _spawn_jobs(self, cmds):
        for cmd in cmds:
            options = cmd.split(' ')
            job_infos = []
            app = dict()
            env = []
            args = []
            arg_taken = False
            for i in range(len(options)):
                if arg_taken:
                    arg_taken = False
                    continue

                if options[i] == "-np":
                    app['maxprocs'] = int(options[i + 1])
                    arg_taken = True
                    continue
                elif options[i] == "-x":
                    envar = {'envar': options[i + 1], 'value': os.environ.get(options[i + 1]), 'separator': ':'}
                    env.append(options[i + 1]+"="+str(os.environ.get(options[i + 1])))
                    arg_taken = True
                    continue
                elif options[i] == "--host":
                    job_infos.append({'key': PMIX_HOST, 'flags': 0, 'value': options[i + 1], 'val_type': PMIX_STRING})
                    arg_taken = True
                    continue
                elif options[i].startswith("/"):
                    cmd = options[i]
                    args = options[i + 1:]
                    break
            job_infos.append({'key': PMIX_NOTIFY_COMPLETION, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
            job_infos.append({'key': "pmix.setup.env", 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
            job_infos.append({'key': PMIX_FWD_STDOUT, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
            job_infos.append({'key': PMIX_PERSONALITY, 'flags': 0, 'value': 'ompi', 'val_type': PMIX_STRING})
             

            app['cmd'] = cmd[cmd.find('/'):]
            app['env'] = env
            
            app['argv'] = args
            app['info'] = job_infos

            # PMIx_Spawn
            rc, jobid = self.my_pmix.my_tool.spawn(job_infos, [app])

            if rc == PMIX_SUCCESS:
                job = Job(jobid)
                self.my_system.add_jobs([job])

                nodes = self.my_pmix.get_node_map(jobid)
                ppn = self.my_pmix.get_proc_map(jobid)


                # Insert Procs
                for node, proc_ranks in zip(nodes, ppn):
                    job.add_node_names([node])

                    for proc_rank in proc_ranks.split(','):
                        proc = Proc(jobid, proc_rank, node)
                        self.my_system.add_procs([proc])

                    self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                                                DefaultNodeLogger, "NODE_OCCUPATION_CHANGED", 
                                                self.my_system.node_pool[node])

                # Set jobids for the jobs PSets
                job_pset_names = self.my_pmix.query_job_psets(jobid)

                for pset_name in job_pset_names:
                    self.my_system.pset_assign_to_job(pset_name, jobid)
            
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT", 
                                            DefaultJobLogger, "JOB_STARTED", job)

    def submit_job(self, path):
        model = None
        model_params = None
        mappings = None
        constraints = None
        
        with open(path, 'r') as json_file:
            bash_script = json.load(json_file)
        
        if bash_script["model_name"] == "AMDAHL":
            model = create_module("SET_MODEL", "AMDAHL")

        self.my_system.queue.append([cmd])

    def stop_scheduling_loop(self):
        self.event_loop.stop()

def get_policy(policy, verbosity_level):
    if policy == 'default':
        return Fifo_Hard_Requests("Fifo + hard requests", verbosity_level=verbosity_level)
    if policy == 'dmr':
        return DMR_Scheduler("DMR Scheduling Policy", verbosity_level=verbosity_level)  


def get_parameters():
    parser = argparse.ArgumentParser()# Add an argument
    parser.add_argument('--server_pid', type=int, required=False)
    parser.add_argument('--verbosity_level', type=int, required=False)
    parser.add_argument('--sched_interval', type=float, required=False)
    parser.add_argument('--hosts', type=str, required=True)
    parser.add_argument('--jobs', type=str, required=True)
    parser.add_argument('--output', type=str, required=False)
    parser.add_argument('--policy', type=str, required=False, choices=['default', 'dmr'])
    parser.add_argument('--tmpdir', type=str, required=False)

    args = parser.parse_args()

    pid = -1
    if args.server_pid is not None:
        pid = args.server_pid

    hosts = args.hosts
    jobs = args.jobs

    verbosity_level = 0
    if args.verbosity_level is not None: 
            verbosity_level = args.verbosity_level

    sched_interval = 1.0
    if args.sched_interval is not None: 
            sched_interval = args.sched_interval

    policy = 'default'
    if args.policy is not None:
        policy = args.policy
    
    output = args.output

    tmpdir = args.tmpdir

    return pid, verbosity_level, sched_interval, hosts, jobs, output, policy, tmpdir
