
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule
from dyn_rm.mca.base.system.module.psets.pset import MCAPSetModule
from dyn_rm.mca.base.system.module.psets.pset_graph_object import MCAPsetGraphObject

from dyn_rm.util.constants import *

class MCAPSetopModule(MCAEdgeModule, MCAPsetGraphObject):

    PSETOP_STATUS_DEFINED = 0
    PSETOP_STATUS_CANCELED = 1
    PSETOP_STATUS_SCHEDULED = 2
    PSETOP_STATUS_PENDING = 3
    PSETOP_STATUS_ORDERED = 4
    PSETOP_STATUS_FINALIZED = 5
    

    PSETOP_ATTRIBUTE_OP = "PSETOP_OP"
    PSETOP_ATTRIBUTE_STATUS = "PSETOP_STATUS"
    PSETOP_ATTRIBUTE_JOBID = "PSETOP_JOBID"
    PSETOP_ATTRIBUTE_PREDECESSORS = "PSETOP_PREDECESSORS"
    PSETOP_ATTRIBUTE_SUCCESSORS = "PSETOP_SUCCESSORS"
    PSETOP_ATTRIBUTE_PRIORITY = "PSETOP_PRIORITY"

    PSETOP_OP_NULL = 0
    PSETOP_OP_ADD = 1
    PSETOP_OP_SUB = 2
    PSETOP_OP_GROW = 3
    PSETOP_OP_SHRINK = 4
    PSETOP_OP_REPLACE = 5
    PSETOP_OP_UNION = 6
    PSETOP_OP_DIFFERENCE = 7
    PSETOP_OP_INTERSECTION = 8
    PSETOP_OP_SPLIT = 9
    PSETOP_OP_CANCEL = 10

    def __init__(self, name, op, input, output = [], model_name = None, model_module = None, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.__class__.register_base_services(self)
        self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_OP, op)
        self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_STATUS, MCAPSetopModule.PSETOP_STATUS_DEFINED)
        self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS, [])
        self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_SUCCESSORS, [])
        self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PRIORITY, 1)

        self.run_service("SET", "NAME", name)
        if None != model_module and None != model_name:
            self.run_service("ADD", "EDGE_MODEL", model_name, model_module)

        self.run_service("SET", "INPUT", input)
        self.run_service("SET", "OUTPUT", output)
        self._cbfunc = None
        self._cbdata = None

    @staticmethod    
    def register_base_services(self):
        self.register_service("SET", "PSETOP_OUTPUT", self.set_psetop_output)
        self.register_service("GET", "PSETOP_OP", self.get_psetop_op)
        self.register_service("ADD", "PSETOP_MODEL", self.add_psetop_model)
        self.register_service("GET", "PSETOP_MODEL", self.get_psetop_model)
        self.register_service("SET", "PSETOP_STATUS", self.set_psetop_status)
        self.register_service("GET", "PSETOP_STATUS", self.get_psetop_status)
        self.register_service("SET", "PSETOP_CBFUNC", self.set_cbfunc)
        self.register_service("SET", "PSETOP_CBDATA", self.set_cbdata)
        self.register_service("GET", "PSETOP_CBFUNC", self.get_cbfunc)
        self.register_service("GET", "PSETOP_CBDATA", self.get_cbdata)
        self.register_service("GET", "PSET_GRAPH", self.get_pset_graph)
        self.register_service("GET", "PRIORITY", self.get_priority)
        self.register_service("SET", "PRIORITY", self.set_priority)


    def get_priority(self):
        return self.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PRIORITY)
    def set_priority(self, priority):
        return self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PRIORITY, priority)


    def set_psetop_output(self, output):
        return self.run_service("SET", "OUTPUT", output)
    
    def get_psetop_op(self):
        return self.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_OP)

    def add_psetop_model(self, model_name, model):
        return self.run_service("ADD", "EDGE_MODEL", model_name, model)

    def get_psetop_model(self, model_name):
        return self.run_service("GET", "EDGE_MODEL", model_name)

    def set_psetop_status(self, status):
        return self.run_service("SET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_STATUS, status)
    
    def get_psetop_status(self):
        return self.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_STATUS)

    def set_cbfunc(self, cbfunc):
        self._cbfunc = cbfunc
        return DYNRM_MCA_SUCCESS
    
    def set_cbdata(self, cbdata):
        self._cbdata = cbdata
        return DYNRM_MCA_SUCCESS

    def get_cbfunc(self):
        return self._cbfunc

    def get_cbdata(self):
        return self._cbdata
    
    def get_pset_graph(self):
        graphs = self.run_service("GET", "GRAPHS")
        for graph in graphs:
            if isinstance(graph, MCAPSetModule):
                return graph
        return None

    

        



    

