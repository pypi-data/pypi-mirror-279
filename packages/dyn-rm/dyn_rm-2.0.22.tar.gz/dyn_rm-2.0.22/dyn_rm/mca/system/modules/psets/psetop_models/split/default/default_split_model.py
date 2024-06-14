from dyn_rm.mca.base.system.module.psets.psetop_model import MCAPSetOpModelModule

import numpy as np

class DefaultSplitModel(MCAPSetOpModelModule):

    def initialize_params(self):
        pass

    def eval_model_params_function(self):
        pass

    def is_valid_transition(self, set_state):
        return True
    

    # TODO: Do more checks. Currently just checking the number of output PSets
    def validate_output_space_function(self, output_lists, adapted_objects, params):
        return True

    def eval_input_function(self, input, metrics):
        if len(input) < 1:
            output = dict()
            for metric in metrics:
                output[metric] = None
            return output
        model_names = input[0].run_service("GET", "VERTEX_MODEL_NAMES")
        if len(model_names) < 1:
            output = dict()
            for metric in metrics:
                output[metric] = None
            return output
        
        model = input[0].run_service("GET", "VERTEX_MODEL", model_names[0])
        return model.run_service("EVAL", "VERTEX", input[0], metrics)
    
    def eval_output_function(self, output, metrics):
        if len(output) < 1:
            output = dict()
            for metric in metrics:
                output[metric] = None
            return output
        model_names = output[0].run_service("GET", "VERTEX_MODEL_NAMES")
        if len(model_names) < 1:
            output = dict()
            for metric in metrics:
                output[metric] = None
            return output
        model = output[0].run_service("GET", "VERTEX_MODEL", model_names[0])
        return model.run_service("EVAL", "VERTEX", output[0], metrics)
    
    # For add, the gain is just the performance of the output PSet (as we add it)
    def eval_edge_function(self, input, output, metrics):
        input_res = self.eval_input_function(input, metrics)
        output_res = self.eval_output_function(output, metrics)
        output = dict()
        for metric in metrics:
            if input_res[metric] != None and output_res[metric] != None:
                output[metric] = output_res[metric] - input_res[metric]
            else:
                output[metric] = None
        return output


