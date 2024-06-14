from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule
from dyn_rm.util.constants import *
from dyn_rm.mca.base.system.module.tasks.task_graph_object import MCATaskGraphObject

class MCATaskDependencyModule(MCAEdgeModule, MCATaskGraphObject):

    TASK_DEPENDENCY_EDGE_ATTRIBUTE = "TASK_DEPENDENCY_EDGE"
    TASK_DEPENDENCY_NAME_ATTRIBUTE = "TASK_DEPENDENCY_NAME"

    def __init__(self, dependency_name, in_task, out_task, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCATaskDependencyModule.register_base_services(self)
        self.run_service("SET", "ATTRIBUTE", MCATaskDependencyModule.TASK_DEPENDENCY_EDGE_ATTRIBUTE, True)
        self.run_service("SET", "INPUT", [in_task])
        self.run_service("SET", "OUTPUT", [out_task])
        self.run_service("SET", "NAME", dependency_name)



    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "TASK_DEPENDENCY_NAME", self.set_task_dependency_name)
        self.register_service("GET", "TASK_DEPENDENCY_NAME", self.get_task_dependency_name)
        
    def set_task_dependency_name(self, name):
        return self.run_service("SET", "ATTRIBUTE", MCATaskDependencyModule.TASK_DEPENDENCY_NAME_ATTRIBUTE, name)

    def get_task_dependency_name(self):
        return self.run_service("GET", "ATTRIBUTE", MCATaskDependencyModule.TASK_DEPENDENCY_NAME_ATTRIBUTE)
