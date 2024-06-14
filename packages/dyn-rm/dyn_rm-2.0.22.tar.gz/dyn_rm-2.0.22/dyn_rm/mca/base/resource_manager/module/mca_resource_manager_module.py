from dyn_rm.mca.mca import MCAModule,MCAClass
from dyn_rm.mca.base.policy.component import MCAPolicyComponent
from dyn_rm.mca.base.submission.component import MCASubmissionComponent
from dyn_rm.mca.base.submission.module import MCASubmissionModule
from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.base.callback.module import MCACallbackModule
from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule
from dyn_rm.mca.base.system.component import MCASystemComponent,MCATopologyCreationComponent,MCATaskGraphCreationComponent
from dyn_rm.mca.base.system.module import *

from dyn_rm.util.constants import *
from dyn_rm.util.functions import v_print

from abc import abstractmethod

from queue import Queue

from functools import partial
from random import random
from threading import Lock

class MCAResourceManagerModule(MCAModule, MCAClass):

    ALL_TASK_GRAPHS_TERMINATED = "ALL_TASK_GRAPHS_TERMINATED_EVENT"

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._params = dict()
        self._terminate_soon = False
        self._submission_buffer = Queue()
        self._instance_lock = Lock()
        self._delayed_tasks = 0
        # CALLBACKS
        self.register_component(MCACallbackComponent(verbosity=self.verbosity))
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASystemModule.PSETOP_DEFINED_EVENT, self._psetop_defined_callback)
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASystemModule.PSETOP_FINALIZED_EVENT, self._psetop_finalized_callback)
        self.run_component_service(MCACallbackComponent, "REGISTER", "CALLBACK", MCASystemModule.TASK_TERMINATED_EVENT, self._task_terminated_callback)
        # SUBMISSION
        self.register_component(MCASubmissionComponent())
        self.run_component_service(MCASubmissionComponent, "REGISTER", "SUBMISSION_MODULE", MCASubmissionModule())
        rc = self.run_component_service(MCASubmissionComponent, "REGISTER", "OBJECT_SUBMITTED_CALLBACK", self._object_submitted_callback)
        if rc != DYNRM_MCA_SUCCESS:
            print("'REGISTER', 'OBJECT_SUBMITTED_CALLBACK' failed with ", rc)
            exit(1)
        
        # EVENT_LOOP
        self.register_component(MCAEventLoopComponent())
        self.run_component_service(MCAEventLoopComponent, "REGISTER", "EVENT_LOOP", MCAEventLoopModule, "MAIN_LOOP")
        self.run_component_service(MCAEventLoopComponent, "START", "EVENT_LOOP", "MAIN_LOOP")
        
        # TOPOLOGY
        self.register_component(MCATopologyCreationComponent())
        
        # TASKS
        self.register_component(MCATaskGraphCreationComponent())

        # SYSTEMS
        self.register_component(MCASystemComponent(parent=self, enable_output = enable_output, verbosity=self.verbosity))

        # POLICIES
        self.register_component(MCAPolicyComponent(parent=self, enable_output = enable_output, verbosity=self.verbosity))
        
        MCAResourceManagerModule.register_base_services(self)

    def register_base_services(self):
        self.register_service("SET", "PARAMETER", self.set_parameter)
        self.register_service("ADD", "SYSTEM", self.add_system)
        self.register_service("GET", "SYSTEM", self.get_system)
        self.register_service("ADD", "POLICY", self.add_policy)
        self.register_service("APPLY", "POLICY", self.apply_policy)
        self.register_service("SET", "ACTIVE_POLICY", self.set_active_policy)
        self.register_service("REGISTER", "TOPOLOGY_MODULE", self.register_topo_module)
        self.register_service("REGISTER", "TASK_GRAPH_MODULE", self.register_task_module)
        self.register_service("REGISTER", "SUBMISSION_MODULE", self.register_submission_module)
        self.register_service("SUBMIT", "OBJECT", self.submit_object)
        self.register_service("SUBMIT", "MIX", self.submit_mix)

    def set_parameter(self, key, value):
        self._params[key] = value
        return DYNRM_MCA_SUCCESS    

    def apply_policy(self, system_name, policy_name = None):
        system = self.run_component_service(MCASystemComponent, "GET", "SYSTEM", system_name)
        if None == system:
            return DYNRM_MCA_ERR_BAD_PARAM
        if None == policy_name:
            policy = self.run_component_service(MCAPolicyComponent, "GET", "ACTIVE_POLICY")
        else:
            policy = self.run_component_service(MCAPolicyComponent, "GET", "POLICY", policy_name)
        if None == policy:
            return DYNRM_MCA_ERR_BAD_PARAM

        v_print("", 2, self.verbosity)
        v_print("EVAL POLICY  " + policy.mca_get_name(), 2, self.verbosity)       
        result = policy.run_service("EVAL", "POLICY", system)
        v_print("*** FINAL RESULT: ***", 2, self.verbosity)

        total_gain = 0
        for setop, gain, output in zip(result["setops"], result["performances"], result["outputs"]):
            nodes_before = setop.run_service("GET", "INPUT")[0].run_service("GET", "ACCESSED_NODES")
            nodes_after = output[len(output) - 1].run_service("GET", "ACCESSED_NODES")
            model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
            prev_perf = model.run_service("EVAL", "INPUT", setop.run_service("GET", "INPUT"), ["SPEEDUP"])
            past_perf = model.run_service("EVAL", "OUTPUT", output, ["SPEEDUP"])
            gain = model.run_service("EVAL", "EDGE", setop.run_service("GET", "INPUT"), output, ["SPEEDUP"])

            v_print("     Setop "+ setop.run_service("GET", "GID") + ":", 2, self.verbosity)
            v_print("         Nodes before: " + str([node.run_service("GET", "NAME") for node in nodes_before]), 2, self.verbosity)
            v_print("         Nodes after: " + str([node.run_service("GET", "NAME") for node in nodes_after]), 2, self.verbosity)
            v_print("         Speedup before: " + str(prev_perf["SPEEDUP"]), 2, self.verbosity)
            v_print("         Speedup after: " + str(past_perf["SPEEDUP"]), 2, self.verbosity)
            v_print("         Speedup gain: " + str(gain["SPEEDUP"]), 2, self.verbosity)
            v_print("         Speedup gain (normalized): " + str(gain["SPEEDUP"]/(abs(len(nodes_after)-len(nodes_before)))), 2, self.verbosity)
            total_gain += gain["SPEEDUP"]
        
        v_print("*** TOTAL GAIN: " + str(total_gain) + "***", 2, self.verbosity)

        return system.run_service("APPLY", "PSETOPS", result["setops"], result["outputs"], result["a_lists"])

    def _psetop_finalized_callback(self, conn_name, event_name, system, psetop):

        v_print("PSETOP '"+psetop.run_service("GET", "NAME")+"' FINALIZED in system '"+system.run_service("GET", "NAME")+"'", 10, self.verbosity)

        return system.run_service("EXECUTE", "IN_LOOP", self.apply_policy, system.run_service("GET", "NAME"))


    def _psetop_defined_callback(self, conn_name, event_name, system, psetop):

        v_print("PSETOP '"+psetop.run_service("GET", "NAME")+"' DEFINED in system '"+system.run_service("GET", "NAME")+"'", 10, self.verbosity)

        return system.run_service("EXECUTE", "IN_LOOP", self.apply_policy, system.run_service("GET", "NAME"))

    def _task_terminated_callback(self, conn_name, event_name, system, task):
        v_print("TASK '"+task.run_service("GET", "NAME")+"' TERMINATED in system '"+system.run_service("GET", "NAME")+"'", 5, self.verbosity)

        task_graph = task.run_service("GET", "TASK_GRAPH")
        if task_graph.run_service("GET", "TASK_STATUS") == MCATaskModule.TASK_STATUS_TERMINATED:
            v_print("\n### TASK GRAPH "+task_graph.run_service("GET", "GID")+" COMPLETED ###\n", 5, self.verbosity)

        task_graphs = system.run_service("GET", "TASK_GRAPHS")
        num_running_task_graphs = len([t for t in task_graphs if t.run_service("GET", "TASK_STATUS") != MCATaskModule.TASK_STATUS_TERMINATED])
        if "max_task_graphs" in self._params:
            if num_running_task_graphs < self._params["max_task_graphs"] and self._submission_buffer.qsize() > 0:
                try:
                    func = self._submission_buffer.get()
                    delay = 0
                    if "max_task_graphs_delay" in self._params:
                        if all(key in self._params["max_task_graphs_delay"] for key in ['a', 'b', 'c']):
                            delay = self._params["max_task_graphs_delay"]["a"] + \
                                    int(random() * self._params["max_task_graphs_delay"]["b"])*\
                                    self._params["max_task_graphs_delay"]["c"]
                    v_print("RUN with delay="+str(delay), 8, self.verbosity)
                    rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB_DELAYED", "MAIN_LOOP", delay, None, None, self._executor, func)
                    if rc != DYNRM_MCA_SUCCESS:
                        v_print("MCA_RESOURCE_MANAGER_MODULE: Error submitting new job: "+str(rc), 3, self.verbosity)
                    self._instance_lock.acquire()
                    self._delayed_tasks +=1
                    self._instance_lock.release()
                except(Exception):
                    pass

        rc = system.run_service("EXECUTE", "IN_LOOP", self.apply_policy, system.run_service("GET", "NAME"))
        if rc != DYNRM_MCA_SUCCESS:
            return rc

        if self._terminate_soon:    
            if num_running_task_graphs == 0:
                v_print("ALL TASK GRAPHS TERMIANTED", 5, self.verbosity)
                rc = self.run_component_service(MCACallbackComponent, "BCAST", "EVENT", MCAResourceManagerModule.ALL_TASK_GRAPHS_TERMINATED)
                if rc != DYNRM_MCA_SUCCESS:
                    print("System Bcast event 'PSETOP_DEFINED' failed ", rc)
                return rc

        return DYNRM_MCA_SUCCESS

    def _object_submitted_callback(self, module, object, params):
        v_print("OBJECT_SUBMITTED "+str(object)+" "+str(params), 3, self.verbosity)
        
        if "system_name" not in params:
            return DYNRM_MCA_ERR_BAD_PARAM
        system_name = params["system_name"]
        system = self.get_system(system_name)
        if None == system:
            return DYNRM_MCA_ERR_BAD_PARAM
        
        if "max_task_graphs" in self._params:
            num_running_task_graphs = len([t for t in system.run_service("GET", "TASK_GRAPHS") if t.run_service("GET", "TASK_STATUS") != MCATaskModule.TASK_STATUS_TERMINATED])
            if num_running_task_graphs >= self._params["max_task_graphs"]:
                self._submission_buffer.put(partial(self._object_submitted_callback, module, object, params)) 
                return DYNRM_MCA_SUCCESS
            
        if "terminate_soon" in params:
            self._terminate_soon = True
        
        gid = system.run_service("GET", "NEW_GID")

        task_graph = MCATaskGraphModule(gid)
        task_graph.run_service("SET", "GID", gid)

        #TODO: cycle through the suggested modules and try to create a topo_graph
        rc = DYNRM_MCA_ERR_BAD_PARAM
        if "task_graph_creation_modules" in params:
            for module in params["task_graph_creation_modules"]:
                comp = self.get_component(MCATaskGraphCreationComponent)
                if module not in [m.__class__ for m in comp.get_modules()]:
                    comp.register_module(module())
                task_graph = self.run_component_service(MCATaskGraphCreationComponent, "CREATE", "TASK_GRAPH", module, task_graph, object, params)
                if None != task_graph:
                    rc = system.run_service("SUBMIT", "TASK_GRAPH", task_graph)                    
        else:
            task_graph = self.run_component_service(MCATaskGraphCreationComponent, "CREATE", "TASK_GRAPH", MCATaskGraphCreationModule, task_graph, object, params)
            if None != task_graph:
                rc = system.run_service("SUBMIT", "TASK_GRAPH", task_graph)
        
        if rc != DYNRM_MCA_SUCCESS:
            v_print("Task Graph submission falied: "+str(rc), 3, self.verbosity)
            return rc

        return system.run_service("EXECUTE", "IN_LOOP", self.apply_policy, system_name)
    
    def add_policy(self, name, policy, params = dict()):
        policy_comp = self.get_component(MCAPolicyComponent)
        p = policy(parent = policy_comp, enable_output = policy_comp.enable_output, verbosity=policy_comp.verbosity)
        p.run_service("ADD", "PARAMS", params)
        return self.run_component_service(MCAPolicyComponent, "ADD", "POLICY", name, p)

    def set_active_policy(self, name):
        return self.run_component_service(MCAPolicyComponent, "SET", "ACTIVE_POLICY", name)


    def register_topo_module(self, module_class, *args, **kwargs):
        module = module_class(*args, **kwargs)
        comp = self.get_component(MCATopologyCreationComponent)
        comp.register_module(module)
        return DYNRM_MCA_SUCCESS

    def register_task_module(self, module_class, *args, **kwargs):
        module = module_class(*args, **kwargs)
        comp = self.get_component(MCATaskGraphCreationComponent)
        comp.register_module(module)
        return DYNRM_MCA_SUCCESS

    def register_submission_module(self, module_class, *args, **kwargs):
        module = module_class(*args, **kwargs)
        comp = self.get_component(MCASubmissionComponent)
        comp.run_service("REGISTER", "SUBMISSION_MODULE", module)
        return DYNRM_MCA_SUCCESS

    def add_system(self, name, system_module, topo_creation_module, topology_file):
        sys_comp = self.get_component(MCASystemComponent)
        system = system_module(parent = sys_comp, enable_output = sys_comp.enable_output, verbosity=sys_comp.verbosity)
        system.run_service("SET", "NAME", name)
        topo_graph = MCATopologyGraphModule(name+"_topology_graph")
        topo_graph.run_service("SET", "GID", system.run_service("GET", "NEW_GID"))

        comp = self.get_component(MCATopologyCreationComponent)
        if topo_creation_module not in [m.__class__ for m in comp.get_modules()]:
            comp.register_module(topo_creation_module())
        v_print("Creating topology graph from "+topology_file, 3, self.verbosity)
        topo_graph = self.run_component_service(MCATopologyCreationComponent, "CREATE", "TOPOLOGY_GRAPH", topo_creation_module, topo_graph, topology_file, dict())
        v_print("Created topology graph from "+topology_file, 3, self.verbosity)
        system.run_service("SET", "TOPOLOGY_GRAPH", topo_graph)
        rc = self.run_component_service(MCASystemComponent, "ADD", "SYSTEM", name, system)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        
        # Make a connection so we get notified of system events
        return self.run_component_service(MCACallbackComponent, "REQUEST", "CONNECTION", MCACallbackModule, name, self, system, dict())


    def get_system(self, name):
        return self.run_component_service(MCASystemComponent, "GET", "SYSTEM", name)

    def submit_object(self, system_name, module_class, object, params):
        system = self.run_component_service(MCASystemComponent, "GET", "SYSTEM", system_name)
        if None == system:
            return DYNRM_MCA_ERR_NOT_FOUND
        if None == params:
            params = dict()
        params["system_name"] = system_name
        return self.run_component_service(MCASubmissionComponent, "SUBMIT", "OBJECT", module_class, MCASubmissionComponent.LOOPBACK, object, params)
        

    def submit_mix(self, system_name, module_class, mix, params):
        system = self.run_component_service(MCASystemComponent, "GET", "SYSTEM", system_name)
        if None == system:
            return DYNRM_MCA_ERR_NOT_FOUND
        if None == params:
            params = dict()
        params["system_name"] = system_name
        params["system"] = system
        return self.run_component_service(MCASubmissionComponent, "SUBMIT", "MIX", module_class, MCASubmissionComponent.LOOPBACK, mix, params)
    
    def _executor(self, func):
        print(func)

        self._instance_lock.acquire()
        self._delayed_tasks -= 1
        self._instance_lock.release()
        return func()