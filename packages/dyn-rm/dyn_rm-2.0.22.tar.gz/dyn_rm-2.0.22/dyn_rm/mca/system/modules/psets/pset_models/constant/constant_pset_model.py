from dyn_rm.mca.base.system.module.psets.pset_model import MCAPSetModelModule

class ConstantPsetModel(MCAPSetModelModule):

    def initialize_params(self):
        self.params['speedup'] = 1

    def eval_model_params_function(self):
        pass

    def eval_vertex_function(self, vertex, metrics):
        output = dict()
        for metric in metrics:
                if metric == "SPEEDUP":
                    output[metric] = self.params['speedup']
                else:
                    output[metric] = None
        return output    
    
    def eval_vertex_gradient_function(self, vertex, metrics):
        output = dict()
        for metric in metrics:
                if metric == "SPEEDUP":
                    output[metric] = 0
                else:
                    output[metric] = None
        return output   