from dyn_rm.my_pmix_constants import *
from pmix import *

class My_PMIx:

    my_tool = PMIxTool()
    my_procid = None

    def tool_init_and_connect(self, pid):
        
        info = [
                    {'key':PMIX_SERVER_PIDINFO, 'value':pid, 'val_type':PMIX_PID},
                    {'key': "SCHEDULER", 'value': True, 'val_type':PMIX_BOOL}
        ]

        rc, self.my_procid = self.my_tool.init(info)

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Tool_init")
        return self.my_procid

    def get_node_map(self, jobid: str):
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_NODE_MAP], 'qualifiers': [{'key': PMIX_NSPACE, 'flags': 0, 'value': jobid, 'val_type': PMIX_STRING}]},
            ]
        )
        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")
        
        nodes = info[0]['value']['array'][1]['value'].split(',')
        return nodes

    def get_proc_map(self, jobid: str):
        
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_PROC_MAP], 'qualifiers': [{'key': PMIX_NSPACE, 'flags': 0, 'value': jobid, 'val_type': PMIX_STRING}]},
            ]
        )
        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")
        
        ppn = info[0]['value']['array'][1]['value'].split(';')
        return ppn

    def register_event_handler(self, event_code, cbfunc):
        rc, id = self.my_tool.register_event_handler([event_code], None, cbfunc)
        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Register_event_handler")

        return id

    def query_nodelist(self):
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_ALLOCATED_NODELIST], 'qualifiers': []}
            ]
        )

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")

        nodelist = filter(None, info[0]['value']['array'][0]['value'].split(","))

        return nodelist

    def query_namespaces(self):
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_QUERY_NAMESPACES], 'qualifiers': []}
            ]
        )

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")

        nspaces = filter(None, info[0]['value']['array'][0]['value'].split(","))

        return nspaces

    def query_psets(self):

        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_QUERY_PSET_NAMES], 'qualifiers': []}
            ]
        )

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")

        pset_names = filter(None, info[0]['value']['array'][0]['value'].split(","))

        return pset_names
    
    def query_node_slots(self, node_name: str):
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_NUM_SLOTS], 'qualifiers': [{'key': PMIX_HOSTNAME, 'flags': 0, 'value': node_name, 'val_type': PMIX_STRING}]}
            ]
        )

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")

        slots = int(info[0]['value']['array'][1]['value'])
        return slots

    def get_node_slots(self, jobid: str, node_name: str):

        rc, val = self.my_tool.get   ( 
                                    {'nspace': jobid, 'rank': PMIX_RANK_WILDCARD}, 
                                    PMIX_NUM_SLOTS,                                   
                                    [
                                        {'key': PMIX_NODE_INFO , 'flags': 0, 'value': True, 'val_type': PMIX_BOOL},
                                        {'key': PMIX_HOSTNAME, 'flags': 0, 'value': node_name, 'val_type': PMIX_STRING}
                                    ]                                    
                                )
        if rc != PMIX_SUCCESS and rc != PMIX_ERR_NOT_FOUND:
            raise PMIx_Error(rc, "PMIx_Get")

        if rc == PMIX_ERR_NOT_FOUND:
            return -1
        else:
            return val['value']

    def query_job_psets(self, jobid: str):

        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_QUERY_PSET_NAMES], 'qualifiers': [{'key': PMIX_NSPACE, 'flags': 0, 'value': jobid, 'val_type': PMIX_STRING}]},
            ]
        )
        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")
        
        psets = info[0]['value']['array'][1]['value'].split(',')

        return psets

    def query_pset_membership(self, pset_name: str):
        rc, info = self.my_tool.query(
            [
                {'keys': [PMIX_QUERY_PSET_MEMBERSHIP], 'qualifiers': [{'key': PMIX_PSET_NAME, 'flags': 0, 'value': pset_name, 'val_type': PMIX_STRING}]},
            ]
        )

        if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Query_info")

        pset_members = [{'nspace': proc['nspace'].decode("utf-8"), 'rank': proc['rank']} for proc in info[0]['value']['array'][2]['value']['array']]  
        
        return pset_members

    def notify_event(self, event_code: int, range, infos: list):
        self.my_tool.notify_event(event_code, self.my_procid, range, infos)
    
    def publish_data(self, pdata, pset_name=None):
    	if None != pset:
    		pdata.append({'key': PMIX_PSET_NAME, 'value': pset_name, 'flags': 0, 'val_type': PMIX_STRING})
    	rc = self.my_tool.publish({'proc': self.my_tool.my_procid, 'directives': pdata})
    	if rc != PMIX_SUCCESS:
            raise PMIx_Error(rc, "PMIx_Publish")
    	

class PMIx_Error(Exception):

    def __init__(self, error_code, pmix_function):
        message = "PMIx function '"+pmix_function+"' returned error code: "+str(error_code)
        super().__init__(message)        
