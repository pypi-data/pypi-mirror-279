from dyn_rm.mca.mca import MCA, MCAModule
from dyn_rm.util.constants import *

from abc import abstractmethod
 
import inspect
import asyncio
from concurrent.futures import ThreadPoolExecutor

from time import sleep

class MCAEventLoopModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.event_loops = dict()
        MCAEventLoopModule.register_base_services(self)
        
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


    # module functions
    def register_event_loop(self, module_class, loop_name):
        if loop_name in self.event_loops:
            return DYNRM_MCA_ERR_EXISTS
        return self.register_event_loop_function(loop_name)
    
    def start_event_loop(self, loop_name):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.start_event_loop_function(loop_name)
    
    def get_current_loop(self):
        try:
            # Check if the function is running inside an asyncio event loop
            #task = asyncio.current_task()
            #if task == None:
            #    print("Task None")
            #    return None
            
            loop = asyncio._get_running_loop()
            if None == loop:
                return None
            
            for loop_name in self.event_loops.keys():
                if self.event_loops[loop_name] == loop:
                    return loop_name
            return None

        except RuntimeError:
            return None  # Not running inside an event loop

    def run_func(self, loop_name, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_function(loop_name, func, *args, **kwargs)
    
    def run_func_nb(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_nb_function(loop_name, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_async(self,  loop_name, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_async_function(loop_name, func, *args, **kwargs)
    
    def run_func_delayed(self, loop_name, delay, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_delayed_function(loop_name, delay, func, *args, **kwargs)
    
    def run_func_nb_delayed(self, loop_name, delay, cbfunc, cbdata, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_nb_delayed_function(loop_name, delay, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_nb_async(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_nb_async_function(loop_name, cbfunc, cbdata, func, *args, **kwargs)
    
    def run_func_async_delayed(self, loop_name, delay, func, *args, **kwargs):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.run_func_async_delayed_function(loop_name, delay, func, *args, **kwargs)
    
    def stop_event_loop(self, loop_name):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.stop_event_loop_function(loop_name)
    
    def deregister_event_loop(self, loop_name):
        if loop_name not in self.event_loops:
            return DYNRM_MCA_ERR_NOT_FOUND
        return self.deregister_event_loop_function(loop_name)


    # Functions for module implementations
    def add_event_loop(self, loop_name, event_loop):
        self.event_loops[loop_name] = event_loop
        return DYNRM_MCA_SUCCESS

    def get_event_loop(self, loop_name):
        return self.event_loops.get(loop_name)
    
    def remove_event_loop(self, loop_name):
        return self.event_loops.pop(loop_name)



    # Abstract Functions

    # Module function implementations
    def mca_shutdown(self):
        for loop_name in [key for key in self.event_loops.keys()]:
            rc = self.stop_event_loop(loop_name)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
            rc = self.deregister_event_loop(loop_name)
            if rc != DYNRM_MCA_SUCCESS:
                return rc
        
        return DYNRM_MCA_SUCCESS
        

    def register_event_loop(self, loop_name):
        self.add_event_loop(loop_name, asyncio.new_event_loop())
        return DYNRM_MCA_SUCCESS

    def start_event_loop_function(self, loop_name):
        loop = self.get_event_loop(loop_name)
        ThreadPoolExecutor().submit(loop.run_forever)
        return DYNRM_MCA_SUCCESS

    def run_func_function(self, loop_name, func, *args, **kwargs):
        loop = self.get_event_loop(loop_name)
        future = asyncio.run_coroutine_threadsafe(self.execute_as_coroutine(func, *args, **kwargs), loop)
        result = future.result()
        return result

    # Create a seperate thread which runs the nb_wrapper in the event loop. 
    # CAN access critical data
    def run_func_nb_function(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        loop = self.get_event_loop(loop_name)
        # Submit the synchronous function to the executor
        asyncio.run_coroutine_threadsafe(self.nb_wrapper(cbfunc, cbdata, func, *args, **kwargs), loop)
        return DYNRM_MCA_SUCCESS

    # Runs the function in a seperate thread but blocks until the results are there.
    # CAN NOT access critical data 
    # Not very useful, but anyways
    def run_func_async_function(self, loop_name, func, *args, **kwargs):
        future = ThreadPoolExecutor().submit(func, *args, **kwargs)
        results = future.result()
        return results

    # Runs the function after some delay in the event_loop and blocks until results are ready
    # CAN ACCESS critical_data
    def run_func_delayed_function(self, loop_name, delay, func, *args, **kwargs):
        loop = self.get_event_loop(loop_name)
        future = asyncio.run_coroutine_threadsafe(self.execute_as_delayed_coroutine(delay, func, *args, **kwargs), loop)
        result = future.result()
        return result     

    # Runs the function after some delay in the event_loop but does not block
    # CAN ACCESS critical_data
    def run_func_nb_delayed_function(self, loop_name, delay, cbfunc, cbdata, func, *args, **kwargs):
        loop = self.get_event_loop(loop_name)
        asyncio.run_coroutine_threadsafe(self.execute_as_delayed_coroutine(delay, self.nb_wrapper, cbfunc, cbdata, func, *args, **kwargs), loop)
        return DYNRM_MCA_SUCCESS    

    # Runs the function asynchronously, non-blocking and delivers results to given cbfunc
    # CAN NOT ACCESS critical_data
    def run_func_nb_async_function(self, loop_name, cbfunc, cbdata, func, *args, **kwargs):
        loop = self.get_event_loop(loop_name)
        # Submit the synchronous function to the executor
        ThreadPoolExecutor().submit(self.nb_wrapper, cbfunc, cbdata, func, *args, **kwargs)
        return DYNRM_MCA_SUCCESS
    
    # Runs function asynchronously after some delay
    def run_func_async_delayed(self, loop_name, delay, func, *args, **kwargs):
        return self.run_func_async_function(loop_name, self.execute_as_delayed_function, delay, func, *args, **kwargs)

    def stop_event_loop_function(self, loop_name):
        loop = self.get_event_loop(loop_name)
        self.run_func_function(loop_name, loop.call_soon_threadsafe, loop.stop)
        while loop.is_running():
            sleep(0.05)
        return DYNRM_MCA_SUCCESS

    def deregister_event_loop_function(self, loop_name):
        self.get_event_loop(loop_name).close()
        self.remove_event_loop(loop_name)
        return DYNRM_MCA_SUCCESS
    

    # ===== Internal functions =========

    async def execute_as_coroutine(self, func, *args, **kwargs):
        return func(*args, **kwargs)
    
    async def execute_as_delayed_coroutine(self, delay, func, *args, **kwargs):
        await asyncio.sleep(delay)
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)
    
    def execute_as_delayed_function(self, delay, func, *args, **kwargs):
        sleep(delay)
        return func(*args, **kwargs)

    async def nb_wrapper(self, cbfunc, cbdata, func, *args, **kwargs):
        if None == cbfunc:
            func(*args, **kwargs)
        else:
            cbfunc(func(*args, **kwargs), cbdata = cbdata)
    
    
