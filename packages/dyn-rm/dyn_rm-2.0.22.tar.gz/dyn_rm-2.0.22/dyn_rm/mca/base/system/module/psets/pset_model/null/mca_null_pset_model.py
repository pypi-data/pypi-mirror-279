from dyn_rm.mca.base.system.module.psets.pset_model.mca_pset_model import MCAPSetModelModule

class MCANullPSetModel(MCAPSetModelModule):

    def initialize_params(self):
        pass

    def eval_model_params_function(self):
        pass

    def eval_vertex_function(self, vertex, metrics):
        output = dict()
        for metric in metrics:
            if metric == "SPEEDUP":
                output[metric] = 0
            else:
                output[metric] = None
        return output    
    
    def eval_vertex_gradient_function(self, vertex, metrics):
        output = dict()
        for metric in metrics:
            if metric == "SPEEDUP":
                output[metric] = 1
            else:
                output[metric] = None
        return output   