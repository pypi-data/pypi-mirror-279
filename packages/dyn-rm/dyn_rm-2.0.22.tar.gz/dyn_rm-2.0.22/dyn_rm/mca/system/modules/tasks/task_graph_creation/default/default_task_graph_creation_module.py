from dyn_rm.mca.base.system.module.tasks.task_graph_creation import MCATaskGraphCreationModule
from dyn_rm.util.constants import *

from abc import abstractmethod
import imp


class DefaultTaskGraphCreationModule(MCATaskGraphCreationModule):

    # Creates a Topology Graph and adds it to the system
    def create_task_graph_function(self, graph, object, params):
        try:
            user_module = imp.load_source("user_task_graph", object)
            graph = user_module.create_task_graph_function(graph, params)
        except Exception as e:
            raise Exception("Cannot import user module for task creation")
        return graph
            
    def update_task_graph_function(self, mix, system, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    def create_object_from_graph_function(self, graph, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    

