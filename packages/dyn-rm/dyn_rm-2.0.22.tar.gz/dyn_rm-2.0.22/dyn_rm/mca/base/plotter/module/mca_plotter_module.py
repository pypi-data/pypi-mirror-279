from dyn_rm.mca.mca import MCAModule
from dyn_rm.util.functions import v_print

from abc import abstractmethod

import os
import csv

class MCAPlotterModule(MCAModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = True, input_dir="."):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)

        self.input_dir = input_dir
        self.register_service("SET", "INPUT_MODULE", self.set_input_module)
        self.register_service("UNSET", "INPUT_MODULE", self.unset_input_module)
        self.register_service("PROCESS", "PRE", self.preprocess)
        self.register_service("PROCESS", "POST", self.postprocess)

        MCAPlotterModule.register_base_services(self)

    # User Interface
    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
    
    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def set_input_module(self, input_module):
        self.add_connection("INPUT", input_module, bidrectional=False)

    def unset_input_module(self):
        self.delete_connection("INPUT")
    
    def get_input_module(self):
        if not "INPUT" in self.connections:
            return None
        
        return self.connections["INPUT"]
    
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
    def register_base_services(self):
        v_print("Postprocessing Data of plotter '"+self.name+"'", 1, self.verbosity)
    @abstractmethod
    def postprocessing_function(self):
        v_print("Postprocessing Data of plotter '"+self.name+"'", 1, self.verbosity)   
    @abstractmethod
    def preprocessing_function(self):
        v_print("Preprocessing Data of plotter '"+self.name+"'", 1, self.verbosity)      

