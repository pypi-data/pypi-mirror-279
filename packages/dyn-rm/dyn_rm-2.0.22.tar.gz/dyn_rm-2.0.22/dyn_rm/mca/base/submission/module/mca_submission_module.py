from dyn_rm.mca.mca import MCAModule,MCAClass

from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.base.callback.module import MCACallbackModule

from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule

from dyn_rm.util.constants import *

from abc import abstractmethod

import csv

class MCASubmissionModule(MCAModule, MCAClass):

    OBJECT_SUBMITTED_EVENT = 0
    OBJECT_SUBMITTED_RESPONSE_EVENT = 1
    MIX_SUBMITTED_EVENT = 2
    MIX_SUBMITTED_RESPONSE_EVENT = 3

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.params = dict()
        self._loopback_conn = None
        self.register_component(MCACallbackComponent())

        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASubmissionModule.OBJECT_SUBMITTED_EVENT, self._object_submitted_callback)
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASubmissionModule.MIX_SUBMITTED_EVENT, self._mix_submitted_callback)

        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASubmissionModule.OBJECT_SUBMITTED_RESPONSE_EVENT, self._object_submitted_response_callback)
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASubmissionModule.MIX_SUBMITTED_RESPONSE_EVENT, self._mix_submitted_response_callback)

        MCASubmissionModule.register_base_services(self)

        self.startup_function()

    @staticmethod
    def register_base_services(self):
        self.register_service("SET", "PARAMETERS", self.set_parameters)
        self.register_service("UNSET", "PARAMETER", self.unset_parameters)
        self.register_service("GET", "PARAMETERS", self.get_parameters)
        
        self.register_service("SUBMIT", "OBJECT", self.submit_object)  
        self.register_service("SUBMIT", "MIX", self.submit_mix)
        
        self.register_service("CREATE", "LOOPBACK_CONNECTION", self.create_loopback_connection)
        
        self.register_service("REQUEST", "CONNECTION", self.request_connection)

        self.register_service("SHUTDOWN", "SUBMISSION_MODULE", self.shutdown)


    def set_parameters(self, params: dict):
        self.params.update(params)
        return DYNRM_MCA_SUCCESS
    
    def unset_parameters(self, key):
        self.params.pop(key)
        return DYNRM_MCA_SUCCESS

    def get_parameters(self):
        return self.params
    
    def create_loopback_connection(self, conn_name, loopback_peer):
        rc = self.run_component_service(MCACallbackComponent, "REQUEST", "CONNECTION", MCACallbackModule, conn_name, self, loopback_peer, dict())
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        self._loopback_conn = conn_name
        return DYNRM_MCA_SUCCESS
    
    def request_connection(self, params):
        return self.request_connection_function(self, params)

    # TODO
    def submit_mix(self, conn_name, mix, params):
        if conn_name == self._loopback_conn:
            rc = self.submit_mix_function(mix, params)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
            rc = self._mix_submitted_response_callback(self._loopback_conn, MCASubmissionModule.MIX_SUBMITTED_RESPONSE_EVENT, rc, conn_name)
            return rc
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.MIX_SUBMITTED_EVENT, object, params, conn_name)
    
    def submit_object(self, conn_name, object, params):
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.OBJECT_SUBMITTED_EVENT, object, params, conn_name)

    def shutdown(self):
        return self.shutdown_function()


    def _object_submitted_callback(self, conn_name, event_name, object, params):
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", self._loopback_conn, MCASubmissionModule.OBJECT_SUBMITTED_EVENT, object, params, conn_name)

    def _mix_submitted_callback(self, conn_name, event_name, mix, params):
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", self._loopback_conn, MCASubmissionModule.MIX_SUBMITTED_EVENT, mix, params, conn_name)

    # cbdata is the conn_name where the request came from 
    def _object_submitted_response_callback(self, conn_name, event_name, rc, cbdata):
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.OBJECT_SUBMITTED_RESPONSE_EVENT, rc, cbdata)

    # cbdata is the conn_name where the request came from 
    def _mix_submitted_response_callback(self, conn_name, event_name, rc, cbdata):
        return self.run_component_service(MCACallbackComponent, "SEND", "EVENT", conn_name, MCASubmissionModule.MIX_SUBMITTED_RESPONSE_EVENT, rc, cbdata)


    @abstractmethod
    def startup_function(self):
        ev = MCAEventLoopComponent()
        ev.register_module(MCAEventLoopModule())
        self.register_component(ev)
        self.run_component_service(MCAEventLoopComponent, "REGISTER", "EVENT_LOOP", MCAEventLoopModule, "MIX_LOOP")
        self.run_component_service(MCAEventLoopComponent, "START", "EVENT_LOOP", "MIX_LOOP")

    @abstractmethod
    def request_connection_function(self, params):
        return self.run_component_service(MCACallbackComponent, "REQUEST", "CONNECTION", MCACallbackModule, self, params, dict())


    # Abstract Functions
    @abstractmethod
    def submit_object_function(self, object, system, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    @abstractmethod
    def submit_mix_function(self, mix, params):
        with open(mix, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) < 3:
                    continue
                # Each row is one submission
                arrival, object, obj_params = row
                if obj_params == "":
                    obj_params = dict()
                else:
                    obj_params = eval(obj_params)
                obj_params.update(params)
                rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB_DELAYED", "MIX_LOOP", int(arrival), None, None, self.submit_object, self._loopback_conn, object, obj_params)
                if rc != DYNRM_MCA_SUCCESS:
                    return rc
        return DYNRM_MCA_SUCCESS
    
    @abstractmethod
    def shutdown_function(self):
        rc  = self.run_component_service(MCAEventLoopComponent, "STOP", "EVENT_LOOP", "MIX_LOOP")
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        return self.run_component_service(MCAEventLoopComponent, "DEREGISTER", "EVENT_LOOP", "MIX_LOOP")
