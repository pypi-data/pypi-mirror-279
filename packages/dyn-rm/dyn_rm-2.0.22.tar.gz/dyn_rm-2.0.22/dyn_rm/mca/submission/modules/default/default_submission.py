from dyn_rm.mca.base.submission.module import MCASubmissionModule

from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
#from dyn_rm.mca.components.base.system.system import MCASystemComponent
#from dyn_rm.mca.components.base.set_model import MCASetModelComponent
#from dyn_rm.mca.components.base.setop_model import MCASetopModelComponent
from dyn_rm.mca.event_loop.modules.asyncio import AsyncioEventLoopModule
#from dyn_rm.mca.modules.setop_model.add.default import DefaultAddModel
#from dyn_rm.mca.modules.set_model import *


from dyn_rm.util.constants import *
from dyn_rm.util.functions import *


import asyncio
#import yaml

class DefaultSubmissionModule(MCASubmissionModule):

    def __init__(self, parent=None, parent_dir=".", verbosity=0, enable_output=False):
        super().__init__(parent, parent_dir, verbosity, enable_output)
