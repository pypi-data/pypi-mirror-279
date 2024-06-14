from dyn_rm.mca.base.policy.module import MCAPolicyModule
from dyn_rm.mca.base.system.module import *
from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule

# TODO: Replace with dyn_rm constants
from dyn_rm.my_pmix_constants import *

import numpy as np
import sys

class FirstFitFirst(MCAPolicyModule):

    def eval_policy_function(self, system: MCASystemModule):

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

        #################################
        # First eval all ordered setops #
        #################################
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
        # Assign all free nodes #
        #########################
        print("num_assigned ", num_nodes_assigned, " num free "+str(num_free_nodes))
        num_nodes_assigned = 0

        # The nodes that are assigned in this step
        newly_assigned_nodes = []
        # The nodes to assign with this step size
        i = 0
        for data in setops_data:
            setop = data["setop"]
            task = data["task"]
            if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                i+=1
                continue
            num_required = task.run_service("GET", "ATTRIBUTE", MCATaskModule.TASK_ATTRIBUTE_REQ_NODES)
            print("Task requires num_nodes: ",num_required)
            if len(free_nodes) - num_nodes_assigned < num_required:
                # Backfill
                i+=1 
                continue
            
            new_nodes_to_assign = free_nodes[num_nodes_assigned:num_nodes_assigned + num_required]
            pset_graph = data["pset_graph"]
            task_graph = data["task_graph"]
            prev_topo = data["topology_graph_add"]
            input = [data["output"][len(data["output"]) - 1]]
            priority = setop.run_service("GET", "PRIORITY")
            
            # current new assignments + new nodes 
            topo_graph = MCATopologyGraphModule("delta_add")
            topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", new_nodes_to_assign)
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
                i+=1
                continue
            # Collaps Output Space to a single output list
            o_list = model.run_service("COLLAPS", "OUTPUT_SPACE", input, o_lists, ["SPEEDUP"])
            a_list = a_lists[o_lists.index(o_list)]
            
            result = model.run_service("EVAL", "EDGE", input, o_list, ["SPEEDUP"])
            
            # need to decide how to handle missing metrics
            # for now ingore setop
            if None in result.values():
                #print("SetOp", setop.run_service("GET", "NAME"), " ==> Speedup: ", 0)
                i+=1
                continue
            
            #setop_gains[i] = np.linalg.norm([x for x in result.values()]) / step_size
            gain = np.mean([x for x in result.values()]) / num_required
            gain *= priority
            newly_assigned_nodes = new_nodes_to_assign
            num_nodes_assigned += len(newly_assigned_nodes)
            # Update setop for this decision
            setops_data[i]["topology_graph_add"].run_service("ADD", "GRAPH_VERTICES", newly_assigned_nodes, assign_graph = False)
            setops_data[i]["gain"] = gain / setops_data[i]["setop"].run_service("GET", "PRIORITY")
            setops_data[i]["adapted_objects"] = a_list
            setops_data[i]["output"] = o_list
            setops_data[i]["cur_nodes"].extend(newly_assigned_nodes)
            #print("ADD: Setop #", i, " Assigning new nodes: ",
            #      [node.run_service("GET", "NAME") for node in newly_assigned_nodes],
            #      "Total nodes: ",
            #       [node.run_service("GET", "NAME") for node in 
            #        setops_data[i]["topology_graph_add"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)]
            #    )
            nodes_after = o_list[len(o_list) - 1].run_service("GET", "ACCESSED_NODES") 
            #print("         Nodes after: " + str([node.run_service("GET", "NAME") for node in nodes_after]))
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


        return {"setops": setops, "performances": results, "outputs" : outputs, "a_lists" : a_lists}