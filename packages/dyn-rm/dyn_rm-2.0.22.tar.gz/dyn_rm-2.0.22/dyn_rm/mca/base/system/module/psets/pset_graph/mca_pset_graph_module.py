from dyn_rm.mca.base.graph.module.graph import MCAGraphModule
from dyn_rm.mca.base.system.module.psets.pset import MCAPSetModule
from dyn_rm.mca.base.system.module.psets.psetop import MCAPSetopModule
from dyn_rm.mca.base.system.module.psets.pset_graph_object import MCAPsetGraphObject

from dyn_rm.util.constants import *

class MCAPSetGraphModule(MCAPSetModule, MCAGraphModule, MCAPsetGraphObject):


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__("", [], parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCAPSetGraphModule.register_base_services(self)
        self.run_service("SET", "NAME", "")

    @staticmethod
    def register_base_services(self):
        self.register_service("ADD", "PSETS", self.add_psets)
        self.register_service("REMOVE", "PSETS", self.remove_psets)
        self.register_service("ADD", "PSETOPS", self.add_psetops)
        self.register_service("REMOVE", "PSETOPS", self.remove_psetops)
        self.register_service("CREATE", "PSETOP", self.create_psetop)
        self.register_service("GET", "PSETOPS", self.get_psetops)
        self.register_service("GET", "PSETS", self.get_psets)
        self.register_service("PRINT", "PSET_GRAPH", self.print_pset_graph)

    def add_psets(self, psets):
        return self.run_service("ADD", "GRAPH_VERTICES", psets)
    
    def add_psetops(self, psetops):
        return self.run_service("ADD", "GRAPH_EDGES", psetops)
    
    def get_psetops(self):
        return self.run_service("GET", "GRAPH_EDGES_BY_FILTER", lambda x: isinstance(x, MCAPSetopModule))

    def get_psets(self):
        return self.run_service("GET", "GRAPH_EDGES_BY_FILTER", lambda x: isinstance(x, MCAPSetModule))

    def remove_psets(self, pset_gids):
        return self.run_service("REMOVE", "GRAPH_VERTICES", pset_gids)

    def remove_psetops(self, pset_gids):
        return self.run_service("REMOVE", "GRAPH_EDGES", pset_gids)
    
    def remove_task_psetops(self, psetop_gids):
        return self.run_service("REMOVE", "GRAPH_EDGES", psetop_gids)
    
    def create_psetop(self, op, input, output=[]):
        id = self.run_service("GET", "NEW_GID")
        psetop = MCAPSetopModule(id, op, input, output)
        psetop.run_service("SET", "GID", id)
        psetop.run_service("SET", "INPUT", input)
        psetop.run_service("SET", "OUTPUT", output)
        self.run_service("ADD", "PSETOPS", [psetop])

        return psetop

    def print_pset_graph(self, params = dict()):

        print()
        print("========= PSET GRAPH ========")
        for pset in self.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCAPSetModule)):
            print("PSET: "+pset.run_service("GET", "GID")+ " ("+ pset.run_service("GET", "GID")+")")
            print("==>TASK: "+str(pset.run_service("GET", "TASK").run_service("GET", "GID")))
            print("==> PROCS: "+str(pset.run_service("GET", "PROC_IDS")))

        print()
        for psetop in self.run_service("GET", "GRAPH_EDGES_BY_FILTER", lambda x: isinstance(x, MCAPSetopModule)):
            print("PSETOP: "+psetop.run_service("GET", "GID")+ " ("+ psetop.run_service("GET", "GID")+")")
            print("===> OP: "+str(psetop.run_service("GET", "PSETOP_OP")))
            print("===> STATUS: "+str(psetop.run_service("GET", "PSETOP_STATUS")))
            print("===> INPUT: "+str([pset.run_service("GET", "GID") for pset in psetop.run_service("GET", "INPUT")]))
            print("===> OUTPUT: "+str([pset.run_service("GET", "GID") for pset in psetop.run_service("GET", "OUTPUT")]))

        print("=================================")
        print()

        return DYNRM_MCA_SUCCESS