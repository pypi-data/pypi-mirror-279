from dyn_rm.mca.base.policy.module import MCAPolicyModule
from dyn_rm.mca.base.system.module import *
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule

# TODO: Replace with dyn_rm constants
from dyn_rm.my_pmix_constants import *
from dyn_rm.util.functions import v_print

import numpy as np
import sys
import time

class EasyBackfilling(MCAPolicyModule):

    def eval_policy_function(self, system: MCASystemModule):

        self.params["current_time"] = time.time()

        # Get System Topology
        system_topology = system.run_service("GET", "TOPOLOGY_GRAPH")
        nodes = system_topology.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)

        free_nodes = [n for n in nodes if len(n.run_service("GET", "FREE_CORES")) == len(n.run_service("GET", "CORES"))]
        num_free_nodes = len(free_nodes)
        num_nodes_assigned = 0
        priority = 1

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
                    op != MCAPSetopModule.PSETOP_OP_SUB:
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

        #print("Num setops: "+str(len(setops_data))+" assign num_free nodes: ", num_free_nodes)
        if num_setops == 0:
            return {"setops": [], "performances": [], "outputs" : [], "a_lists" : []}

        ######################################################################
        # First eval all ordered setops (create setops for task termination) #
        ######################################################################
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
                
        #########################
        # EASY BACKFILLING #
        #########################
        # NOTE: There are many variants for EasyBackfilling.
        # Here we use the following approach:
            # FCFS ordering of queue
            # 1. If possible: Start jobs from head of queue if enough free resource  
            # 2. The next job can not be started anymore:
                # reserve nodes for this job (This might contain some free nodes + some occupied nodes)
                # The expected start time is the highest release time of all reserved nodes
            # 3. Backfilling: There might be some free nodes reserved:
                # Start jobs if they fit onto the free nodes and 
                # take less then expected start time of the reserved job
            # COMMENT: The reservation will be renewed in the next scheduling pass 
        
        # Set Occupation for running jobs:
        self.update_current_occupation(task_graphs)
        
        # The nodes that are assigned in this step
        newly_assigned_nodes = []
        # The nodes to assign with this step size
        i = 0
        for data in setops_data:
            setop = data["setop"]
            if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                i+=1
                continue

            task_graph = data["task_graph"]
            task_graph_id = task_graph.run_service("GET", "GID")
            num_required = task_graph.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_REQ_NODES)
            task_duration = task_graph.run_service("GET", "ATTRIBUTE", "ESTIMATED_RUNTIME") 
            v_print("Task '"+task_graph_id+"' requires num_nodes: "+str(num_required)+" and free nodes = "+str(len(free_nodes)), 5, self.verbosity)
            if num_required <= len(free_nodes):
                
                assignment = free_nodes[:num_required]
                if self.start_task(setops_data, i, assignment, task_duration):
                    free_nodes = free_nodes[num_required:]

            else:
                reserved_nodes, start_time = self.reserve_nodes(num_required, task_duration, nodes)
                if i < len(setops_data) - 1:
                    self.backfill_tasks(setops_data, i+1, reserved_nodes, start_time)
                
                # We only beackfill one time
                break

            i+=1

        setops = [setops_data[i]["setop"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        results = [setops_data[i]["gain"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        outputs = [setops_data[i]["output"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        a_lists = [setops_data[i]["adapted_objects"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]


        # Now subsitute all proc placeholders with the real objects (slow)
        new_pset_procs = []
        procs = dict()
        for output,a_list in zip(outputs,a_lists):
            nodes_after = output[len(output) - 1].run_service("GET", "ACCESSED_NODES") 
            #print("         Nodes after: " + str([node.run_service("GET", "NAME") for node in nodes_after]))
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

        # Clear node reservations
        for node in nodes:
            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_FROM", -1)
            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_UNTIL", -1)

        return {"setops": setops, "performances": results, "outputs" : outputs, "a_lists" : a_lists}

    # create a launch set operation for this task if possible
    def start_task(self, setops_data, index, nodes, duration):
        
        data = setops_data[index]
        setop = data["setop"]
        pset_graph = data["pset_graph"]
        task_graph = data["task_graph"]
        prev_topo = data["topology_graph_add"]
        input = [data["output"][len(data["output"]) - 1]]
        task_graph_id = task_graph.run_service("GET", "GID")
        
        v_print("Starting task '"+task_graph_id+"' with "+str(len(nodes))+" nodes for "+str(duration)+" seconds", 5, self.verbosity)

        # current new assignments + new nodes 
        topo_graph = MCATopologyGraphModule("delta_add")
        topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", nodes)
        topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", prev_topo.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
        
        model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
        if None == model:
            model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")
        o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                             setop, 
                                             setop.run_service("GET", "INPUT"),
                                            {"TOPOLOGY_GRAPH_ADD": topo_graph,
                                             "TOPOLOGY_GRAPH_SUB": MCATopologyGraphModule("delta_sub"),
                                             "PSET_GRAPH" : pset_graph,
                                             "TASK_GRAPH" : task_graph
                                            })
        
        # Output Space is empty
        if 0 == len(o_lists):
            #print("Output Space empty")
            #print("SetOp", setop.run_service("GET", "NAME"), " ==> Normailzed Gain: ", 0)
            return False
        
        # Collaps Output Space to a single output list
        o_list = model.run_service("COLLAPS", "OUTPUT_SPACE", input, o_lists, ["SPEEDUP"])
        a_list = a_lists[o_lists.index(o_list)]
        
        result = model.run_service("EVAL", "EDGE", input, o_list, ["SPEEDUP"])
        
        # need to decide how to handle missing metrics
        # for now ingore setop
        if None in result.values():
            #print("SetOp", setop.run_service("GET", "NAME"), " ==> Speedup: ", 0)
            i+=1
            return False
        
        gain = np.mean([x for x in result.values()]) / len(nodes)

        # Update setop for this decision
        setops_data[index]["topology_graph_add"].run_service("ADD", "GRAPH_VERTICES", nodes, assign_graph = False)
        setops_data[index]["gain"] = gain
        setops_data[index]["adapted_objects"] = a_list
        setops_data[index]["output"] = o_list
        setops_data[index]["cur_nodes"].extend(nodes)

        task_graph.run_service("SET", "ATTRIBUTE", "START_TIME", self.params["current_time"])
        for node in nodes:
            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_FROM", self.params["current_time"])
            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_UNTIL", self.params["current_time"] + duration)

        return True

    # find the earliest reservation for the giben number of nodes and duration
    def reserve_nodes(self, num_required, duration, nodes):
        v_print("Reserving a slice of "+str(num_required)+" nodes x "+str(duration)+" seconds", 5, self.verbosity)

        sorted_nodes = sorted(nodes, key=lambda x: x.run_service("GET", "ATTRIBUTE", "OCCUPIED_UNTIL"))
        reserved_nodes = sorted_nodes[:num_required]
        task_start = max(self.params["current_time"], reserved_nodes[-1].run_service("GET", "ATTRIBUTE", "OCCUPIED_UNTIL"))

        for node in reserved_nodes:
            if node.run_service("GET", "ATTRIBUTE", "OCCUPIED_UNTIL") == -1:
                node.run_service("SET", "ATTRIBUTE", "OCCUPIED_FROM", task_start)
            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_UNTIL", task_start + duration)
        v_print("Reserved a slice of "+str(num_required)+" nodes x "+str(duration)+" seconds starting at "+str(task_start), 5, self.verbosity)
        return reserved_nodes, task_start

    # Backfill as many tasks as possible into the given window
    def backfill_tasks(self, setops_data, start_index, reserved_nodes, end_time):
        
        v_print("Applying Backfilling for a slice of "+str(len(reserved_nodes))+" nodes until "+str(end_time), 5, self.verbosity)

        for i in range(start_index, len(setops_data)):
            data = setops_data[i]
            task_graph = data["task_graph"]
            task_graph_id = task_graph.run_service("GET", "GID")

            num_required = task_graph.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_REQ_NODES)
            task_duration = task_graph.run_service("GET", "ATTRIBUTE", "ESTIMATED_RUNTIME")

            v_print("Backfilling: Task '"+task_graph_id+"' requires "+str(num_required)+" nodes for "+str(task_duration)+" seconds", 7, self.verbosity)

            # Skip task that do not fit into the window
            if task_duration > end_time - self.params["current_time"]:
                continue 
            
            free_nodes = []
            for node in reserved_nodes:
                if node.run_service("GET", "ATTRIBUTE", "OCCUPIED_FROM") > self.params["current_time"]:
                    free_nodes.append(node)
            
            if num_required <= len(free_nodes):
                self.start_task(setops_data, i, free_nodes[:num_required], task_duration)

    def update_current_occupation(self, task_graphs):
        v_print("Updating current occupation", 9, self.verbosity)
        for task_graph in task_graphs.values():
            for task in task_graph.run_service("GET", "TASKS"):
                if task.run_service("GET", "TASK_STATUS") != MCATaskModule.TASK_STATUS_RUNNING:
                    continue
                task_start = task_graph.run_service("GET", "ATTRIBUTE", "START_TIME")
                task_duration = task_graph.run_service("GET", "ATTRIBUTE", "ESTIMATED_RUNTIME") 
                procs = task.run_service("GET", "PROCS")
                for proc in procs:
                    cores = proc.run_service("GET", "CORE_ACCESS")
                    if len(cores) > 0:
                        for core in cores:
                            node = core.run_service("GET", "NODE")
                            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_FROM", task_start)
                            node.run_service("SET", "ATTRIBUTE", "OCCUPIED_UNTIL", task_start + task_duration)