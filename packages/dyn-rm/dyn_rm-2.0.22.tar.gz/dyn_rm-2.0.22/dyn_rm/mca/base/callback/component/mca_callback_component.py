from dyn_rm.mca.mca import MCAComponent
from dyn_rm.mca.base.callback.module import MCACallbackModule

from dyn_rm.util.constants import *
from dyn_rm.util.functions import v_print

class MCACallbackComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.connections = dict()
        self.connection_filters = []
        self.connection_accepted_callbacks = []
        self.connection_terminated_callbacks = []

        self.connection_counter = 0
        MCACallbackComponent.register_base_services(self)
        # By default register the Dedault Module
        self.register_module(MCACallbackModule())
        
    def register_base_services(self):
        self.register_service("GENERATE", "CONNECTION_NAME", self.generate_connection_name)
        self.register_service("GET", "PEER", self.get_peer)
        self.register_service("ADD", "CONNECTION_PARAMS", self.add_connection_params)
        self.register_service("ADD", "CONNECTION_FILTER", self.add_connection_filter)
        self.register_service("ADD", "CONNECTION_ACCEPTED_CALLBACK", self.add_connection_accepted_callback)
        self.register_service("ADD", "CONNECTION_TERMINATED_CALLBACK", self.add_connection_terminated_callback)
        self.register_service("REQUEST", "CONNECTION", self.request_connection)
        self.register_service("ACCEPT", "CONNECTION", self.accept_connection)
        self.register_service("REGISTER", "CALLBACK", self.register_callback)
        self.register_service("REGISTER", "CONNECTION_CALLBACK", self.register_connection_callback)
        self.register_service("SEND", "EVENT", self.send_event)
        self.register_service("BCAST", "EVENT", self.bcast_event)
        self.register_service("TERMINATE", "CONNECTION", self.terminate_connection)
        self.register_service("ACCEPT", "CONNECTION_TERMINATION", self.accept_connection_termination)

    def generate_connection_name(self, peer):
        peer_comp = peer.get_component(MCACallbackComponent)
        if None == peer_comp:
            return None

        return str(self.get_next_id())+"-"+peer_comp.get_next_id()

    def get_peer(self, conn_name):
        module = self._get_module_for_connection(conn_name)
        if None == module:
            return None
        return self.run_module_service(module, "GET", "PEER", conn_name)
    
    def add_connection_params(self, conn_name, params):
        module = self._get_module_for_connection(conn_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service("ADD", "CONNECTION_PARAMS", conn_name, params)
    

    def add_connection_filter(self, filter):
        self.connection_filters.append(filter)

    def add_connection_accepted_callback(self, callback):
        self.connection_accepted_callbacks.append(callback)

    def add_connection_terminated_callback(self, callback):
        self.connection_terminated_callbacks.append(callback)
    
    def request_connection(self, module, conn_name, mypeer, peer, params):
        if conn_name in self.connections:
            return DYNRM_MCA_ERR_EXISTS
        rc = self.run_module_service(module, "REQUEST", "CONNECTION", conn_name, mypeer, peer, params)
        if rc == DYNRM_MCA_SUCCESS:
            self.connections[conn_name] = module
        return rc

    def accept_connection(self, module, conn_name, peer, params):
        if conn_name in self.connections:
            return DYNRM_MCA_ERR_EXISTS
        for filter in self.connection_filters:
            rc = filter(module, conn_name, peer, params)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        rc = self.run_module_service(module, "ACCEPT", "CONNECTION", conn_name, peer, params)
        if rc == DYNRM_MCA_SUCCESS:
            self.connections[conn_name] = module
            for callback in self.connection_accepted_callbacks:
                callback(module, conn_name, peer, params)
        return rc
    
    def set_connection_accepted_callback(self, callback):
        for module in self.connections.values():
            rc = self.run_module_service(module, "SET", "CONNECTION_ACCEPTED_CALLBACK", callback)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS
            
    def set_connection_terminated_callback(self, callback):
        for module in self.connections.values():
            rc = self.run_module_service(module, "SET", "CONNECTION_TERMINATED_CALLBACK", callback)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS
    
    def register_callback(self, event_name, callback):
        for module in self.get_modules():
            rc = self.run_module_service(module, "REGISTER", "CALLBACK", event_name, callback)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS
        
        
    def register_connection_callback(self, conn_name, event_name, callback):
        module = self._get_module_for_connection(conn_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "REGISTER", "CONNECTION_CALLBACK", conn_name, event_name, callback)

    def send_event(self, conn_name, event_name, *args, **kwargs):
        module = self._get_module_for_connection(conn_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "SEND", "EVENT", conn_name, event_name, *args, **kwargs)
    
    def bcast_event(self, event_name, *args, **kwargs):
        for module in self.connections.values():
            rc = self.run_module_service(module, "BCAST", "EVENT", event_name, *args, **kwargs)
            if rc != DYNRM_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    def terminate_connection(self, conn_name):
        module = self._get_module_for_connection(conn_name)
        if None == module:
            return DYNRM_SUCCESS
        rc = self.run_module_service("TERMINATE", "CONNECTION", conn_name)
        if rc == DYNRM_MCA_SUCCESS:
            self.connections.pop(conn_name)
        return rc
    
    def accept_connection_termination(self, conn_name):
        module = self._get_module_for_connection(conn_name)
        peer = module.run_module_service(module, "GET", "PEER", conn_name)
        if None == module:
            return DYNRM_SUCCESS
        rc = self.run_module_service("ACCEPT", "CONNECTION_TERMINATION", conn_name)
        if rc == DYNRM_MCA_SUCCESS:
            self.connections.pop(conn_name)
            for callback in self.connection_accepted_callbacks:
                callback(module, conn_name, peer)
        return rc

    # private function
    def _get_module_for_connection(self, conn_name):
        if conn_name not in self.connections:
            v_print("WARNING: _get_module_for_connection couldn't find connection "+conn_name, 1, self.verbosity)
        return self.connections.get(conn_name)    
