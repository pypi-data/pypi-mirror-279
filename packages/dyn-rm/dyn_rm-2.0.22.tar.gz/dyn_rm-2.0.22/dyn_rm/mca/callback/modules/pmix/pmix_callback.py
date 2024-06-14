from dyn_rm.mca.base.callback.module import MCACallbackModule
from dyn_rm.util.constants import *
from dyn_rm.util.functions import *

from pmix import *

class PmixCallbackModule(MCACallbackModule):
    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.connections_my_peer = dict()
        self.connections_my_procid = dict()

    # simply call PMIx's connect to server function
    def request_connection_function(self, conn_name, mypeer, peer, params):
        
        if "pid" in params:
            info = [
                    {'key':PMIX_SERVER_PIDINFO, 'value':params["pid"], 'val_type':PMIX_PID},
                    {'key': "SCHEDULER", 'value': True, 'val_type':PMIX_BOOL}
            ]

            rc, myprocid = mypeer.init(info)

            if rc != PMIX_SUCCESS:
                return DYNRM_MCA_ERR_NOT_FOUND
        else:
            return DYNRM_MCA_ERR_BAD_PARAM
        rc, servers = mypeer.get_servers()
        if rc != PMIX_SUCCESS or len(servers) < 1:
            return DYNRM_MCA_ERR_NOT_FOUND
        if mypeer not in self.connections_my_peer.values():
            self.connections_my_peer[conn_name] = mypeer
        if myprocid not in self.connections_my_procid.values():
            self.connections_my_procid[conn_name] = myprocid
        self.add_connection(conn_name, servers[0], params)

        return DYNRM_MCA_SUCCESS

    # We accept all connection so just add it
    def accept_connection_function(self, conn_name, peer, params):
        self.add_connection(conn_name, peer, params)
        return DYNRM_MCA_SUCCESS
    
    # We accept all connection terminations so just remove it
    def accept_connection_termination_function(self, conn_name):
        return self.remove_connection(conn_name)

    def register_callback_function(self, conn_name, event_name, callback):
        my_peer = self.connections_my_peer.get(conn_name)
        if None == my_peer:
            return DYNRM_MCA_ERR_NOT_FOUND
        rc, id = my_peer.register_event_handler([event_name], None, callback)
        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Register_event_handler")
        return self.add_callback(conn_name, event_name, callback)
    
    # We don't need to actually send anything - just execute the peers callback
    def send_event_function(self, conn_name, event_name, *args, **kwargs):
        if len(args) != 1:
            return DYNRM_MCA_SUCCESS
        mypeer = self.connections_my_peer.get(conn_name)
        if None == mypeer:
            return DYNRM_MCA_ERR_BAD_PARAM
        myprocid = self.connections_my_procid.get(conn_name)
        if None == myprocid:
            return DYNRM_MCA_ERR_BAD_PARAM
        rc = mypeer.notify_event(event_name, myprocid, PMIX_RANGE_RM, *args)
        if rc != PMIX_SUCCESS:
            return DYNRM_MCA_ERR_BAD_PARAM
        return DYNRM_MCA_SUCCESS

    # simply call the accept function of the remote components default module
    def terminate_connection_function(self, conn_name):
        peer = self.get_peer(conn_name)
        return DYNRM_MCA_SUCCESS
    

    class PMIx_Error(Exception):

        def __init__(self, error_code, pmix_function):
            message = "PMIx function '"+pmix_function+"' returned error code: "+str(error_code)
            super().__init__(message)   