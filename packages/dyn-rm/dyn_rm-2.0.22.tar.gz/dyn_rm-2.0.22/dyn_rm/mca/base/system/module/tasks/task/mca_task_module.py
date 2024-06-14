from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.system.module.tasks.task_dependency import MCATaskDependencyModule
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.system.module.tasks.task_graph_object import MCATaskGraphObject
from dyn_rm.mca.base.system.module.psets.pset import MCAPSetModule

from dyn_rm.util.constants import *

class MCATaskModule(MCAVertexModule, MCATaskGraphObject):

    TASK_ATTRIBUTE_STATUS = "TASK_STATUS"
    TASK_ATTRIBUTE_EXECUTABLE = "TASK_EXECUTABLE"
    TASK_ATTRIBUTE_EXECUTION_ARGUMENTS = "TASK_ARGUMENTS"
    TASK_ATTRIBUTE_LAUNCH_OUTPUT_SPACE_GENERATOR = "LAUNCH_OUTPUT_SPACE_GENERATOR"
    TASK_ATTRIBUTE_REQ_NODES = "TASK_REQ_NODES"

    TASK_STATUS_NEW = 0
    TASK_STATUS_WAITING = 1
    TASK_STATUS_READY = 2
    TASK_STATUS_STARTING = 3
    TASK_STATUS_RUNNING = 4
    TASK_STATUS_TERMINATING = 5
    TASK_STATUS_TERMINATED = 6

    TASK_PSET_EDGE_ATTRIBUTE = "TASK_PSET_EDGE"

    def __init__(self, task_id, executable, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCATaskModule.register_base_services(self)
        self.run_service("SET", "NAME", task_id)
        self.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_NEW)
        self.run_service("SET", "TASK_EXECUTABLE", executable)
        

    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "TASK_STATUS", self.set_task_status)
        self.register_service("SET", "TASK_EXECUTABLE", self.set_task_executable)
        self.register_service("SET", "TASK_EXECUTION_ARGUMENTS", self.set_task_execution_arguments)
        self.register_service("SET", "TASK_LAUNCH_OUTPUT_SPACE_GENERATOR", self.set_task_launch_output_space_generator)
        self.register_service("GET", "TASK_LAUNCH_OUTPUT_SPACE_GENERATOR", self.get_task_launch_output_space_generator)

        self.register_service("ADD", "TASK_DICT_ENTRY", self.add_task_dict_entry)
        self.register_service("ADD", "TASK_DEPENDENCY", self.add_task_dependency)
        self.register_service("ADD", "TASK_DEPENDENCIES", self.add_task_dependency)

        self.register_service("GET", "TASK_STATUS", self.get_task_status)
        self.register_service("GET", "TASK_GRAPH", self.get_task_graph)
        self.register_service("GET", "TASK_EXECUTABLE", self.get_task_executable)
        self.register_service("GET", "TASK_EXECUTION_ARGUMENTS", self.get_task_execution_arguments)
        self.register_service("GET", "TASK_DEPENDENCY", self.get_task_dependency)
        self.register_service("GET", "TASK_DEPENDENCIES", self.get_task_dependencies)
        self.register_service("GET", "PSETS", self.get_psets)
        self.register_service("GET", "PROCS", self.get_procs)

        self.register_service("GET", "PREDECESSOR_TASKS", self.get_predecessor_tasks)
        self.register_service("GET", "SUCCESOR_TASKS", self.get_successor_tasks)

        self.register_service("REMOVE", "TASK_DEPENDENCY", self.remove_task_dependency)
        self.register_service("REMOVE", "TASK_DICT_ENTRY", self.remove_task_dict_entry)

    def set_task_status(self, status):
        return self.run_service("SET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_STATUS, status)
    def set_task_executable(self, ex):
        return self.run_service("SET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_EXECUTABLE, ex)
    def set_task_execution_arguments(self, args):
        return self.run_service("SET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_EXECUTION_ARGUMENTS, args)
        
    def set_task_launch_output_space_generator(self, generator):
        return self.run_service("SET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_LAUNCH_OUTPUT_SPACE_GENERATOR, generator)

    def get_task_status(self):
        return self.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_STATUS)

    def get_task_executable(self):
        return self.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_EXECUTABLE)
    
    def get_task_execution_arguments(self):
        return self.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_EXECUTION_ARGUMENTS)

    def get_task_launch_output_space_generator(self):
        return self.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_LAUNCH_OUTPUT_SPACE_GENERATOR)

    def get_task_graph(self):
        for edge in self.run_service("GET", "OUT_EDGES"):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION):
                return edge.run_service("GET", "OUTPUT")[0]
        return None

    def get_psets(self):
        edges = [edge for edge in self.run_service("GET", "IN_EDGES") if None != edge.run_service("GET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_TASK)]
        psets = set()
        for edge in edges:
            input = edge.run_service("GET", "INPUT")
            if len(input) == 1:
                psets.add(input[0])
        return list(psets)
    
    def get_procs(self):
        psets = self.get_psets()
        procs = set()
        for pset in psets:
            pset_procs = pset.run_service("GET", "PROCS")
            for proc in pset_procs:
                procs.add(proc)
        return list(procs)

    def add_task_dict_entry(self, key, val):
        return self.run_service("SET", "ATTRIBUTE", key, val)
    
    def remove_task_dict_entry(self, key):
        return self.run_service("UNSET", "ATTRIBUTE", key)

    def add_task_dependency(self, dep):
        input = dep.run_service("GET", "INPUT")
        if self.run_service("GET", "NAME") in [t.run_service("GET", "NAME") for t in input]:
            self.run_service("ADD", "OUT_EDGE", dep)
            return DYNRM_MCA_SUCCESS
        
        output = dep.run_service("GET", "OUTPUT")
        if self.run_service("GET", "NAME") in [t.run_service("GET", "NAME") for t in output]:
            self.run_service("ADD", "IN_EDGE", dep)
            return DYNRM_MCA_SUCCESS
        
        return DYNRM_MCA_ERR_BAD_PARAM

    def add_task_dependencies(self, deps):
        for dep in deps:
            rc = self.add_task_dependency(dep)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    def get_task_dependency(self, name):
        def filter(edge):
            if (    None != edge.run_service("GET", "ATTRIBUTE", MCATaskDependencyModule.TASK_DEPENDENCY_EDGE_ATTRIBUTE) and 
                    name == edge.run_service("GET", "TASK_DEPENDENCY_NAME")):
                return True
            return False
        deps = self.run_service("GET", "EDGES_BY_FILTER", filter)
        if len(deps) != 1:
            return None
        return deps[0]

    def get_task_dependencies(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCATaskDependencyModule.TASK_DEPENDENCY_EDGE_ATTRIBUTE):
                return True
            return False
        return self.run_service("GET", "EDGES_BY_FILTER", filter)
    
    def get_predecessor_tasks(self):
        predecessor_tasks = []
        dependencies = self.get_task_dependencies()
        for dep in dependencies:
            if self in dep.run_service("GET", "OUTPUT"):
                predecessor_tasks.append(dep.run_service("GET", "INPUT")[0])
        return predecessor_tasks

    def get_successor_tasks(self):
        successor_tasks = []
        dependencies = self.get_task_dependencies()
        for dep in dependencies:
            if self in dep.run_service("GET", "INPUT"):
                successor_tasks.append(dep.run_service("GET", "OUTPUT")[0])
        return successor_tasks
    
    def remove_task_dependency(self, dep):
        return self.run_service("REMOVE", "EDGE", dep.run_service("GET", "GID"))

