from dyn_rm.mca.mca import MCAClass
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.graph.component.vertex_model import MCAVertexModelComponent

from dyn_rm.util.constants import *


class MCAVertexModule(MCAGraphObjectModule, MCAClass):

    MCA_VERTEX_STATUS_INVALID = -1
    MCA_VERTEX_STATUS_VALID = 0
    MCA_VERTEX_STATUS_NEW = 1
    MCA_VERTEX_STATUS_UPDATED = 2


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)

        self.in_edges = []
        self.out_edges = []
        self.monitoring_data = dict()
        self.register_component(MCAVertexModelComponent())
        MCAVertexModule.register_base_services_(self)

        
    @staticmethod
    def register_base_services_(self):

        # add edges
        self.register_service("ADD", "IN_EDGE", self.add_in_edge)
        self.register_service("ADD", "OUT_EDGE", self.add_out_edge)
        
        # set edges
        self.register_service("SET", "IN_EDGES", self.set_in_edges)
        self.register_service("SET", "OUT_EDGES", self.set_out_edges)

        # get edges
        self.register_service("GET", "EDGE", self.get_edge)
        self.register_service("GET", "EDGES", self.get_edges)
        self.register_service("GET", "IN_EDGES", self.get_in_edges)
        self.register_service("GET", "OUT_EDGES", self.get_out_edges)
        self.register_service("GET", "EDGES_BY_FILTER", self.get_edges_by_filter)

        # remove edges
        self.register_service("REMOVE", "IN_EDGE", self.remove_in_edge)
        self.register_service("REMOVE", "OUT_EDGE", self.remove_out_edge)
        self.register_service("REMOVE", "EDGE", self.remove_edge)
        self.register_service("REMOVE", "EDGES", self.remove_edge)
        self.register_service("REMOVE", "EDGES_BY_FILTER", self.remove_edge)

        # monitoring data
        self.register_service("ADD", "MONITORING_ENTRY", self.add_monitoring_entry)
        self.register_service("GET", "MONITORING_ENTRY", self.get_monitoring_entry)
        self.register_service("REMOVE", "MONITORING_ENTRY", self.remove_monitoring_entry)
        self.register_service("SET", "MONITORING_DATA", self.set_monitoring_data)
        self.register_service("GET", "MONITORING_DATA", self.get_monitoring_data)

        # Vertex Models
        self.register_service("ADD", "VERTEX_MODEL", self.add_vertex_model)
        self.register_service("SET", "ACTIVE_VERTEX_MODEL", self.set_active_vertex_model)
        self.register_service("GET", "ACTIVE_VERTEX_MODEL", self.get_active_vertex_model)
        self.register_service("GET", "VERTEX_MODEL", self.get_vertex_model)  
        self.register_service("GET", "VERTEX_MODEL_NAMES", self.get_vertex_model_names)       
        self.register_service("REMOVE", "VERTEX_MODEL", self.remove_vertex_model)


    # Graphs
    def add_graph(self, graph):
        self._graphs[graph.run_service("GET", "GID")] = graph
        return DYNRM_MCA_SUCCESS
    def get_graphs(self):
        return list(self._graphs.values())
    def remove_graph(self, name):
        return self._graphs.pop(name, None)
    
    # Add Edge
    def add_in_edge(self, edge):
        self.in_edges.append(edge)
        return DYNRM_MCA_SUCCESS
    
    def add_out_edge(self, edge):
        self.out_edges.append(edge)
        return DYNRM_MCA_SUCCESS
    
    # Set Edges
    def set_in_edges(self, edges):
        self.in_edges = edges
    def set_out_edges(self, edges):
        self.out_edges = edges

    # Remove Edge
    def remove_in_edge(self, name):
        r_edge = None
        for edge in self.in_edges:
            if edge.run_service("GET", "GID") == name:
                r_edge = self.in_edges.remove(edge)      
        return r_edge
    def remove_out_edge(self, name):
        r_edge = None
        for edge in self.out_edges:
            if edge.run_service("GET", "GID") == name:
                r_edge = self.out_edges.remove(edge)      
        return r_edge
    

    # Get Edges
    def get_edge(self, name):
        r_edge = None
        for edge in self.in_edges:
            if edge.run_service("GET", "GID") == name:
                r_edge = edge 
                break  
        if None == r_edge:
            for edge in self.out_edges:
                if edge.run_service("GET", "GID") == name:
                    r_edge = edge
                    break
        return r_edge
    
    def get_edges(self):
        output = []
        output.extend(self.in_edges)
        for edge in self.out_edges:
            if edge not in output:
                output.append(edge)
        return output
    
    def get_in_edges(self):
        return [] + self.in_edges
    def get_out_edges(self):
        return [] + self.out_edges
    
    def get_edges_by_filter(self, edge_filter):
        output = []
        edges = self.get_edges()
        for edge in edges:
            if edge not in output and edge_filter(edge):
                output.append(edge)
        return output
    

    

    # Remove Edges
    def remove_edge(self, name):
        edge = None
        if name in [e.run_service("GET", "GID") for e in self.in_edges]:
            index = [e.run_service("GET", "GID") for e in self.in_edges].index(name)
        else:
            index = -1
        if -1 < index:
            return self.in_edges.pop(index)

        if name in [e.run_service("GET", "GID") for e in self.out_edges]:
            index = [e.run_service("GET", "GID") for e in self.out_edges].index(name)
        else:
            index = -1
        if -1 < index:
            return self.out_edges.pop(index)
        return edge

   

    def add_monitoring_entry(self, entry_name, entry):
        self.monitoring_data[entry_name] = entry
        return DYNRM_MCA_SUCCESS
    
    def get_monitoring_entry(self, entry_name):
        return self.monitoring_data.get(entry_name)
    
    def remove_monitoring_entry(self, entry_name):
        return self.monitoring_data.pop(entry_name, None)
        
    def set_monitoring_data(self, data: dict):
        self.monitoring_data = data
        return DYNRM_MCA_SUCCESS
    def get_monitoring_data(self):
        return self.monitoring_data
    

    
    def add_vertex_model(self, model_name, model):
        return self.run_component_service(MCAVertexModelComponent, "ADD", "MODEL", model_name, model)
    def set_active_vertex_model(self, model_name):
        return self.run_component_service(MCAVertexModelComponent, "SET", "ACTIVE_MODEL", model_name)
    def get_active_vertex_model(self):
        return self.run_component_service(MCAVertexModelComponent, "GET", "ACTIVE_MODEL")
    def get_vertex_model(self, model_name):
        return self.run_component_service(MCAVertexModelComponent, "GET", "MODEL", model_name) 
    def get_vertex_model_names(self):
        return self.run_component_service(MCAVertexModelComponent, "GET", "MODEL_NAMES")  
    def remove_vertex_model(self, model_name):
        return self.run_component_service(MCAVertexModelComponent, "REMOVE", "MODEL", model_name)   

    @staticmethod
    def get_copy(self, vertex_copy):
        vertex_copy = MCAGraphObjectModule.get_copy(self, vertex_copy)

        for edge in self.in_edges:
            vertex_copy.run_service("ADD", "IN_EDGE", edge)
        for edge in self.out_edges:
            vertex_copy.run_service("ADD", "OUT_EDGE", edge)
        names = self.get_vertex_model_names()
        for name in names:
            model = self.get_vertex_model(name)
            vertex_copy.run_service("ADD", "MODEL", name, model)
        for key in self.monitoring_data.keys():
            vertex_copy.run_service("ADD", "MONITORING_ENTRY", key, self.monitoring_data[key])
        return vertex_copy