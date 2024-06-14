from dyn_rm.mca.mca import MCAModule
from dyn_rm.util.constants import *

from abc import abstractmethod

import time

class MCAGraphObjectModule(MCAModule):

    STATUS_NONE = 0
    STATUS_NEW = 1
    STATUS_ADD = 2
    STATUS_VALID = 3
    STATUS_UPDATE = 4
    STATUS_DELETE = 5
    STATUS_INVALID = 6

    ATTRIBUTE_NAME = 0
    ATTRIBUTE_CONTAINMENT_RELATION = 1
    ATTRIBUTE_DEPENDENCY_RELATION = 2
    ATTRIBUTE_SETOP_RELATION = 3
    ATTRIBUTE_ACCESS_RELATION = 4
    ATTRIBUTE_OBJ_TIMESTAMP = "OBJ_TIMESTAMP"

    GRAPH_OBJECT_DEFAULT_GID = "MCAGraphObject:/"


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._gid = MCAGraphObjectModule.GRAPH_OBJECT_DEFAULT_GID
        self._status = MCAGraphObjectModule.STATUS_NEW
        self._graphs = dict()
        self._attributes = dict()
        self._obj_counter = 0
        MCAGraphObjectModule.register_base_services_(self)
        self.run_service("SET", "NAME", "MCAGraphObject:/")
        self.run_service("SET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_OBJ_TIMESTAMP, time.time())

        
    @staticmethod
    def register_base_services_(self):
        self.register_service("SET", "GID", self.set_gid)
        self.register_service("SET", "NAME", self.set_name)
        self.register_service("SET", "STATUS", self.set_status)
        self.register_service("SET", "ATTRIBUTE", self.set_attribute)
        self.register_service("UNSET", "ATTRIBUTE", self.unset_attribute)

        self.register_service("GET", "GID", self.get_gid)
        self.register_service("GET", "NAME", self.get_name)
        self.register_service("GET", "STATUS", self.get_status)
        self.register_service("GET", "ATTRIBUTE", self.get_attribute)
        self.register_service("GET", "ATTRIBUTES", self.get_attributes)
        self.register_service("GET", "GRAPHS", self.get_graphs)

        self.register_service("EXTEND", "ATTRIBUTE_LIST", self.extend_attribute_list)
        self.register_service("SHRINK", "ATTRIBUTE_LIST", self.shrink_attribute_list)

        # graphs
        self.register_service("ADD", "GRAPH", self.add_graph)
        self.register_service("GET", "GRAPHS", self.get_graphs)
        self.register_service("REMOVE", "GRAPH", self.remove_graph)
    
        self.register_service("GET", "NEW_GID", self._get_new_object_id)

        self.register_service("GET", "COPY", self.get_copy_runner)


    def set_gid(self, gid):
        self._gid = gid
        return DYNRM_MCA_SUCCESS
    def set_name(self, name):
        return self.run_service("SET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_NAME, name)
    def set_status(self, status):
        self._status = status
        return DYNRM_MCA_SUCCESS
    def set_attribute(self, key, val):
        self._attributes[key] = val
        return DYNRM_MCA_SUCCESS
    
    def unset_attribute(self, key):
        return self._attributes.pop(key)


    def get_gid(self):
        return self._gid
    def get_name(self):
        return self.run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_NAME)
    def get_status(self):
        return self._status
    def get_attribute(self, key):
        return self._attributes.get(key)
    def get_attributes(self):
        return self._attributes
    
    def extend_attribute_list(self, key, values: list):
        attr = self.get_attribute(key)
        if None == attr or not isinstance(attr, list):
            return DYNRM_ERR_BAD_PARAM
        new_attr = attr + values
        self.set_attribute(key, new_attr)

        return DYNRM_MCA_SUCCESS

    def shrink_attribute_list(self, key, values: list):
        attr = self.get_attribute(key)
        if None == attr or not isinstance(attr, list):
            return DYNRM_ERR_BAD_PARAM
        new_attr = [a for a in attr if a not in values]
        self.set_attribute(key, new_attr)

        return DYNRM_MCA_SUCCESS


    # Graphs
    def add_graph(self, graph):
        self._graphs[graph.run_service("GET", "GID")] = graph
        return DYNRM_MCA_SUCCESS
    def get_graphs(self):
        return list(self._graphs.values())
    def remove_graph(self, name):
        self._graphs.pop(name, None)
        return self._graphs.pop(name, None)  


    def _get_new_object_id(self):
        id = self.run_service("GET", "GID") +"/"+str(self._obj_counter)
        self._obj_counter +=1
        return id

    #copy
    def get_copy_runner(self, graph_object):
        return self.__class__.get_copy(self, graph_object)

    @staticmethod
    def get_copy(self, graph_object):
        graph_object.run_service("SET", "GID", self.run_service("GET", "GID"))
        graph_object.run_service("SET", "STATUS", self.run_service("GET", "STATUS"))

        graphs = self.run_service("GET", "GRAPHS")
        for graph in graphs:
            graph_object.run_service("ADD", "GRAPH", graph)
        attributes = self.run_service("GET", "ATTRIBUTES")
        for key in attributes:
            graph_object.run_service("SET", "ATTRIBUTE", key, attributes[key])
        
        graph_object.run_service("SET", "STATUS", self.run_service("GET", "STATUS"))
        return graph_object