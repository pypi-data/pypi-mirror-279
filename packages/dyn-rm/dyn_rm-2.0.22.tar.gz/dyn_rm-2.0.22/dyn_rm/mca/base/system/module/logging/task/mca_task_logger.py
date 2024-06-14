from dyn_rm.mca.base.logger.module import MCALoggerModule
import time

class MCATaskLogger(MCALoggerModule):
    filename = "job.csv"

    def get_header(self) -> list:
        return ['timestamp', 'event', 'task_id', 'task_name', 'task_graph_id']
        
    def create_event_function(self, ev, task):
        event = dict()
        event['timestamp'] = time.time()
        event['event'] = ev
        event['task_id'] = task.run_service("GET", "GID")
        event['task_name'] = task.run_service("GET", "NAME")
        task_graph = task.run_service("GET", "TASK_GRAPH")
        event['task_graph_id'] = "" if task_graph == None else task_graph.run_service("GET", "GID")
        return event

    def log_event_function(self, event: dict):
        row = [event['timestamp'], event['event'], event['task_id'], event['task_name'], event['task_graph_id']]
        self.write_rows(self.get_filename(), [row])

    def log_events_function(self, events: dict):
        rows = []
        for event in events:
            row = [event['timestamp'], event['event'], event['task_id'], event['task_name'], event['task_graph_id']]
            rows.append(row)
        self.write_rows(self.get_filename(), rows)

    def postprocessing_function(self, params: dict):
        pass

    def preprocessing_function(self, params: dict):
        pass
