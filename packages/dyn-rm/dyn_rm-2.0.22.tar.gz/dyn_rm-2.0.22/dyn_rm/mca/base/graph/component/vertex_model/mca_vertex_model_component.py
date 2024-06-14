from dyn_rm.mca.mca import MCAComponent
from dyn_rm.util.constants import *

class MCAVertexModelComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self._models = dict()
        self._active_model = None
        MCAVertexModelComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("ADD", "MODEL", self.add_model)
        self.register_service("SET", "ACTIVE_MODEL", self.set_active_model)
        self.register_service("GET", "ACTIVE_MODEL", self.get_active_model)
        self.register_service("GET", "MODEL", self.get_model)
        self.register_service("GET", "MODEL_NAMES", self.get_model_names)
        self.register_service("REMOVE", "MODEL", self.remove_model)

    def add_model(self, model_name, model):
        self._models[model_name] = model
        if None == self._active_model:
            self._active_model = model
        return DYNRM_MCA_SUCCESS
    def set_active_model(self, model_name):
        model = self._models.get(model_name)
        if None == model:
            return DYNRM_MCA_ERR_NOT_FOUND
        self._active_model = model
        return DYNRM_MCA_SUCCESS
    def get_active_model(self):
        return self._active_model
    def get_model(self, model_name):
        return self._models.get(model_name)
    def get_model_names(self):
        return list(self._models.keys())
    def remove_model(self, model_name):
        if model_name == self._active_model.run_service("GET", "GID"):
            self._active_model = None
        return self._models.pop(model_name)