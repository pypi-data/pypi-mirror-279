from dyn_rm.mca.mca import MCAClass
from dyn_rm.mca.base.graph.component.edge_model import MCAEdgeModelComponent
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule

from dyn_rm.util.constants import *

class MCAEdgeModule(MCAGraphObjectModule, MCAClass):

    MCA_EDGE_STATUS_INVALID = -1
    MCA_EDGE_STATUS_VALID = 0
    MCA_EDGE_STATUS_NEW = 1
    MCA_EDGE_STATUS_UPDATED = 2

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.input = []
        self.output = []
        self.monitoring_data = dict()
        self.register_component(MCAEdgeModelComponent())
        MCAEdgeModule.register_base_services(self)

        
    @staticmethod    
    def register_base_services(self):

        self.register_service("SET", "INPUT", self.set_input)
        self.register_service("SET", "OUTPUT", self.set_output)
        self.register_service("SET", "INPUT_AT_INDEX", self.set_input_at_index)
        self.register_service("SET", "OUTPUT_AT_INDEX", self.set_output_at_index)

        self.register_service("APPEND", "INPUT", self.append_input)
        self.register_service("APPEND", "OUTPUT", self.append_output)

        self.register_service("GET", "INPUT", self.get_input)
        self.register_service("GET", "INPUT_SIZE", self.get_input_size)
        self.register_service("GET", "OUTPUT", self.get_output)
        self.register_service("GET", "OUTPUT_SIZE", self.get_output_size)
        self.register_service("GET", "INPUT_AT_INDEX", self.get_input_at_index)
        self.register_service("GET", "OUTPUT_AT_INDEX", self.get_output_at_index)
        self.register_service("GET", "INDEX_IN_INPUT", self.get_index_in_input)
        self.register_service("GET", "INDEX_IN_OUTPUT", self.get_index_in_output)
        self.register_service("REMOVE", "INPUT_AT_INDEX", self.remove_input_at_index)
        self.register_service("REMOVE", "OUTPUT_AT_INDEX", self.remove_output_at_index)

        self.register_service("ADD", "MONITORING_ENTRY", self.add_monitoring_entry)
        self.register_service("GET", "MONITORING_ENTRY", self.get_monitoring_entry)
        self.register_service("REMOVE", "MONITORING_ENTRY", self.remove_monitoring_entry)

        self.register_service("SET", "MONITORING_DATA", self.set_monitoring_data)
        self.register_service("GET", "MONITORING_DATA", self.get_monitoring_data)
        
        self.register_service("ADD", "EDGE_MODEL", self.add_edge_model)
        self.register_service("GET", "EDGE_MODEL", self.get_edge_model)
        self.register_service("REMOVE", "EDGE_MODEL", self.remove_edge_model)


    def set_input(self, input: list):
        self.input = input
        return DYNRM_MCA_SUCCESS
    def set_output(self, output: list):
        self.output = output
        return DYNRM_MCA_SUCCESS

    def set_input_at_index(self, index, input):
        if index > len(self.input):
            return DYNRM_MCA_ERR_BAD_PARAM
        self.input[index] = input
        return DYNRM_MCA_SUCCESS
    
    def set_output_at_index(self, index, output):
        if index > len(self.output):
            return DYNRM_MCA_ERR_BAD_PARAM
        self.output[index] = output
        return DYNRM_MCA_SUCCESS


    def append_input(self, vertex):
        self.input.append(vertex)
        return DYNRM_MCA_SUCCESS
    
    def append_output(self, vertex):
        self.output.append(vertex)
        return DYNRM_MCA_SUCCESS


    def get_input(self):
        return self.input
    def get_input_size(self):
        return len(self.get_input())
    def get_output(self):
        return self.output
    def get_output_size(self):
        return len(self.get_output())
    def get_input_at_index(self, index):
        if index > len(self.input):
            return DYNRM_MCA_ERR_BAD_PARAM
        return self.input[index]
    def get_output_at_index(self, index):
        if index > len(self.output):
            return DYNRM_MCA_ERR_BAD_PARAM
        return self.output[index]
    def get_index_in_input(self, vertex_name):
        for index in range(len(self.input)):
            if self.input[index].run_service("GET", "GID") == vertex_name:
                return index
        return -1
    def get_index_in_output(self, vertex_name):
        for index in range(len(self.output)):
            if self.output[index].run_service("GET", "GID") == vertex_name:
                return index
        return -1

    def remove_input_at_index(self, index):
        return self.input.pop(index)
    def remove_output_at_index(self, index):
        return self.output.pop(index)



    def add_monitoring_entry(self, name, data: dict):
        if name in self.monitoring_data:
            return DYNRM_MCA_ERR_EXISTS
        self.monitoring_data[name] = data
        return DYNRM_MCA_SUCCESS
    def get_monitoring_entry(self, name):
        return self.monitoring_data.get(name)
    def remove_monitoring_entry(self, name):
        if name not in self.monitoring_data:
            return DYNRM_ERR_NOT_FOUND
        self.monitoring_data.pop(name, None)
        return DYNRM_MCA_SUCCESS
    
    def set_monitoring_data(self, data: dict):
        self.monitoring_data = data
        return DYNRM_MCA_SUCCESS
    def get_monitoring_data(self):
        return self.monitoring_data
    

    def add_edge_model(self, model_name, model):
        return self.run_component_service(MCAEdgeModelComponent, "ADD", "MODEL", model_name, model)
    def get_edge_model(self, model_name):
        return self.run_component_service(MCAEdgeModelComponent, "GET", "MODEL", model_name)   
    def get_edge_model_names(self):
        return self.run_component_service(MCAEdgeModelComponent, "GET", "MODEL_NAMES")     
    def remove_edge_model(self, model_name):
        return self.run_component_service(MCAEdgeModelComponent, "REMOVE", "MODEL", model_name)
    
    @staticmethod
    def get_copy(self, edge_copy):
        edge_copy = MCAGraphObjectModule.get_copy(self, edge_copy)
        for vertex in self.input:
            edge_copy.run_service("ADD", "INPUT", vertex)
        for vertex in self.output:
            edge_copy.run_service("SET", "OUTPUT", vertex)
        names = self.get_edge_model_names()
        for name in names:
            model = self.get_edge_model(name)
        edge_copy.run_service("ADD", "MODEL", name, model)
        for key in self.monitoring_data.keys():
            edge_copy.run_service("ADD", "MONITORING_ENTRY", key, self.monitoring_data[key])
        return edge_copy
    
    