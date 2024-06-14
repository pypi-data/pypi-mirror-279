from dyn_rm.mca.mca import MCAComponent

from dyn_rm.util.constants import *

class MCAGraphComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._graphs = dict()
        MCAGraphComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("ADD", "GRAPH", self.add_graph)
        self.register_service("GET", "GRAPH", self.get_graph)
        self.register_service("GET", "GRAPHS", self.get_graphs)
        self.register_service("REMOVE", "GRAPH", self.remove_graph)



    def add_graph(self, name, graph_module):
        self._graphs[name] = graph_module
        return DYNRM_MCA_SUCCESS
    
    def get_graph(self, name):
        return self._graphs.get(name)
    def get_graphs(self):
        return list(self._graphs.values())
    
    def remove_graph(self, name):
        self._graphs.pop(name, None)
        return DYNRM_MCA_SUCCESS
 