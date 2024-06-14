from dyn_rm.mca.mca import MCAModule

from dyn_rm.util.constants import *

from abc import abstractmethod
import numpy as np

class MCAEdgeModelModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        
        self.params = dict()
        self.monitoring_data = []

        self.output_space_generator = None

        ##### MODEL PARAMS #####
        self.register_service("GET", "MODEL_PARAMS", self.get_model_params)
        self.register_service("SET", "MODEL_PARAMS", self.set_model_params)
        self.register_service("GET", "MODEL_PARAM", self.get_model_param)
        self.register_service("SET", "MODEL_PARAM", self.set_model_param)

        ##### MONITORING #####
        self.register_service("GET", "MONITORING_DATA", self.get_monitoring_data)
        self.register_service("SET", "MONITORING_DATA", self.set_monitoring_data)
        self.register_service("ADD", "MONITORING_ENTRY", self.add_monitoring_entry)
        self.register_service("GET", "MONITORING_ENTRY", self.get_monitoring_entry)
        self.register_service("REMOVE", "MONITORING_ENTRY", self.remove_monitoring_entry)

        ##### SPACE GENERATOR ######
        self.register_service("SET", "OUTPUT_SPACE_GENERATOR", self.set_output_generator)
        self.register_service("GENERATE", "OUTPUT_SPACE", self.generate_output_space) 
        self.register_service("COLLAPS", "OUTPUT_SPACE", self.collaps_output_space) 

        ##### COL ####
        self.register_service("ADD", "COL_DATA", self.add_col_data)

        ##### EVALUATIONS #####
        self.register_service("EVAL", "MODEL_PARAMS", self.eval_model_params)
        self.register_service("EVAL", "INPUT", self.eval_input)
        self.register_service("EVAL", "OUTPUT", self.eval_output)
        self.register_service("EVAL", "EDGE", self.eval_edge)
    

    ##### MODEL PARAMS #####
    def get_model_param(self, key):
        return self.params.get(key)
    def set_model_param(self, key, val):
        self.params[key] = val
        return DYNRM_MCA_SUCCESS
    def get_model_params(self) -> dict:
        return self.params
    def set_model_params(self, model_params: dict):
        for key in model_params.keys():
            self.params[key] = model_params[key]
        return DYNRM_MCA_SUCCESS

    ##### MONITORING #####
    def set_monitoring_data(self, data: dict):
        self.monitoring_data = data
        return DYNRM_MCA_SUCCESS
    def get_monitoring_data(self) -> dict():
        return self.monitoring_data

    def add_monitoring_entry(self, entry_name, data: dict):
        self.monitoring_data[entry_name] = data
        return DYNRM_MCA_SUCCESS
    def get_monitoring_entry(self, entry_name):
        return self.monitoring_data.get(entry_name)
    def remove_monitoring_entry(self, entry_name):
        self.monitoring_data.pop(entry_name, None)
        return DYNRM_MCA_SUCCESS

    ##### INPUT / OUTPUT #####
    def set_input(self, input : list):
        self.input = input
        return DYNRM_MCA_SUCCESS
    def set_output(self, output : list): 
        self.output = output
        return DYNRM_MCA_SUCCESS

    ##### MODELS #####
   
    def get_input_model(self, index):
        if index > len(self.input) - 1:
            return DYNRM_ERR_BAD_PARAM
        return self.input[index]
    def get_output_model(self, index):
        if index > len(self.output) - 1:
            return DYNRM_ERR_BAD_PARAM
        return self.output[index]
    def get_input_models(self):
        return self.input
    def get_output_models(self):
        return self.output
    
    def set_input_model(self, index, input_model):
        if index > len(self.input) - 1:
            return DYNRM_ERR_BAD_PARAM
        self.input_models.insert(index, input_model)
                
    def set_output_model(self, index, output_model):
        if index > len(self.output) - 1:
            return DYNRM_ERR_BAD_PARAM
        self.input_models.insert(index, output_model)
    def set_input_models(self, input_models):
        self.input_models = input_models
    def set_output_models(self, output_models):
        self.output_models = output_models


    ##### COL ######
    # Process all general data, but pass the rest down to the specific model
    def add_col_data(self, col):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED

    ##### SPACE GENERATOR ######
    def set_output_generator(self, generator):
        self.output_space_generator = generator
        return DYNRM_MCA_SUCCESS

    # Call the provided output_generator and validate the result 
    def generate_output_space(self, setop, input, graphs, *args, **kwargs):
        if self.output_space_generator == None:
            return [], []
        output_lists, adapted_objects_lists  = self.output_space_generator(setop, input, graphs, *args, **kwargs)
        
        # validate the output space
        if not self.validate_output_space_function(output_lists, adapted_objects_lists, dict()):
            return [], []
        
        return output_lists, adapted_objects_lists

    # Collapses an output space based on the edge model with a given input, norm, seletor and wheights
    def collaps_output_space(self, input, output_lists, metrics, norm=np.mean, selector=max, weights=None):
        
        if(0 == len(output_lists)):
            return []

        # First eval the edge model for the given metrics for all given output lists
        # This is a list of dicts 
        performances = [self.eval_edge(input, output, metrics) for output in output_lists]
        # Filter out any metrics where we did not get a performance result (i.e. None)
        weighted_performances = [dict() for _ in performances]
        for index in range(len(performances)):
            for key in performances[index].keys():
                if performances[index][key] != None:
                    weighted_performances[index][key] = performances[index][key]

        if None != weights:
            for perf in weighted_performances:
                for key in perf.keys():
                    if key not in weights:
                        continue
                    perf[key] *= weights[key]

        # normalize
        normalized_perf = [norm(list(perf.values())) for perf in weighted_performances]
        
        # select
        selected_index = normalized_perf.index(selector(normalized_perf))
        
        return output_lists[selected_index]


    ##### EVAL #####
    def eval_model_params(self):
        return self.eval_model_params_function()
    
    def eval_input(self, input, metrics):
        return self.eval_input_function(input, metrics)
    
    def eval_output(self, output, metrics):
        return self.eval_output_function(output, metrics)
    
    def eval_edge(self, input, output, metrics):
        return self.eval_edge_function(input, output, metrics)
    

    ##### MODULE IMPLEMENTATION #####
    
    # give the module a change to set default parameters for the model
    @abstractmethod
    def initialize_params(self):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    # (re-)evaluate the model paramters based on monitoring data
    @abstractmethod
    def eval_model_params_function(self):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    # evaluate the input of the edge (e.g. for transition edges)
    @abstractmethod
    def eval_input_function(self, input, metrics):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    # evaluate the output of the edge (e.g. for transition edges)
    @abstractmethod
    def eval_output_function(self, output, metrics):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    # evaluate the edge (e.g. gain, costs, etc.)
    @abstractmethod
    def eval_edge_function(self, input, output, metrics):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    # give the model implementation the chance to validate the generated output space
    @abstractmethod
    def validate_output_space_function(self, output_lists, adapted_objects_lists, params):
        return True
    



    class MissingInputParameterException(Exception):
        def __init__(self, module, parameter, description):
            message = "Evaluation of Model '"+module.__class__.mca_get_name()+"' requires input parameter '"+parameter+"' ("+description+")"
            super().__init__(message)

    class MissingModelParameterException(Exception):
        def __init__(self, module, parameter, description):
            message = "Evaluation of Model '"+module.__class__.mca_get_name()+"' requires model parameter '"+parameter+"' ("+description+")"
            super().__init__(message)