from dyn_rm.mca.mca import MCAComponent

class MCAPlotterComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCAPlotterComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("SET", "INPUT_MODULE", self.set_input_module)
        self.register_service("PLOT", "MODULE_SERVICE", self.plot_module_service, make_dir=True)
        self.register_service("PLOT", "MODULE", self.plot_module, make_dir=True)
        self.register_service("PLOT", "ALL", self.plot_all, make_dir=True)
        self.register_service("PROCESS", "PRE", self.postprocess, make_dir=True)
        self.register_service("PROCESS", "POST", self.postprocess, make_dir=True)

    def set_input_module(self, module, input_module):
        return self.run_module_service(module, "SET", "INPUT_MODULE", input_module)
    def unset_input_module(self, module):
        return self.run_module_service(module, "UNSET", "INPUT_MODULE")
    def plot_module_service(self, module, service_name, params):
        return self.run_module_service(module, "PLOT", service_name, params)
    
    def plot_module(self, module,params):
        for service_name in self.children["MCA_MODULE"][module.class_name()].services["PLOT"].keys():
            self.run_module_service(module, "PLOT", service_name, params)

    def plot_all(self, params):
        for module in self.children["MCA_MODULE"].keys():
            for service_name in self.children["MCA_MODULE"][module.class_name()].services["PLOT"].keys():
                self.run_module_service(module, "PLOT", service_name, params)

    def preprocess(self, module, event, objects):
        return self.run_module_service(module, "PROCESS", "EVENTS", event, objects)
    def postprocess(self, module, event, objects):
        return self.run_module_service(module, "LOG", "EVENTS", event, objects)

