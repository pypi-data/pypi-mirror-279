from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule
from dyn_rm.util.constants import *
from dyn_rm.util.functions import *

import asyncio
from concurrent.futures import ThreadPoolExecutor

from time import sleep

class AsyncioEventLoopModule(MCAEventLoopModule):
    
    # Module function implementations
    def register_event_loop(self, loop_name):
        self.add_event_loop(loop_name, asyncio.new_event_loop())
        return DYNRM_MCA_SUCCESS

    def start_event_loop_function(self, loop_name):
        loop = self.get_event_loop(loop_name)
        future = ThreadPoolExecutor().submit(loop.run_forever)
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
        ThreadPoolExecutor().submit(loop.call_soon_threadsafe, self.nb_wrapper, cbfunc, cbdata, func, *args, **kwargs)
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
        return func(*args, **kwargs)
    
    def execute_as_delayed_function(self, delay, func, *args, **kwargs):
        sleep(delay)
        return func(*args, **kwargs)

    def nb_wrapper(self, cbfunc, cbdata, func, *args, **kwargs):
        cbfunc(func(*args, **kwargs), cbdata = cbdata)
    
    
