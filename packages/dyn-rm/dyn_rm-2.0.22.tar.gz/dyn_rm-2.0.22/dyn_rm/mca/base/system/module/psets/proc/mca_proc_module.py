from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.system.module.psets.pset import MCAPSetModule
from dyn_rm.mca.base.system.module.psets.pset_graph_object import MCAPsetGraphObject

from dyn_rm.util.constants import *

class MCAProcModule(MCAVertexModule, MCAPsetGraphObject):

    PROC_ATTRIBUTE_STATUS = "PROC_STATUS"
    PROC_ATTRIBUTE_JOBID = "PROC_JOBID"
    PROC_ATTRIBUTE_EXECUTABLE = "PROC_EXECUTABLE"

    PROC_STATUS_NEW = 0
    PROC_STATUS_LAUNCH_REQUESTED = 1
    PROC_STATUS_IN_LAUNCH = 2
    PROC_STATUS_RUNNING = 3
    PROC_STATUS_TERMINATION_REQUESTED = 4
    PROC_STATUS_IN_TERMINATION = 5
    PROC_STATUS_TERMINATED = 6

    PROC_CORE_ACCESS_EDGE_KEY = "CORE_ACCESS"

    def __init__(self, procid, executable, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCAProcModule.register_base_services(self)
        self.run_service("SET", "NAME", procid)
        self.run_service("SET", "EXECUTABLE", executable)
        self.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_NEW)

    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "PROC_STATUS", self.set_proc_status)
        self.register_service("SET", "CORE_ACCESS", self.set_core_access)
        self.register_service("SET", "EXECUTABLE", self.set_proc_executable)
        
        self.register_service("GET", "PROC_STATUS", self.get_proc_status)
        self.register_service("GET", "CORE_ACCESS", self.get_core_access)
        self.register_service("GET", "EXECUTABLE", self.get_proc_executable)
        
        self.register_service("GET", "PSETS", self.get_psets)
        self.register_service("GET", "PSET_GRAPH", self.get_pset_graph)
        self.register_service("GET", "PSET_EDGES", self.get_pset_edges)
        

    def set_proc_status(self, status):
        return self.run_service("SET", "ATTRIBUTE", MCAProcModule.PROC_ATTRIBUTE_STATUS, status)

    def get_proc_status(self):
        return self.run_service("GET", "ATTRIBUTE", MCAProcModule.PROC_ATTRIBUTE_STATUS)


    def set_core_access(self, cores):
        core_access_edge = MCAEdgeModule()
        core_access_edge.run_service("SET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_ACCESS_RELATION, True)
        core_access_edge.run_service("SET", "INPUT", [self])
        core_access_edge.run_service("SET", "OUTPUT", cores)
        self.run_service("ADD", "OUT_EDGE", core_access_edge)

    def get_core_access(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_ACCESS_RELATION):
                return True
            return False
        edges = self.run_service("GET", "EDGES_BY_FILTER", filter)
        if 1 != len(edges):
            return []
        return edges[0].run_service("GET", "OUTPUT")
    

    def set_proc_executable(self, executable):
        return self.run_service("SET", "ATTRIBUTE", MCAProcModule.PROC_ATTRIBUTE_EXECUTABLE, executable)

    def get_proc_executable(self):
        return self.run_service("GET", "ATTRIBUTE", MCAProcModule.PROC_ATTRIBUTE_EXECUTABLE)



    def get_pset_edges(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_MEMBERSHIP):
                return True
            return False
        return self.run_service("GET", "EDGES_BY_FILTER", filter)

    def get_psets(self):
        return [edge.run_service("GET", "INPUT")[0] for edge in self.get_pset_edges()]
    

    def get_pset_graph(self):
        graphs = self.run_service("GET", "GRAPHS")
        for graph in graphs:
            if isinstance(graph, MCAPSetModule):
                return graph
        return None


