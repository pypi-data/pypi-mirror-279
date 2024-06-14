from dyn_rm.mca.base.logger.module import MCALoggerModule
import time
import json

class MCAPolicyLogger(MCALoggerModule):
    filename = "policy.csv"

    def get_header(self) -> list:
        return ['timestamp', 'event', 'setop_results', 'gain', 'gain_normalized']

    def create_event_function(self, ev, result):

        setop_dicts = []
        total_gain = 0
        total_gain_normalized = 0
        if None == result:
            return {    "timestamp" : time.time(),
                        "event" : ev,
                        "setop_results" : "",
                        "gain" : 0,
                        "gain_normalized" : 0}

        for setop, output in zip(result["setops"], result["outputs"]):

            nodes_before = setop.run_service("GET", "INPUT")[0].run_service("GET", "ACCESSED_NODES")
            nodes_after = output[len(output) - 1].run_service("GET", "ACCESSED_NODES")
            model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
            prev_perf = model.run_service("EVAL", "INPUT", setop.run_service("GET", "INPUT"), ["SPEEDUP"])
            after_perf = model.run_service("EVAL", "OUTPUT", output, ["SPEEDUP"])
            gain = model.run_service("EVAL", "EDGE", setop.run_service("GET", "INPUT"), output, ["SPEEDUP"])

            setop_dict = dict()
            setop_dict['setop_id'] = setop.run_service("GET", "GID")
            setop_dict['nodes_before'] = ';'.join([node.run_service("GET", "NAME") for node in nodes_before])
            setop_dict['nodes_after'] = ';'.join([node.run_service("GET", "NAME") for node in nodes_after])
            setop_dict['speedup_before'] = prev_perf
            setop_dict['speedup_after'] = after_perf
            setop_dict['gain'] = gain["SPEEDUP"]
            setop_dict['normalized_gain'] = gain["SPEEDUP"]/(abs(len(nodes_after)-len(nodes_before)))
            setop_dicts.append(setop_dict)

            total_gain += gain["SPEEDUP"]
            total_gain_normalized += gain["SPEEDUP"]/(abs(len(nodes_after)-len(nodes_before)))
        
        
        event = dict()
        event["timestamp"] = time.time()
        event["event"] = ev
        event["setop_results"] = ';'.join([json.dumps(sd) for sd in setop_dicts])
        event["gain"] = total_gain
        event["gain_normalized"] = total_gain_normalized

        return event

    def log_event_function(self, event: dict):
        row = [event["timestamp"], event['event'], event["setop_results"], event["gain"], event["gain_normalized"]]
        self.write_rows(self.get_filename(), [row]) 

    def log_events_function(self, events: list):
        rows = []
        for event in events:
            row = [event["timestamp"], event['event'], event["setop_results"], event["gain"], event["gain_normalized"]]
            rows.append(row)
            
        self.write_rows(self.get_filename(), rows)               

    def postprocessing_function(self, params: dict):
        pass
    
    def preprocessing_function(self, params: dict):
        pass