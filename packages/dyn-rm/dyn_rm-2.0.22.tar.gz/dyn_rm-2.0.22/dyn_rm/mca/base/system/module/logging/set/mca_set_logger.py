from dyn_rm.mca.base.logger.module import MCALoggerModule
import time

class MCASetLogger(MCALoggerModule):
    filename = "set.csv"

    def get_header(self) -> list:
        return ['timestamp', 'event', 'id', 'task_id', 'size', 'model', 'model_params']

    def create_event_function(self, ev, set):
        event = dict()
        event['timestamp'] = time.time()
        event['event'] = ev
        event['id'] = set.run_service("GET", "GID")
        event['task_id'] = set.run_service("GET", "TASK").run_service("GET", "GID")
        event['size'] = set.run_service("GET", "NUM_PROCS")
        model = set.run_service("GET", "PSET_MODEL", "USER_MODEL")
        event['model'] = str(model.mca_get_name()) if None != model else ''
        event['model_params'] = str(model.run_service("GET", "MODEL_PARAMS")) if None != model else ''

        return event
    
    def log_event_function(self, event: dict):
        row = [event['timestamp'], event['event'], event['id'], event['task_id'], event['size'], event['model'], event['model_params']]
        self.write_rows(self.get_filename(), [row])   

    def log_events_function(self, events: list):
        rows = []
        for event in events:
            row = [event['timestamp'], event['event'], event['id'], event['task_id'], event['size'], event['model'], event['model_params']]
            rows.append(row)
        self.write_rows(self.get_filename(), rows)         

    def postprocessing_function(self, params: dict):
        pass

    def preprocessing_function(self, params: dict):
        pass