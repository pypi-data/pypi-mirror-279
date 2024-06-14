from dyn_rm.mca.mca import MCAComponent
from dyn_rm.mca.callback.modules import DefaultCallbackModule


from dyn_rm.util.constants import *
from dyn_rm.util.functions import v_print


class DefaultCallbackComponent(MCAComponent):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.register_module(DefaultCallbackModule())