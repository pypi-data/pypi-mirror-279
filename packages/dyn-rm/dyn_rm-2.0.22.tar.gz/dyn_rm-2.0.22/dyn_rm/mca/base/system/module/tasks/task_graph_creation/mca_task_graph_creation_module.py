from dyn_rm.mca.mca import MCAModule
from dyn_rm.util.constants import *
from abc import abstractmethod

class MCATaskGraphCreationModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.params = dict()
        self.event_loops = dict()
        self.systems = dict()
        MCATaskGraphCreationModule.register_base_services(self)

    @staticmethod    
    def register_base_services(self):
        self.register_service("SET", "PARAMETERS", self.set_parameters)
        self.register_service("GET", "PARAMETERS", self.set_parameters)
        self.register_service("UNSET", "PARAMETERS", self.unset_parameters)
        self.register_service("CREATE", "TASK_GRAPH", self.create_task_graph)
        self.register_service("UPDATE", "TASK_GRAPH", self.update_task_graph)
        self.register_service("CREATE", "OBJECT_FROM_GRAPH", self.create_object_from_graph)  

    def set_parameters(self, params: dict):
        self.params.update(params)
        return DYNRM_MCA_SUCCESS
    
    def get_parameters(self, params: dict):
        return self.params
    
    def unset_parameters(self, keys: list):
        for key in keys:
            self.params.pop(key)
        return DYNRM_MCA_SUCCESS
    
    

    def create_task_graph(self, object, system, params):
        return self.create_task_graph_function(object, system, params)
    
    def update_task_graph(self, object, system, params):
        return self.update_task_graph_function( object, system, params)


    # Abstract Functions
    @abstractmethod
    def create_task_graph_function(self, graph, object, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    @abstractmethod
    def update_task_graph_function(self, graph, object, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    @abstractmethod
    def create_object_from_graph(self, graph, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED

