from dyn_rm.mca.mca import MCAModule

from dyn_rm.util.functions import v_print
from dyn_rm.util.constants import *
from abc import abstractmethod

class MCACallbackModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.connections = dict()
        self._default_callbacks = dict()
        MCACallbackModule.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("GET", "PEER", self.get_peer)
        self.register_service("ADD", "CONNECTION_PARAMS", self.add_connection_params)
        self.register_service("REQUEST", "CONNECTION", self.request_connection)
        self.register_service("ACCEPT", "CONNECTION", self.accept_connection)
        self.register_service("ACCEPT", "CONNECTION_TERMINATION", self.accept_connection_termination)
        self.register_service("REGISTER", "CALLBACK", self.register_callback)
        self.register_service("REGISTER", "CONNECTION_CALLBACK", self.register_connection_callback)
        self.register_service("EXECUTE", "CALLBACK", self.execute_callback)
        self.register_service("SEND", "EVENT", self.send_event)
        self.register_service("BCAST", "EVENT", self.bcast_event)    
        self.register_service("TERMINATE", "CONNECTION", self.terminate_connection)

    def get_peer(self, conn_name):
        if not conn_name in self.connections.keys():
            return None
        return self.connections[conn_name]["PEER"]
    def add_connection_params(self, conn_name, params):
        if not conn_name in self.connections.keys():
            return DYNRM_MCA_ERR_NOT_FOUND
        self.connections[conn_name]["PARAMS"].update(params)

    # try to establish a connection with the peer's connection module
    def request_connection(self, conn_name, mypeer, peer, params):
        if conn_name in self.connections.keys():
            return DYNRM_MCA_ERR_NOT_FOUND

        rc = self.request_connection_function(conn_name, mypeer, peer, params)
        if rc != DYNRM_MCA_SUCCESS:
            v_print(self.mca_get_name()+": Cannot connect! Peer refused connection: "+str(rc), 1, self.verbosity)
            return rc
        
        # Add our default callbacks to this connection
        for event in self._default_callbacks.keys():
            rc = self.add_callback(conn_name, event, self._default_callbacks[event])
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS
    
    def terminate_connection(self, conn_name):
        if conn_name in self.connections.keys():
            return DYNRM_MCA_SUCCESS
        
        rc = self.terminate_connection_function(conn_name)
        if rc != DYNRM_MCA_SUCCESS:
            v_print("DEFAULT_CALLBACK_MODULE: Error in connection termination: "+str(rc), 1, self.verbosity)
            return rc

        return self.remove_connection(conn_name)        

    
    def accept_connection(self, conn_name, peer, params):
        if conn_name in self.connections.keys():
            return DYNRM_MCA_ERR_EXISTS

        rc =  self.accept_connection_function(conn_name, peer, params)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        # Add our default callbacks to this connection
        for event in self._default_callbacks.keys():
            rc = self.add_callback(conn_name, event, self._default_callbacks[event])
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    def accept_connection_termination(self, conn_name):
        if conn_name not in self.connections.keys():
            return DYNRM_MCA_ERR_EXISTS
        return self.accept_connection_termination_function(conn_name)


    def register_callback(self, event_name, callback):
        
        self._default_callbacks[event_name] = callback
        for conn_name in self.connections.keys():
            rc = self.register_callback_function(conn_name, event_name, callback)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS
    
    def register_connection_callback(self, conn_name, event_name, callback):
        return self.register_callback_function(conn_name, event_name, callback)
    
    def send_event(self, conn_name, event_name, *args, **kwargs):
        return self.send_event_function(conn_name, event_name, *args, **kwargs)
    
    def bcast_event(self, event_name,  *args, **kwargs):
        for conn_name in self.connections.keys():
            #if event_name in self.connections[conn_name]["CALLBACKS"].keys():
            rc = self.send_event(conn_name, event_name,  *args, **kwargs)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    # utils for modules
    def add_connection(self, conn_name, peer, params):
        self.connections[conn_name] = dict()
        self.connections[conn_name]["PEER"] = peer
        self.connections[conn_name]["PARAMS"] = dict()
        if None != params:
            self.connections[conn_name]["PARAMS"].update(params)
        self.connections[conn_name]["CALLBACKS"] = dict()
    
    def remove_connection(self, conn_name):
        self.connections.pop(conn_name)
        return DYNRM_MCA_SUCCESS

    def add_callback(self, conn_name, event_name, callback):
        self.connections[conn_name]["CALLBACKS"][event_name] = callback
        return DYNRM_MCA_SUCCESS

    def execute_callback(self, conn_name, event_name, *args, **kwargs):
        callback = self.connections[conn_name]["CALLBACKS"].get(event_name)
        if None == callback:
            return DYNRM_SUCCESS
        return callback(conn_name, event_name, *args, **kwargs)

    def run_peer_component_service(self, peer, service_class, service_name, *args, **kwargs):
        peer_comp = peer.get_component(self.get_parent().__class__)
        if peer_comp == None:
            vprint("run_peer_module_service: Peer has no Callback Component")
            return DYNRM_MCA_ERR_BAD_PARAM
        return peer_comp.run_service(service_class, service_name, *args, **kwargs)

    def run_peer_module_service(self, peer, service_class, service_name, *args, **kwargs):
        peer_comp = peer.get_component(self.get_parent().__class__)
        if peer_comp == None:
            vprint("run_peer_module_service: Peer has no Callback Component")
            return DYNRM_MCA_ERR_BAD_PARAM
        peer_module = peer_comp.get_module(self.__class__)
        if peer_module == None:
            vprint("run_peer_module_service: Peer has no "+self.mca_get_name())
            return DYNRM_MCA_ERR_BAD_PARAM
        return peer_module.run_service(service_class, service_name, *args, **kwargs)

    @abstractmethod
    def request_connection_function(self, conn_name, mypeer, peer, params):
        
        # Cross check compatibility
        peer_comp = peer.get_component(self.get_parent().__class__)
        if  peer_comp == None:
            v_print(self.mca_get_name()+": Cannot connect! (Peer has no "+self.get_paren().__class__.mca_get_name()+")", 1, self.verbosity)
            return DYNRM_MCA_ERR_BAD_PARAM
        peer_module = peer_comp.get_module(self.__class__)
        if peer_module == None:
            v_print(self.mca_get_name()+": Cannot connect! (Peer has no "+self.mca_get_name()+")", 1, self.verbosity)
            return DYNRM_MCA_ERR_BAD_PARAM

        
        rc = self.run_peer_component_service(peer, "ACCEPT", "CONNECTION", self.__class__, conn_name, mypeer, params)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        self.add_connection(conn_name, peer, params)
        return DYNRM_MCA_SUCCESS
    
    @abstractmethod
    def accept_connection_function(self, conn_name, peer, params):
        # Cross check compatibility
        peer_comp = peer.get_component(self.get_parent().__class__)
        if  peer_comp == None:
            v_print(self.mca_get_name()+": Cannot connect! (Peer has no "+self.get_paren().__class__.mca_get_name()+")", 1, self.verbosity)
            return DYNRM_MCA_ERR_BAD_PARAM
        peer_module = peer_comp.get_module(self.__class__)
        if peer_module == None:
            v_print(self.mca_get_name()+": Cannot connect! (Peer has no "+self.mca_get_name()+")", 1, self.verbosity)
            return DYNRM_MCA_ERR_BAD_PARAM
        
        self.add_connection(conn_name, peer, params)
        return DYNRM_MCA_SUCCESS
    
    @abstractmethod
    def accept_connection_termination_function(self, conn_name):
        return self.remove_connection(conn_name)
    
    @abstractmethod
    def register_callback_function(self, conn_name, event_name, callback):
        return self.add_callback(conn_name, event_name, callback)

    @abstractmethod
    def send_event_function(self, conn_name, event_name, *args, **kwargs):
        peer = self.get_peer(conn_name)
        return self.run_peer_module_service(peer, "EXECUTE", "CALLBACK", conn_name, event_name, *args, **kwargs)
    
    @abstractmethod
    def terminate_connection_function(self, conn_name):
        peer = self.get_peer(conn_name)
        return self.run_peer_component_service(peer, "ACCEPT", "CONNECTION_TERMINATION", conn_name)


