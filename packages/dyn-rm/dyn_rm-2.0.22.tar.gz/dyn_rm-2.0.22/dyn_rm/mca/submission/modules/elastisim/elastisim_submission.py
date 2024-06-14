from dyn_rm.mca.base.submission.module import MCASubmissionModule
from dyn_rm.util.constants import *
from dyn_rm.util.functions import *

import os

class ElastiSimSubmissionModule(MCASubmissionModule):

    def __init__(self, parent=None, parent_dir=".", verbosity=0, enable_output=False):
        super().__init__(parent, parent_dir, verbosity, enable_output)

    # TODO: Add implementation
    #   The function reads an elastiSim job mix file and calls
    #   "RUN", "FUNC_NB_DELAYED" for each job object where delay is the arrival time of the job
    #   The job object will be the input to the task graph creation module 
    #   ==> See function below for reference 
    def submit_mix_function(self, mix, params):
        
        '''
        # If we use an ElastiSim System we need to start elastisim now
        if "system" in params:
            system = params["system"]
            if system.mca_get_name() == "ELASTI_SIM_SYSTEM":
                os.system("elastisim "+mix+" --log=root.thresh:warning")
                algorithm = system.run_service("GET", "ATTRIBUTE", "ELASTISIM_ALGORITHM")
                
                pass_algorithm(algorithm)
                return DYNRM_MCA_SUCCESS
        '''
            
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    '''    
    @abstractmethod
    def submit_mix_function(self, mix, params):
        with open(mix, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # Each row is one submission
                arrival, object, obj_params = row
                if obj_params == "":
                    obj_params = dict()
                else:
                    obj_params = eval(obj_params)
                obj_params.update(params)
                rc = self.run_component_service(MCAEventLoopComponent, "RUN", "FUNC_NB_DELAYED", "MIX_LOOP", int(arrival), None, None, self.submit_object, self._loopback_conn, object, obj_params)
                if rc != DYNRM_MCA_SUCCESS:
                    return rc
        return DYNRM_MCA_SUCCESS
    '''