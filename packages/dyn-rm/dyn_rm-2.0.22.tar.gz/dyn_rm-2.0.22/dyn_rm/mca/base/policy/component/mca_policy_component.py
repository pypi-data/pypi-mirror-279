from dyn_rm.mca.mca import MCAComponent
from dyn_rm.util.constants import *

class MCAPolicyComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._policies = dict()
        self._active_policy = None

        MCAPolicyComponent._register_base_services(self)

        
    def _register_base_services(self):
        self.register_service("ADD", "POLICY", self._add_policy)
        self.register_service("GET", "POLICY", self._get_policy)
        self.register_service("SET", "ACTIVE_POLICY", self._set_active_policy)
        self.register_service("GET", "ACTIVE_POLICY", self._get_active_policy)
        self.register_service("REMOVE", "POLICY", self._remove_policy)


    def _add_policy(self, name, policy):
        self.register_module(policy)
        self._policies[name] = policy
        if self._active_policy == None:
            self._active_policy = policy
        return DYNRM_MCA_SUCCESS

    def _get_policy(self, name):
        return self._policies.get(name)
    
    def _set_active_policy(self, name):
        if name not in self._policies:
            return DYNRM_MCA_ERR_BAD_PARAM
        self._active_policy = self._policies.get(name)
        return DYNRM_MCA_SUCCESS

    def _get_active_policy(self):
        return self._active_policy

    def _remove_policy(self, name):
        return self._policies.pop(name) 

    def mca_shutdown(self):
        for policy in self._policies.values():
            policy.run_service("MCA", "SHUTDOWN")
        return self.mca_default_shutdown() 