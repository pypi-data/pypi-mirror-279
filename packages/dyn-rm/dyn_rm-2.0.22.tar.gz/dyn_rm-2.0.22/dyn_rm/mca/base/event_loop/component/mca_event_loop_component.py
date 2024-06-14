from dyn_rm.mca.mca import MCAComponent

from dyn_rm.util.constants import *

import sys

class MCAEventLoopComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.event_loops = dict()
        MCAEventLoopComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("REGISTER", "EVENT_LOOP", self.register_event_loop)
        self.register_service("START", "EVENT_LOOP", self.start_event_loop)
        self.register_service("GET", "CURRENT_LOOP", self.get_current_loop)
        self.register_service("RUN", "FUNC", self.run_func) # call_soon_threadsafe
        self.register_service("RUN", "FUNC_NB", self.run_func_nb) #  
        self.register_service("RUN", "FUNC_ASYNC", self.run_func_async)
        self.register_service("RUN", "FUNC_DELAYED", self.run_func_delayed)
        self.register_service("RUN", "FUNC_NB_DELAYED", self.run_func_nb_delayed)
        self.register_service("RUN", "FUNC_NB_ASYNC", self.run_func_nb_async)
        self.register_service("RUN", "FUNC_ASYNC_DELAYED", self.run_func_async_delayed)
        self.register_service("STOP", "EVENT_LOOP", self.stop_event_loop)
        self.register_service("DEREGISTER", "EVENT_LOOP", self.deregister_event_loop)


    def register_event_loop(self, module_class, loop_name):
        if loop_name in self.event_loops:
            return DYNRM_MCA_ERR_EXISTS
        module = self.get_module(module_class)
        if None == module:
            module = module_class()
            self.register_module(module)
        rc = self.run_module_service(module, "REGISTER", "EVENT_LOOP", loop_name)
        if rc == DYNRM_MCA_SUCCESS:
            self.event_loops[loop_name] = module
        return rc
    
    def start_event_loop(self, loop_name):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "START", "EVENT_LOOP", loop_name)
    
    def get_current_loop(self, module):
        module = self.get_module(module)
        if None == module:
            return None
        return module.run_service("GET", "CURRENT_LOOP")

    def run_func(self, loop_name, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC", loop_name, func, *args, **kwargs)
    
    def run_func_nb(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_NB", loop_name, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_async(self,  loop_name, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_ASYNC", loop_name, func, *args, **kwargs)
    
    def run_func_delayed(self, loop_name, delay, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_DELAYED", loop_name, delay, func, *args, **kwargs)
    
    def run_func_nb_delayed(self, loop_name, delay, cbfunc, cbdata, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_NB_DELAYED", loop_name, delay, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_nb_async(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_NB_ASYNC", loop_name, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_async_delayed(self, loop_name, delay, func, *args, **kwargs):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "RUN", "FUNC_ASYNC_DELAYED", loop_name, delay, func, *args, **kwargs)
    
    def stop_event_loop(self, loop_name):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_module_service(module, "STOP", "EVENT_LOOP", loop_name)
    
    def deregister_event_loop(self, loop_name):
        module = self.event_loops.get(loop_name)
        if None == module:
            return DYNRM_MCA_ERR_NOT_FOUND
        rc = self.run_module_service(module, "DEREGISTER", "EVENT_LOOP", loop_name)
        if rc == DYNRM_MCA_SUCCESS:
            self.event_loops.pop(loop_name)
        return rc
