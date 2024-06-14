from dyn_rm.mca.base.logger.component import MCALoggerComponent
from dyn_rm.mca.base.system.module.logging import *
from dyn_rm.mca.base.system.module import MCASystemModule
from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule
from dyn_rm.mca.base.system.module import *
from dyn_rm.mca.system.modules.psets.psetop_models import *
from dyn_rm.mca.system.modules.psets.pset_models import *
from dyn_rm.util.constants import *
from dyn_rm.util.functions import v_print
from pmix import *

import time
import asyncio
from functools import partial

#from typing import Any
#from elastisim_python import JobState, JobType, NodeState, pass_algorithm, Job, Node, InvocationType


#define a set of directives for pset operation requests */
#typedef uint8_t pmix_psetop_directive_t;

#PMIX_PSETOP_NULL            =       0   # Invalid pset operation
#PMIX_PSETOP_ADD             =       1   # Resources are added
#PMIX_PSETOP_SUB             =       2   # Resources are removed
#PMIX_PSETOP_REPLACE         =       3   # Resources are replaced
#PMIX_PSETOP_MALLEABLE       =       4   # Resources are added or removed depending on scheduler decision
#PMIX_PSETOP_GROW            =       5   # ADD + UNION
#PMIX_PSETOP_SHRINK          =       6   # SUB + DIFFERENCE
#PMIX_PSETOP_UNION           =       7   # The union of two psets is requested
#PMIX_PSETOP_DIFFERENCE      =       8   # The difference of two psets is requested
#PMIX_PSETOP_INTERSECTION    =       9   # The intersection of two psets is requested
#PMIX_PSETOP_MULTI           =       10  # Multiple operations specified in the info object
#PMIX_PSETOP_SPLIT           =       11  # Splt operation
#PMIX_PSETOP_CANCEL          =       12  # Cancel PSet Operations
#define a value boundary beyond which implementers are free
#to define their own directive values */

### TODO: This class does not yet implement the system module interface ###

