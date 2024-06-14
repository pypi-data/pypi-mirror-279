from dyn_rm.mca.base.policy.module import MCAPolicyModule
from dyn_rm.mca.base.system.module import *

# TODO: Replace with dyn_rm constants
from dyn_rm.my_pmix_constants import *
from dyn_rm.util.functions import v_print

import numpy as np
import sys

class Discrete_Steepest_Ascend(MCAPolicyModule):

    def eval_policy_function(self, system: MCASystemModule):
        # Get System Topology
        system_topology = system.run_service("GET", "TOPOLOGY_GRAPH")
        nodes = system_topology.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)

        free_nodes = [n for n in nodes if len(n.run_service("GET", "FREE_CORES")) == len(n.run_service("GET", "CORES"))]
        num_free_nodes = len(free_nodes)
        num_nodes_assigned = 0

        occupied_nodes = [n for n in nodes if node not in free_nodes]
        num_occupied_nodes = len(occupied_nodes)
        num_nodes_removed = 0
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
                    op != MCAPSetopModule.PSETOP_OP_GROW and \
                    op != MCAPSetopModule.PSETOP_OP_SHRINK and \
                    op != MCAPSetopModule.PSETOP_OP_REPLACE and \
                    op != MCAPSetopModule.PSETOP_OP_SUB:
                    continue
                
                valid = True
                for pset in setop.run_service("GET", "INPUT"):
                    for in_edge in pset.run_service("GET", "IN_EDGES"):
                        if isinstance(in_edge, MCAPSetopModule):
                            status = in_edge.run_service("GET", "PSETOP_STATUS")
                            if status != MCAPSetopModule.PSETOP_STATUS_FINALIZED:
                                valid = False
                                break
                if not valid:
                    #print("Prev OP pending. Skip!")
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
                    "adapted_objects" : None
                })
        # Order them (ascending)

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
                
        ########################### 
        # Remove nodes not needed #
        ###########################
        while True:
            if "step_size" in self.params.keys():
                if self.params["step_size"] == 'power_of_2':
                    step_sizes = [2 ** i for i in range(num_occupied_nodes.bit_length())]
                elif self.params["step_size"] == 'linear':
                    step_sizes = range(1, num_occupied_nodes + 1)
                elif self.params["step_size"] == 'single':
                    step_sizes = [1]
            else:
                step_sizes = [2 ** i for i in range(num_occupied_nodes.bit_length())]
            
            best_gain = -1
            best_a_list = None
            best_setop_index = -1

            # The nodes that are removed in this step
            newly_removed_nodes = []
    
            # Test for all Step sizes
            for step_size in step_sizes:
                #print("*************************")
                #print("Testing step size ", step_size)
                #print("Removed so far: ", num_nodes_removed)

                # The nodes to assign with this step size
                

                # gain when using this step size
                gain = -1
    
                # index of best setop for this step size
                setop_index = -1
    
                # Here we store the gain and output for each setop for this step size
                setop_gains = [0 for _ in range(num_setops)]
                setop_a_lists = [None for _ in range(num_setops)]
                setop_outputs = [None for _ in range(num_setops)]

                i = 0
                for data in setops_data:
                    setop = data["setop"]
                    if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                        i+=1
                        continue
                    new_nodes_to_check = data["cur_nodes"][max(0, len(data["cur_nodes"]) - step_size): len(data["cur_nodes"])]
                    if len(new_nodes_to_check) < 1:
                        i+=1
                        continue
                    
                    pset_graph = data["pset_graph"]
                    task_graph = data["task_graph"]
                    prev_topo = data["topology_graph_sub"]
                    input = [data["output"][len(data["output"]) - 1]]
                    priority = setop.run_service("GET", "PRIORITY")
                    
                    # prev removed nodes + new nodes to remove
                    topo_graph = MCATopologyGraphModule("delta_sub")
                    topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", new_nodes_to_check)
                    topo_graph.run_service("ADD", "TOPOLOGY_OBJECTS", prev_topo.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))

                    model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
                    if None == model:
                        model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

                    o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                         setop, 
                                                         setop.run_service("GET", "INPUT"),
                                                        {"TOPOLOGY_GRAPH_ADD": MCATopologyGraphModule("delta_add"),
                                                         "TOPOLOGY_GRAPH_SUB": topo_graph,
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
                    setop_gains[i] = np.mean([x for x in result.values()]) / step_size * priority
                    setop_a_lists[i] = a_list
                    setop_outputs[i] = o_list
                    i+=1
                    
                # Get the best gain for this setp size over all setops
                gains = [x for x in setop_gains if x != None]
                gain = max(gains) if len(gains) > 0 else -1 
                
                if gain < 0:
                    continue
                    
                setop_index = setop_gains.index(gain)
                if gain > best_gain:
                    best_gain = gain
                    best_olist = setop_outputs[setop_index]
                    best_a_list = setop_a_lists[setop_index]
                    best_setop_index = setop_index
                    newly_removed_nodes = new_nodes_to_check
            

            if best_gain <= 0:
                # reached maximum
                break

            num_nodes_removed += len(newly_removed_nodes)

            # Update setop for this decision
            setops_data[best_setop_index]["topology_graph_sub"].run_service("ADD", "GRAPH_VERTICES", newly_removed_nodes, assign_graph = False)
            setops_data[best_setop_index]["gain"] = best_gain / setops_data[best_setop_index]["setop"].run_service("GET", "PRIORITY")
            setops_data[best_setop_index]["adapted_objects"] = best_a_list
            setops_data[best_setop_index]["output"] = best_olist
            setops_data[best_setop_index]["cur_nodes"] = [n for n in setops_data[best_setop_index]["cur_nodes"] if n not in newly_removed_nodes]

            #print("REMOVE: Setop #", best_setop_index, " Assigning new nodes: ",
            #      [node.run_service("GET", "NAME") for node in newly_removed_nodes],
            #      "Total nodes: ",
            #       [node.run_service("GET", "NAME") for node in 
            #        setops_data[best_setop_index]["topology_graph_sub"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)]
            #    ) 


        #########################
        # Assign all free nodes #
        #########################
        v_print("num_assigned "+str(num_nodes_assigned)+ " num free "+str(num_free_nodes), 5, self.verbosity)
        while num_nodes_assigned < num_free_nodes:
            if "step_size" in self.params.keys():
                if self.params["step_size"] == 'power_of_2':
                    step_sizes = [2 ** i for i in range(num_free_nodes.bit_length())]
                elif self.params["step_size"] == 'linear':
                    step_sizes = range(1, num_free_nodes + 1)
                elif self.params["step_size"] == 'single':
                    step_sizes = [1]
            else:
                step_sizes = [2 ** i for i in range(num_free_nodes.bit_length())]

            best_gain = 0
            best_a_list = None
            best_setop_index = -1

            # The nodes that are assigned in this step
            newly_assigned_nodes = []
            # Test for all Step sizes
            for step_size in step_sizes:
                v_print("*************************", 6, self.verbosity)
                v_print("Testing step size "+str(step_size), 6, self.verbosity)
                v_print("Assignment so far: "+str(num_nodes_assigned), 6, self.verbosity)

                # The nodes to assign with this step size
                new_nodes_to_assign = free_nodes[num_nodes_assigned:num_nodes_assigned + step_size]
                #print("NEW nodes to assign: "+str([n.run_service("GET", "NAME") for n in new_nodes_to_assign]))

                # gain when using this step size
                gain = 0
    
                # index of best setop for this step size
                setop_index = -1
    
                # Here we store the gain and output for each setop for this step size
                setop_gains = [0 for _ in range(num_setops)]
                setop_a_lists = [None for _ in range(num_setops)]
                setop_outputs = [None for _ in range(num_setops)]

                i = 0
                for data in setops_data:

                    setop = data["setop"]
                    if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                        i+=1
                        continue

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
                        v_print("Output Space empty", 7, self.verbosity)
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
                    setop_gains[i] = np.mean([x for x in result.values()]) / step_size
                    setop_a_lists[i] = a_list
                    setop_outputs[i] = o_list
                    v_print("SetOp "+str(setop.run_service("GET", "NAME"))+ " ==> Normailzed Gain: "+str(setop_gains[i]), 7, self.verbosity)
                    i+=1
                    

                # Get the best gain for this setp size over all setops
                gains = [x for x in setop_gains if x != None]
                gain = max(gains) if len(gains) > 0 else 0 
                if gain > 0:
                    setop_index = setop_gains.index(gain)
                gain *= priority

                v_print("best gain: "+str(gain)+" setop "+str(setop_index), 6, self.verbosity)
                if gain > best_gain:
                    best_gain = gain
                    best_olist = setop_outputs[setop_index]
                    best_a_list = setop_a_lists[setop_index]
                    best_setop_index = setop_index
                    newly_assigned_nodes = new_nodes_to_assign
            

            if best_gain <= 0:
                # reached maximum
                break

            num_nodes_assigned += len(newly_assigned_nodes)

            # Update setop for this decision
            setops_data[best_setop_index]["topology_graph_add"].run_service("ADD", "GRAPH_VERTICES", newly_assigned_nodes, assign_graph = False)
            setops_data[best_setop_index]["gain"] = best_gain / setops_data[best_setop_index]["setop"].run_service("GET", "PRIORITY")
            setops_data[best_setop_index]["adapted_objects"] = best_a_list
            setops_data[best_setop_index]["output"] = best_olist
            setops_data[best_setop_index]["cur_nodes"].extend(newly_assigned_nodes)

            #print("ADD: Setop #", best_setop_index, " Assigning new nodes: ",
            #      [node.run_service("GET", "NAME") for node in newly_assigned_nodes],
            #      "Total nodes: ",
            #       [node.run_service("GET", "NAME") for node in 
            #        setops_data[best_setop_index]["topology_graph_add"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)]
            #    )
            nodes_after = best_olist[len(best_olist) - 1].run_service("GET", "ACCESSED_NODES") 
            #print("         Nodes after: " + str([node.run_service("GET", "NAME") for node in nodes_after]))
        #############################
        # Swap nodes between setops #
        #############################
        #print()
        #print("SWAP NODES") 
        #print()
        last_swap = (None, None)
        while True:
            #print("while True")
            if len(setops_data) < 2:
                break
            #step_sizes = [2 ** i for i in range((len(nodes)).bit_length())]
            #step_sizes = range(1, len(nodes) + 1)
            if "step_size" in self.params.keys():
                if self.params["step_size"] == 'power_of_2':
                    step_sizes = [2 ** i for i in range((len(nodes)).bit_length())]
                elif self.params["step_size"] == 'linear':
                    step_sizes = range(1, len(nodes) + 1)
                elif self.params["step_size"] == 'single':
                    step_sizes = [1]

            else:
                step_sizes = [2 ** i for i in range((len(nodes)).bit_length())]
            
            best_gain = -sys.float_info.max
            best_a_lists = [None, None]
            best_setop_indices = [-1,-1]

            # The nodes that are removed in this step
            newly_removed_nodes = []
    
            #print()
            #print("FIND SETOP TO SHRINK "+str(step_sizes))
            #print()
            # Test for all Step sizes
            for step_size in step_sizes:

                ###############################
                # Find best setop to shrink   #
                ###############################

                #print("*************************")
                #print("Testing step size ", step_size)
                #print("Removed so far: ", num_nodes_removed)

                # gain when using this step size
                gain = 0
    
                # index of best setop for this step size
                setop_index_add = -1
                setop_index_sub = -1
    
                # Here we store the gain and output for each setop for this step size
                setop_gains = [-sys.float_info.max for _ in range(num_setops)]
                setop_a_lists = [None for _ in range(num_setops)]
                setop_outputs = [None for _ in range(num_setops)]
                setop_nodes_to_swap = [[] for _ in range(num_setops)]     

                best_setop_sub = None

                i = 0
                for data in setops_data:
                    #print("Setop ", i, " "+data["setop"].run_service("GET", "GID"))
                    #print("cur_nodes: "+str([node.run_service("GET", "NAME") for node in data["cur_nodes"]]))
                    if len(data["cur_nodes"]) == 0:
                        i+=1
                        continue
                    #new_nodes_to_check = data["cur_nodes"][:min(step_size, len(data["cur_nodes"]))]
                    new_nodes_to_check = data["cur_nodes"][max(0, len(data["cur_nodes"]) - step_size): len(data["cur_nodes"])]
                    if len(new_nodes_to_check) < 1:
                        i+=1
                        continue
                    
                    #print("NEW nodes to remove: "+str([n.run_service("GET", "NAME") for n in new_nodes_to_check]))
                    setop = data["setop"]
                    if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                        i+=1
                        continue

                    pset_graph = data["pset_graph"]
                    task_graph = data["task_graph"]
                    priority = setop.run_service("GET", "PRIORITY")
                    
                    # create the new delta_sub graph (prev removed nodes + new nodes to remove)
                    graph_sub = MCATopologyGraphModule("delta_sub")
                    graph_sub.run_service("ADD", "TOPOLOGY_OBJECTS", data["topology_graph_sub"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
                    graph_sub.run_service("ADD", "GRAPH_VERTICES", new_nodes_to_check, assign_graph = False)
                    
                    # create the new delta_add graph (prev added nodes - new nodes to remove)
                    graph_add = MCATopologyGraphModule("delta_add")
                    graph_add.run_service("ADD", "TOPOLOGY_OBJECTS", data["topology_graph_add"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
                    graph_add.run_service("REMOVE", "GRAPH_VERTICES", [n.run_service("GET", "GID") for n in new_nodes_to_check])
                    
                    num_delta = abs(len(graph_add.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)) -\
                                len(graph_sub.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)))

                    input = [data["output"][len(data["output"]) - 1]]

                    model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
                    if None == model:
                        model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

                    o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                         setop, 
                                                         setop.run_service("GET", "INPUT"),
                                                        {"TOPOLOGY_GRAPH_ADD": graph_add,
                                                         "TOPOLOGY_GRAPH_SUB": graph_sub,
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
                    #print("Input "+str(input)+" Output "+str(o_list))
                    #print("EVAL ", input[0].run_service("GET", "NUM_PROCS"), " ", o_list[len(o_list) -1].run_service("GET", "NUM_PROCS"))
                    result = model.run_service("EVAL", "EDGE", input, o_list, ["SPEEDUP"])
                    #print("Result "+str(result))
                    # need to decide how to handle missing metrics
                    # for now ingore setop
                    if None in result.values():
                        #print("SetOp", setop.run_service("GET", "GID"), " ==> Speedup: ", 0)
                        i+=1
                        continue
                    
                    # setop_gains[i] = np.linalg.norm([x for x in result.values()]) / step_size
                    setop_gains[i] = np.mean([x for x in result.values()]) / step_size
                    setop_a_lists[i] = a_list
                    setop_outputs[i] = o_list
                    #print("Setting setop_nodes_to_swap ", i, " "+str(new_nodes_to_check))
                    setop_nodes_to_swap[i] = new_nodes_to_check
                    #print("SetOp", setop.run_service("GET", "GID"), " ==> Normailzed Gain: ", setop_gains[i])
                    i+=1
                    

                # Get the best gain for this setp size over all setops
                gains = [x for x in setop_gains if x != None]
                gain_sub = max(gains) if len(gains) > 0 else -sys.float_info.max
                setop_index_sub = setop_gains.index(gain_sub)
                best_setop_sub = setops_data[setop_index_sub]["setop"]
                gain_sub *= priority

                #print("best gain_sub for step size ", step_size ," ", gain_sub, " by setop ", setop_index_sub)
                if gain_sub == -sys.float_info.max:
                    continue
                ###########################
                # Find best setop to grow #
                ###########################
                #print()
                #print("Searching for swapping mate!")
                #print()
                i = 0
                setop_gains = [-sys.float_info.max for _ in range(num_setops)]
                for data in setops_data:
                    # Don't swap with ourselves
                    if i == setop_index_sub:
                        i+=1
                        continue

                    # Don't swap back 
                    if i == last_swap[0]:
                        i+=1
                        continue

                    setop = data["setop"]
                    if setop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_ORDERED:
                        i+=1
                        continue
                    #print("setop_index_sub for swap ", setop_index_sub)
                    #print("setop_index_sub for swap "+str([n.run_service("GET", "NAME") for n in setop_nodes_to_swap[setop_index_sub]]))
                    pset_graph = data["pset_graph"]
                    task_graph = data["task_graph"]
                    prev_topo = data["topology_graph_add"]
                    input = [data["output"][len(data["output"]) - 1]]
                    priority = setop.run_service("GET", "PRIORITY")

                    # create the new delta_sub graph (prev removed nodes - new nodes to add)
                    graph_sub = MCATopologyGraphModule("delta_sub")
                    graph_sub.run_service("ADD", "TOPOLOGY_OBJECTS", data["topology_graph_sub"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
                    graph_sub.run_service("REMOVE", "GRAPH_VERTICES", [n.run_service("GET", "GID") for n in setop_nodes_to_swap[setop_index_sub]])
                    
                    # create the new delta_add graph (prev added nodes + new nodes to remove)
                    graph_add = MCATopologyGraphModule("delta_add")
                    graph_add.run_service("ADD", "TOPOLOGY_OBJECTS", data["topology_graph_add"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule))
                    graph_add.run_service("ADD", "GRAPH_VERTICES", setop_nodes_to_swap[setop_index_sub], assign_graph = False)
                    

                    input_nodes = input[0].run_service("GET", "ACCESSED_NODES")
                    #print("ADD INPUT NODES = "+str([n.run_service("GET", "NAME") for n in input_nodes]))

                    model = setop.run_service("GET", "PSETOP_MODEL", "USER_MODEL")
                    if None == model:
                        model = setop.run_service("GET", "PSETOP_MODEL", "DEFAULT_MODEL")

                    o_lists, a_lists = model.run_service("GENERATE", "OUTPUT_SPACE", 
                                                         setop, 
                                                         setop.run_service("GET", "INPUT"),
                                                        {"TOPOLOGY_GRAPH_ADD": graph_add,
                                                         "TOPOLOGY_GRAPH_SUB": graph_sub,
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
                    setop_gains[i] = np.mean([x for x in result.values()]) / step_size
                    setop_a_lists[i] = a_list
                    setop_outputs[i] = o_list

                    #print("SetOp", setop.run_service("GET", "NAME"), " ==> Normailzed Gain: ", setop_gains[i])
                    i+=1
                    

                # Get the best gain for this setp size over all setops
                gains = [x for x in setop_gains if x != None]
                gain_add = max(gains) if len(gains) > 0 else -sys.float_info.max 
                setop_index_add = setop_gains.index(gain_add)
                gain_add *= priority
                #print("best gain_add for step size ", step_size ," ", gain_add, " by setop ", setop_index_add)
                
                gain = gain_add + gain_sub


                #print("best gain: ", gain, " setop ", setop_index_sub, " to ", setop_index_add)
                #print()
                if gain > best_gain:
                    #print("UPDATING BEST GAIN FROM ", best_gain, " to ", gain, " by setop ", setop_index_sub)
                    best_gain = gain
                    best_gain_add = gain_add
                    best_gain_sub = gain_sub

                    best_olist_sub = setop_outputs[setop_index_sub]
                    best_a_list_sub = setop_a_lists[setop_index_sub]
                    best_setop_index_sub = setop_index_sub
                    #print("setting INDEX = ", best_setop_index_sub, " NODES "+str([n.run_service("GET", "NAME") for n in setop_nodes_to_swap[setop_index_sub]]))
                    newly_removed_nodes = setop_nodes_to_swap[setop_index_sub]
                    
                    best_olist_add = setop_outputs[setop_index_add]
                    best_a_list_add = setop_a_lists[setop_index_add]
                    best_setop_index_add = setop_index_add
            

            if best_gain <= 0:
                #print("Reached maximum (best gain:)", best_gain)
                # reached maximum
                break

            #print("FOUND SWAP with gain ", best_gain, " and nodes "+ str([n.run_service("GET", "GID") for n in newly_removed_nodes]) + " from ", setops_data[best_setop_index_sub]["setop"].run_service("GET", "GID"), " to ", setops_data[best_setop_index_add]["setop"].run_service("GET", "GID"))
            last_swap = (best_setop_index_sub, best_setop_index_add)
            num_nodes_removed += len(newly_removed_nodes)

            # Update setop for this decision
            setops_data[best_setop_index_sub]["topology_graph_add"].run_service("REMOVE", "GRAPH_VERTICES", [n.run_service("GET", "GID") for n in newly_removed_nodes])
            setops_data[best_setop_index_sub]["topology_graph_sub"].run_service("ADD", "GRAPH_VERTICES", newly_removed_nodes, assign_graph = False)
            setops_data[best_setop_index_sub]["gain"] = best_gain_sub / setops_data[best_setop_index_sub]["setop"].run_service("GET", "PRIORITY")
            setops_data[best_setop_index_sub]["adapted_objects"] = best_a_list_sub
            setops_data[best_setop_index_sub]["output"] = best_olist_sub
            setops_data[best_setop_index_sub]["cur_nodes"] = [n for n in setops_data[best_setop_index_sub]["cur_nodes"] if n not in newly_removed_nodes]

            # Update setop for this decision
            setops_data[best_setop_index_add]["topology_graph_add"].run_service("ADD", "GRAPH_VERTICES", newly_removed_nodes, assign_graph = False)
            setops_data[best_setop_index_add]["topology_graph_sub"].run_service("REMOVE", "GRAPH_VERTICES", [n.run_service("GET", "GID") for n in newly_removed_nodes])
            setops_data[best_setop_index_add]["gain"] = best_gain_add / setops_data[best_setop_index_add]["setop"].run_service("GET", "PRIORITY")
            setops_data[best_setop_index_add]["adapted_objects"] = best_a_list_add
            setops_data[best_setop_index_add]["output"] = best_olist_add
            setops_data[best_setop_index_add]["cur_nodes"].extend(newly_removed_nodes)

            #print("Setop #", best_setop_index_add, " Assigning new nodes: ",
            #      [node.run_service("GET", "NAME") for node in newly_removed_nodes],
            #      "Total nodes: ",
            #       [node.run_service("GET", "NAME") for node in 
            #        setops_data[best_setop_index_add]["topology_graph_add"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)]
            #    ) 
            #
            #print("Setop #", best_setop_index_sub, " Removing nodes: ",
            #      [node.run_service("GET", "NAME") for node in newly_removed_nodes],
            #      "Total nodes: ",
            #       [node.run_service("GET", "NAME") for node in 
            #        setops_data[best_setop_index_sub]["topology_graph_sub"].run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)]
            #    ) 

        setops = [setops_data[i]["setop"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        results = [setops_data[i]["gain"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        outputs = [setops_data[i]["output"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]
        a_lists = [setops_data[i]["adapted_objects"] for i in range(num_setops) if setops_data[i]["gain"] > -sys.float_info.max]


        # Now subsitute all proc placeholders with the real objects (slow)
        new_pset_procs = []
        procs = dict()
        for output,a_list in zip(outputs,a_lists):
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
