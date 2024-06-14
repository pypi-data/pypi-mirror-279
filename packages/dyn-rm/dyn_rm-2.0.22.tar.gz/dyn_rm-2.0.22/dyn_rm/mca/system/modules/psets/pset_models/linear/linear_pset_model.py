from dyn_rm.mca.base.system.module.psets.pset_model import MCAPSetModelModule

class LinearPSetModel(MCAPSetModelModule):

    def initialize_params(self):
        self.params['a'] = 1
        self.params['b'] = 0

    def eval_model_params_function(self):
        pass

    def eval_vertex_function(self, vertex, metrics):
        output = dict()
        size = vertex.run_service("GET", "NUM_PROCS")
        for metric in metrics:
                if metric == "SPEEDUP":
                    output[metric] = self.params['a']*size + self.params['b']
                else:
                    output[metric] = None
        return output    
    
    def eval_vertex_gradient_function(self, vertex, metrics):
        output = dict()
        for metric in metrics:
                if metric == "SPEEDUP":
                    output[metric] = self.params['a']
                else:
                    output[metric] = None
        return output   