from dyn_rm.mca.mca import MCAComponent
from dyn_rm.mca.mca import MCAClass
from dyn_rm.mca.base.graph.component.vertex_model import MCAVertexModelComponent
from dyn_rm.mca.base.graph.component.edge_model import MCAEdgeModelComponent

from dyn_rm.util.constants import *

class MCASystemComponent(MCAComponent, MCAClass):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._systems = dict()
        MCASystemComponent.register_base_services(self)

        
    def register_base_services(self):
        self.register_service("ADD", "SYSTEM", self.add_system)
        self.register_service("GET", "SYSTEM", self.get_system)
        self.register_service("REMOVE", "SYSTEM", self.remove_system)


    def add_system(self, name, system):
        self.register_module(system)
        self._systems[name] = system
        return DYNRM_MCA_SUCCESS

    def get_system(self, name):
        return self._systems.get(name)

    def remove_system(self, name):
        return self._systems.pop(name) 

    def mca_shutdown(self):
        for system in self._systems.values():
            system.run_service("MCA", "SHUTDOWN")
        return self.mca_default_shutdown()

'''
    def create_setop(
        id, 
	    job_id, 
	    op, 
	    input, 
	    output,
        info,
        cbdata, 
	    setop_model_module_class,
	    setop_model_params : dict,
	    set_model_modules : dict, 
	    set_model_params : dict,
	    active_states : dict, 
	    state_spaces : dict,
        verbosity=0):

        # Create a setop with a Grow SetOp Model
        setop = MCASystemComponent.SetOp(id, job_id, op, input, output, info, cbdata)
        setop_model_component = MCAEdgeModelComponent(verbosity=verbosity)
        setop_model_module = setop_model_module_class(verbosity=verbosity)
        setop_model_component.register_module(setop_model_module)
        setop_model_component.run_service("SET", "MODEL_PARAMS", setop_model_params)

        for name in set_model_modules.keys():
            set_model_component = MCAVertexModelComponent(verbosity=verbosity)
            set_model_module = set_model_modules[name](verbosity=verbosity)
            set_model_component.register_module(set_model_module)
            if name in set_model_params:
                set_model_component.run_service("SET", "MODEL_PARAMS", set_model_params[name])

            setop_model_component.run_service("ADD", "SET_MODEL", name, set_model_component)
            
            if name in active_states:
                setop_model_component.run_service("SET", "SET_STATE_ACTIVE", name, active_states[name])
            if name in state_spaces:
                setop_model_component.run_service("SET", "STATE_SPACE", name, state_spaces[name])
        
        setop.model = setop_model_component
        return setop

    def generate_new_set_id(self):
        set_id =  self.system_name+"/sets/"+str(self.set_id)
        self.set_id += 1
        return set_id

    def generate_new_setop_id(self):
        setop_id =  self.system_name+"/setops/"+str(self.setop_id)
        self.setop_id += 1
        return setop_id
    
    def generate_new_job_id(self):
        job_id =  self.system_name+"/jobs/"+str(self.job_id)
        self.job_id += 1
        return job_id
'''
    ########### Common classes for representing Nodes, Jobs, Sets and SetOps ###########
