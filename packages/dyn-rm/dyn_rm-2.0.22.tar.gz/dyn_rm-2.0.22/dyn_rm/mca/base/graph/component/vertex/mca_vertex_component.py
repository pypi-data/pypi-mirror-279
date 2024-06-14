from dyn_rm.mca.mca import MCAComponent

from dyn_rm.util.constants import *

# This Component Class provides services to manage a dictionary of vertex modules
class MCAVertexComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._vertices = dict()
        MCAVertexComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("ADD", "VERTEX", self.add_vertex)
        self.register_service("ADD", "VERTICES", self.add_vertices)
        self.register_service("GET", "VERTEX", self.get_vertex)
        self.register_service("GET", "VERTICES", self.get_vertices)
        self.register_service("GET", "ALL_VERTICES", self.get_all_vertices)
        self.register_service("GET", "VERTICES_BY_FILTER", self.get_vertices_by_filter)
        self.register_service("REMOVE", "VERTEX", self.remove_vertex)
        self.register_service("REMOVE", "VERTICES_BY_FILTER", self.remove_vertices_by_filter)
        self.register_service("GET", "NUM_VERTICES", self.get_num_vertices)



    def add_vertex(self, vertex):
        self._vertices[vertex.run_service("GET", "GID")] = vertex
        return DYNRM_MCA_SUCCESS

    def add_vertices(self, vertices):
        for vertex in vertices:
            self.add_vertex(vertex)
        return DYNRM_MCA_SUCCESS

    def get_vertex(self, name):
        return self._vertices.get(name, None)
    
    def get_vertices(self, names):
        vertices = []
        for name in names:
            vertices.append(self.get_vertex(name))
        return vertices
    
    def get_all_vertices(self):
        return [vertex for vertex in self._vertices.values()]
    
    def remove_vertex(self, name):
        return self._vertices.pop(name, None)

    def remove_vertices(self, names):
        for name in names:
            self.remove_vertex(name)
        return DYNRM_MCA_SUCCESS

    def get_num_vertices(self):
        return len(self._vertices)
    
    def get_vertices_by_filter(self, edge_filter):
        output = dict()
        for name in self._vertices:
            if edge_filter(self._vertices[name]):
                output[name] = self._vertices[name]
                
        return list(output.values())
    
    def remove_vertices_by_filter(self, name, edge_filter):
        vertices = self.get_vertices_by_filter(name, edge_filter)
        self.remove_vertices([e.run_service("GET", "GID") for e in vertices])        
        return DYNRM_MCA_SUCCESS
    

