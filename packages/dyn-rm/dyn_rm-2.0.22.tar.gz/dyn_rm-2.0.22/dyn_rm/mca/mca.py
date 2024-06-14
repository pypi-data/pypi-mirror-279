import os
from abc import ABC, abstractmethod

from dyn_rm.util.functions import v_print
from dyn_rm.util.constants import *

DYNRM_OUTPUT_MODE_FORBIDDEN = 0
DYNRM_OUTPUT_MODE_OPTIONAL = 1
DYNRM_OUPUT_MODE_REQUIRED = 2

DYNRM_SUCCESS = 0
DYNRM_ERR_UNKNOWN = 1
DYNRM_ERR_BAD_PARAM = 2
DYNRM_ERR_CHILD_NOT_FOUND = 3
DYNRM_ERR_CHILD_NOT_FOUND = 4
DYNRM_ERR_CONNECTION_NOT_FOUND = 5
DYNRM_ERR_SERVICE_NOT_FOUND = 6
DYNRM_ERR_INCONSISTENT_OUPUT = 7
DYNRM_ERR_NO_SUCH_FILE_OR_DIR = 8


class MCA:
    mca_name = None
    output_mode = DYNRM_OUTPUT_MODE_OPTIONAL

    @classmethod
    def mca_get_name(cls):
        return cls.mca_name

    def __new__(cls, *args, **kwargs):
        
        input_string = cls.__name__
        
        if input_string.startswith("MCA"):
            result = "MCA_"
            index = 3
        else:
            result = input_string[0].upper()
            index = 1
        prev_was_upper = True    
        for char in input_string[index:]:
            if char.isupper():
                if not prev_was_upper:
                    result+='_'
                    result += char
                else:
                    prev_was_upper = True
                    result+= char
            else:
                result += char.upper()
                prev_was_upper = False
            
        if result != cls.mca_name:
            cls.mca_name = result
        return super().__new__(cls)



    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):    
        
        self.parent = None
        self.children = dict()
        self.connections = dict()
        self.services = dict()
        self.active_class = None
        self.active_service = None



        self.parent = parent
        if parent != None:
            self.parent_dir = parent.run_service("MCA_GET", "CHILD_DIR")
        else:
            if parent_dir != None:
                self.parent_dir = parent_dir
            else: 
                self.parent_dir = "."
        self.enable_output = enable_output
        self.verbosity = verbosity

        if enable_output and self.output_mode == DYNRM_OUTPUT_MODE_FORBIDDEN:
            raise Exception("This mca object does not allow output!")

        self.output_enabled = enable_output

        self.child_base_dir = parent_dir

        self._register_mca_base_services()


    @abstractmethod
    def register_base_services(self):
        pass


    def _register_mca_base_services(self):
        self.register_service("MCA_GET", "NAME", self.__class__.mca_get_name)
        self.register_service("MCA_GET", "PARENT", self.get_parent)
        self.register_service("MCA_GET", "PARENT_DIR", self.get_parent_dir)
        self.register_service("MCA_GET", "CHILD_DIR", self.get_child_dir)
        self.register_service("MCA_GET", "CHILD", self.get_child)
        self.register_service("MCA", "SHUTDOWN", self.mca_shutdown)

    @abstractmethod
    def get_base_dir_name():
        return "mca"

    def mca_default_shutdown(self):
        if MCAClass in self.__class__.mro():
            for component in self.get_components():
                rc = component.run_service("MCA", "SHUTDOWN")
                if rc != DYNRM_MCA_SUCCESS:
                    return rc
        if MCAComponent in self.__class__.mro():
            for module in self.get_modules():
                rc = module.run_service("MCA", "SHUTDOWN")
                if rc != DYNRM_MCA_SUCCESS:
                    return rc
        return DYNRM_MCA_SUCCESS
    
    @abstractmethod
    def mca_shutdown(self):
        return self.mca_default_shutdown()
    
    def set_output_enabled(self, value):
        self.output_enabled = value

    def get_output_enabled(self):
        return self.output_enabled
    
    def set_verbosity(self, verbosity):
        self.verbosity = verbosity
    
    # parent
    def get_parent(self):
        return self.parent
    def get_parent_dir(self):
        return self.parent_dir

    def set_parent(self, parent):
        self.parent = parent

    def set_child_base_dir(self, dir):
        self.child_base_dir = dir
    def get_child_base_dir(self):
        return self.child_base_dir

    # Children
    def register_child(self, child_class, child_name, child):
        
        child_base_dir = os.path.join(self.child_base_dir,
                                "children",
                                child_class,
                                child_name)
        # Prepare Output
        if child.output_enabled:
            if not self.output_enabled:
                if child.output_mode == DYNRM_OUPUT_MODE_REQUIRED:
                    raise Exception("Child required output but parent output is diabled")
                else:
                    v_print("Child requested optional output but parent output is disabled", 1, self.verbosity)
            else:
                os.system("mkdir -p " + child_base_dir)

        child.set_parent_dir(child_base_dir)
        child.set_parent(self)
        child.set_child_base_dir(child_base_dir)

        child.set_verbosity(self.verbosity)

        if child_class not in self.children:
            self.children[child_class] = {child_name: child}
        else: 
            self.children[child_class][child_name] = child

    def get_child(self, class_name, name):
        if not class_name in self.children:
            return None
        if not name in self.children[class_name]:
            return None
        return self.children[class_name][name]
    
    def get_child_by_path(self, path):

        if len(path) == 0:
            return self
        
        if len(path) > 2:
            return self.children[path[0]][path[1]].get_child(path[2:])       
        return self.children[path[0]][path[1]]

    def set_active_class(self, cls):
        if cls.mca_get_name() not in self.children["MCA_CLASS"]:
            v_print("No class '"+cls.mca_get_name()+"' registered", 1, self.verbosity)
            return
        self.active_class = self.children["MCA_CLASS"][cls.mca_get_name()]

    def set_active_service(self, service_class, service_name):
        if service_class not in self.services:
            v_print("No service_class '"+service_class+"' registered", 1, self.verbosity)
            return
        if service_name not in self.services[service_class]:
            v_print("No service '"+service_name+"' registered in service_class "+service_class, 1, self.verbosity)
            return
        self.active_service = self.services[service_class][service_name]

    def get_active_class(self):
        return self.active_class
    def get_active_service(self, service_class):
        return self.active_service
    
    # Services
    def register_service(self, class_name, name, service, make_dir = False, active = False):

        # create a dir for the service if required
        #if make_dir:
        #    # if our output is disabled we cannot register this service 
        #    if not self.output_enabled:
        #        return "PARENT_OUTPUT_DISABLED"
        #    
        #    service_base_dir = os.path.join(self.parent_dir, 
        #                "..",
        #                "services",
        #                class_name,
        #                name)
        #    os.system("mkdir -p " + service_base_dir)

        if class_name not in self.services:
            self.services[class_name] = {name: service}
        else: 
            self.services[class_name][name] = service
        
        if active:
            self.active_service = service
    
    def get_service(self, class_name, name):
        if not class_name in self.services:
            return None
        if not name in self.service_classes[class_name]:
            return None
        return self.service_classes[class_name][name]  

    def run_service(self, class_name, name, *args, **kwargs):
        if not class_name in self.services:
            print(type(self).__name__+": CANNOT RUN SERVICE: No service of type '"+class_name+"' registered")
            return None
        if not name in self.services[class_name]:
            print(type(self).__name__+": CANNOT RUN SERVICE: "+self.mca_get_name()+" has no service of name '"+name+"' registered")
            return None
        return self.services[class_name][name](*args, **kwargs)

    def run_service_by_path(self, path, service_class, service_name, *args, **kwargs):
        child = self.get_child_by_path(path)
        if None == child:
            return
        return child.run_service(service_class, service_name, *args, **kwargs)

    def run_service_c_m_s(self, component, module, service_class, service_name, *args, **kwargs):
        if "MCA_COMPONENT" not in self.children:
            print("CANNOT RUN SERVICE: No components registered")
            return None
        if component.mca_get_name() not in self.children["MCA_COMPONENT"]:
            print("CANNOT RUN SERVICE: No component with name '"+component.mca_get_name()+"' registered")
            return None            
        return self.children["MCA_COMPONENT"][component.mca_get_name()].run_module_service(module.mca_get_name(), service_class, service_name, *args, **kwargs)

    def run_service_m_s(self, module, service_class, service_name, *args, **kwargs):
        if "MCA_MODULE" not in self.children:
            print("CANNOT RUN SERVICE: No components registered")
            return None
        if module.mca_get_name() not in self.children["MCA_MODULE"]:
            print("CANNOT RUN SERVICE: No module with name '"+module.mca_get_name()+"' registered")
            return None            
        return self.children["MCA_MODULE"][module.mca_get_name()].run_service_s(service_class, service_name, *args, **kwargs)

    def run_service_s(self, service_class, service_name, *args, **kwargs):
        if service_class not in self.services:
            print("CANNOT RUN SERVICE: Service class not registered")
            return None
        if service_name not in self.services[service_class]:
            print("CANNOT RUN SERVICE: No service with name '"+service_name+"' registered")
            return None            
        return self.children[service_class][service_name](*args, **kwargs)

    def run_service_ca_ma_sa(self, *args, **kwargs):
        if None == self.active_component:
            print("CANNOT RUN SERVICE: No active component")
            return None
                   
        return self.active_component.run_service_ma_sa(*args, **kwargs)

    def run_service_ma_sa(self, *args, **kwargs):
        if None == self.active_module:
            print("CANNOT RUN SERVICE: No active component")
            return None
                               
        return self.active_module.run_service_sa(*args, **kwargs)

    def run_service_sa(self, *args, **kwargs):
        if None == self.active_service:
            print("CANNOT RUN SERVICE: No active service")
            return None
          
        return self.active_service(*args, **kwargs)

    def run_service_ca_ma_s(self, service_class, service_name, *args, **kwargs):
        if None == self.active_component:
            print("CANNOT RUN SERVICE: No active component")
            return None
                   
        return self.active_component.run_service_ma_s(service_class, service_name, *args, **kwargs)

    def run_service_ca_m_s(self, module, service_class, service_name, *args, **kwargs):
        if None == self.active_component:
            print("CANNOT RUN SERVICE: No active component")
            return None
                   
        return self.active_component.run_service_m_s(module.mca_get_name(), service_class, service_name, *args, **kwargs)

    def run_service_c_ma_s(self, component, service_class, service_name, *args, **kwargs):
        if "MCA_COMPONENT" not in self.children:
            print("CANNOT RUN SERVICE: No components registered")
            return None
        if component.mca_get_name() not in self.children["MCA_COMPONENT"]:
            print("CANNOT RUN SERVICE: No component with name '"+component.mca_get_name()+"' registered")
            return None
                    
        return self.children["MCA_COMPONENT"][component.mca_get_name()].run_service_ma_s(service_class, service_name, *args, **kwargs)

    def run_service_ma_s(self, service_class, service_name, *args, **kwargs):
        if None == self.active_module:
            print("CANNOT RUN SERVICE: No active component")
            return None
                               
        return self.active_module.run_service_s(service_class, service_name, *args, **kwargs)
 
    def run_service_c_ma_sa(self, component, *args, **kwargs):
        if "MCA_COMPONENT" not in self.children:
            print("CANNOT RUN SERVICE: No components registered")
            return None
        if component.mca_get_name() not in self.children["MCA_COMPONENT"]:
            print("CANNOT RUN SERVICE: No component with name '"+component.mca_get_name()+"' registered")
            return None
                    
        return self.children["MCA_COMPONENT"][component.mca_get_name()].run_service_ma_sa(*args, **kwargs)

    def run_service_ca_m_sa(self, module, *args, **kwargs):
        if None == self.active_component:
            print("CANNOT RUN SERVICE: No active component")
            return None            
                    
        return self.active_component.run_service_m_sa(module.mca_get_name(), *args, **kwargs)

    def run_service_c_m_sa(self, component, module, *args, **kwargs):
        if "MCA_COMPONENT" not in self.children:
            print("CANNOT RUN SERVICE: No components registered")
            return None
        if component.mca_get_name() not in self.children["MCA_COMPONENT"]:
            print("CANNOT RUN SERVICE: No component with name '"+component.mca_get_name()+"' registered")
            return None
                    
        return self.children["MCA_COMPONENT"][component.mca_get_name()].run_service_m_sa(module.mca_get_name(), *args, **kwargs)

    def run_service_m_sa(self, module, *args, **kwargs):
        if "MCA_MODULE" not in self.children:
            print("CANNOT RUN SERVICE: No module registered")
            return None
        if module.mca_get_name() not in self.children["MCA_MODULE"]:
            print("CANNOT RUN SERVICE: No module with name '"+module.mca_get_name()+"' registered")
            return None
                    
        return self.children["MCA_MODULE"][module.mca_get_name()].run_service_m_sa(module.mca_get_name(), *args, **kwargs)


    # connections
    def add_connection(self, connection_name, obj, bidrectional=False):
        self.connections[connection_name] = obj
        
        if bidrectional:
            obj.add_connection(connection_name, self, bidrectional)

    def add_connection_by_path(self, connection_name, path1, path2, bidirectional = False):
        child1 = self.get_child(path1)

        if None == child1:
            return "CHILD_NOT_FOUND"
        
        child2 = self.get_child(path2)

        if None == child2:
            return "CHILD_NOT_FOUND"
        
        child1.add_connection(connection_name, child2)

        if bidirectional:
            child2.add_connection(connection_name, child1)

    def delete_connection(self, connection_name):
        self.connections.pop(connection_name)

    def delete_connection_by_path(self, connection_name, path, bidirectional = False):
        child1 = self.get_child(path)

        if None == child1:
            return "CHILD_NOT_FOUND"
        
        peer = child1.get_connection(connection_name)
        
        child1.delete_connection(connection_name)

        if bidirectional and None != peer:
            peer.delete_connection(connection_name)

    def get_connection(self, connection_name):
        return self.connections[connection_name]

    # Paths
    def set_parent_dir(self, parent_dir):
        self.parent_dir = parent_dir
    
    def get_full_path(self):
        return os.path.join(self.parent_dir) 
    
    def get_child_dir(self):
        return os.path.join(self.get_full_path(), "children")

