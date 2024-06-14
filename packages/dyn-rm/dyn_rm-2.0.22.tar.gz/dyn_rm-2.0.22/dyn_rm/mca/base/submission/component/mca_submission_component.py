from dyn_rm.mca.mca import MCAComponent
from dyn_rm.mca.mca import MCAClass

from dyn_rm.mca.base.submission.module import MCASubmissionModule
from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.base.callback.module import MCACallbackModule
from dyn_rm.util.constants import *


from abc import abstractmethod

class MCASubmissionComponent(MCAComponent, MCAClass):

    LOOPBACK = 0

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.params = dict()
        comp = MCACallbackComponent()
        comp.register_module(MCACallbackModule())
        self.register_component(comp)
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASubmissionModule.OBJECT_SUBMITTED_EVENT, self._object_submitted_callback)

        self._user_callbacks = []

        MCASubmissionComponent.register_base_services(self)


    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "PARAMETERS", self.set_parameters)
        self.register_service("UNSET", "PARAMETER", self.unset_parameter)
        self.register_service("GET", "PARAMETERS", self.get_parameters)

        self.register_service("SET", "MODULE_PARAMETERS", self.set_module_parameters)
        self.register_service("UNSET", "MODULE_PARAMETER", self.unset_module_parameter)
        self.register_service("GET", "MODULE_PARAMETERS", self.get_module_parameters)


        self.register_service("REQUEST", "CONNECTION", self.request_connection)

        self.register_service("SUBMIT", "OBJECT", self.submit_object) 
        self.register_service("SUBMIT", "MIX", self.submit_mix)

        self.register_service("REGISTER", "SUBMISSION_MODULE", self.register_submission_module)

        self.register_service("REGISTER", "OBJECT_SUBMITTED_CALLBACK", self.register_object_submitted_callback)

        self.register_service("SHUTDOWN", "SUBMISSION_COMPONENT", self.shutdown)

    def set_parameters(self, params: dict):
        self.params.update(params)
        return DYNRM_MCA_SUCCESS
    
    def unset_parameter(self, key):
        self.params.pop(key)
        return DYNRM_MCA_SUCCESS

    def get_parameters(self):
        return self.params


    def set_module_parameters(self, module_class, params: dict):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module_class, "SET", "PARAMETERS", params)
    
    def unset_module_parameter(self, module_class, key):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "UNSET", "PARAMETER", key)
    def get_module_parameters(self, module_class):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND        
        return self.run_module_service(module, "GET", "PARAMETERS")
  

    def submit_mix(self, module_class, conn_name, mix, params):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        # Handler Loopback
        if conn_name == MCASubmissionComponent.LOOPBACK:
            conn_name = module_class.mca_get_name()
        return self.run_module_service(module, "SUBMIT", "MIX", conn_name, mix, params)
    
    def submit_object(self, module_class, conn_name, object, params):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        if conn_name == MCASubmissionComponent.LOOPBACK:
            conn_name = module_class.mca_get_name()
        return self.run_module_service(module, "SUBMIT", "OBJECT", conn_name, object, params)
    
    # returns the conn name
    def request_connection(self, module_class, params):
        module = self.get_module(module_class)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return module.run_service("REQUEST", "CONNECTION", params)

    def register_submission_module(self, module, *args, **kwargs):
        rc = self.register_module(module, *args, **kwargs)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        rc =  module.run_service("CREATE", "LOOPBACK_CONNECTION", module.mca_get_name(), self)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        return DYNRM_MCA_SUCCESS
        

    def register_object_submitted_callback(self, cbfunc):
        self._user_callbacks.append(cbfunc)
        return DYNRM_MCA_SUCCESS


    def shutdown(self):
        for module in self.get_modules():
            rc = module.run_service("SHUTDOWN", "SUBMISSION_MODULE")
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        return DYNRM_MCA_SUCCESS

    def _object_submitted_callback(self, conn_name, event_name, object, params, cbdata):
        
        # Answer invalid requests 
        if None == object or None == params:
            return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.OBJECT_SUBMITTED_RESPONSE_EVENT, DYNRM_MCA_ERR_BAD_PARAM, cbdata)
        
        module = self.run_component_service(MCACallbackComponent, "GET", "PEER", conn_name)
        # Call the user callbacks
        for cbfunc in self._user_callbacks:
            rc = cbfunc(module.__class__, object, params)
            if rc != DYNRM_SUCCESS:
                break

        # Send back the results
        self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.OBJECT_SUBMITTED_RESPONSE_EVENT, rc, cbdata)
        return DYNRM_MCA_SUCCESS
            