from dyn_rm.mca.base.graph.module.graph import MCAGraphModule
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule

from dyn_rm.util.constants import *

class MCATopologyGraphModule(MCAGraphModule):

    def __init__(self, topology_name, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCATopologyGraphModule.register_base_services(self)
        self.run_service("SET", "NAME", topology_name)

    @staticmethod
    def register_base_services(self):
        self.register_service("ADD", "CONTAINMENT_RELATION", self.add_containment_relation)
        self.register_service("ADD", "TOPOLOGY_OBJECTS", self.add_topology_objects)
        self.register_service("GET", "TOPOLOGY_OBJECTS", self.get_topology_objects)
        self.register_service("PRINT", "TOPOLOGY_GRAPH", self.print_topology)
    

    def add_containment_relation(self, parent, children: list):
        if None == self.run_service("GET", "GRAPH_VERTEX", parent.run_service("GET", "GID")):
            return DYNRM_ERR_NOT_FOUND
        for child in children:
            if None == self.run_service("GET", "GRAPH_VERTEX", child.run_service("GET", "GID")):
                return DYNRM_ERR_NOT_FOUND
        
        edge = MCAEdgeModule()
        edge.run_service("SET", "GID", self.run_service("GET", "NEW_GID"))
        edge.run_service("SET", "INPUT", [parent])
        edge.run_service("SET", "OUTPUT", children)
        edge.run_service("SET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION, True)
        
        parent.run_service("ADD", "OUT_EDGE", edge)
        for child in children:
            child.run_service("ADD", "IN_EDGE", edge)

        return self.run_service("ADD", "GRAPH_EDGES", [edge])
    
    def add_topology_objects(self, objects):
        return self.run_service("ADD", "GRAPH_VERTICES", objects)
    
    def get_topology_objects(self, object_type):
        return self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, object_type))
    
    def print_dfs(self, level, vertex):
        def filter(edge):
            if not vertex in edge.run_service("GET", "INPUT"):
                return False
            return None != edge.run_service("GET", "ATTRIBUTE",  MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION)
            
        prefix = ' ' * level * 4
        print(prefix+str(type(vertex).__name__)+": "+vertex.run_service("GET", "NAME"))
        containment_edges = vertex.run_service("GET", "EDGES_BY_FILTER", filter)
        for edge in containment_edges:
            children = edge.run_service("GET", "OUTPUT")
            for child in children:
                rc = self.print_dfs(level + 1, child)
                if rc != DYNRM_MCA_SUCCESS:
                    return rc
        return DYNRM_MCA_SUCCESS 

    def print_topology(self, params = dict()):
        def filter(vertex):
            edges = vertex.run_service("GET", "IN_EDGES")
            for edge in edges:
                if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION):
                    return False
            return True
        root_objects = self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", filter)
        print()
        print("========= TOPOLOGY GRAPH ========")
        for root_object in root_objects:
            self.print_dfs(1, root_object)
        print("=================================")
        print()

