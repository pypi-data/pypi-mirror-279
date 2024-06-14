from dyn_rm.mca.mca import MCAComponent

class MCAResourceManagerComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.systems = dict()
        MCAResourceManagerComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("REQUEST", "SETOP", self.request_setop)
        self.register_service("REGISTER_CALLBACK", "SETOP", self.register_callback_setop)
    
    def request_setop(self, module, setop):
        return self.run_module_service(module, "REQUEST", "SETOP", setop)

    def register_callback_setop(self, module, callback):
        return self.run_module_service(module, "REGISTER_CALLBACK", "SETOP", callback)
