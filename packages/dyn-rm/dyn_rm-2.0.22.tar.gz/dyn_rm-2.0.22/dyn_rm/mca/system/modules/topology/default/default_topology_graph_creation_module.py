from dyn_rm.mca.base.system.module.topology.topology_creation import MCATopologyCreationModule
from dyn_rm.mca.base.system.module.topology.node import MCANodeModule
from dyn_rm.mca.base.system.module.topology.core import MCACoreModule
from dyn_rm.util.constants import *

from abc import abstractmethod
import itertools

import yaml

class DefaultTopologyGraphCreationModule(MCATopologyCreationModule):

    # Creates a Topology Graph and adds it to the system
    def create_topology_graph_function(self, graph, object, params):

        
        # read yaml file
        with open(object) as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

            cores = dict()
            nodes = dict()
            index = 0
            # create node and core objects based on the description in the yaml file
            node_dicts = yaml_dict["topology"]["nodes"]
            for node_name in node_dicts.keys():

                #create the node object
                node = MCANodeModule(node_name)
                # Optional: Add node attributes:
                # node.run_service("SET", "ATTRIBUTE", "key", "value")
                nodes[node_name] = node

                # create the core objects
                num_cores = node_dicts[node_name]["num_cores"]
                cores[node_name] = []
                for n in range(num_cores):
                    cores[node_name].append(MCACoreModule(str(index)))
                    index += 1

            # Add all nodes and cores to the topology graph
            graph.run_service("ADD", "TOPOLOGY_OBJECTS", list(nodes.values()))
            graph.run_service("ADD", "TOPOLOGY_OBJECTS", [core for core_set in cores.values() for core in core_set ])
            
            # create containment relations to associate nodes and cores
            index = 0
            for node_name in nodes.keys():
                graph.run_service("ADD", "CONTAINMENT_RELATION", nodes[node_name], cores[node_name])

        return graph
    

    def update_topology_graph_function(self, mix, system, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED
    
    def create_object_from_graph_function(self, graph, params):
        return DYNRM_MCA_ERR_NOT_IMPLEMENTED

