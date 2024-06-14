from dyn_rm.mca.base.system.module.psets.pset_model import MCAPSetModelModule
from dyn_rm.util.functions import v_print
from dyn_rm.util.constants import *

import numpy as np

class InverseAmdahlPsetModel(MCAPSetModelModule):

    def initialize_params(self):
        self.run_service("SET", "MODEL_PARAMS", {"t_s": 1, "t_p": 100})

    # L1 - Minimization
    def eval_model_params_function(self):
        if len(self.monitoring_data) < 2:
            v_print("Not enough monitoring data to infer model parameters", 1, self.verbosity)
            return

        A = [[data["p"], 1] for data in self.monitoring_data]
        b = [[data["p"] * data["iteration_time"]] for data in self.monitoring_data]

        x, *_ = np.linalg.lstsq(A, b, rcond=None)

        self.params["t_s"] = x[0][0]
        self.params["t_p"] = x[1][0]


    def eval_vertex_function(self, vertex, metrics):
        #if vertex.__class__ != MCAPSetModule:
        #    raise Exception("Provided vertex is not a PSet: "+str(vertex.__class__))
        size = vertex.run_service("GET", "NUM_PROCS")
        output = dict()
        for metric in metrics:
            if metric == "SPEEDUP":
                output[metric] = self.eval_state_speedup_function(size)
            elif metric == "RUNTIME":
                output[metric] = self.eval_state_runtime_function(size)
            else:
                output[metric] = None
        return output    
    
    def eval_vertex_gradient_function(self, vertex, metrics):
        #if vertex.__class__ != MCAPSetModule:
        #    raise Exception("Provided vertex is not a PSet")
        size = vertex.run_service("GET", "NUM_PROCS")

        output = dict()
        for metric in metrics:
            if metric == "SPEEDUP":
                output[metric] = self.eval_state_gradient_speedup_function(size)
            elif metric == "RUNTIME":
                output[metric] = - self.eval_state_gradient_speedup_function(size)
            else:
                output[metric] = None  
        return output


    def eval_state_speedup_function(self, num_procs) -> list:
        if num_procs == 0:
            return 0
        
        if "t_s" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_s", "Total time for serial parts")
        if "t_p" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_p", "Total time for parallel parts")
        return 1 / ((self.params["t_p"] + self.params["t_s"]) / (self.params["t_s"] + self.params["t_p"] / num_procs))

    def eval_state_runtime_function(self, num_procs):
        if num_procs == 0:
            return 2 * (self.params["t_s"] + self.params["t_p"])
        if "t_s" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_s", "Total time for serial parts")
        if "t_p" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_p", "Total time for parallel parts")

        return self.params["t_s"] + self.params["t_p"] / num_procs
    
    def eval_state_gradient_speedup_function(self, num_procs):
        if "t_s" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_s", "Total time for serial parts")
        if "t_p" not in self.params:
            raise MCAVertexModelModule.MissingModelParameterException(self, "t_p", "Total time for parallel parts")

        return 1 / ((self.params["t_p"]*(self.params["t_p"] + self.params["t_s"])) / \
                ((self.params["t_p"]/num_procs + self.params["t_s"])**2 * num_procs**2))