'''
    class Job:
        STATUS_NONE = 0
        STATUS_SUBMITTED = 1
        STATUS_RUNNING = 2
        STATUS_PAUSED = 3
        STATUS_TERMINATED = 5

        def __init__(self, jobid, node_ids, proc_ids, pset_ids, setop_ids):
            self.id = jobid
            self.node_ids = node_ids
            self.proc_ids = proc_ids
            self.pset_ids = pset_ids
            self.setop_ids = setop_ids
            self.status = MCASystemComponent.Job.STATUS_NONE

        def __str__(self):
            return f"{self.id}"

        def add_node_ids(self, node_ids):
            for node_id in node_ids:
                self.node_ids[node_id] = node_id

        def remove_node_ids(self, node_ids):
            for node_id in node_ids:
                self.node_ids.pop(node_id)

        def add_proc_ids(self, proc_ids):
            for proc_id in proc_ids:
                self.proc_ids[proc_id] = proc_ids

        def remove_proc_ids(self, proc_ids):
            for proc_id in proc_ids:
                self.proc_ids.pop(proc_id)

        def add_pset_ids(self, pset_ids):
            for pset_id in pset_ids:
                self.pset_ids[pset_id] = pset_id

        def remove_pset_ids(self, pset_ids):
            for pset_id in pset_ids:
                self.pset_ids.pop(pset_id)

        def add_setop_id(self, setop_id):
            self.setops.append(setop_id)

        def remove_setop_id(self, setop):
            self.setops.pop(setop)



    class Node:
        def __init__(self, id, num_slots):
            self.id = id
            self.num_slots = num_slots
            self.proc_ids = []
            self.job_ids = []

        def __str__(self):
            return f"{self.id}"

        def add_procs(self, procs):
            for proc in procs:
                self.proc_ids[proc] = proc

        def remove_procs(self, procs):
            for proc in procs:
                self.proc_ids.pop(proc)


    class Proc:
        def __init__(self, jobid, rank, node_id):
            self.id = jobid+":"+str(rank)
            self.jobid = jobid
            self.rank = rank
            self.node_id = node_id

        def __str__(self):
            return f"{self.id}"

        @staticmethod
        def convert_to_procid(jobid, rank):
            return str(jobid)+":"+str(rank)

    class Set:
        MEMBER_TYPE_PROC = 0
        MEMBER_TYPE_NODE = 2
        MEMBER_TYPE_SOCKET = 3
        MEMBER_TYPE_NUMA = 4
        MEMBER_TYPE_CORE = 5
        MEMBER_TYPE_GPU = 6
        MEMBER_TYPE_MEM_UNIT = 7
        MEMBER_TYPE_L1_CACHE = 8
        MEMBER_TYPE_L2_CACHE = 9
        MEMBER_TYPE_L3_CACHE = 10

        # Directedness of 
        RELATION_DIRECTION_OUT = 100
        RELATION_DIRECTION_IN = 101
        RELATION_DIRECTION_INOUT = 102


        def __init__(self, id, graph_id, vertex_id, member_ids, related_sets = [], maps = []):
            self.id = id
            self.vertex_id = vertex_id
            self.graph_id = graph_id
            self.member_ids = member_ids
            self.size = len(member_ids)
            self.related_sets = related_sets if related_sets != None else []
            self.maps = maps if maps != None else []

        
    def __str__(self):
        return f"{self.id}({self.size})"
    
    def set_membership(self, proc_ids):
        for proc_id in proc_ids:
            self.procs[proc_id] = proc_id
        size = len(self.procs)

    def set_pset_state(self, state):
        self.state = state


    def set_jobid(self, jobid):
        self.jobid = jobid


    class SetOp:

        STATUS_UNPROCESSED = 0
        STATUS_PENDING = 1
        STATUS_APPLIED = 2

        OP_NULL            =       0   # Invalid pset operation
        OP_ADD             =       1   # Resources are added
        OP_SUB             =       2   # Resources are removed
        OP_GROW            =       3   # ADD + UNION
        OP_SHRINK          =       4   # SUB + DIFFERENCE
        OP_REPLACE         =       5   # Resources are replaced
        OP_UNION           =       6   # The union of two psets is requested
        OP_DIFFERENCE      =       7   # The difference of two psets is requested
        OP_INTERSECTION    =       8   # The intersection of two psets is requested
        OP_MULTI           =       9  # Multiple operations specified in the info object
        OP_SPLIT           =       10  # Splt operation
        OP_CANCEL          =       11  # Cancel PSet Operations

        def __init__(self, id, jobid, op, input, output, info, cbdata):
            self.id = id
            self.status = MCASystemComponent.SetOp.STATUS_UNPROCESSED
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
            return f"{self.op}: Input={[pset.id for pset in self.input]} Output={[pset.id for pset in self.output]}, Info={self.info}"

        def __eq__(self, other):
            if isinstance(other, SetOp):
                return self.id == other.id
            return False

        def set_status(self, status):
            self.status = status

        def get_status(self):
            return self.status

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

    '''