from dyn_rm.mca.mca import MCAComponent

class MCALoggerComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        MCALoggerComponent.register_base_services(self)
        
    def register_base_services(self):
        self.register_service("CREATE", "EVENT_OBJECT", self.create_event_object)
        self.register_service("LOG", "EVENT_OBJECT", self.log_event_object, make_dir=True)
        self.register_service("LOG", "EVENT_OBJECTS", self.log_event_objects, make_dir=True)
        self.register_service("LOG", "EVENT", self.log_event, make_dir=True)
        self.register_service("LOG", "EVENTS", self.log_events, make_dir=True)
        self.register_service("PROCESS", "PRE", self.postprocess, make_dir=True)
        self.register_service("PROCESS", "POST", self.postprocess, make_dir=True)

    def create_event_object(self, module, event, object):
        return self.run_module_service(module, "CREATE", "EVENT", event, object)
    def log_event_object(self, module, event_object):
        return self.run_module_service(module, "LOG", "EVENT_OBJECT", event_object)
    def log_event_objects(self, module, event_objects):
        return self.run_module_service(module, "LOG", "EVENT_OBJECTS", event_objects)
    def log_event(self, module, event, object):
        return self.run_module_service(module, "LOG", "EVENT", event, object)
    def log_events(self, module, event, objects):
        return self.run_module_service(module, "LOG", "EVENTS", event, objects)
    def preprocess(self, module):
        return self.run_module_service(module, "PROCESS", "PRE")
    def postprocess(self, module):
        return self.run_module_service(module, "PROCESS", "POST")

