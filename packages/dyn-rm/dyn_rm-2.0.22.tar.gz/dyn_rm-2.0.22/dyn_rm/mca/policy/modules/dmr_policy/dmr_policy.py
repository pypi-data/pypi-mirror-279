from dyn_rm.mca.base.policy.module import MCAPolicyModule
from dyn_rm.mca.base.system.module import *
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.policy.modules.easy_backfilling import EasyBackfilling

# TODO: Replace with dyn_rm constants
from dyn_rm.my_pmix_constants import *
from dyn_rm.util.functions import v_print

import numpy as np
import sys
import time

class DMR_Policy(MCAPolicyModule):

    def eval_policy_function(self, system: MCASystemModule):

        # Apply EasyBAckfilling
        easy_bf = EasyBackfilling(verbosity=self.verbosity)
        results = easy_bf.run_service("EVAL", "POLICY", system)
        for setop in results["setops"]:
            if setop.run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_ADD:
                return results

        # EasyBackfilling couldn't schedule anything
        # Apply DMR
        self.params["current_time"] = time.time()

        # Get System Topology
        system_topology = system.run_service("GET", "TOPOLOGY_GRAPH")
        nodes = system_topology.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)

        free_nodes = [n for n in nodes if len(n.run_service("GET", "FREE_CORES")) == len(n.run_service("GET", "CORES"))]
        # Get a Task Graphs dictionary
        task_graphs = {task_graph.run_service("GET", "GID") : task_graph for task_graph in system.run_service("GET", "TASK_GRAPHS")}
        # Get a pset_graphs_dictionary
        pset_graphs = {pset_graph.run_service("GET", "TASK").run_service("GET", "GID") : pset_graph for pset_graph in system.run_service("GET", "PSET_GRAPHS")}
        
        # Pack all relevant setop data 
        setops_data = []
        for task_graph_id in task_graphs.keys():
            task_graph = task_graphs[task_graph_id]
            pset_graph = pset_graphs[task_graph_id]

            for setop in pset_graph.run_service("GET", "EDGES_BY_FILTER", lambda x: isinstance(x, MCAPSetopModule)):
                status = setop.run_service("GET", "PSETOP_STATUS")
                if  status != MCAPSetopModule.PSETOP_STATUS_DEFINED and \
                    status != MCAPSetopModule.PSETOP_STATUS_ORDERED:
                    continue
                op = setop.run_service("GET", "PSETOP_OP")
                if  op != MCAPSetopModule.PSETOP_OP_ADD and \
                    op != MCAPSetopModule.PSETOP_OP_SUB and \
                    op != MCAPSetopModule.PSETOP_OP_REPLACE:
                    continue
                setops_data.append({
                    "setop": setop, 
                    "pset_graph": pset_graph, 
                    "task_graph": task_graph, 
                    "topology_graph_add": MCATopologyGraphModule("delta_add"),
                    "topology_graph_sub": MCATopologyGraphModule("delta_sub"),
                    "cur_nodes": setop.run_service("GET", "INPUT")[0].run_service("GET", "ACCESSED_NODES"), 
                    "gain": -sys.float_info.max,
                    "output" : [setop.run_service("GET", "INPUT")[0]],
                    "adapted_objects" : None,
                    "task" : setop.run_service("GET", "INPUT")[0].run_service("GET", "TASK")
                })
        # Order them (ascending)
        setops_data = sorted(setops_data, key=lambda x: x["setop"].run_service("GET", "ATTRIBUTE", MCAGraphObjectModule.ATTRIBUTE_OBJ_TIMESTAMP))
        num_setops = len(setops_data)

        v_print("Num setops: "+str(len(setops_data))+" num_free nodes: "+str(len(free_nodes)), 5, self.verbosity)
        if num_setops == 0:
            return {"setops": [], "performances": [], "outputs" : [], "a_lists" : []}

        ######################################################################
        # First eval all ordered setops (create setops for task termination) #
        ######################################################################
        #self.eval_ordered_setops(setops_data)
                
        #########################
        # DMR Policy #
        #########################

        # NOTE: DMR Policy as described in DOI: 10.1109/TC.2020.3022933.
        pending_setops = [data for data in setops_data if data["setop"].run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_ADD]
        running_setops = [data for data in setops_data if data["setop"].run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_REPLACE]

        # The nodes to assign with this step size
        i = 0
        for data in running_setops:
            setop = data["setop"]
            if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                i+=1
                continue

            task_graph = data["task_graph"]
            task_graph_id = task_graph.run_service("GET", "GID")
            model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
            model_params = model.run_service("GET", "MODEL_PARAMS")
            
            cur_num_procs = setop.run_service("GET", "INPUT")[0].run_service("GET", "NUM_PROCS")
            ppn = self.get_ppn(model_params['mapping'], nodes[0])
            
            # If it is smaller than pref try growing up to pref
            if cur_num_procs < model_params['pref']:
                if self.try_expand(model_params['max'], setops_data, setops_data.index(data), free_nodes, model_params):
                    return self.get_result(system, setops_data)
                else:
                    v_print("Expansion not possible", 9, self.verbosity)
            # If jobs in queue try shrinking to start them
            elif len(pending_setops) > 0:
                #if current > preferred then
                if cur_num_procs >= model_params['pref']:
                    for pending_data in pending_setops:
                        pending_task_graph = pending_data["task_graph"]
                        # fixed num start nodes
                        num_required = pending_task_graph.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_REQ_NODES)
                        duration = pending_task_graph.run_service("GET", "ATTRIBUTE", "ESTIMATED_RUNTIME")

                        procs_after = cur_num_procs - num_required*ppn
                        if model_params["power_of_two"]:
                            procs_after = self.get_power_2_below(procs_after)
                        if procs_after >= model_params['min']:
                            nodes_to_remove = data["cur_nodes"][-int(procs_after/ppn):]
                            v_print("Shrink setop "+str(i)+" to "+str(procs_after), 4, self.verbosity)
                            if self.apply_op("SUB", setops_data, setops_data.index(data), nodes_to_remove, 0):
                                if self.apply_op("ADD", setops_data, setops_data.index(pending_data), nodes_to_remove[-num_required:], duration):
                                    return self.get_result(system, setops_data)
                            v_print("Shrink failed", 4, self.verbosity)

            # Try expand up to max
            if cur_num_procs < model_params['max']:
                if self.try_expand(model_params['max'], setops_data, setops_data.index(data), free_nodes, model_params):
                    return self.get_result(system, setops_data)
                else:
                    v_print("Expansion not possible", 9, self.verbosity)
            i+=1

        return self.get_result(system, setops_data)


    def get_result(self, system, setops_data):
        num_setops = len(setops_data) 
        setops = [setops_data[i]["setop"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        results = [setops_data[i]["gain"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        outputs = [setops_data[i]["output"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        a_lists = [setops_data[i]["adapted_objects"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]


        # Now subsitute all proc placeholders with the real objects (slow)
        new_pset_procs = []
        procs = dict()
        for output,a_list in zip(outputs,a_lists):
            nodes_after = output[len(output) - 1].run_service("GET", "ACCESSED_NODES") 
            for pset in output:
                new_pset_procs = []
                for proc in pset.run_service("GET", "PROCS"):
                    # This is a placholder we need to replace
                    if isinstance(proc, dict):
                        gid = proc["gid"]
                        if proc["status"] == MCAProcModule.PROC_STATUS_LAUNCH_REQUESTED:
                            if gid in procs.keys():
                                proc_obj = procs[gid]
                            else:
                                proc_obj = MCAProcModule(proc["name"], proc["exec"])
                                proc_obj.run_service("SET", "PROC_STATUS", proc["status"])
                                proc_obj.run_service("SET", "CORE_ACCESS", proc["cores"])
                                procs[gid] = proc_obj
                            new_pset_procs.append(proc_obj)
                            try:
                                a_list[a_list.index(proc)] = proc_obj
                            except ValueError:
                                pass
                        elif proc["status"] == MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED:
                            old_proc = system.run_service("GET", "GRAPH_VERTEX", gid)
                            delta_proc = MCAProcModule("", "")
                            delta_proc = old_proc.run_service("GET", "COPY", delta_proc)
                            delta_proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED)
                            procs[gid] = delta_proc
                            new_pset_procs.append(delta_proc)
                            try:
                                a_list[a_list.index(proc)] = delta_proc
                            except ValueError:
                                pass
                    else:
                        new_pset_procs.append(proc)
                
                if len(new_pset_procs) > 0:
                    # update PSet membership with real procs
                    proc_edge = pset.run_service("GET", "PROC_EDGE")
                    proc_edge.run_service("SET", "OUTPUT", new_pset_procs)
        return {"setops": setops, "performances": results, "outputs" : outputs, "a_lists" : a_lists}

    def eval_ordered_setops(self, setops_data):
        i = 0
        for data in setops_data:
            setop = data["setop"]

            if setop.run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_SUB: 
                if setop.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_ORDERED:
                    i+=1
                    continue
                input = [data["output"][len(data["output"]) - 1]]
                new_nodes_to_check = data["cur_nodes"]
                pset_graph = data["pset_graph"]
                task_graph = data["task_graph"]
                # prev removed nodes + new nodes to remove
                topo_graph_sub = MCATopologyGraphModule("delta_sub")
                topo_graph_sub.run_service("ADD", "TOPOLOGY_OBJECTS", new_nodes_to_check)
                
                model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
                if None == model:
                    model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

                o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                         setop, 
                                                         setop.run_service("GET", "INPUT"),
                                                        {"TOPOLOGY_GRAPH_ADD": MCATopologyGraphModule("delta_add"),
                                                         "TOPOLOGY_GRAPH_SUB": topo_graph_sub,
                                                         "PSET_GRAPH" : pset_graph,
                                                         "TASK_GRAPH" : task_graph
                                                        })
                # Output Space is empty
                if 0 == len(o_lists):
                    i+=1
                    continue
                # Collaps Output Space to a single output list
                o_list = model.run_service("COLLAPS", "OUTPUT_SPACE", input, o_lists, ["SPEEDUP"])
                a_list = a_lists[o_lists.index(o_list)]

                result = model.run_service("EVAL", "EDGE", input, o_list, ["SPEEDUP"])
                if None in result.values():
                    i+=1
                    continue

                # Update setop for this decision
                setops_data[i]["topology_graph_sub"].run_service("ADD", "GRAPH_VERTICES", new_nodes_to_check, assign_graph = False)
                setops_data[i]["gain"] = np.mean([x for x in result.values()]) / len(new_nodes_to_check)
                setops_data[i]["adapted_objects"] = a_list
                setops_data[i]["output"] = o_list
                setops_data[i]["cur_nodes"] = [n for n in setops_data[i]["cur_nodes"] if n not in new_nodes_to_check]

                #print(i, " EVALUATED SUB OPERATION: " + str(setops_data[i]))
            i+=1

    # create a launch set operation for this task if possible
    def apply_op(self, op, setops_data, index, nodes, duration):
        data = setops_data[index]
        setop = data["setop"]
        pset_graph = data["pset_graph"]
        task_graph = data["task_graph"]

        if op == "ADD":
            prev_topo = data["topology_graph_add"]
        else:
            prev_topo = data["topology_graph_sub"]

        input = [data["output"][len(data["output"]) - 1]]
        task_graph_id = task_graph.run_service("GET", "GID")

        v_print("Apply op "+op+" for task '"+task_graph_id+"' with "+str(len(nodes))+" nodes for "+str(duration)+" seconds", 5, self.verbosity)

        # current new assignments + new nodes 
        topo_graph = MCATopologyGraphModule("delta_"+op)
        topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", nodes)
        topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", prev_topo.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
        
        model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
        if None == model:
            model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

        if op == "ADD":
            o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                 setop, 
                                                 setop.run_service("GET", "INPUT"),
                                                {"TOPOLOGY_GRAPH_ADD": topo_graph,
                                                 "TOPOLOGY_GRAPH_SUB": MCATopologyGraphModule("delta_sub"),
                                                 "PSET_GRAPH" : pset_graph,
                                                 "TASK_GRAPH" : task_graph
                                                })
        else:
            o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                     setop, 
                                     setop.run_service("GET", "INPUT"),
                                    {"TOPOLOGY_GRAPH_ADD": MCATopologyGraphModule("delta_ADD"),
                                     "TOPOLOGY_GRAPH_SUB": topo_graph,
                                     "PSET_GRAPH" : pset_graph,
                                     "TASK_GRAPH" : task_graph
                                    })

        # Output Space is empty
        if 0 == len(o_lists):
            #print("SetOp", setop.run_service("GET", "NAME"), " ==> Normailzed Gain: ", 0)
            return False

        # Collaps Output Space to a single output list
        o_list = model.run_service("COLLAPS", "OUTPUT_SPACE", input, o_lists, ["SPEEDUP"])
        a_list = a_lists[o_lists.index(o_list)]
        
        result = model.run_service("EVAL", "EDGE", input, o_list, ["SPEEDUP"])
        
        # need to decide how to handle missing metrics
        # for now ingore setop
        if None in result.values():
            i+=1
            return False
        
        gain = np.mean([x for x in result.values()]) / len(nodes)
        # Update setop for this decision
        setops_data[index]["topology_graph_add"].run_service("ADD", "GRAPH_VERTICES", nodes, assign_graph = False)
        setops_data[index]["gain"] = gain
        setops_data[index]["adapted_objects"] = a_list
        setops_data[index]["output"] = o_list
        setops_data[index]["cur_nodes"].extend(nodes)


        if setop.run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_ADD:
            task_graph.run_service("SET", "ATTRIBUTE", "START_TIME", self.params["current_time"])
            for node in nodes:
                node.run_service("SET", "ATTRIBUTE", "OCCUPIED_FROM", self.params["current_time"])
                node.run_service("SET", "ATTRIBUTE", "OCCUPIED_UNTIL", self.params["current_time"] + duration)
        return True
    
    def try_expand(self, limit, setops_data, index, free_nodes, params):
        
        v_print("Try expand setop "+str(index)+" to "+str(limit)+" with num_nodes "+str(len(free_nodes)), 8, self.verbosity)
        if len(free_nodes) < 1:
            return False
        cur_num_procs = setops_data[index]["setop"].run_service("GET", "INPUT")[0].run_service("GET", "NUM_PROCS")
        # Number of procs per node
        ppn = self.get_ppn(params['mapping'], free_nodes[0])        
        target_procs = min(limit, cur_num_procs + len(free_nodes)*ppn)
        delta_procs = target_procs - cur_num_procs
        if params['power_of_two']:
            power = 1
            while power < target_procs:
                power <<= 1
            if power > target_procs:
                power >>= 1
            delta_procs = power - cur_num_procs
            if delta_procs < 1 or delta_procs % ppn != 0:
                v_print("Did not find a fitting power of two", 8, self.verbosity)
                return False
        num_nodes = int(delta_procs/ppn)
        v_print("Expand setop "+str(index)+" from "+str(cur_num_procs)+" by "+str(delta_procs)+" in task "+str(setops_data[index]["task_graph"].run_service("GET", "GID")), 4, self.verbosity)
        if not self.apply_op("ADD", setops_data, index, free_nodes[:num_nodes], 0):
            v_print("Expansion failed", 4, self.verbosity)
            return False
        return True

    def get_ppn(self, mapping, node):
        if mapping == 'sparse':
            return 1 
        elif mapping == 'dense':
            return node.run_service("GET", "NUM_CORES")
        elif mapping.endswith(":node"):
            return int(mapping.split(":")[0])
        else:
            return 1
        
    def get_power_2_below(self, target_procs):
        power = 1
        while power < target_procs:
            power <<= 1
        if power > target_procs:
            power >>= 1
        return power
