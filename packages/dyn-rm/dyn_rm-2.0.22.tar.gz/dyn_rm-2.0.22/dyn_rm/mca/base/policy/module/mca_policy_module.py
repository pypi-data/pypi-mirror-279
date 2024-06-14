from dyn_rm.mca.mca import MCAModule,MCAClass
from dyn_rm.mca.base.logger.component import MCALoggerComponent
from dyn_rm.mca.base.policy.module.logging import MCAPolicyLogger


from abc import abstractmethod

class MCAPolicyModule(MCAModule, MCAClass):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        
        self.params = dict()

        if None != parent:
            parent.register_module(self)

        logger_comp = MCALoggerComponent(parent = self, verbosity=verbosity, enable_output=enable_output)
        self.register_component(logger_comp)
        logger_comp.register_module(MCAPolicyLogger(parent = logger_comp, enable_output=enable_output))

        self.register_service("ADD", "PARAMS", self.add_params)
        self.register_service("SET", "PARAMS", self.set_params)
        self.register_service("GET", "PARAMS", self.get_params)
        self.register_service("EVAL", "POLICY", self.eval_policy)

    def set_params(self, params: dict):
        self.params = params

    def add_params(self, params: dict):
        self.params.update(params)   

    def get_params(self) -> dict:
        return self.params
    
    def eval_policy(self, system):
        if self.enable_output:
            self.run_component_service(MCALoggerComponent, "LOG", "EVENT", MCAPolicyLogger, 
                           "POLICY_EVALUATION_START", None)
            result = self.eval_policy_function(system)
            self.run_component_service(MCALoggerComponent, "LOG", "EVENT", MCAPolicyLogger, 
                                       "POLICY_EVALUATED", result)
            return result

        return self.eval_policy_function(system)

    # abstract methods
    @abstractmethod
    def eval_policy_function(self, input):
        pass