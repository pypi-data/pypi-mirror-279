from dyn_rm.mca.base.logger.component import MCALoggerComponent
from dyn_rm.mca.base.system.module.logging import *
from dyn_rm.mca.base.system.module import MCASystemModule
from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.callback.modules.pmix import PmixCallbackModule
from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule
from dyn_rm.mca.base.system.module import *
from dyn_rm.mca.system.modules.psets.psetop_models import *
from dyn_rm.mca.system.modules.psets.pset_models import *
from dyn_rm.util.constants import *
from dyn_rm.util.functions import v_print
from pmix import *
import os
import time
from functools import partial


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
PMIX_PSETOP_EXTERNAL        =       128

PMIX_EVENT_PSETOP_DEFINED   =       PMIX_EXTERNAL_ERR_BASE - 1
PMIX_EVENT_PSETOP_GRANTED   =       PMIX_EXTERNAL_ERR_BASE - 2
PMIX_EVENT_PSETOP_CANCELED  =       PMIX_EXTERNAL_ERR_BASE - 3
PMIX_EVENT_PSETOP_EXECUTED  =       PMIX_RC_FINALIZED
### TODO: This class does not yet implement the system module interface ###

class PrrteSystem(MCASystemModule):

    ATTRIBUTE_SERVER_PID = "SERVER_PID"
    ATTRIBUTE_PMIX_TOOL = "PMIX_TOOL"
    ATTRIBUTE_PMIX_PROCID = "PMIX_PROCID"
    ATTRIBUTE_TASK_ALIAS = "TASK_ALIAS"
    ATTRIBUTE_PSETOP_ALIAS = "PSETOP_ALIAS"


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
    
        
        cb_comp = self.get_component(MCACallbackComponent)
        cb_comp.register_module(PmixCallbackModule())
        self.run_component_service(MCAEventLoopComponent, "REGISTER", "EVENT_LOOP", MCAEventLoopModule, "PMIX_LOOP")
        self.run_component_service(MCAEventLoopComponent, "START", "EVENT_LOOP", "PMIX_LOOP")
        self.register_service("SET", "PMIX_TOOL", self.set_pmix_tool)
        self.register_service("GET", "PMIX_TOOL", self.set_pmix_tool)
        
        my_tool = PMIxTool()
        self.run_service("SET", "PMIX_TOOL", PMIxTool())

        self._pmix_aliases = dict()
        #self.pmix_tool_init(my_tool)
        
    def pmix_tool_init(self, my_tool):
        info = [
            {'key': PMIX_TOOL_DO_NOT_CONNECT, 'value': True, 'val_type':PMIX_BOOL}  
        ]
        rc, my_procid = my_tool.init(info)
        if rc != PMIX_SUCCESS:
            print(rc)
            raise PMIx_Error(rc, "PMIx_Tool_init")
        self.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PMIX_PROCID, my_procid)
        return DYNRM_MCA_SUCCESS
    
    def set_pmix_tool(self, tool):
        self.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PMIX_TOOL, tool)
        return DYNRM_MCA_SUCCESS

    def get_pmix_tool(self):
        return self.run_service("GET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PMIX_TOOL)

    def get_pmix_procid(self):
        return self.run_service("GET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PMIX_PROCID)

    def register_callbacks(self):

        # PSET DEFINED
        rc = self.run_component_service(
            MCACallbackComponent, "REGISTER", "CONNECTION_CALLBACK", "PRRTE_MASTER", 
            PMIX_PROCESS_SET_DEFINE, partial(PrrteSystem.set_defined_evhandler, self=self))
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        # PSETOP DEFINED
        rc = self.run_component_service(
            MCACallbackComponent, "REGISTER", "CONNECTION_CALLBACK", "PRRTE_MASTER", 
            PMIX_EVENT_PSETOP_DEFINED, partial(PrrteSystem.psetop_defined_evhandler, self=self))
        if rc != DYNRM_MCA_SUCCESS:
            return rc

        # PSETOP FINALIZED
        rc = self.run_component_service(
            MCACallbackComponent, "REGISTER", "CONNECTION_CALLBACK", "PRRTE_MASTER", 
            PMIX_EVENT_PSETOP_EXECUTED, partial(PrrteSystem.psetop_finalized_evhandler, self=self))
        if rc != DYNRM_MCA_SUCCESS:
            return rc

        # TASK TERMINATED
        rc = self.run_component_service(
            MCACallbackComponent, "REGISTER", "CONNECTION_CALLBACK", "PRRTE_MASTER", 
            PMIX_EVENT_JOB_END, partial(PrrteSystem.task_terminated_evhandler, self=self))
        if rc != DYNRM_MCA_SUCCESS:
            return rc

        return DYNRM_MCA_SUCCESS   

    # creates Prrte DVM and connects to it as PMIx Tool
    def _set_system_topology(self, topo_graph):
        rc = super()._set_system_topology(topo_graph)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        timeout = 30
        filename = None
        suffix = str(time.time())
        if None != filename:
            filename = os.path.join(self.tmpdir, "pid_"+suffix)
        else:
            filename = os.path.join(os.getcwd(), "pid_"+suffix)
        
        nodes = topo_graph.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)
        if len(nodes) < 1:
            return DYNRM_MCA_ERR_BAD_PARAM
        hosts = ",".join([n.run_service("GET", "NAME")+":"+str(n.run_service("GET", "NUM_CORES"))for n in nodes])
        
        # Start PRRTE
        if self.verbosity > 9:
            cmd = "prte --report-pid "+filename+" --debug-daemons --leave-session-attached --mca ras timex --mca odls_base_verbose 10 --mca ras_base_verbose 10 --mca plm_base_verbose 10 --mca state_base_verbose 10 --mca pmix_server_verbose 10 --host "+hosts+" > prte_mca.out 2>&1 &"
        else:
            cmd = "prte --report-pid "+filename+" --daemonize --mca ras timex --host "+hosts+" > /dev/null 2>&1 &"
        v_print(cmd, 3, self.verbosity)
        os.system(cmd)
        start = time.time()
        v_print("Waiting for PID in file "+filename, 3, self.verbosity)
        # get the pid of the PRRTE Master
        pid = -1
        while pid < 0:
            if time.time() - start > timeout:
                raise Exception("PRRTE startup timed out!") 
            
            try:
                pid = int(open(filename, 'r').readlines()[0])
                self.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_SERVER_PID, pid)

                # Connect to the server via the PMIxCallbackModule
                rc = self.run_component_service(MCACallbackComponent, "REQUEST", "CONNECTION", PmixCallbackModule, "PRRTE_MASTER", self.get_pmix_tool(), None, {"pid" : pid})
                if rc != DYNRM_MCA_SUCCESS:
                    print("request connetion failed")
                    return rc

                
                rc = self.register_callbacks()
                if rc != DYNRM_MCA_SUCCESS:
                    print("request connetion failed")
                    return rc
                
                
                #my_tool.register_event_handler()
            except FileNotFoundError:
                time.sleep(0.1)
                v_print("File not found, try again in 0.1 seconds ", 5, self.verbosity)
        try: 
            if os.path.exists(filename):
                os.remove(filename)
        except Exception:
            pass

        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                                    MCANodeLogger, "NODE_STARTED", 
                                    nodes)        

        return DYNRM_MCA_SUCCESS


    @staticmethod
    def task_terminated_evhandler(evhdlr, status, source, info, results, self=None):
        
        alias = None
        for item in info:
            if item['key'] == PMIX_EVENT_AFFECTED_PROC.decode("utf-8"):
                alias = item['value']['nspace']

        if None == alias:
            return
        
        task_id = self._pmix_aliases.get(alias)

        #print("TASK "+task_id+" TERMINATED")

        if None == task_id:
            return PMIX_ERR_BAD_PARAM, []

        rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB", "MAIN_LOOP", 
                                       self.null_cbfunc, None, 
                                       self.finalize_task, task_id)
        if rc != DYNRM_MCA_SUCCESS:
            return PMIX_ERR_BAD_PARAM, []
        
        return PMIX_SUCCESS, []



    @staticmethod
    def psetop_finalized_evhandler(evhdlr, status, source, info, results, self=None):
        alias = None
        for item in info:
            if item['key'] == PMIX_ALLOC_ID.decode("utf-8"):
                alias = item['value']
        if None == alias:
                return PMIX_ERR_BAD_PARAM, []
        
        setopid = self._pmix_aliases.get(alias)

        if None == setopid:
            return DYNRM_MCA_ERR_NOT_FOUND, []
        
        rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB", "MAIN_LOOP", 
                                       self.null_cbfunc, None, 
                                       self._finalize_psetop, setopid)
        if rc != DYNRM_MCA_SUCCESS:
            return PMIX_ERR_BAD_PARAM, []
        
        return PMIX_SUCCESS, []
    
    @staticmethod
    def set_defined_evhandler(evhdlr, status, source, info, results, self=None):
        pset_name = None
        members = None
        for item in info:

            if item['key'] == PMIX_PSET_NAME.decode("utf-8"):
                pset_name = item['value']
            elif item['key'] == PMIX_PSET_MEMBERS.decode("utf-8"):
                members = item['value']['array']
        return PMIX_SUCCESS, []
    
    @staticmethod 
    def psetop_defined_evhandler(evhdlr, status, source, event_infos, results, self=None):
        
        id = op = input = output = opinfo = jobid = None
        for event_info in event_infos:
            if event_info['key'] == "prte.alloc.reservation_number":
                id = event_info['value']
            elif event_info['key'] == "prte.alloc.client":
                jobid = event_info['value']['nspace'] 
            elif event_info['key'] == "mpi.rc_op_handle":
                for info in event_info['value']['array']:
                    if info['key'] == "pmix.psetop.type":
                        op = info['value']
                    if info['key'] == "mpi.op_info":
                        for mpi_op_info in info['value']['array']:
                            if mpi_op_info['key'] == "mpi.op_info.input":
                                input = mpi_op_info['value'].split(',')
                            elif mpi_op_info['key'] == "mpi.op_info.output":
                                output = mpi_op_info['value'].split(',')
                            elif mpi_op_info['key'] == "mpi.op_info.info":
                                op_info = mpi_op_info['value']['array']
        
        # Create a pset operation. Need to run it in the system Main Loop
        if op != None and input != None:
            rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB", "MAIN_LOOP", 
                                       self.null_cbfunc, None, 
                                       self.define_new_psetop, id, self._pmix_dynrm_convert_psetop(op), input, op_info)
        return PMIX_SUCCESS, []

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

        
    def _finalize_task(task_id):
        rc = super().finalize_task(task_id)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        return DYNRM_MCA_SUCCESS
        


    def null_cbfunc(*args, **kwargs):
        pass
        
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
        if op == MCASystemModule.PSETOP_CANCEL:
            cancel_psetop = MCAPSetopModule("new_op", op, in_psets)
            cancel_psetop.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PSETOP_ALIAS, id)

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

        if None == psetop:        
            psetop = MCAPSetopModule("new_op", op, in_psets)
            psetop.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PSETOP_ALIAS, id)

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
                    PrrteSystem._insert_kvt(monitoring_data, kvt)
 

            # Get models for the input PSets
            elif info['key'].startswith('input_pset_models'):
                index = int(info['key'].split('_')[-1])
                input_pset_models[int(key)] = eval(info['value'])

            # Update paramters for the input PSet 
            elif info['key'].startswith('input_pset_model_params'):
                index = int(info['key'].split('_')[-1])
                input_pset_model_params[index] = dict()
                kvs = info['value'].split(',')
                for kvt in kvs:
                    PrrteSystem._insert_kvt(input_pset_model_params, kvt)

            # Update paramters for the input PSet 
            elif info['key'].startswith('input_pset_model_monitoring'):
                index = int(info['key'].split('_')[-1])
                input_pset_model_monitoring[index] = dict()
                kvs = info['value'].split(',')
                for kvt in kvs:
                    PrrteSystem._insert_kvt(input_pset_model_monitoring[index], kvt)

        # TODO:        
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


        # Send a setop command to PRRTE
        return self._send_setop_cmd(psetops)

    def _send_setop_cmd(self, psetops):
        if 0 == len(psetops):
            return DYNRM_MCA_SUCCESS
        
        my_tool = self.get_pmix_tool()
        if None == my_tool:
            return DYNRM_MCA_ERR_NOT_FOUND
        
        # LOG EVENT
        #print("SETOP scheduled")
        self.run_component_service(MCALoggerComponent, "LOG", "EVENTS",
                        MCASetOpLogger, "SETOP_SCHEDULED", 
                        psetops) 
        
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
                
                job_infos = []
                job_infos.append({'key': PMIX_NOTIFY_COMPLETION, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
                job_infos.append({'key': PMIX_SETUP_APP_ENVARS, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
                #job_infos.append({'key': PMIX_FWD_STDOUT, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
                job_infos.append({'key': PMIX_PERSONALITY, 'flags': 0, 'value': 'ompi', 'val_type': PMIX_STRING})
                job_infos.append({'key': PMIX_PSET_NAME, 'flags' : 0, 'value': launch_pset.run_service("GET", "GID"), 'val_type': PMIX_STRING})
                job_infos.append({'key': PMIX_PPR, 'flags': 0, 'value': ppr, 'val_type': PMIX_STRING})
                job_infos.append({'key': PMIX_RANKBY, 'flags': 0, 'value': "slot", 'val_type': PMIX_STRING})
                #job_infos.append({'key': PMIX_DISPLAY_MAP, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})
                #job_infos.append({'key': PMIX_NSPACE, 'flags' : 0, 'value': task.run_service("GET", "GID"), 'val_type': PMIX_STRING})

                app = dict()
                app['maxprocs'] = num_procs
                app['cmd'] = executable
                #app['env'] = env

                app['argv'] = arguments
                app['info'] = []
                app['info'].append({'key': PMIX_HOST, 'flags': 0, 'value': hosts, 'val_type': PMIX_STRING})
                app['info'].append({'key': PMIX_SETUP_APP_ENVARS, 'flags': 0, 'value': True, 'val_type': PMIX_BOOL})

                v_print("Launching Task "+task.run_service("GET", "NAME")+ " on hosts "+hosts, 2, self.verbosity)
                # PMIx_Spawn
                rc, jobid = my_tool.spawn(job_infos, [app])
                if rc != PMIX_SUCCESS:
                    v_print("Launch of Task "+task.run_service("GET", "NAME")+" failed with "+str(rc), 2, self.verbosity)
                    return DYNRM_MCA_ERR_BAD_PARAM
                v_print("Launch of Task "+task.run_service("GET", "NAME")+" successful", 2, self.verbosity)
                
                task.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_RUNNING)
                task.run_service("SET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_TASK_ALIAS, jobid)
                self._pmix_aliases[jobid] = task.run_service("GET", "GID")
                
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
                hdict_add = dict()
                hdict_sub = dict()
                for pset in psetop.run_service("GET", "OUTPUT"):
                    if 0 == pset.run_service("GET", "NUM_PROCS"):
                        continue
                    for proc in pset.run_service("GET", "PROCS"):
                        if proc.run_service("GET", "PROC_STATUS") == MCAProcModule.PROC_STATUS_LAUNCH_REQUESTED:
                            host = proc.run_service("GET", "CORE_ACCESS")[0].run_service("GET", "NODE").run_service("GET", "NAME")
                            if host not in hdict_add:
                                hdict_add[host] = dict()
                            hdict_add[host][proc] = proc
                        elif proc.run_service("GET", "PROC_STATUS") == MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED:
                            host = proc.run_service("GET", "CORE_ACCESS")[0].run_service("GET", "NODE").run_service("GET", "NAME")
                            if host not in hdict_sub:
                                hdict_sub[host] = dict()
                            hdict_sub[host][proc] = proc
                hosts_add = ",".join(hdict_add.keys())
                ppr_add = ",".join([str(len(val)) for val in hdict_add.values()])
                num_add = sum([len(val) for val in hdict_add.values()])
                
                hosts_sub = ",".join(hdict_sub.keys())
                ppr_sub = ",".join([str(len(val)) for val in hdict_sub.values()])
                num_sub = sum([len(val) for val in hdict_sub.values()])

                output = ",".join([s.run_service("GET", "GID") if s.run_service("GET", "NAME") != '' else '' for s in psetop.run_service("GET", "OUTPUT")])
                alias_id = psetop.run_service("GET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_PSETOP_ALIAS)
                self._pmix_aliases[alias_id] = psetop.run_service("GET", "GID")

                info = []
                info.append({'key': 'SETOP_ID', 'value': alias_id, 'val_type': PMIX_SIZE})
                info.append({'key': PMIX_NODE_LIST, 'value': hosts_add, 'val_type': PMIX_STRING})
                info.append({'key': PMIX_NODE_LIST_SUB, 'value': hosts_sub, 'val_type': PMIX_STRING})
                info.append({'key': PMIX_PPR, 'value': ppr_add, 'val_type': PMIX_STRING})
                info.append({'key': PMIX_PPR_SUB, 'value': ppr_sub, 'val_type': PMIX_STRING})
                info.append({'key': PMIX_PSETOP_OUTPUT, 'value': output, 'val_type': PMIX_STRING})
                info.append({'key': 'mpi_num_procs_add', 'value': str(num_add), 'val_type': PMIX_STRING})
                info.append({'key': 'mpi_num_procs_sub', 'value': str(num_sub), 'val_type': PMIX_STRING})
                
                if psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_CANCELED:
                    info.append({'key': 'PMIX_PSETOP_CANCELED', 'value' : True, 'val_type': PMIX_BOOL})
                
                #print(psetop.run_service("GET", "GID")+": add_hosts: "+hosts_add+" sub_hosts "+hosts_sub)
                rc = self.run_component_service(MCACallbackComponent, "SEND", "EVENT", "PRRTE_MASTER", PMIX_EVENT_PSETOP_GRANTED, info)

        return DYNRM_MCA_SUCCESS
    
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

    def _pmix_dynrm_convert_psetop(pmix_op):
        if pmix_op == PMIX_PSETOP_NULL:
            return MCASystemModule.PSETOP_NULL
        elif pmix_op == PMIX_PSETOP_ADD:
            return MCASystemModule.PSETOP_ADD
        elif pmix_op == PMIX_PSETOP_SUB:
            return MCASystemModule.PSETOP_SUB
        elif pmix_op == PMIX_PSETOP_GROW:
            return MCASystemModule.PSETOP_GROW
        elif pmix_op == PMIX_PSETOP_SHRINK:
            return MCASystemModule.PSETOP_SHRINK
        elif pmix_op == PMIX_PSETOP_REPLACE:
            return MCASystemModule.PSETOP_REPLACE
        elif pmix_op == PMIX_PSETOP_SPLIT:
            return MCASystemModule.PSETOP_SPLIT
        elif pmix_op == PMIX_PSETOP_UNION:
            return MCASystemModule.PSETOP_UNION
        elif pmix_op == PMIX_PSETOP_DIFFERENCE:
            return MCASystemModule.PSETOP_DIFFERENCE
        elif pmix_op == PMIX_PSETOP_INTERSECTION:
            return MCASystemModule.PSETOP_INTERSECTION
        elif pmix_op == PMIX_PSETOP_CANCEL:
            return MCASystemModule.PSETOP_CANCEL
        else:
            return MCASystemModule.PSETOP_NULL
        


    def mca_shutdown(self):
        pid = self.run_service("GET", "ATTRIBUTE", PrrteSystem.ATTRIBUTE_SERVER_PID)
        if None != pid:
            os.system("pterm --pid "+str(pid))

        return self.mca_default_shutdown()

    def tool_init_and_connect(self, my_tool, pid):
        
        info = [
                    {'key':PMIX_SERVER_PIDINFO, 'value':pid, 'val_type':PMIX_PID},
                    {'key': "SCHEDULER", 'value': True, 'val_type':PMIX_BOOL}
        ]

        rc, self.my_procid = my_tool.init(info)

        if rc != PMIX_SUCCESS:
            return rc
        return self.my_procid   


    def _pmix_dynrm_convert_psetop(self, op):
        if op == PMIX_PSETOP_NULL:
            return MCASystemModule.PSETOP_NULL
        elif op == PMIX_PSETOP_ADD:
            return MCASystemModule.PSETOP_ADD
        elif op == PMIX_PSETOP_SUB:
            return MCASystemModule.PSETOP_SUB
        elif op == PMIX_PSETOP_GROW:
            return MCASystemModule.PSETOP_GROW
        elif op == PMIX_PSETOP_SHRINK:
            return MCASystemModule.PSETOP_SHRINK
        elif op == PMIX_PSETOP_REPLACE:
            return MCASystemModule.PSETOP_REPLACE
        elif op == PMIX_PSETOP_SPLIT:
            return MCASystemModule.PSETOP_SPLIT
        elif op == PMIX_PSETOP_UNION:
            return MCASystemModule.PSETOP_UNION
        elif op == PMIX_PSETOP_DIFFERENCE:
            return MCASystemModule.PSETOP_DIFFERENCE
        elif op == PMIX_PSETOP_INTERSECTION:
            return MCASystemModule.PSETOP_INTERSECTION
        elif op == PMIX_PSETOP_CANCEL:
            return MCASystemModule.PSETOP_CANCEL
        else:
            return MCASystemModule.PSETOP_NULL

'''
    # abstract methods
    def get_node_ids_function(self):
        return [id for id in self.nodes.keys()]

    def get_job_ids_function(self):
        return [id for id in self.nodes.keys()]
    
    @abstractmethod
    def get_set_ids_function(self):
        pass
    @abstractmethod
    def get_setop_ids_function(self):
        pass

    @abstractmethod
    def get_node_function(self, id):
        pass
    @abstractmethod
    def get_job_function(self, id):
        pass
    @abstractmethod
    def get_set_function(self, id):
        pass
    @abstractmethod
    def get_setop_function(self, id):
        pass

    @abstractmethod
    def add_node_function(self, node):
        pass
    @abstractmethod
    def add_job_function(self, job):
        pass
    @abstractmethod
    def add_set_function(self, set):
        pass
    @abstractmethod
    def add_setop_function(self, setop):
        pass

    @abstractmethod
    def remove_node_function(self, id):
        pass
    @abstractmethod
    def remove_job_function(self, id):
        pass
    @abstractmethod
    def remove_set_function(self, id):
        pass
    @abstractmethod
    def remove_setop_function(self, id):
        pass

    @abstractmethod
    def apply_setop_function(self, setop):
        pass    

    def apply_placeholder_setop(self, setop):

        num_procs = setop.get_proc_hard_request(setop.op)
        rank = num_procs
        job = self.jobs[setop.jobid]
        nodes_names = self.node_pool.keys()
        for node_name in nodes_names:
            if node_name not in setop.nodelist:
                continue
            node = self.node_pool[node_name]
            if len(node.proc_names) < node.num_slots: 
                num_slots_to_use = min(node.num_slots - len(node.proc_names), num_procs)
                num_procs -= num_slots_to_use
                self.job_add_node_names(job.name, [node_name])
                for i in range(num_slots_to_use):
                    self.add_procs([Proc("setop:"+str(setop.id), -rank, node_name)])
                    rank -= 1

            if num_procs == 0:
                break
        
    
    #####################################
    #Nodes
    #####################################
    def add_nodes(self, nodes):
        for node in nodes:
            self.node_pool[node.name] = node
    
    def remove_nodes(self, nodes):
        for node in nodes:
            self.node_pool.pop(node.name)
    
    def get_num_nodes(self):
        return len(self.node_pool.values())

    def node_set_slots(self, node_name, num_slots):
        self.node_pool[node_name].num_slots = num_slots
    
    # get all nodes that are not part of a job
    def get_free_nodes(self):
        free_nodes = [node.name for node in self.node_pool.values()]
        for job in self.jobs.values():
            for node in job.node_names:
                if node in free_nodes:
                    free_nodes.remove(node)
        return free_nodes

    
    #####################################
    #Jobs
    #####################################
    def add_jobs(self, jobs):
        for job in jobs:
            self.jobs[job.name] = job
    
    def remove_jobs(self, jobs):
        for job in jobs:
            self.jobs.pop(job.name)

    def job_add_node_names(self, jobid, node_names):
        if self.jobs.get(jobid) == None:
            self.add_jobs(Job(jobid))
        self.jobs[jobid].add_node_names(node_names)

    def job_remove_empty_nodes(self, jobid):
        job = self.jobs[jobid]
        node_names = job.node_names.copy()
        for node_name in node_names.keys():
            node = self.node_pool[node_name]
            empty = True
            for proc_name in node.proc_names.keys():
                if proc_name.split(':')[0] == jobid:
                    empty = False
            if empty:
                job.node_names.pop(node_name)

    #####################################
    #PSets
    #####################################
    def add_psets(self, psets):
        for pset in psets:
            self.psets[pset.name] = pset
            if pset.jobid != 'no_jobid':
                self.jobs[pset.jobid].pset_names[pset.name] = pset.name
    
    def pset_assign_to_job(self, pset_name, jobid):
        if self.psets.get(pset_name) == None:
            self.psets[pset_name] = PSet(pset_name, jobid)
        else:
            self.psets[pset_name].set_jobid(jobid)
        if self.jobs.get(jobid) == None:
            self.jobs[jobid] = Job(jobid)
        self.jobs[jobid].add_pset_names([pset_name])

    def pset_set_membership(self, pset_name, proc_names):
        if self.psets.get(pset_name) == None:
            self.psets.add(PSet("no_jobid", pset_name))
        self.psets[pset_name].set_membership(proc_names)
        self.psets[pset_name].size = len(proc_names)

    def remove_psets(self, psets):
        for pset in psets:
            self.psets.pop(pset.name)

    #####################################
    # Procs
    #####################################

    # add a proc to the proc_pool, job object and node
    def add_procs(self, procs):
        for proc in procs:
            self.procs[proc.name] = proc

            if not proc.jobid.startswith("setop:"):
                if self.jobs.get(proc.jobid) == None:
                    job = Job(proc.jobid)
                    self.add_jobs([job])
        
                self.jobs[proc.jobid].add_proc_names([proc.name])

            if self.node_pool.get(proc.node_name) == None:
                node = Node(proc.node_name, 8)
                self.add_nodes([node])
            self.node_pool[proc.node_name].add_procs([proc.name])

    def remove_procs(self, proc_names):
        for proc_name in proc_names:
            if not proc_name.startswith("setop:"):
                self.jobs[proc_name.split(':')[0]].proc_names.pop(proc_name)
            if proc_name in self.procs: 
                proc = self.procs[proc_name]
                self.node_pool[proc.node_name].remove_procs([proc_name])

    #####################################
    # SetOP
    #####################################
    def get_setop(self, setop_id):
        setop = None
        for job in self.jobs.values():
            for i in range(len(job.setops)):
                if job.setops[i].id == setop_id:
                    setop = job.setops[i]
        return setop

    def remove_setop(self, setop_id):
        for job_name in self.jobs.keys():
            for setop in self.jobs[job_name].setops:
                if setop.id == setop_id:
                    self.jobs[job_name].setops.remove(setop)
                    return
    
    def get_setops(self):
        setops=[]
        for job_name in self.jobs.keys():
            for setop in self.jobs[job_name].setops:
                setops.append(setop)
        return setops

    def setop_assign_to_job(self, jobid, setop):
        if self.jobs[jobid] == None:
            self.add_jobs[Job(jobid)]
        self.jobs[jobid].add_setop(setop)

    def setop_apply(self, setop_id, node_map = None, proc_map = None):
        setop = self.get_setop(setop_id)
        if None == setop:
            return

        job = self.jobs[setop.jobid]
        job.setops.remove(setop)


        # For SUB or SHRINK: just remove the processes & nodes from the job, delete the setop
        if setop.op == PMIX_PSETOP_SHRINK or setop.op == PMIX_PSETOP_SUB or setop.op == PMIX_PSETOP_REPLACE:
                pset_name = setop.output[0] # sub delta PSet is always the first ouput PSet
                pset = self.psets[pset_name]
                self.remove_procs([proc_name for proc_name in pset.procs.values()])
                self.job_remove_empty_nodes(job.name)
        # For ADD or GROW: remove placeholder processes, add new procs, delete setop
        if setop.op == PMIX_PSETOP_GROW or setop.op == PMIX_PSETOP_ADD or setop.op == PMIX_PSETOP_REPLACE:
            if None == node_map or None == proc_map:
                return
            num_procs = setop.get_proc_hard_request(setop.op)
            self.remove_procs([Proc.convert_to_procname("setop:"+str(setop.id), -(i+1)) for i in range(num_procs)])

            for node_name, procs in zip(node_map, proc_map):
                node = self.node_pool[node_name]
                if node not in job.node_names.keys():
                    job.node_names[node_name] = node_name
                for rank in procs.split(','):
                    proc_name = Proc.convert_to_procname(job.name, rank)
                    if proc_name not in node.proc_names.keys():
                        proc = Proc(job.name, rank, node_name) 
                        self.add_procs([proc])
                self.job_remove_empty_nodes(job.name)

    #####################################
    # Queue
    #####################################

    def get_waiting_job_size(waiting_job):
        argv = waiting_job[0].split(' ')
        for i in range(len(argv)):
            if argv[i] == '-np':
                return int(argv[i + 1])
        return 0
    
    # get the range of sizes a job can run on
    # returns dict with values for keys 'min', 'max', 'pref' (default = 0)
    def get_waiting_job_size_range(waiting_job):
        range = {'min' : 0, 'max' : 0, 'pref' : 0}

        argv = waiting_job[0].split(' ')
        for i in range(len(argv)):
            if argv[i] == '-np':
                sizes = argv[i + 1].split(',')
                if len(sizes > 0):
                    range['min'] = int(sizes[0])
                    if len(sizes) > 1:
                        range['max'] = int(sizes(1))
                        if len(sizes) > 2:
                            range['pref'] =int(sizes[2])
        return range
    
    def set_waiting_job_size(waiting_job, size):
        argv = waiting_job[0].split(' ')
        for i in range(len(argv)):
            if argv[i] == '-np':
                argv.insert(i, size)
        return 0    

    #####################################
    # Policy
    #####################################
    def set_policy(self, policy):
        self.scheduling_policy = policy            

    
    def schedule(self, parameter_list) -> dict:
        return self.scheduling_policy.schedule(self, parameter_list);

    #####################################
    # System Sate
    #####################################

    def get_num_free_slots(self):
        free_slots = 0

        for node in self.node_pool.values():
            if len(node.proc_names.values()) == 0:
                free_slots += node.num_slots

        return free_slots

    def print(self):
        
        print("")
        print("=================================================")
        print("CURRENT SYSTEM STATE OF SYSTEM '"+self.name+"':")
        print("=================================================")

        print("")
        print(" *********************")
        print("     NODES:")
        i = 1
        for node in self.node_pool.values():
            print("     "+str(i)+": "+node.name+"(slots="+str(node.num_slots)+")") 
            i = i+1
        print(" *********************")

        print("")
        print(" *********************")
        print("     JOBS:")
        i = 1
        for job in self.jobs.values():
            print("     "+str(i)+". '"+str(job.name)+"' (num_nodes = "+str(len(job.node_names))+", num_procs = "+str(len(job.proc_names))+" (+"
                    +str(sum([setop.get_proc_hard_request(PMIX_PSETOP_ADD) for setop in job.setops if setop.is_pending() and (setop.op == PMIX_PSETOP_ADD or setop.op == PMIX_PSETOP_GROW or setop.op == PMIX_PSETOP_REPLACE)]))+"/-"
                    +str(sum([setop.get_proc_hard_request(PMIX_PSETOP_SUB) for setop in job.setops if setop.is_pending() and (setop.op == PMIX_PSETOP_SUB or setop.op == PMIX_PSETOP_SHRINK or setop.op == PMIX_PSETOP_REPLACE)]))
                    +" pending), num_psets = "+str(len(job.pset_names))+")")
            print("         Nodes:")
            for node in job.node_names.values():
                print("             "+str(node)+"   ==>  Procs on this node : "+str([self.procs[proc].rank for proc in self.node_pool[node].proc_names.values()]))
            print("         PSets:")
            for pset in job.pset_names.values():
                print("             "+str(pset)+":  ==> Procs in this PSet: "+str([proc_name.split(':')[1] for proc_name in self.psets[pset].procs.values()]))
            print("         Number of Pending Set Operations:")
            print("             "+str(len([setop for setop in job.setops if setop.is_pending()])))
            i += 1
        print("===================================================")
        print()

    def write_output(self, filename, iter):
        if None == filename:
            return
        nodes = []
        for node in self.node_pool.keys():
            nodes.append(node)
        sorted(nodes)

        with open(filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            if os.path.getsize(filename) == 0:
                header = ["Iteration"]
                for node in nodes:
                    header.append(node)
                writer.writerow(header)

            row = [iter]

            for node in nodes:
                occupied = False
                for job in self.jobs.values():
                    if node in job.node_names.keys():
                        row.append(job.name)
                        occupied = True;
                        break
                if not occupied:    
                    row.append("")

            writer.writerow(row)


    

class Job:

    def __init__(self, jobid):
        self.name = jobid
        self.node_names = dict()
        self.proc_names = dict()
        self.pset_names = dict()
        self.setops = []

    def __str__(self):
        return f"{self.name}"
    
    def add_node_names(self, node_names):
        for node_name in node_names:
            self.node_names[node_name] = node_name
    
    def remove_node_names(self, node_names):
        for node_name in node_names:
            self.node_names.pop(node_name)

    
    def add_proc_names(self, proc_names):
        for proc_name in proc_names:
            self.proc_names[proc_name] = proc_names
    
    def remove_proc_names(self, proc_names):
        for proc_name in proc_names:
            self.proc_names.pop(proc_name)

    def add_pset_names(self, pset_names):
        for pset_name in pset_names:
            self.pset_names[pset_name] = pset_name
    
    def remove_pset_names(self, pset_names):
        for pset_name in pset_names:
            self.pset_names.pop(pset_name)
    
    def add_setop(self, setop):
        self.setops.append(setop)

    def remove_setop(self, setop):
        self.setops.pop(setop)



class Node:
    def __init__(self, name, num_slots):
        self.name = name
        self.num_slots = num_slots
        self.proc_names = dict()


    def __str__(self):
        return f"{self.name}"
    
    def add_procs(self, procs):
        for proc in procs:
            self.proc_names[proc] = proc
    
    def remove_procs(self, procs):
        for proc in procs:
            self.proc_names.pop(proc)


class Proc:
    def __init__(self, jobid, rank, node_name):
        self.name = jobid+":"+str(rank)
        self.jobid = jobid
        self.rank = rank
        self.node_name = node_name
        


    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def convert_to_procname(jobid, rank):
        return str(jobid)+":"+str(rank)

class PSetState:
    def __init__(self, size, res_block, mapping):
        self.size = size
        self.res_block = res_block
        self.mapping = mapping

class PSet:
    def __init__(self, jobid, name):
        self.jobid = jobid
        self.name = name
        self.size = 0
        self.procs = dict()
        self.state = dict()
        self.models = dict()
        
        
    def __str__(self):
        return f"{self.name}({self.size})"
    
    def set_membership(self, proc_names):
        for proc_name in proc_names:
            self.procs[proc_name] = proc_name
        size = len(self.procs)

    def set_pset_state(self, state):
        self.state = state


    def set_jobid(self, jobid):
        self.jobid = jobid


class SetOp:

    STATUS_UNPROCESSED = 0
    STATUS_PENDING = 1
    STATUS_ACKNOWLEDGED = 2

    def __init__(self, id, jobid, op, input, output, info, cbdata):
        self.id = id
        self.status = SetOp.STATUS_UNPROCESSED
        self.jobid = jobid
        self.op = op
        self.input = input
        self.output = output
        self.model = None
        self.info = info
        self.cbdata = cbdata
        self.nodelist = []
        self.additional_info = []
        
    def __str__(self):
        return f"{self.op}: Input={[pset.name for pset in self.input]} Output={[pset.name for pset in self.output]}, Info={self.info}"

    def __eq__(self, other):
        if isinstance(other, SetOp):
            return self.id == other.id
        return False

    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status

    def is_unprocessed(self):
        return self.status == SetOp.STATUS_UNPROCESSED
    
    def is_pending(self):
        return self.status == SetOp.STATUS_PENDING

    def is_acknowleged(self):
        return self.status == SetOp.STATUS_ACKNOWLEDGED
    
    def set_unprocessed(self):
        self.status = SetOp.STATUS_UNPROCESSED

    def set_processed(self):
        self.status = SetOp.STATUS_PENDING

    def set_acknowdlged(self):
        self.status = SetOp.STATUS_ACKNOWLEDGED
    
    def from_info(event_infos):

        id = op = input = output = opinfo = jobid = None
        for event_info in event_infos:
            if event_info['key'] == "prte.alloc.reservation_number":
                id = event_info['value']
            elif event_info['key'] == "prte.alloc.client":
                jobid = event_info['value']['nspace'] 
            elif event_info['key'] == "mpi.rc_op_handle":
                for info in event_info['value']['array']:
                    if info['key'] == "pmix.psetop.type":
                        op = info['value']
                    if info['key'] == "mpi.op_info":
                        for mpi_op_info in info['value']['array']:
                            if mpi_op_info['key'] == "mpi.op_info.input":
                                input = mpi_op_info['value'].split(',')
                            elif mpi_op_info['key'] == "mpi.op_info.output":
                                output = mpi_op_info['value'].split(',')
                            elif mpi_op_info['key'] == "mpi.op_info.info":
                                op_info = mpi_op_info['value']['array']

        if op == None or id == None or input == None or output == None or jobid == None or op_info == None:
            return None

        return SetOp(id, jobid, op, input, output, op_info, event_info)
    

    def get_proc_hard_request(self, op):

        infos = self.additional_info if op == PMIX_PSETOP_REPLACE else self.info

        for info in infos:
            if op == PMIX_PSETOP_ADD or op == PMIX_PSETOP_GROW or op == PMIX_PSETOP_REPLACE:
                if info['key'] == "mpi_num_procs_add":               
                    return int(float(info['value']))
            elif op == PMIX_PSETOP_SUB or op == PMIX_PSETOP_SHRINK:
                if info['key'] == "mpi_num_procs_sub":               
                    return int(float(info['value']))
        

        return 0
    
    def get_proc_max(self):
        for info in self.info:
            if info['key'] == "mpi_num_procs_max":
                return int(info['value'])
        return -1

    def get_proc_min(self):
        for info in self.info:
            if info['key'] == "mpi_num_procs_min":
                return int(info['value'])
        return -1

    def get_proc_pref(self):
        for info in self.info:
            if info['key'] == "mpi_num_procs_pref":
                return int(info['value'])
        return -1
    
    def get_affected_nodes(self, system: DefaultSystemModule):
        node_dict = dict()

        num_delta_sets = 0
        if self.op == PMIX_PSETOP_ADD or self.op == PMIX_PSETOP_SUB or self.op == PMIX_PSETOP_GROW or self.op == PMIX_PSETOP_SHRINK:
            num_delta_sets = 1
        elif self.op == PMIX_PSETOP_REPLACE:
            num_delta_sets = 2
        
        for i in range(num_delta_sets):
            pset = system.psets[self.output[i]]
            for proc_name in pset.procs.keys():
                proc = system.procs[proc_name]
                node_dict[proc.node_name] = system.node_pool[proc.node_name]

        return [node for node in node_dict.values()]

    def toString(self):
        return "Setop: op = "+str(self.op)+", job = "+str(self.jobid)+", input = "+str(self.input)+", output = "+str(self.output)+", info = "+str(self.info)+", nodelist = "+str(self.nodelist)+", additional_info = "+str(self.additional_info)

    

class SchedulingPolicy:

    def __init__(self, name, verbosity_level = 0):
        self.name = name
        self.verbosity_level = verbosity_level

    def schedule(self, my_system: DefaultSystemModule, params: list) -> dict:
        return self.scheduling_function(my_system, params)
    
    @abstractmethod
    def scheduling_function(self, my_system: DefaultSystemModule, params) -> dict:
        v_print("SCHEDULING RESOURCES OF SYSTEM '"+my_system.name+"' WITH POLICY '"+self.name+"'", 1, self.verbosity_level)


class Fifo_Hard_Requests(SchedulingPolicy):

    def scheduling_function(self, my_system: DefaultSystemModule, params: list) ->dict:
        super().scheduling_function(my_system, params)

        jobs_to_start = []
        setops_to_execute = []

        cur_free_slots = my_system.get_num_free_slots()
        cur_free_nodes = my_system.get_free_nodes()
        if len(my_system.queue) > 0:
            v_print("1. Checking if jobs from queue can be scheduled", 2, self.verbosity_level)
            for waiting_job in my_system.queue:
                
                job_size = DefaultSystemModule.get_waiting_job_size(waiting_job)
                if job_size <= cur_free_slots:
                    nodes = []
                    slots = 0
                    for node in my_system.node_pool.values():
                        if len(node.proc_names.values()) == 0:
                            nodes.append(node.name+":"+str(node.num_slots))
                            slots += node.num_slots
                            if slots >= job_size:
                                break
                    if slots >= job_size:
                        index_to_insert = waiting_job[0].index("-np")
                        my_system.queue.remove(waiting_job)
                        waiting_job[0] = waiting_job[0][:index_to_insert] + "--host "+','.join(nodes) +" "+ waiting_job[0][index_to_insert:]
                        return {"jobs_to_start" : [waiting_job], "setops_to_execute" : []}
        else: 
            v_print(" 1. There are no jobs in the job queue", 2, self.verbosity_level)

        v_print("  2. Checking for unprocessed Set Operations ...", 2, self.verbosity_level)
        for jobname in my_system.jobs.keys():
            job = my_system.jobs[jobname]
            if len(job.setops) > 0:
                for i in range(len(job.setops)):
                    setop = job.setops[i]
                    if(setop.is_unprocessed()):
                        v_print("     Checking if Setop '"+str(setop.id)+"' in job '"+job.name+"' can be executed", 3, self.verbosity_level)
                        if (setop.op == PMIX_PSETOP_SUB or  setop.op == PMIX_PSETOP_SHRINK):
                            if setop.get_proc_hard_request(PMIX_PSETOP_SUB) < len(job.proc_names) - sum([setop.get_proc_hard_request() for setop in job.setops if setop.is_pending() and (setop.op == PMIX_PSETOP_SUB or setop.op == PMIX_PSETOP_SHRINK)]):
                                v_print("         Setop '"+str(setop.id)+"' in job '"+job.name+"' is a substraction. Can be executed", 4, self.verbosity_level)
                                setop.set_processed()
                                setop.nodelist = [node for node in my_system.jobs[setop.jobid].node_names]
                                num_to_remove = setop.get_proc_hard_request(PMIX_PSETOP_SUB)
                                for node in list(reversed(list(job.node_names.values()))):
                                    if num_to_remove > 0:
                                        setop.nodelist.remove(node)
                                        num_to_remove -= my_system.node_pool[node].num_slots
                                    else:
                                        break
                                setops_to_execute.append(setop)
                            else:
                                v_print("         Setop '"+str(setop.id)+"' in job '"+job.name+"' is a substraction, but there are not enough procs in the job to substract "+str(setop.get_proc_hard_request())+" processes", 4, self.verbosity_level)
                                
                        elif  setop.op == PMIX_PSETOP_ADD or  setop.op == PMIX_PSETOP_GROW or setop.op == PMIX_PSETOP_REPLACE:
                            v_print("         Setop '"+str(setop.id)+"' in job '"+job.name+"' is an addition. Checking slots", 3, self.verbosity_level)
                            num_procs = setop.get_proc_hard_request(PMIX_PSETOP_ADD)
                            if num_procs > 0:
                                if cur_free_slots - num_procs >= 0:
                                    v_print("         Free slots = "+str(cur_free_slots)+" requested procs = "+str(num_procs)+" ==> GRANTED", 4, self.verbosity_level)
                                    setop.set_processed()
                                    setops_to_execute.append(setop)
                                    setop.nodelist = [node for node in my_system.jobs[setop.jobid].node_names]
                                    num_to_add = num_procs
                                    for node in cur_free_nodes:
                                        if num_to_add > 0:
                                            setop.nodelist.append(node)
                                            num_to_add -= my_system.node_pool[node].num_slots
                                        else:
                                            break
                                    
                                    my_system.apply_placeholder_setop(setop)
                                    cur_free_slots -= num_procs
                                else:
                                    v_print("         Free slots = "+str(cur_free_slots)+" requested procs = "+str(num_procs)+" ==> DENIED", 4, self.verbosity_level)
                        else:
                            #always execute setops which do not require resource changes
                            setops_to_execute.append(setop)
            else:
                v_print("         There are no setops in job "+job.name, 3, self.verbosity_level)

        return {"jobs_to_start" : jobs_to_start, "setops_to_execute" : setops_to_execute}

class DMR_Scheduler(SchedulingPolicy):

    def scheduling_function(self, my_system: DefaultSystemModule, params: list) ->dict:
        super().scheduling_function(my_system, params)

        jobs_to_start = []
        setops_to_execute = []
        #blocked_nodes = []

        cur_free_slots = my_system.get_num_free_slots()
        cur_free_nodes = my_system.get_free_nodes()
        if len(my_system.queue) > 0:
            v_print("1. Checking if jobs from queue can be scheduled", 2, self.verbosity_level)
            for waiting_job in my_system.queue:
                
                job_size = DefaultSystemModule.get_waiting_job_size(waiting_job)
                if job_size <= cur_free_slots:
                    nodes = []
                    slots = 0
                    for node in my_system.node_pool.values():
                        if len(node.proc_names.values()) == 0:
                            nodes.append(node.name+":"+str(node.num_slots))
                            #blocked_nodes.append(node.name)
                            slots += node.num_slots
                            if slots >= job_size:
                                break
                    if slots >= job_size:
                        index_to_insert = waiting_job[0].index("-np")
                        my_system.queue.remove(waiting_job)
                        waiting_job[0] = waiting_job[0][:index_to_insert] + "--host "+','.join(nodes) +" "+ waiting_job[0][index_to_insert:]
                        #cur_free_slots -= job_size
                        return {"jobs_to_start" : [waiting_job], "setops_to_execute" : []}
        else: 
            v_print(" 1. There are no jobs in the job queue", 2, self.verbosity_level)

        # Check if jobs can be resized to start a job from the job queue
        if len(my_system.queue) > 0:
           v_print("1. Checking if jobs from queue can be scheduled by resizing others", 2, self.verbosity_level)
           for waiting_job in my_system.queue:
               job_size = DefaultSystemModule.get_waiting_job_size(waiting_job)

               required_slots = job_size - cur_free_slots

               for jobname in my_system.jobs.keys():
                    job = my_system.jobs[jobname]
                    if len(job.setops) > 0:
                        rm_setops = []
                        for i in range(len(job.setops)):
                            setop = job.setops[i]
                            if(setop.is_unprocessed()):
                                v_print("     Checking if Setop '"+str(setop.id)+"' in job '"+job.name+"' can be executed", 3, self.verbosity_level)

                                if setop.op == PMIX_PSETOP_REPLACE:
                                    v_print("         Setop '"+str(setop.id)+"' in job '"+job.name+"' is an replace. Checking slots", 3, self.verbosity_level)
                
                                    pref = False
                                    if setop.get_proc_pref() != -1:
                                        pref = True
                                        min_procs = setop.get_proc_pref()
                                    else:
                                        min_procs = setop.get_proc_min()
                                    
                                    job_shrink = True
                                    
                                    if not pref:
                                        gathered_slots = 0
                                        aux_cur = cur_procs
                                        while gathered_slots < required_slots:
                                            aux_cur  = aux_cur / 2
                                            if aux_cur < min_procs:
                                                job_shrink = False
                                                break
                                            gathered_slots = cur_procs - aux_cur
                                        
                                        
                                        min_procs = cur_procs - gathered_slots 

                                        
                                    cur_procs = my_system.psets[setop.input[0]].size
                                    num_procs = cur_procs - min_procs

                                    if not job_shrink:
                                        continue

                                    if num_procs >= required_slots:
                                        
                                        v_print("         Free slots = "+str(cur_free_slots)+" requested procs = "+str(num_procs)+" ==> GRANTED", 4, self.verbosity_level)
                                        setop.set_processed()
                                        setop.additional_info.append({'key' : "mpi_num_procs_add", 'flags': 0, 'value' : str(0), 'val_type' : PMIX_STRING})
                                        setop.additional_info.append({'key' : "mpi_num_procs_sub", 'flags': 0, 'value' : str(num_procs), 'val_type' : PMIX_STRING})
                                        setops_to_execute.append(setop)
                                        setop.nodelist = [node for node in my_system.jobs[setop.jobid].node_names]
                                        #num_to_add = num_procs
                                        #occupied_nodes = []
                                        #for node in cur_free_nodes:
                                        #    if num_to_add > 0:
                                        #        setop.nodelist.append(node)
                                        #        occupied_nodes.append(node)
                                        #        num_to_add -= my_system.node_pool[node].num_slots
                                        #    else:
                                        #        break
#
                                        #for node in occupied_nodes:
                                        #    cur_free_nodes.remove(node)    
                                        #my_system.apply_placeholder_setop(setop)
                                        #cur_free_slots -= num_procs
                                        #else:

                                    #always execute setops which do not require resource changes
                                #    setops_to_execute.append(setop)
                                elif setop.op == PMIX_PSETOP_NULL:
                                    rm_setops.append(setop)
                                    setop.additional_info.append({'key' : "PMIX_PSETOP_CANCELED", 'flags': 0, 'value' : True, 'val_type' : PMIX_BOOL})
                                    setop.set_processed()
                                    setops_to_execute.append(setop)
                                elif setop.op == PMIX_PSETOP_CANCEL:
                                    setop.set_processed()
                                    setops_to_execute.append(setop)
                                    
                        for setop in rm_setops:
                            job.setops.remove(setop)
            


        if len(setops_to_execute) > 0:
            return {"jobs_to_start" : jobs_to_start, "setops_to_execute" : setops_to_execute}

        v_print("  2. Checking for unprocessed Set Operations ...", 2, self.verbosity_level)
        for jobname in my_system.jobs.keys():
            job = my_system.jobs[jobname]
            if len(job.setops) > 0:
                rm_setops = []
                for i in range(len(job.setops)):
                    setop = job.setops[i]
                    if(setop.is_unprocessed()):
                        v_print("     Checking if Setop '"+str(setop.id)+"' in job '"+job.name+"' can be executed", 3, self.verbosity_level)

                        if setop.op == PMIX_PSETOP_REPLACE:
                            v_print("         Setop '"+str(setop.id)+"' in job '"+job.name+"' is an addition. Checking slots", 3, self.verbosity_level)
                            max_procs = setop.get_proc_max()
                            cur_procs = my_system.psets[setop.input[0]].size

                            gathered_slots = 0
                            aux_cur = cur_procs
                            while aux_cur <= cur_free_slots:
                                aux_cur  = aux_cur * 2
                                if aux_cur > max_procs:
                                    aux_cur /= 2
                                    break
                            if aux_cur == cur_procs: # then check next
                                continue

                            max_procs = aux_cur


                            num_procs = max_procs - cur_procs
                            
                            if num_procs > 0:
                                if cur_free_slots - num_procs >= 0:
                                    v_print("         Free slots = "+str(cur_free_slots)+" requested procs = "+str(num_procs)+" ==> GRANTED", 4, self.verbosity_level)
                                    setop.set_processed()
                                    setop.additional_info.append({'key' : "mpi_num_procs_add", 'flags': 0, 'value' : str(num_procs), 'val_type' : PMIX_STRING})
                                    setop.additional_info.append({'key' : "mpi_num_procs_sub", 'flags': 0, 'value' : str(0), 'val_type' : PMIX_STRING})
                                    setops_to_execute.append(setop)
                                    setop.nodelist = [node for node in my_system.jobs[setop.jobid].node_names]
                                    num_to_add = num_procs
                                    occupied_nodes = []
                                    for node in cur_free_nodes:
                                        if num_to_add > 0:
                                            setop.nodelist.append(node)
                                            occupied_nodes.append(node)
                                            num_to_add -= my_system.node_pool[node].num_slots
                                        else:
                                            break
                                    
                                    my_system.apply_placeholder_setop(setop)
                                    for node in occupied_nodes:
                                        cur_free_nodes.remove(node)    
                                    cur_free_slots -= num_procs
                                else:
                                    v_print("         Free slots = "+str(cur_free_slots)+" requested procs = "+str(num_procs)+" ==> DENIED", 4, self.verbosity_level)
                        elif setop.op == PMIX_PSETOP_NULL:
                            rm_setops.append(setop)
                            setop.additional_info.append({'key' : "PMIX_PSETOP_CANCELED", 'flags': 0, 'value' : True, 'val_type' : PMIX_BOOL})
                            setop.set_processed()
                            setops_to_execute.append(setop)
                        elif setop.op == PMIX_PSETOP_CANCEL:
                            setop.set_processed()
                            setops_to_execute.append(setop)
                                    
                for setop in rm_setops:
                            job.setops.remove(setop)

                        #else:
                            #always execute setops which do not require resource changes
                        #    setops_to_execute.append(setop)
            else:
                v_print("         There are no setops in job "+job.name, 3, self.verbosity_level)

        return {"jobs_to_start" : jobs_to_start, "setops_to_execute" : setops_to_execute}
'''