from dyn_rm.mca.mca import MCAModule
from dyn_rm.util.functions import v_print

import os
import csv

from abc import abstractmethod

class MCALoggerModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.header_written = False
        self.register_service("CREATE", "EVENT_OBJECT", self.create_event_object)
        self.register_service("LOG", "EVENT_OBJECT", self.log_event_object)
        self.register_service("LOG", "EVENT_OBJECTS", self.log_event_objects)
        self.register_service("LOG", "EVENT", self.log_event)
        self.register_service("LOG", "EVENTS", self.log_events)
        self.register_service("PROCESS", "PRE", self.preprocess)
        self.register_service("PROCESS", "POST", self.postprocess)

    # User Interface
    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
    
    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def create_event_object(self, event, object):
        return self.create_event_function(event, object)
    
    def log_event_object(self, event: dict):
        return self.log_event_function(event)
    
    def log_event_objects(self, events: list):
        return self.log_events_function(events)
    
    def log_event(self, event, object):
        return self.log_event_function(self.create_event_function(event, object))
    
    def log_events(self, event, objects):
        return self.log_events_function([self.create_event_function(event, object) for object in objects])

    
    def postprocess(self):
        return self.postprocessing_function()
    
    def preprocess(self):
        return self.preprocessing_function()

    def write_header(self, filename):
        os.system("mkdir -p "+os.path.join(self.parent_dir, "output"))
        with open(os.path.join(self.parent_dir, "output", filename), 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.get_header())
        self.header_written = True
    
    # private functions
    def write_rows(self, filename, rows):
        if not self.header_written:
            self.write_header(self.get_filename())
        with open(os.path.join(self.parent_dir, "output", filename), 'a+') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in rows:
                writer.writerow(row)

    def read_rows(self, filename):
        with open(os.path.join(self.parent_dir, "output", filename), 'a+', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            return reader
    
    def get_filename(self):
        return self.filename
    
    # abstract methods
    @abstractmethod
    def get_header(self) -> list:
        pass

    @abstractmethod
    def create_event_function(self, event, object):
        pass

    @abstractmethod
    def log_event_function(self, event: dict):
        v_print("Logging event with Logger '"+self.name+"'", 1, self.verbosity)   

    @abstractmethod
    def log_events_function(self, events: list):
        v_print("Logging "+str(len(events))+"event with Logger '"+self.name+"'", 1, self.verbosity)   

    @abstractmethod
    def postprocessing_function(self):
        v_print("Postprocessing Data of Logger '"+self.name+"'", 1, self.verbosity)   
    
    @abstractmethod
    def preprocessing_function(self):
        v_print("Preprocessing Data of Logger '"+self.name+"'", 1, self.verbosity)       

