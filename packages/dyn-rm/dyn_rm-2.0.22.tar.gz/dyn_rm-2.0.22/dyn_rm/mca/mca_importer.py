import importlib
import ast
import os

class MCA_Importer():

    def __init__(self):
        self.components = dict()
        self.modules = dict()

    def get_filenames_in_directory(self, directory_path):
        filenames = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return filenames

    def get_class_names(self, file_path):
        with open(file_path, 'r') as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        return class_names

    def import_classes(self, file_path):
        class_names = [x for x in self.get_class_names(file_path) if "Component" in x or "Module" in x]
        print(class_names)
        # Import classes dynamically
        imported_classes = {}
        for class_name in class_names:
            print(file_path)
            #module_name = f"{file_path[:-3]}_{class_name}"  # Assume the module name is based on the file name
            module_name = file_path.split("/")[-1][:-3]
            print(module_name)
            module = importlib.import_module("dyn_rm.mca.components."+module_name)
            imported_class = getattr(module, class_name)
            imported_classes[class_name] = imported_class

        return imported_classes

    def import_mca(self):
        # Example usage:
        components_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components")
    
        component_files = self.get_filenames_in_directory(components_path)
        for file in component_files:
            imported_classes = self.import_classes(os.path.join(components_path, file))

            # Now you can use the imported classes
            for class_name, imported_class in imported_classes.items():
                self.components[class_name] = imported_class
                print(f"Added an component {class_name}")
        
        print("**** Components: ****")
        print(self.components)
