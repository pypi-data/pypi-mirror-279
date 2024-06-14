from dyn_rm.mca.base.graph.module.graph import MCAGraphModule
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.system.module.tasks.task_dependency import MCATaskDependencyModule
from dyn_rm.mca.base.system.module.tasks.task import MCATaskModule

from dyn_rm.util.constants import *

class MCATaskGraphModule(MCATaskModule, MCAGraphModule):

    TASK_GRAPH_ATTRIBUTE_STATUS = "TASK_GRAPH_STATUS"

    TASK_GRAPH_STATUS_NEW = 0
    TASK_GRAPH_STATUS_SUBMITTED = 1
    TASK_GRAPH_STATUS_RUNNING = 2
    TASK_GRAPH_STATUS_TERMINATED = 3


    def __init__(self, task_graph_name, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(task_graph_name, None, parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCATaskGraphModule.register_base_services(self)
        self.run_service("SET", "NAME", task_graph_name)
        self.run_service("SET", "TASK_GRAPH_STATUS", MCATaskGraphModule.TASK_GRAPH_STATUS_NEW)
        self.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_NEW)

    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "TASK_GRAPH_STATUS", self.set_task_graph_status)
        self.register_service("ADD", "TASKS", self.add_tasks)
        self.register_service("GET", "TASKS", self.get_tasks)
        self.register_service("GET", "TASK_BY_NAME", self.get_task_by_name)
        self.register_service("REMOVE", "TASKS", self.remove_tasks)
        self.register_service("MAKE", "TASK_DEPENDENCY", self.make_task_dependency)
        self.register_service("ADD", "TASK_DEPENDENCIES", self.add_task_dependency)
        self.register_service("REMOVE", "TASK_DEPENDENCIES", self.remove_task_dependency)
        self.register_service("PRINT", "TASK_GRAPH", self.print_task_graph)

    def set_task_graph_status(self, status):
        return self.run_service("SET", "ATTRIBUTE", MCATaskGraphModule.TASK_GRAPH_ATTRIBUTE_STATUS, status)

    def get_task_graph_status(self):
        return self.run_service("GET", "ATTRIBUTE",  MCATaskGraphModule.TASK_GRAPH_ATTRIBUTE_STATUS)

    def get_task_by_name(self, name):
        tasks = self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCATaskModule) and x.run_service("GET", "NAME") == name)
        if len(tasks) != 1:
            return None
        return tasks[0]
    def get_tasks(self):
        return self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCATaskModule))


    def add_tasks(self, tasks):
        rc = self.run_service("ADD", "GRAPH_VERTICES", tasks)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        for task in tasks:
            dep = self.make_task_dependency(task, self)
            dep.run_service("SET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION, True)
        return DYNRM_MCA_SUCCESS

    def remove_tasks(self, task_names):
        tasks = [self.get_task_by_name(task_name) for task_name in task_names]
        for task in tasks:
            self.remove_task_dependencies(task.run_service("GET", "TASK_DEPENDENCIES"))
        return self.run_service("REMOVE", "GRAPH_VERTICES", task_names)

    def add_task_dependencies(self, task_deps):
        for dep in task_deps:
            in_task = dep.run_service("GET", "INPUT")[0]
            in_task.run_service("ADD", "TASK_DEPENDENCY", dep)
            out_task = dep.run_service("GET", "OUTPUT")[0]
            out_task.run_service("ADD", "TASK_DEPENDENCY", dep)
        return self.run_service("ADD", "GRAPH_EDGES", task_deps)
    
    def remove_task_dependencies(self, task_deps):
        for dep in task_deps:
            in_task = dep.run_service("GET", "INPUT")[0]
            in_task.run_service("REMOVE", "TASK_DEPENDENCY", dep)
            out_task = dep.run_service("GET", "OUTPUT")[0]
            out_task.run_service("ADD", "TASK_DEPENDENCY", dep)
        return self.run_service("REMOVE", "GRAPH_EDGES", task_deps)
    
    def make_task_dependency(self, in_task, out_task):
        gid = self.run_service("GET", "NEW_GID")
        dep = MCATaskDependencyModule(gid, in_task, out_task)
        dep.run_service("SET", "GID", gid)
        self.add_task_dependencies([dep])
        return dep
    
    def unmake_task_dependency(self, in_task, out_task):
        deps = in_task.run_service("GET", "TASK_DEPENDENCIES")
        deps = [dep for dep in deps if out_task in dep.run_service("GET", "OUTPUT")]

        self.remove_task_dependencies(deps)
        return deps


    def print_task_graph(self, params = dict()):

        print()
        print("========= TASK GRAPH ========")
        for task in self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCATaskModule)):
            print("TASK: "+task.run_service("GET", "GID")+" ("+task.run_service("GET", "NAME")+")")
            print("====> STATUS: "+str(task.run_service("GET", "TASK_STATUS")))
            in_deps = [dep for dep in task.run_service("GET", "TASK_DEPENDENCIES") if task in dep.run_service("GET", "OUTPUT")]
            print("====> PREDECESSORS: "+str([dep.run_service("GET", "INPUT")[0].run_service("GET", "NAME") for dep in in_deps]))

            out_deps = [dep for dep in task.run_service("GET", "TASK_DEPENDENCIES") if task in dep.run_service("GET", "INPUT")]
            print("====> SUCCESSORS: "+str([dep.run_service("GET", "OUTPUT")[0].run_service("GET", "NAME") for dep in out_deps]))

        print("=================================")
        print()
