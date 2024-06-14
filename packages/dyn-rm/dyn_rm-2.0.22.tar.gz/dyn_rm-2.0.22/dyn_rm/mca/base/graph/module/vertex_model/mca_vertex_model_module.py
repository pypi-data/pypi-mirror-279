from dyn_rm.mca.mca import MCAModule

from abc import abstractmethod

class MCAVertexModelModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        
        self.params = dict()
        self.monitoring_data = []

        self.register_service("GET", "MODEL_PARAMS", self.get_model_params)
        self.register_service("GET", "MONITORING_DATA", self.add_monitoring_data)
        self.register_service("SET", "MODEL_PARAMS", self.set_model_params)
        self.register_service("ADD", "MONITORING_DATA", self.add_monitoring_data)
        
        self.register_service("EVAL", "MODEL_PARAMS", self.eval_model_params)
        self.register_service("EVAL", "VERTEX", self.eval_vertex)
        self.register_service("EVAL", "VERTEX_DELTA", self.eval_vertex_delta)
        self.register_service("EVAL", "VERTEX_GRADIENT", self.eval_vertex_gradient)

        self.initialize_params()

    def set_model_params(self, model_params: dict):
        for key in model_params.keys():
            self.params[key] = model_params[key]
    
    def get_model_params(self) -> dict:
        return self.params

    def add_monitoring_data(self, data: dict):
        self.monitoring_data.append(data)

    def get_monitoring_data(self) -> list:
        return self.monitoring_data

    def eval_model_params(self):
        return self.eval_model_params_function()
    
    def eval_vertex(self, vertex, metrics):
        return self.eval_vertex_function(vertex, metrics)

    def eval_vertex_delta(self, vertex1, vertex2, metrics):
        output1 = self.eval_vertex( vertex1, metrics)
        output2 = self.eval_vertex( vertex2, metrics)
        output = dict()
        for metric in metrics:
            output[metric] = None if output1[metric] == None or output2[metric] == None else \
            output2[metric] - output1[metric] 
        return output
    
    def eval_vertex_gradient(self, vertex, metrics):
        return self.eval_vertex_gradient_function(vertex, metrics)

    # abstract methods
    @abstractmethod
    def initialize_params(self):
        pass
    @abstractmethod
    def eval_model_params_function(self):
        pass
    @abstractmethod
    def eval_vertex_function(self, vertex, metric):
        pass
    @abstractmethod
    def eval_vertex_gradient_function(self, vertex, metric):
        pass


    class MissingInputParameterException(Exception):
        def __init__(self, module, parameter, description):
            message = "Evaluation of Model '"+module.mca_get_name()+"' requires input parameter '"+parameter+"' ("+description+")"
            super().__init__(message)

    class MissingModelParameterException(Exception):
        def __init__(self, module, parameter, description):
            message = "Evaluation of Model '"+module.mca_get_name()+"' requires model parameter '"+parameter+"' ("+description+")"
            super().__init__(message)