class MCAClass(MCA):
    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.active_component = None

    def get_component(self, component):
        if "MCA_COMPONENT" not in self.children:
            return None
        return self.children["MCA_COMPONENT"].get(component.mca_get_name())
    
    def get_components(self):
        if "MCA_COMPONENT" not in self.children:
            return []
        return list(self.children["MCA_COMPONENT"].values())

    def set_active_component(self, component):
        if component.mca_get_name() not in self.children["MCA_MODULE"]:
            v_print("No module '"+component.mca_get_name()+"' registered", 1, self.verbosity)
            return
        self.active_module = self.children["MCA_MODULE"][component.mca_get_name()]  

    def get_active_component(self):
        return self.active_component

    def register_component(self, component, acitive=False):
        self.register_child("MCA_COMPONENT", component.__class__.mca_get_name(), component)
        if acitive:
            self.active_component = component
        return DYNRM_MCA_SUCCESS
    
    def run_component_service(self, component, service_class, service_name, *args, **kwargs):
        if "MCA_COMPONENT" not in self.children:
            print("CANNOT RUN COMPONENT SERVICE: No components registered")
            return None
        if component.mca_get_name() not in self.children["MCA_COMPONENT"]:
            print("CANNOT RUN COMPONENT SERVICE: No component with name '"+component.mca_get_name()+"' registered")
            return None            
        return self.children["MCA_COMPONENT"][component.mca_get_name()].run_service(service_class, service_name, *args, **kwargs)

    @abstractmethod
    def get_base_dir_name():
        return "mca_class"
    


