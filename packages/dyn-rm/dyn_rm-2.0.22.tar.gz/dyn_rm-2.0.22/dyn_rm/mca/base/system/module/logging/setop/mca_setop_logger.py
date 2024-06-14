from dyn_rm.mca.base.logger.module import MCALoggerModule
from dyn_rm.mca.base.system.module.psets.psetop import MCAPSetopModule
import time
import json

class MCASetOpLogger(MCALoggerModule):
    filename = "setop.csv"

    def get_header(self) -> list:
        return ['timestamp', 'event', 'id', 'alias', 'op', 'status', 'input', 'output', 'nodelist_in', 'nodelist_out', 'predecessors', 'successors']

    def create_event_function(self, ev, setop):
        event = dict()
        event['timestamp'] = time.time()
        event['event'] = ev
        event['id'] = setop.run_service("GET", "GID")
        event['alias'] = setop.run_service("GET", "ATTRIBUTE", "PSETOP_ALIAS")
        event['op'] = setop.run_service("GET", "PSETOP_OP")
        event['status'] = setop.run_service("GET", "PSETOP_STATUS")
        event['input'] = ";".join(i.run_service("GET", "GID") for i in setop.run_service("GET", "INPUT"))
        event['output'] = ";".join(o.run_service("GET", "GID") for o in setop.run_service("GET", "OUTPUT"))
        event['nodelist_in'] = ";".join(n.run_service("GET", "NAME") for n in setop.run_service("GET", "INPUT")[0].run_service("GET", "ACCESSED_NODES"))
        noutput = len(setop.run_service("GET", "OUTPUT"))
        if noutput == 0:
            event['nodelist_out'] = ''
        else:
            event['nodelist_out'] = ";".join(n.run_service("GET", "NAME") for n in setop.run_service("GET", "OUTPUT")[noutput-1].run_service("GET", "ACCESSED_NODES"))
        event['predecessors'] = ";".join([s.run_service("GET", "GID") for s in setop.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_PREDECESSORS)])
        event['successors'] = ";".join([s.run_service("GET", "GID") for s in setop.run_service("GET", "ATTRIBUTE", MCAPSetopModule.PSETOP_ATTRIBUTE_SUCCESSORS)])
        return event


    def log_event_function(self, event: dict):
        row = [event['timestamp'], event['event'], event['id'], event['alias'], event['op'], event['input'], event['output'], event['nodelist_in'], event['nodelist_out'], event['predecessors'], event['successors']]
        self.write_rows(self.get_filename(), [row])               

    def log_events_function(self, events: list):
        rows = []
        for event in events:
            row = [event['timestamp'], event['event'], event['id'], event['alias'], event['op'], event['input'], event['output'], event['nodelist_in'], event['nodelist_out'], event['predecessors'], event['successors']]
            rows.append(row)
        self.write_rows(self.get_filename(), rows)  

    def postprocessing_function(self, params: dict):
        pass

    def preprocessing_function(self, params: dict):
        pass