class ElastiSimSystem(MCASystemModule):


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._queue = asyncio.Queue()
        self.run_component_service(MCAEventLoopComponent, "REGISTER", "EVENT_LOOP", MCAEventLoopModule, "PMIX_LOOP")
        self.run_component_service(MCAEventLoopComponent, "START", "EVENT_LOOP", "ELASTISIM_LOOP")

        self.run_service("SET", "ATTRIBUTE", "ELASTISIM_ALGORITHM", self.schedule)
        

    # Not much to be done. ElastiSim will be started when job mix is submitted using topo file
    # We just LOG that the nodes were started
    def _set_system_topology(self, topo_graph):
        rc = super()._set_system_topology(topo_graph)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        nodes = topo_graph.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)
        if len(nodes) < 1:
            return DYNRM_MCA_ERR_BAD_PARAM

        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                                    MCANodeLogger, "NODE_STARTED", 
                                    nodes)        

        return DYNRM_MCA_SUCCESS

    # We don't use a reconfiguration period in elastisim.
    # Therefore call this at the end of the schedule function for each applied psetop
    def _finalize_psetop(self, psetop_id):
        #print("####### FINALIZE PSETOP "+str(psetop_id)+" #######")
        rc = self.finalize_psetop(psetop_id)
        if rc != DYNRM_MCA_SUCCESS:
            return rc

        # Check if a successor operation can be applied
        psetop = self.run_service("GET", "GRAPH_EDGE", psetop_id)

        # LOG EVENT
        self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                MCASetOpLogger, "SETOP_FINALIZED", 
                psetop)
        

        nodes = {n.run_service("GET", "NAME") : n for n in psetop.run_service("GET", "OUTPUT")[0].run_service("GET", "ACCESSED_NODES")}
        if len(psetop.run_service("GET", "OUTPUT")) > 0:
            for pset in psetop.run_service("GET", "OUTPUT")[1:-1]:
                nodes.update({n.run_service("GET", "NAME") : n for n in pset.run_service("GET", "ACCESSED_NODES")})
        
        # LOG EVENT
        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                MCANodeLogger, "NODE_OCCUPATION_CHANGED", 
                list(nodes.values()))

        successors = psetop.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_SUCCESSORS)
        ready_successors = []
        for successor in successors:
            if successor.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_SCHEDULED:
                continue
            successor.run_service("SHRINK", "ATTRIBUTE_LIST", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS, [psetop])
            if len(successor.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS)) == 0:
                ready_successors.append(successor)
        
        rc = self._send_setop_cmd(ready_successors)
        if rc != DYNRM_MCA_SUCCESS:
            print("_send_setop_cmd failed with ", rc)
        rc = self.run_component_service(MCACallbackComponent, "BCAST", "EVENT", MCASystemModule.PSETOP_FINALIZED_EVENT, self, psetop)
        if rc != DYNRM_MCA_SUCCESS:
            print("System Bcast event 'PSETOP_DEFINED' failed ", rc)
        return rc

    # Call this when a job terminates    
    def _finalize_task(task_id):
        rc = super().finalize_task(task_id)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        return DYNRM_MCA_SUCCESS
        
    def null_cbfunc(*args, **kwargs):
        pass

    # This function defines a new psetop and adds it to the system 
    # TODO: implement something like this for elastisim
    #   -   Called at reconf point / evolving request
    #   -   If there is already a psetop for this elastiSim job just trigger scheduling     
    #   -   Op is always REPLACE, input is the current 
    #   -   Input is the currently active PSet for the job (you might need some tracking for this)
    def define_new_psetop(self, id, op, input, op_info):
        
        # For now, assume processes do not specify operations on the null psets
        in_psets = [self.run_service("GET", "GRAPH_VERTEX", name ) for name in input]
        if None in in_psets:
            return DYNRM_ERR_BAD_PARAM
        

        task = in_psets[0].run_service("GET", "TASK")
        if None == task:
            return DYNRM_ERR_BAD_PARAM

        pset_graph = in_psets[0].run_service("GET", "PSET_GRAPH")
        if None == pset_graph:
            return DYNRM_ERR_BAD_PARAM
        

        # See if we already have such a set operation, i.e. it's an update
        # ELASTISIM: just trigger scheduling if 
        psetop = None
        for _psetop in pset_graph.run_service("GET", "PSETOPS"):
            diff = 0
            for name in input:
                if name not in [s.run_service("GET", "GID") for s in _psetop.run_service("GET", "INPUT")]:
                    diff = 1 
                    break
            if diff > 0:
                continue
            if  (_psetop.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_DEFINED and
                _psetop.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_SCHEDULED):
                continue
            psetop = _psetop
            break

        # Handle CANCELATION here
        # ELASTISIM: You can leave it here for future extensions but currently no cancelation with elastisim
        if op == MCASystemModule.PSETOP_CANCEL:
            cancel_psetop = MCAPSetopModule("new_op", op, in_psets)

            self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                MCASetOpLogger, "SETOP_DEFINED", 
                cancel_psetop) 

            psetops = [cancel_psetop]
            output_lists = [[]]
            a_lists = [[]]

            # We are successfully cancelling the PSet Operation
            if None != psetop and (
                psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_DEFINED or
                psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_SCHEDULED):
                psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_CANCELED)
                psetops.append(psetop)
                output_lists.append([])
                a_lists.append([])
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                    MCASetOpLogger, "SETOP_CANCELED", 
                    psetop) 
            # There was no PSet Operation to cancel
            else:
                cancel_psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_CANCELED)
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                    MCASetOpLogger, "SETOP_CANCELED", 
                    cancel_psetop)
            rc =  self.add_psetops([cancel_psetop])
            if rc != DYNRM_MCA_SUCCESS:
                return rc
            


            
            rc = self.apply_psetops(psetops, output_lists, a_lists)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
            
            return DYNRM_MCA_SUCCESS

            
        # SETUP THE PSETOP WITH EVERYTHING THEY PROVIDED IN THE COL OBJECT
        # TODO: Instead of op_info retrieve neccessary data from the elastisim job : 
        if None == psetop:        
            psetop = MCAPSetopModule("new_op", op, in_psets)

        # Get the 'USER_MODEL' for the PSet Operation
        model = None
        priority = None
        model_params = dict()
        monitoring_data = dict()
        output_space_generator = None
        input_pset_models = dict()
        input_pset_model_monitoring = dict()
        input_pset_model_params = dict()
        for info in op_info:
            # Get the PSet Operation model
            if info['key'] == 'model':
                model = eval(info['value'])
            elif info['key'] == 'task_attribute_key_model_class':
                model = task.run_service("GET", "ATTRIBUTE", info['value'])()
            elif info['key'] == 'task_attribute_key_model_expression':
                model = eval(task.run_service("GET", "ATTRIBUTE", info['value']))

            # Get the parameters for the PSet Operation Model   
            elif info['key'] == 'model_params':
                kvs = info['value'].split(',')
                for kv in kvs:
                    key, val, t = kv.split(':')
                    if t == 'int':
                        model_params[key] = int(val)
                    elif t == 'float':
                        model_params[key] = float(val)
                    elif t == 'string':
                        model_params[key] = str(val)
                    elif t == 'bool':
                        model_params[key] = bool(val)
                    else:
                        model_params[key] = val
            elif info['key'] == 'task_attribute_key_model_params':
                model_params.update(task.run_service("GET", "ATTRIBUTE", info['value']))    
            
            # Get the priority for the psetop
            elif info['key'] == 'priority':
                priority = int(info['value'])

            # Get the output space generator
            elif info['key'] == 'output_space_generator':
                output_space_generator = eval(info['value'])


            elif info['key'] == 'generator_key':
                output_space_generator = task.run_service("GET", "ATTRIBUTE", info['value'])
        

            # Get the monitoring data
            elif info['key'] == 'monitoring_data':
                kvs = info['value'].split(',')
                for kvt in kvs:
                    ElastiSimSystem._insert_kvt(monitoring_data, kvt)
 

            # Get models for the input PSets
            elif info['key'] == 'input_pset_models':
                index = int(info['key'].split('_')[-1])
                input_pset_models[int(key)] = eval(val)

            # Update paramters for the input PSet 
            elif info['key'].startswith('input_pset_model_params'):
                index = int(info['key'].split('_')[-1])
                input_pset_model_params[index] = dict()
                kvs = info['value'].split(',')
                for kvt in kvs:
                    ElastiSimSystem._insert_kvt(input_pset_model_params, kvt)

            # Update paramters for the input PSet 
            elif info['key'].startswith('input_pset_model_monitoring'):
                index = int(info['key'].split('_')[-1])
                input_pset_model_monitoring[index] = dict()
                kvs = info['value'].split(',')
                for kvt in kvs:
                    ElastiSimSystem._insert_kvt(input_pset_model_monitoring[index], kvt)

        # ELASTSIM: You can keep the code below as it is

        #if None == model:
            # Assign defaut model for the operation 
        #if None == model_params:
            # Set some default parameters if necessary
        #if None == output_space_generator:
            # Set Default output_space_generator for this PSetop
        if None == model:
            print("MODEL == NONE !!!")


        if len(model_params) > 0:
            model.run_service("SET", "MODEL_PARAMS", model_params)


        model.run_service("SET", "OUTPUT_SPACE_GENERATOR", output_space_generator)

        if len(monitoring_data) > 0:
            model.run_service("ADD", "MONITORING_ENTRY", time.time(), monitoring_data)

        psetop.run_service("ADD", "PSETOP_MODEL", "USER_MODEL", model)

        if None != priority:
            psetop.run_service("SET", "PRIORITY", priority)

        # Update models of input sets
        for index in input_pset_models.keys():
            in_psets[index].run_service("ADD", "PSET_MODEL", "USER_MODEL", input_pset_models[index])
            for k,v in input_pset_models[index]:
                    pset_model.run_service("SET", "MODEL_PARAM", k, v)

        # update parameters of input pset models
        for index in input_pset_model_params.keys():
            pset_model = in_psets[index].run_service("GET", "PSET_MODEL")
            for k,v in input_pset_models[index]:
                pset_model.run_service("SET", "MODEL_PARAM", k, v)
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                                MCASetLogger, "SET_MODEL_UPDATE", in_psets[index])

        # update monitoting data of input pset models
        for index in input_pset_model_monitoring.keys():
            pset_model = in_psets[index].run_service("GET", "PSET_MODEL", "USER_MODEL")
            if None != pset_model:
                pset_model.run_service("ADD", "MONITORING_DATA", input_pset_model_monitoring[index])
                pset_model.run_service("EVAL", "MODEL_PARAMS")
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                                MCASetLogger, "SET_MODEL_UPDATE", in_psets[index])

        rc =  self.add_psetops([psetop])
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        # LOG EVENT
        self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                        MCASetOpLogger, "SETOP_DEFINED", 
                        psetop)

        # APPLY SETOP IF IT DOES NOT REQUIRE RESOURCE SCHEDULING
        if (op == MCASystemModule.PSETOP_UNION or 
            op == MCASystemModule.PSETOP_SPLIT or
            op == MCASystemModule.PSETOP_DIFFERENCE):

            model = psetop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
            if None == model:
                model = psetop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

            o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                            psetop, 
                                                            psetop.run_service("GET", "INPUT"),
                                                            None)

            rc = self.apply_psetops([psetop], [o_lists], [a_lists])
            if rc != DYNRM_MCA_SUCCESS:
                return rc
            rc = self.finalize_psetop(psetop.run_service("GET", "GID"))
            return rc

        rc = self.run_component_service(MCACallbackComponent, "BCAST", "EVENT", MCASystemModule.PSETOP_DEFINED_EVENT, self, psetop)
        if rc != DYNRM_MCA_SUCCESS:
            print("System Bcast event 'PSETOP_DEFINED' failed ", rc)
        
        return rc


    def apply_psetops(self, psetops, output_lists, adapted_objects_lists):
        super().apply_psetops(psetops, output_lists, adapted_objects_lists)

        # Log the new PSets
        new_psets = dict()
        for output in output_lists:
            for pset in output:
                if isinstance(pset, MCAPSetGraphModule):
                    continue
                new_psets[pset.run_service("GET", "GID")] = pset
        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                        MCASetLogger, "SET_DEFINED", 
                        new_psets.values())

        # Track dependencies between setops 
        for predecessor in psetops:
            if predecessor.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_PENDING:
                continue
            input = predecessor.run_service("GET", "INPUT")
            input_nodes = [n.run_service("GET", "GID") for n in input[0].run_service("GET", "ACCESSED_NODES")]
            for successor in psetops:
                if predecessor.run_service("GET", "GID") == successor.run_service("GET", "GID"):
                    continue
                output = successor.run_service("GET", "OUTPUT")
                if len(output) == 0:
                    continue
                output_nodes = [n.run_service("GET", "GID") for n in output[len(output) - 1].run_service("GET", "ACCESSED_NODES")]
                if 0 != len([n for n in input_nodes if n in output_nodes]):
                    predecessor.run_service("EXTEND", "ATTRIBUTE_LIST", MCAPSetopModule.PSETOP_ATTRIBUTE_SUCCESSORS, [successor])
                    successor.run_service("EXTEND", "ATTRIBUTE_LIST", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS, [predecessor])
                    successor.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_SCHEDULED)

        if len(psetops) > 0:
            self.run_component_service(MCALoggerComponent, "LOG", "EVENTS",
                            MCASetOpLogger, "SETOP_SCHEDULED", 
                            psetops) 

        # TODO: Here the psetop results are provided back to the elastisim_scheduling_function:
        return self.provide_scheduling_decision(psetops) 
        #   - This will be consumed by the wait_for_scheduling_results function in the elastisim_schedule_function 
        #   - Parts from the _send_setop_cmd func below can be used there

    # TODO: Do something like this with the scheduling results in the elastisim_scheduling_function
    '''
    def _send_setop_cmd(self, psetops):
        
        for psetop in psetops:
            if psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_FINALIZED)
                self.run_component_service(MCALoggerComponent, "LOG", "EVENT",
                        MCASetOpLogger, "SETOP_FINALIZED", 
                        psetop)
                continue
                 
            # skip psetops with predecessors
            if len(psetop.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS)) > 0:
                continue
            
            # LOG EVENT
            self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                        MCASetOpLogger, "SETOP_EXECUTION_START", 
                        psetop) 
            

            # This either starts a job (if) or resizes a job (else)
            # TODO: The same needs to be done with elastisim jobs
            if  psetop.run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_ADD and \
                psetop.run_service("GET", "INPUT")[0].run_service("GET", "NAME") == "":

                launch_pset = psetop.run_service("GET", "OUTPUT")[0]
                num_procs = launch_pset.run_service("GET", "NUM_PROCS")
                hosts = ",".join([n.run_service("GET", "NAME")+":"+str(n.run_service("GET", "NUM_CORES")) for n in launch_pset.run_service("GET", "ACCESSED_NODES")])
                task = launch_pset.run_service("GET", "TASK")
                executable = task.run_service("GET", "TASK_EXECUTABLE")
                arguments = task.run_service("GET", "TASK_EXECUTION_ARGUMENTS")

                hdict_add = dict()
                for proc in launch_pset.run_service("GET", "PROCS"):
                    host = proc.run_service("GET", "CORE_ACCESS")[0].run_service("GET", "NODE").run_service("GET", "NAME")
                    if host not in hdict_add:
                        hdict_add[host] = dict()
                    hdict_add[host][proc] = proc
                ppr = str(len(next(iter(hdict_add.values()))))+":node"
                #env = []    
                #env.append(options[i + 1]+"="+str(os.environ.get(options[i + 1])))
                

                v_print("Launching Task "+task.run_service("GET", "NAME")+ " on hosts "+hosts, 2, self.verbosity)
                # PMIx_Spawn
                rc = DYNRM_MCA_SUCCESS
                # TODO: start elastiSim job
                if rc != DYNRM_MCA_SUCCESS:
                    v_print("Launch of Task "+task.run_service("GET", "NAME")+" failed with "+str(rc), 2, self.verbosity)
                    return DYNRM_MCA_ERR_BAD_PARAM
                v_print("Launch of Task "+task.run_service("GET", "NAME")+" successful", 2, self.verbosity)
                
                task.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_RUNNING)
                
                psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_FINALIZED)
                for proc in launch_pset.run_service("GET", "PROCS"):
                    proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_RUNNING)
                
                # LOG EVENT
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                        MCATaskLogger, "TASK_STARTED", 
                        task)

                # LOG EVENT
                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                        MCASetOpLogger, "SETOP_FINALIZED", 
                        psetop) 
                
                # LOG EVENT
                self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                        MCANodeLogger, "NODE_OCCUPATION_CHANGED", 
                        psetop.run_service("GET", "OUTPUT")[0].run_service("GET", "ACCESSED_NODES"))


            else:
                # TODO: Apply PSetOp
                if psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_CANCELED:
                    # TODO: Cancel a PSetOp
                    pass
                    #info.append({'key': 'PMIX_PSETOP_CANCELED', 'value' : True, 'val_type': PMIX_BOOL})
                
                #print(psetop.run_service("GET", "GID")+": add_hosts: "+hosts_add+" sub_hosts "+hosts_sub)
                # TODO
                #rc = self.run_component_service(MCACallbackComponent, "SEND", "EVENT", "PRRTE_MASTER", PMIX_EVENT_PSETOP_GRANTED, info)
            
        return DYNRM_MCA_SUCCESS
        '''
    
    def _insert_kvt(my_dict, kvt):
        key, val, t = kvt.split(':')
        if t == 'int':
            my_dict[key] = int(val)
        elif t == 'float':
            my_dict[key] = float(val)
        elif t == 'string':
            my_dict[key] = str(val)
        elif t == 'bool':
            my_dict[key] = bool(val)
        else:
            my_dict[key] = val


    def mca_shutdown(self):
        # TODO: Shutdown ElastiSim
        return self.mca_default_shutdown()

    async def provide_scheduling_decision(self, psetops):
        await self._queue.put(psetops)  # Add item to the queue


    async def wait_for_scheduling_decision(self):
        psetops = await self._queue.get()
        return psetops

    # TODO: This function is passed via pass_algorithm() to elastisim
    # This function receives an event (job submitted, reconf_point, evolvng_request)
    #   1. Translate it to dyn_rm
    #   2. trigger dyn_rm scheduling, 
    #   3. gets psetops as result from scheduling 
    #   4. Translates it to elastisim
    '''
    def elastisim_schedule_function(self, jobs: list[Job], nodes: list[Node], system: dict[str, Any]) -> None:
        time = system['time']
    
        if system['invocation_type'] == InvocationType.INVOKE_SCHEDULING_POINT:
            job = system['job']
            num_nodes_to_expand = min(len(free_nodes), job.num_nodes_max - len(job.assigned_nodes))
            if num_nodes_to_expand > 0:
                job.assign(free_nodes[:num_nodes_to_expand])
                del free_nodes[:num_nodes_to_expand]
        elif system['invocation_type'] == InvocationType.INVOKE_EVOLVING_REQUEST:
            job = system['job']
            evolving_request = system['evolving_request']
            num_nodes = len(job.assigned_nodes)
            diff = evolving_request - num_nodes
            if diff < 0:
                job.remove(job.assigned_nodes[diff:])
            elif len(free_nodes) >= diff:
                job.assign(free_nodes[:diff])
        else:
            for job in pending_jobs:
                if job.type == JobType.RIGID:
                    if job.num_nodes <= len(free_nodes):
                        job.assign(free_nodes[:job.num_nodes])
                        del free_nodes[:job.num_nodes]
                    else:
                        break
                else:
                    num_nodes_to_assign = min(len(free_nodes), job.num_nodes_max)
                    if num_nodes_to_assign >= job.num_nodes_min:
                        job.assign(free_nodes[:num_nodes_to_assign])
                        del free_nodes[:num_nodes_to_assign]
                    else:
                        break
        psetops = self.wait_for_scheduling_decision()
    '''