class MCAComponent(MCA):
    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.active_module = None
   
    def get_module(self, module):
        if "MCA_MODULE" not in self.children:
            return None
        return self.children["MCA_MODULE"].get(module.mca_get_name())

    def set_active_module(self, module):
        if module.mca_get_name() not in self.children["MCA_MODULE"]:
            v_print("No module '"+module.mca_get_name()+"' registered", 1, self.verbosity)
            return
        self.active_module = self.children["MCA_MODULE"][module.mca_get_name()]  
    
    def get_modules(self):
        if "MCA_MODULE" not in self.children:
            return []
        return list(self.children["MCA_MODULE"].values())

    def get_active_module(self):
        return self.active_module

    def register_module(self, module, active = True):
        self.register_child("MCA_MODULE", module.__class__.mca_get_name(), module)
        if active:
            self.active_module = module
        return DYNRM_MCA_SUCCESS
    
    def run_module_service(self, module, service_class, service_name, *args, **kwargs):
        if "MCA_MODULE" not in self.children:
            print("CANNOT RUN MODULE SERVICE: No module registered. Requested: "+module.mca_get_name())
            return None
        if module.mca_get_name() not in self.children["MCA_MODULE"]:
            print("CANNOT RUN MODULE SERVICE: No module with name '"+module.mca_get_name()+"' registered")
            return None            
        return self.children["MCA_MODULE"][module.mca_get_name()].run_service(service_class, service_name, *args, **kwargs)


    @abstractmethod
    def get_base_dir_name():
        return "mca_class"
    
            

class MCAModule(MCA):
    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
            super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)

    @abstractmethod
    def get_base_dir_name():
        return "module"
    
