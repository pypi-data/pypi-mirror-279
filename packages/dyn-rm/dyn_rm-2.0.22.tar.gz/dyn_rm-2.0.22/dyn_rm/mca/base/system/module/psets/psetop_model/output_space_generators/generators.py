from dyn_rm.mca.base.system.module.topology.node import MCANodeModule

def output_space_generator_term(setop, 
                                   input, 
                                   graphs):

    pset_graph = graphs["PSET_GRAPH"]
    topology_graph_add = graphs["TOPOLOGY_GRAPH_ADD"]
    topology_graph_sub = graphs["TOPOLOGY_GRAPH_SUB"]
    
    nodes_add = topology_graph_add.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
    nodes_sub = topology_graph_sub.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    if len(nodes_add) > 0:
        return [], []
    
    cur_nodes = input[0].run_service("GET", "ACCESSED_NODES")
    if set([n.run_service("GET", "GID") for n in cur_nodes]) != set([n.run_service("GET", "GID") for n in nodes_sub]):
        return [],[]
    return [[pset_graph]], [[]]