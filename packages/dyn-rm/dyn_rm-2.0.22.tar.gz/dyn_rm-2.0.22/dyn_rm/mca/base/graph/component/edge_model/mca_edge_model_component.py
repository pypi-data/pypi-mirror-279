from dyn_rm.mca.mca import MCAComponent

from dyn_rm.util.constants import *

class MCAEdgeModelComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._models = dict()
        MCAEdgeModelComponent.register_base_services(self)

    def register_base_services(self):
        self.register_service("ADD", "MODEL", self.add_model)
        self.register_service("GET", "MODEL", self.get_model)
        self.register_service("GET", "MODEL_NAMES", self.get_model_names)
        self.register_service("REMOVE", "MODEL", self.remove_model)

    def add_model(self, model_name, model):
        self._models[model_name] = model
        return DYNRM_MCA_SUCCESS
    def get_model(self, model_name):
        return self._models.get(model_name)
    def get_model_names(self):
        return list(self._models.keys())
    def remove_model(self, model_name):
        return self._models.pop(model_name, None)