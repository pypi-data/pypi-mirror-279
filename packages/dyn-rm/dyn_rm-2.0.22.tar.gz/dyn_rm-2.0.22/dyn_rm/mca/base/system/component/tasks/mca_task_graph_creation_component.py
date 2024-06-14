from dyn_rm.mca.mca import MCAComponent
from dyn_rm.mca.mca import MCAClass


class MCATaskGraphCreationComponent(MCAComponent, MCAClass):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCATaskGraphCreationComponent.register_base_services(self)

    @staticmethod    
    def register_base_services(self):
        self.register_service("SET", "PARAMETERS", self.set_parameters)
        self.register_service("UNSET", "PARAMETERS", self.unset_parameters)
        self.register_service("CREATE", "TASK_GRAPH", self.create_task_graph)
        self.register_service("UPDATE", "TASK_GRAPH", self.update_task_graph)  
        self.register_service("CREATE", "OBJECT_FROM_GRAPH", self.create_object_from_graph)

    def set_parameters(self, module, params: dict):
        return self.run_module_service(module, "SET", "PARAMETERS", params)
    def get_parameters(self, module, params: dict):
        return self.run_module_service(module, "SET", "PARAMETERS", params)
    def unset_parameters(self, module, keys: list):
        return self.run_module_service(module, "UNSET", "PARAMETERS", keys)
    def create_task_graph(self, module, graph, object, params):
        return self.run_module_service(module, "CREATE", "TASK_GRAPH", graph, object, params)
    def update_task_graph(self, module, graph, object, params):
        return self.run_module_service(module, "UPDATE", "TASK_GRAPH", graph, object, params)
    def create_object_from_graph(self, module, graph, params):
        return self.run_module_service(module, "CREATE", "OBJECT_FROM_GRAPH", graph, params)
    
    