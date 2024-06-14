from dyn_rm.mca.mca import MCAComponent

from dyn_rm.util.constants import *

# This Component Class provides services to manage a dictionary of edge modules
class MCAEdgeComponent(MCAComponent):

    NAME_NONE = 0

    CLASS_NONE = 0
    CLASS_DIRECTED = 1
    CLASS_UNDIRECTED = 2

    TYPE_NONE = 0
    TYPE_KINSHIP = 1
    TYPE_MAP = 2
    TYPE_DEPENDENCY = 3
    TYPE_TRANSITION = 4
    TYPE_MEMBERSHIP = 5
    TYPE_EXTERNAL = 100

    STATUS_UNPROCESSED = 0
    STATUS_PENDING = 1
    STATUS_APPLIED = 2
    STATUS_EXTERNAL = 100


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._edges = dict()
        MCAEdgeComponent.register_base_services(self)
        
    @staticmethod    
    def register_base_services(self):
        self.register_service("ADD", "EDGE", self.add_edge)
        self.register_service("ADD", "EDGES", self.add_edges)
        self.register_service("GET", "EDGE", self.get_edge)
        self.register_service("GET", "EDGES", self.get_edges)
        self.register_service("GET", "ALL_EDGES", self.get_all_edges)
        self.register_service("GET", "EDGES_BY_FILTER", self.get_edges_by_filter)
        self.register_service("REMOVE", "EDGE", self.remove_edge)
        self.register_service("REMOVE", "EDGES", self.remove_edges)
        self.register_service("REMOVE", "EDGES_BY_FILTER", self.remove_edges_by_filter)
        self.register_service("GET", "NUM_EDGES", self.get_num_edges)


    def add_edge(self, edge):
        self._edges[edge.run_service("GET", "GID")] = edge
        return DYNRM_MCA_SUCCESS

    def add_edges(self, edges):
        for edge in edges:
            rc = self.add_edge(edge)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    def get_edge(self, name):
        return self._edges.get(name, None)
    
    def get_edges(self, names):
        edges = []
        for name in names:
            edges.append(self.get_edge(name))

        return edges

    def get_all_edges(self):
        return list(self._edges.values())

    def remove_edge(self, name):
        return self._edges.pop(name, None)
    
    def remove_edges(self, names):
        for name in names:
            return self.remove_edge(name)

    def get_num_edges(self):
        return len(self._edges)
    
    def get_edges_by_filter(self, edge_filter):
        output = dict()
        for name in self._edges.keys():
            if edge_filter(self._edges[name]):
                output[name] = self._edges[name]
        return list(output.values())
    
    def remove_edges_by_filter(self, name, edge_filter):
        edges = self.get_edges_by_filter(name, edge_filter)
        self.remove_edges([e.run_service("GET", "GID") for e in edges])        
        return DYNRM_MCA_SUCCESS
    

