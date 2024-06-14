from dyn_rm.mca.base.logger.module import MCALoggerModule
import time

class MCANodeLogger(MCALoggerModule):
    filename = "node.csv"

    def get_header(self) -> list:
        return ['timestamp', 'node_id', 'event', 'num_cores', 'num_free_cores', 'num_utilized_cores']

    def create_event_function(self, ev, node):
        event = dict()
        event["timestamp"] = time.time()
        event["event"] = ev
        event["node_id"] = node.run_service("GET", "NAME")
        event["num_cores"] = node.run_service("GET", "NUM_CORES")
        event["num_free_cores"] = len(node.run_service("GET", "FREE_CORES"))
        event["num_utilized_cores"] = len(node.run_service("GET", "UTILIZED_CORES"))

        return event

    def log_event_function(self, event: dict):
        row = [event["timestamp"], event['node_id'], event['event'], event["num_cores"], event["num_free_cores"], event["num_utilized_cores"]]
        self.write_rows(self.get_filename(), [row]) 

    def log_events_function(self, events: list):
        rows = []
        for event in events:
            row = [event["timestamp"], event['node_id'], event['event'], event["num_cores"], event["num_free_cores"], event["num_utilized_cores"]]
            rows.append(row)
            
        self.write_rows(self.get_filename(), rows)               

    def postprocessing_function(self, params: dict):
        pass
    
    def preprocessing_function(self, params: dict):
        pass