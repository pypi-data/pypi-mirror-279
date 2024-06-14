from dyn_rm.mca.mca import MCAClass

from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule

from dyn_rm.mca.base.graph.component.vertex_model import MCAVertexModelComponent

from dyn_rm.mca.base.system.module.psets.pset_graph_object import MCAPsetGraphObject

from dyn_rm.util.constants import *

class MCAPSetModule(MCAVertexModule, MCAPsetGraphObject, MCAClass):

    PSET_ATTRIBUTE_MEMBERSHIP = "PSET_MEMBERSHIP"
    PSET_ATTRIBUTE_JOBID = "PSET_TASK"
    PSET_ATTRIBUTE_TASK = "PSET_TASK"

    def __init__(self, pset_name, procs, model_name = None, model_module = None, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCAPSetModule.register_base_services(self)

        self.run_service("SET", "NAME", pset_name)

        if None != model_module and None != model_name:
            self.run_component_service(MCAVertexModelComponent, "ADD", "MODEL", model_name, model_module)

        proc_edge = MCAEdgeModule()
        proc_edge.run_service("SET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_MEMBERSHIP, True)
        proc_edge.run_service("SET", "INPUT", [self])
        proc_edge.run_service("SET", "OUTPUT", procs)
        self.run_service("ADD", "OUT_EDGE", proc_edge)
         
    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "TASK", self.set_task)
        self.register_service("GET", "TASK", self.get_task)
        self.register_service("ADD", "PSET_MODEL", self.add_pset_model)
        self.register_service("GET", "PSET_MODEL", self.get_pset_model)
        self.register_service("GET", "NUM_PROCS", self.get_num_procs)
        self.register_service("GET", "PROC_IDS", self.get_procids)
        self.register_service("GET", "PROCS", self.get_procs)
        self.register_service("GET", "PROC_EDGE", self.get_proc_edge)
        self.register_service("GET", "PSET_GRAPH", self.get_pset_graph)

        self.register_service("GET", "ACCESSED_CORES", self.get_accessed_cores)
        self.register_service("GET", "ACCESSED_NODES", self.get_accessed_nodes)


    def set_task(self, task):
        edge = MCAEdgeModule()
        edge.run_service("SET", "INPUT", [self])
        edge.run_service("SET", "OUTPUT", [task])
        edge.run_service("SET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_TASK, True)
        self.run_service("ADD", "OUT_EDGE", edge)
        return DYNRM_MCA_SUCCESS

    def get_task(self):
        task_edges = [edge for edge in self.run_service("GET", "OUT_EDGES") if None != edge.run_service("GET","ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_TASK)]
        if len(task_edges) != 1:
            return None
        tasks = task_edges[0].run_service("GET", "OUTPUT")
        if len(tasks) != 1:
            return None
        return tasks[0]

    def add_pset_model(self, model_name, model):
        self.run_component_service(MCAVertexModelComponent, "ADD", "MODEL", model_name, model)

    def get_pset_model(self, model_name):
        return self.run_component_service(MCAVertexModelComponent, "GET", "MODEL", model_name)
    
    def get_num_procs(self):
        proc_edge = self.get_proc_edge()
        if None == proc_edge:
            return 0
        return len(proc_edge.run_service("GET", "OUTPUT"))

    def get_procids(self):
        proc_edge = self.get_proc_edge()
        if None == proc_edge:
            return []
        return [proc.run_service("GET", "GID") for proc in proc_edge.run_service("GET", "OUTPUT")]


    def get_procs(self):
        proc_edge = self.get_proc_edge()
        return proc_edge.run_service("GET", "OUTPUT") if None != proc_edge else []
        
    
    def get_proc_edge(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_MEMBERSHIP):
                return True
            return False
        mem_edges = self.run_service("GET", "EDGES_BY_FILTER", filter)
        if len(mem_edges) != 1:
            return None
        return mem_edges[0]

    def get_pset_graph(self):
        graphs = self.run_service("GET", "GRAPHS")
        for graph in graphs:
            if isinstance(graph, MCAPSetModule):
                return graph
        return None
    
    def get_accessed_cores(self):
        procs = self.get_procs()
        coreset = dict()
        corelist = list()
        for proc in procs:
            if isinstance(proc, dict):
                cores = proc["cores"]
            else:
                cores = proc.run_service("GET", "CORE_ACCESS")
            for core in cores:
                if core.run_service("GET", "GID") not in coreset:
                    coreset[core.run_service("GET", "GID")] = core
                    corelist.append(core)

        return corelist
    
    def get_accessed_nodes(self):
        nodeset = dict() 
        nodelist = list()
        for core in self.get_accessed_cores():
            node = core.run_service("GET", "NODE")
            if node.run_service("GET", "GID") not in nodeset:
                nodeset[node.run_service("GET", "GID")] = node
                nodelist.append(node)        
        return nodelist
