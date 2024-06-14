from dyn_rm.mca.mca import MCAClass

from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.system.module.topology.core import MCACoreModule
from dyn_rm.mca.base.system.module.topology.topology_graph_object import MCATopologyGraphObject


from dyn_rm.util.constants import *

class MCANodeModule(MCAVertexModule, MCAClass, MCATopologyGraphObject):

    NODE_ATTRIBUTE_STATUS = "NODE_STATUS"

    NODE_STATUS_NEW = 0
    NODE_STATUS_IN_STARTUP = 1
    NODE_STATUS_UP = 2
    NODE_STATUS_IN_TEARDOWN = 3
    NODE_STATUS_DOWN = 4

    NODE_CORE_MEMBERSHIP_ATTRIBUTE = "NODE_CORE_MEMBERSHIP"

    def __init__(self, nodeid, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCANodeModule.register_base_services(self)
        self.run_service("SET", "NAME", nodeid)
        self.run_service("SET", "NODE_STATUS", MCANodeModule.NODE_STATUS_NEW)

    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "NODE_STATUS", self.set_node_status)
        self.register_service("GET", "NODE_STATUS", self.get_cores)
        self.register_service("GET", "NUM_CORES", lambda : len(self.get_cores()))
        self.register_service("GET", "CORES", self.get_cores)
        self.register_service("GET", "FREE_CORES", self.get_free_cores)
        self.register_service("GET", "UTILIZED_CORES", self.get_utilized_cores)

    def set_node_status(self, status):
        return self.run_service("SET", "ATTRIBUTE", MCANodeModule.NODE_ATTRIBUTE_STATUS, status)
    def get_node_status(self):
        return self.run_service("GET", "ATTRIBUTE", MCANodeModule.NODE_ATTRIBUTE_STATUS)

    def get_cores(self):
        # assuming only _ONE_ core set
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION):
                output = edge.run_service("GET", "OUTPUT")
                if len(output) == 0:
                    return False
                for elem in output:
                    if not isinstance(elem, MCACoreModule):
                        return False
                return True
            return False
        mem_edges = self.run_service("GET", "EDGES_BY_FILTER", filter)
        if len(mem_edges) == 1:
            return [core for core in mem_edges[0].run_service("GET", "OUTPUT")]
        return []
    
    def get_free_cores(self):      
        return [c for c in self.get_cores() if c.run_service("CHECK", "FREE")]

    def get_utilized_cores(self):      
        return [c for c in self.get_cores() if c.run_service("CHECK", "UTILIZED")]
