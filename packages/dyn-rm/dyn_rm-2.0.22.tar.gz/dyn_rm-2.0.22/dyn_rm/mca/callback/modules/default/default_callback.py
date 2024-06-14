from dyn_rm.mca.base.callback.module import MCACallbackModule
from dyn_rm.util.constants import *
from dyn_rm.util.functions import *

class DefaultCallbackModule(MCACallbackModule):

    # simply call the accept function of the remote components default module
    def request_connection_function(self, conn_name, mypeer, peer, params):
        rc = self.run_peer_component_service(peer, "ACCEPT", "CONNECTION", self.__class__, conn_name, mypeer, params)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        self.add_connection(conn_name, peer, params)
        return DYNRM_MCA_SUCCESS

    # We accept all connection so just add it
    def accept_connection_function(self, conn_name, peer, params):
        self.add_connection(conn_name, peer, params)
        return DYNRM_MCA_SUCCESS
    
    # We accept all connection terminations so just remove it
    def accept_connection_termination_function(self, conn_name):
        return self.remove_connection(conn_name)

    def register_callback_function(self, conn_name, event_name, callback):
        return self.add_callback(conn_name, event_name, callback)
    
    # We don't need to actually send anything - just execute the peers callback
    def send_event_function(self, conn_name, event_name, data):
        peer = self.get_peer(conn_name)
        return self.run_peer_module_service(peer, "EXECUTE", "CALLBACK", conn_name, event_name, data)

    # simply call the accept function of the remote components default module
    def terminate_connection_function(self, conn_name):
        peer = self.get_peer(conn_name)
        return self.run_peer_component_service(peer, "ACCEPT", "CONNECTION_TERMINATION", conn_name)