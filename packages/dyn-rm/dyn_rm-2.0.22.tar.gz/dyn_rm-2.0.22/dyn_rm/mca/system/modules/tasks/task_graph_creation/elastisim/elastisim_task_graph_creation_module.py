from dyn_rm.mca.base.system.module.tasks.task_graph_creation import MCATaskGraphCreationModule
from dyn_rm.util.constants import *

from abc import abstractmethod
import imp


class ElastiSimTaskGraphCreationModule(MCATaskGraphCreationModule):

    # Creates a Task Graph and from a submitted object, e.g. a job batch script or dict
    def create_task_graph_function(self, graph, object, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED

        # Create a Task object for this job
        # Param 1: Task Name, Param 2: Path to executable
        # ElastiSim doesn't need an executable but if we want to compare it to real
        # execution we would need to add an exetuable e.g. in the job attribute field of ElastiSim job
        
        #task1 = MCATaskModule("task1", join(dirname(dirname(__file__)), "build", "bench_sleep"))

        # Set the exectution parameters for the executable (a list of arguments passed to main)
        # Again, elastiSim doesn't need it but for comparsison we would assume they were given in the job attributes 
        #task1.run_service("SET", "TASK_EXECUTION_ARGUMENTS", ["--output", "/opt/hpc/build/dyn_rm/examples/output/expand_dynrm_nb.csv", "--rm", "dyn_rm", "--mode", "expand", "--blocking", "0", "--proc_limit", "32", "--step_size", "8", "--iterations", "10", "--base_duration", "5", "--generator_key", "replace_generator"])
        
        # Set parameters for the initial launch
        # Here, t_s and t_p are the parameters for the scalability (derived from swf)
        
        #task1.run_service("SET", "TASK_LAUNCH_OUTPUT_SPACE_GENERATOR", 
        #              partial(output_space_generator_launch, 
        #                      task=task1, 
        #                      model=AmdahlPsetModel, 
        #                      model_params={'t_s': 1, 't_p' : 300}))
    
        # Set the parameters for reconfiguration
        # This attribute can later be looked up to create a set operation with the given performance model
        # Use the same t_s abd t_p as above

        # task1.run_service("SET", "ATTRIBUTE", "replace_generator", 
        #                partial(output_space_generator_replace,
        #                       model=AmdahlPsetModel, 
        #                       model_params={'t_s': 1, 't_p' : 300}))

        # Finally add the task to the task graph
        # task_graph.run_service("ADD", "TASKS", [task1])
            
    def update_task_graph_function(self, mix, system, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    def create_object_from_graph_function(self, graph, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    

