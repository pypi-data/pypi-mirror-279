from dyn_rm.mca.mca import MCAClass
from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.system.module.topology.topology_graph_object import MCATopologyGraphObject
from dyn_rm.mca.base.system.module.psets.proc import MCAProcModule

from dyn_rm.util.constants import *

class MCACoreModule(MCAVertexModule, MCAClass, MCATopologyGraphObject):

    NODE_ATTRIBUTE_STATUS = "NODE_STATUS"
    NODE_CORE_MEMBERSHIP_ATTRIBUTE = "NODE_CORE_MEMBERSHIP"

    def __init__(self, coreid, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.run_service("SET", "NAME", coreid)
        MCACoreModule.register_base_services(self)

    @staticmethod
    def register_base_services(self):
        self.register_service("GET", "NODE", self.get_node)
        self.register_service("GET", "ACCESSING_PROCS", self.get_accessing_procs)
        self.register_service("GET", "ACCESSING_JOB_IDS", self.get_accessing_job_ids)
        self.register_service("CHECK", "FREE", self.check_free)
        self.register_service("CHECK", "UTILIZED", self.check_utilized)

    def get_node(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_CONTAINMENT_RELATION):
                return True
            return False
        mem_edges = self.run_service("GET", "EDGES_BY_FILTER", filter)
        if len(mem_edges) == 1:
            return mem_edges[0].run_service("GET", "INPUT")[0]
        return []        


    def get_accessing_procs(self):
        def filter(edge):
            if None != edge.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_ACCESS_RELATION):
                return True
            return False
        edges = self.run_service("GET", "EDGES_BY_FILTER", filter)
        procs = dict()
        for input in [edge.run_service("GET", "INPUT") for edge in edges]:
            for proc in input:
                procs[proc.run_service("GET", "GID")] = proc

        return list(procs.values())
    
    def get_accessing_job_ids(self):
        procs = self.get_accessing_procs()
        return [proc.run_service("GET", "JOBID") for proc in procs]
    
    def check_free(self):
        for proc in self.run_service("GET", "ACCESSING_PROCS"):
            status = proc.run_service("GET", "PROC_STATUS")
            if status != MCAProcModule.PROC_STATUS_TERMINATED:
                return False   
        return True
    
    def check_utilized(self):
        for proc in self.run_service("GET", "ACCESSING_PROCS"):
            status = proc.run_service("GET", "PROC_STATUS")
            if status == MCAProcModule.PROC_STATUS_RUNNING:
                return True   
        return False