from dyn_rm.mca.base.logger.component import MCALoggerComponent
from dyn_rm.mca.base.callback.component import MCACallbackComponent
from dyn_rm.mca.base.system.component.topology import MCATopologyCreationComponent
from dyn_rm.mca.base.graph.component.graph import MCAGraphComponent
from dyn_rm.mca.base.system.component.tasks import MCATaskGraphCreationComponent
from dyn_rm.mca.base.submission.component import MCASubmissionComponent
from dyn_rm.mca.base.event_loop.component import MCAEventLoopComponent
from dyn_rm.mca.base.event_loop.module import MCAEventLoopModule

from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.graph.module.graph import MCAGraphModule
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule
from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule
from dyn_rm.mca.base.system.module.topology import *
from dyn_rm.mca.base.system.module.psets import *
from dyn_rm.mca.base.system.module.tasks import *
from dyn_rm.mca.base.system.module.logging import *


from abc import abstractmethod
from dyn_rm.util.constants import *
from functools import partial

class MCASystemModule(MCAGraphModule):

    PSETOP_NULL            =       0   # Invalid pset operation
    PSETOP_ADD             =       1   # Resources are added
    PSETOP_SUB             =       2   # Resources are removed
    PSETOP_GROW            =       3   # ADD + UNION
    PSETOP_SHRINK          =       4   # SUB + DIFFERENCE
    PSETOP_REPLACE         =       5   # Resources are replaced
    PSETOP_UNION           =       6   # The union of two psets is requested
    PSETOP_DIFFERENCE      =       7   # The difference of two psets is requested
    PSETOP_INTERSECTION    =       8   # The intersection of two psets is requested
    PSETOP_MULTI           =       9  # Multiple operations specified in the info object
    PSETOP_SPLIT           =       10  # Splt operation
    PSETOP_CANCEL          =       11  # Cancel PSet Operations


    PSET_DEFINED_EVENT = 0
    PSETOP_DEFINED_EVENT = 1
    PSETOP_FINALIZED_EVENT = 2
    TASK_TERMINATED_EVENT = 3


    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)

        self.procs = dict()
        self.nodes = dict()
        self.jobs = dict()
        self.psets = dict()
        self.psetops = dict()
        self.time = 0

        if None != parent:
            parent.register_module(self)
        
        self.register_component(MCALoggerComponent(parent = self, enable_output = self.enable_output))
        logger_comp = self.get_component(MCALoggerComponent)
        logger_comp.register_module(MCANodeLogger(parent = logger_comp, enable_output = self.enable_output))
        logger_comp.register_module(MCASetOpLogger(parent = logger_comp, enable_output = self.enable_output))
        logger_comp.register_module(MCASetLogger(parent = logger_comp, enable_output = self.enable_output))
        logger_comp.register_module(MCATaskLogger(parent = logger_comp, enable_output = self.enable_output))

        self.register_component(MCACallbackComponent())
        self.register_component(MCATopologyCreationComponent())
        self.register_component(MCASubmissionComponent())
        self.register_component(MCATaskGraphCreationComponent())
        loop_comp = MCAEventLoopComponent()
        loop_comp.register_module(MCAEventLoopModule())
        self.register_component(loop_comp)
        self.run_component_service(MCAEventLoopComponent, "REGISTER", "EVENT_LOOP", MCAEventLoopModule, "MAIN_LOOP")
        self.run_component_service(MCAEventLoopComponent, "START", "EVENT_LOOP", "MAIN_LOOP")


        self.register_component(MCAGraphComponent())
        topology_graph = MCATopologyGraphModule(self._get_topology_graph_name())         
        self.run_component_service(MCAGraphComponent, "ADD", "GRAPH", self._get_topology_graph_name(), topology_graph)
        
        self.run_service("ADD", "GRAPH_VERTICES", [topology_graph])
        self.run_service("MAKE", "EDGE", [self], [topology_graph])

        MCASystemModule.register_base_services(self)



    @staticmethod
    def register_base_services(self):

        self.register_service("EXECUTE", "IN_LOOP", partial(self.execute_in_loop, "MAIN_LOOP"))

        # Topology
        self.register_service("REGISTER", "TOPOLOGY_CREATION_MODULE", partial(self.execute_in_loop, "MAIN_LOOP", self.get_component(MCATopologyCreationComponent).register_module))  
        self.register_service("CREATE", "SYSTEM_TOPOLOGY", partial(self.execute_in_loop, "MAIN_LOOP", self.create_system_topology))
        self.register_service("SET", "TOPOLOGY_GRAPH", partial(self.execute_in_loop, "MAIN_LOOP", self._set_system_topology))        
        self.register_service("GET", "TOPOLOGY_GRAPH", partial(self.execute_in_loop, "MAIN_LOOP", lambda: self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())))


        # Tasks
        self.register_service("SUBMIT", "TASK_GRAPH", partial(self.execute_in_loop, "MAIN_LOOP", self._submit_task_graph))
        self.register_service("GET", "TASK_GRAPHS", partial(self.execute_in_loop, "MAIN_LOOP", self.get_task_graphs))


        # Psets
        self.register_service("GET", "PSET_GRAPHS", partial(self.execute_in_loop, "MAIN_LOOP", self.get_pset_graphs))
        self.register_service("ADD", "PSETOPS", partial(self.execute_in_loop, "MAIN_LOOP", self.add_psetops))
        self.register_service("APPLY", "PSETOPS", partial(self.execute_in_loop, "MAIN_LOOP", self.apply_psetops))
        self.register_service("FINALIZE", "PSETOP", partial(self.execute_in_loop, "MAIN_LOOP", self.finalize_psetop))

        # Print
        self.register_service("PRINT", "SYSTEM", partial(self.execute_in_loop, "MAIN_LOOP", self.print_system))


        self.register_service("GET", "CORE_IDS", self.get_core_ids)
        self.register_service("GET", "NODE_IDS", self.get_node_ids)

        self.register_service("GET", "CORE", self.get_core)
        self.register_service("GET", "CORES", self.get_cores)
        self.register_service("GET", "NODE", self.get_node)
        self.register_service("GET", "NODES", self.get_nodes)

        self.register_service("ADD", "CORE", self.add_core)
        self.register_service("ADD", "NODE", self.add_node)
        self.register_service("ADD", "CORES", self.add_cores)
        self.register_service("ADD", "NODES", self.add_nodes)

        self.register_service("REMOVE", "NODE", self.add_node)


        #self.register_service("APPLY", "UPDATE", self.apply_setop)


    def execute_in_loop(self, loop_name, func, *args, **kwargs):
        
        # Avoid deadlock we are already running in this loop 
        current_loop = self.run_component_service(MCAEventLoopComponent,
                                                     "GET", "CURRENT_LOOP",
                                                     MCAEventLoopModule)
        if loop_name == current_loop:
            return func(*args, **kwargs) 

        return self.run_component_service(MCAEventLoopComponent,
                                   "RUN", "FUNC", loop_name,
                                   func, *args, **kwargs)

    def _set_system_topology(self, topo_graph):
        # Add the topology graph to our graph component 
        self.run_component_service(MCAGraphComponent, "ADD", "GRAPH",self._get_topology_graph_name(), topo_graph)
    
        # Insert everything into the system graph
        new_objects = []
        new_objects.extend(topo_graph.run_service("GET", "ALL_GRAPH_VERTICES"))
        new_objects.extend(topo_graph.run_service("GET", "ALL_GRAPH_EDGES"))
        for object in new_objects:
            object.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_NEW)
        self.run_service("UPDATE", "GRAPH", new_objects)

        # Finally connect us to the graph roots
        self.run_service("MAKE", "EDGE", [self], [topo_graph])
        
        return DYNRM_SUCCESS


    def get_task_graphs(self):
        return [g for g in self.run_component_service(MCAGraphComponent, "GET", "GRAPHS") if isinstance(g, MCATaskGraphModule)]

    def _submit_task_graph(self, task_graph):
        
        pset_graph = MCAPSetGraphModule()
        pset_graph.run_service("SET", "GID", self._get_new_object_id())
        pset_graph.run_service("ADD", "PSET_MODEL", "DEFAULT_MODEL", MCANullPSetModel())

        # Update Task Status
        tasks = task_graph.run_service("GET", "TASKS")

        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                MCATaskLogger, "TASK_SUBMITTED", 
                tasks)

        if len(tasks) > 0:
            task_graph.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_WAITING)
        else:
            task_graph.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_TERMINATED)

        for t in tasks:
            if t != task_graph and 0 == len(t.run_service("GET", "PREDECESSOR_TASKS")):
                # Task is ready to run
                t.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_READY)

                # create an ADD PSet operation and assign the launch_ouput_generator
                psetop = pset_graph.run_service("CREATE", "PSETOP", MCAPSetopModule.PSETOP_OP_ADD, [pset_graph])
                psetop_model = MCALaunchPsetopModel()
                psetop_model.run_service("SET", "OUTPUT_SPACE_GENERATOR", t.run_service("GET", "TASK_LAUNCH_OUTPUT_SPACE_GENERATOR"))
                psetop.run_service("ADD", "PSETOP_MODEL", "USER_MODEL", psetop_model)

                self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                    MCASetOpLogger, "SETOP_DEFINED", 
                    psetop)


            else:
                # task needs to wait for depenencies
                t.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_WAITING)
        
        # Add the task graph to our task 
        self.run_component_service(MCAGraphComponent, "ADD", "GRAPH", task_graph.run_service("GET", "GID"), task_graph)
        self.run_component_service(MCAGraphComponent, "ADD", "GRAPH", pset_graph.run_service("GET", "GID"), pset_graph)
    
        # Insert everything into the system graph
        new_objects = []
        new_objects.extend(task_graph.run_service("GET", "ALL_GRAPH_VERTICES"))
        new_objects.extend(task_graph.run_service("GET", "ALL_GRAPH_EDGES"))
        new_objects.extend(pset_graph.run_service("GET", "ALL_GRAPH_VERTICES"))
        new_objects.extend(pset_graph.run_service("GET", "ALL_GRAPH_EDGES"))

        for object in new_objects:
            object.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_NEW)
        self.run_service("UPDATE", "GRAPH", new_objects)

        # Finally connect us to the graph roots
        self.run_service("MAKE", "EDGE", [self], [task_graph])
        self.run_service("MAKE", "EDGE", [self], [pset_graph])
        edge = self.run_service("MAKE", "EDGE", [pset_graph], [task_graph])
        edge.run_service("SET", "ATTRIBUTE", MCAPSetModule.PSET_ATTRIBUTE_TASK, True)


        return DYNRM_MCA_SUCCESS


    
    def _get_topology_graph_name(self):
        return self.run_service("GET", "GID") + "/"+"hw"

    def create_system_topology(self, module, object, params):
        graph = self.run_service("GET", "TOPOLOGY_GRAPH")
        
        # Let our topology component create the graph
        self.run_component_service(MCATopologyCreationComponent, "CREATE", "TOPOLOGY_GRAPH", module, graph, object, params)
        
        vertices = graph.run_service("GET", "ALL_GRAPH_VERTICES")
        edges = graph.run_service("GET", "ALL_GRAPH_EDGES")

        # Insert the graph in our graph component
        #self.run_component_service(MCAGraphComponent, "ADD", "GRAPH", self._get_topology_graph_name(), graph)

        # make an edge from us to the hw_topology root
        #edge = MCAEdgeModule()
        #edge.run_service("SET", "GID", self.run_service("GET", "NEW_GID"))

        # insert all vertices and edges in our global graph
        self.run_service("ADD", "GRAPH_VERTICES", vertices)
        self.run_service("ADD", "GRAPH_EDGES", edges)

        return DYNRM_MCA_SUCCESS



    def get_pset_graphs(self):
        return [g for g in self.run_component_service(MCAGraphComponent, "GET", "GRAPHS") if isinstance(g, MCAPSetGraphModule)]

    def add_psetops(self, psetops):
        for psetop in psetops:
            if psetop.run_service("GET", "PSETOP_STATUS") != MCAPSetopModule.PSETOP_STATUS_ORDERED:
                psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_DEFINED)
            pset = psetop.run_service("GET", "INPUT")[0]
            for graph in pset.run_service("GET", "GRAPHS"):
                if isinstance(graph, MCAPSetGraphModule):
                    psetop.run_service("SET", "GID", graph.run_service("GET", "NEW_GID"))
                    graph.run_service("ADD", "PSETOPS", [psetop])
        
        
        self.run_service("UPDATE", "GRAPH", psetops)
        return DYNRM_MCA_SUCCESS

    def apply_psetops(self, psetops, output_lists, adapted_objects_lists):
        adapted_objects = dict()
        
        adapted_statuses = {    MCAGraphObjectModule.STATUS_NEW, 
                                MCAGraphObjectModule.STATUS_ADD,
                                MCAGraphObjectModule.STATUS_UPDATE,
                                MCAGraphObjectModule.STATUS_DELETE
                            }
        

        # Todo: Add Psets, Membership Edge and Procs to Pset Graph
        # Todo: Go over vertices/edges in adapted objects and add all edges/vertices with NEW/UPDATE STATUS
                # -> Then throw it into graph update
        # Loop over all psetops
        for psetop, output_list, adapted_objects_list in zip(psetops, output_lists, adapted_objects_lists):
            sys_psetop = self.run_service("GET", "GRAPH_EDGE", psetop.run_service("GET", "GID"))

            # Get the pset graph for this psetop
            pset_graph = psetop.run_service("GET", "PSET_GRAPH")
            if None == pset_graph:
                return DYNRM_MCA_ERR_NOT_FOUND

            # Get the task graph for this psetop
            task_graph = pset_graph.run_service("GET", "TASK")
            if None == pset_graph:
                return DYNRM_MCA_ERR_NOT_FOUND
            
            # Assign GIDs for any new objects
            for object in adapted_objects_list:
                if object.run_service("GET", "GID") == MCAGraphObjectModule.GRAPH_OBJECT_DEFAULT_GID:
                    self._assign_subgid(pset_graph, task_graph, None, object)

            psetop.run_service("SET", "OUTPUT", output_list)
            if psetop.run_service("GET", "PSETOP_STATUS") == MCAPSetopModule.PSETOP_STATUS_DEFINED:
                psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_PENDING)

            for output in output_list:
                output.run_service("ADD", "IN_EDGE", psetop)

            extended_adapted_objects = {o.run_service("GET", "GID"): o for o in adapted_objects_list}
            for object in adapted_objects_list:
                if isinstance(object, MCAVertexModule):
                    edges = object.run_service("GET", "EDGES")
                    for edge in edges:
                        if edge.run_service("GET", "STATUS") in adapted_statuses and \
                        edge.run_service("GET", "GID") not in extended_adapted_objects:

                            # Assign GIDs for any new objects
                            if edge.run_service("GET", "GID") == MCAGraphObjectModule.GRAPH_OBJECT_DEFAULT_GID:
                                self._assign_subgid(pset_graph, task_graph, None, edge)
                            extended_adapted_objects[edge.run_service("GET", "GID")] = edge
                elif isinstance(object, MCAEdgeModule):
                    vertices = object.run_service("GET", "INPUT") + object.run_service("GET", "OUTPUT")
                    for vertex in vertices:
                        if vertex.run_service("GET", "STATUS") in adapted_statuses and \
                        vertex.run_service("GET", "GID") not in extended_adapted_objects:
                            # Assign GIDs for any new objects
                            if vertex.run_service("GET", "GID") == MCAGraphObjectModule.GRAPH_OBJECT_DEFAULT_GID:
                                self._assign_subgid(pset_graph, task_graph, None, vertex)
                            extended_adapted_objects[vertex.run_service("GET", "GID")] = vertex

            # Update the pset graph for this psetop
            pset_graph_updates = []
            for gid in extended_adapted_objects.keys():
                object = extended_adapted_objects[gid]
                if isinstance(object, MCAPsetGraphObject):
                    pset_graph_updates.append(object)
            pset_graph.run_service("UPDATE", "GRAPH", pset_graph_updates, update_statuses = False)
            # Update the task graph for this psetop
            task_graph_updates = []
            for gid in extended_adapted_objects.keys():
                object = extended_adapted_objects[gid]

                if isinstance(object, MCATaskGraphObject):
                    task_graph_updates.append(object)
            task_graph.run_service("UPDATE", "GRAPH", task_graph_updates, update_statuses = False)

            adapted_objects.update(extended_adapted_objects)

        self.run_service("UPDATE", "GRAPH", list(adapted_objects.values()))
        return DYNRM_MCA_SUCCESS


    def _assign_subgid(self, pset_graph, task_graph, topo_graph, object):

        if object.run_service("GET", "STATUS"):
            if isinstance(object, MCAPsetGraphObject):
                object.run_service("SET", "GID", pset_graph.run_service("GET", "NEW_GID"))
            elif isinstance(object, MCATaskGraphObject):
                object.run_service("SET", "GID", task_graph.run_service("GET", "NEW_GID"))
            elif isinstance(object, MCATopologyGraphObject):
                object.run_service("SET", "GID", topo_graph.run_service("GET", "NEW_GID"))
            else:
                object.run_service("SET", "GID", self.run_service("GET", "NEW_GID"))
        return DYNRM_MCA_SUCCESS

    def finalize_task(self, task_id):

        task = self.run_service("GET", "GRAPH_VERTEX", task_id)
        task.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_TERMINATED)

        task_graph = task.run_service("GET", "TASK_GRAPH")
        pset_graph = task_graph.run_service("GET", "PSETS")[0]
        
        # Set Proc Status
        nodes = dict()
        procs = task.run_service("GET", "PROCS")
        for proc in procs:
            proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_TERMINATED)
            cores = proc.run_service("GET", "CORE_ACCESS")
            if len(cores) > 0:
                for core in cores:
                    node = core.run_service("GET", "NODE")
                    nodes[node.run_service("GET", "GID")] = node
                
        # TODO: LOG NODES
        self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                MCANodeLogger, "NODE_OCCUPATION_CHANGED", 
                list(nodes.values()))        

        last_pset = None
        last_pset_index = 0
        psets = task.run_service("GET", "PSETS")
        for pset in psets:

            index = int(pset.run_service("GET", "GID").split('/')[-1])
            if index > last_pset_index:
                last_pset_index = index
                last_pset = pset

            psetops = pset.run_service("GET", "EDGES_BY_FILTER", lambda e: isinstance(e, MCAPSetopModule))
            for psetop in psetops:
                status = psetop.run_service("GET", "PSETOP_STATUS")
                if  status != MCAPSetopModule.PSETOP_STATUS_CANCELED and\
                    status != MCAPSetopModule.PSETOP_STATUS_FINALIZED:
                
                    psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_FINALIZED)
        

        self.run_component_service( MCALoggerComponent, "LOG", "EVENT",
                MCATaskLogger, "TASK_TERMINATED", 
                task)

        # Start successor tasks
        ready_successors = dict()
        successors = task.run_service("GET", "SUCCESOR_TASKS")
        for successor in successors:
            if successor.run_service("GET", "TASK_STATUS") != MCATaskModule.TASK_STATUS_WAITING:
                continue
            preds = successor.run_service("GET", "PREDECESSOR_TASKS")
            all_satisfied = True
            for pred in preds:
                if pred.run_service("GET", "TASK_STATUS") != MCATaskModule.TASK_STATUS_TERMINATED:
                    all_satisfied = False
                    break
            if all_satisfied:
                # This means the whole task graph has been completed
                if successor == task_graph:
                    task_graph.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_TERMINATED)
                else:
                    ready_successors[successor.run_service("GET", "GID")] = successor
        
        new_psetops = []
        for successor in ready_successors.values():
            successor.run_service("SET", "TASK_STATUS", MCATaskModule.TASK_STATUS_READY)

            # create an ADD PSet operation and assign the launch_ouput_generator
            psetop = pset_graph.run_service("CREATE", "PSETOP", MCAPSetopModule.PSETOP_OP_ADD, [pset_graph])
            psetop_model = MCALaunchPsetopModel()
            psetop_model.run_service("SET", "OUTPUT_SPACE_GENERATOR", successor.run_service("GET", "TASK_LAUNCH_OUTPUT_SPACE_GENERATOR"))
            psetop.run_service("ADD", "PSETOP_MODEL", "USER_MODEL", psetop_model)

            new_psetops.append(psetop)
        
        if last_pset != None:
            sub_model = MCATerminatePsetopModel()
            sub_model.run_service("SET", "OUTPUT_SPACE_GENERATOR", output_space_generator_term)
            sub_setop = MCAPSetopModule("sub_psetop", MCAPSetopModule.PSETOP_OP_SUB, [last_pset])
            sub_setop.run_service("ADD", "PSETOP_MODEL", "USER_MODEL", sub_model)
            sub_setop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_ORDERED)
            new_psetops.append(sub_setop)

        self.add_psetops(new_psetops)
        #self.run_service("UPDATE", "GRAPH", new_psetops)

        if len(new_psetops) > 0:
            self.run_component_service( MCALoggerComponent, "LOG", "EVENTS",
                    MCASetOpLogger, "SETOP_DEFINED", 
                    new_psetops)

        rc = self.run_component_service(MCACallbackComponent, "BCAST", "EVENT", MCASystemModule.TASK_TERMINATED_EVENT, self, task)
        if rc != DYNRM_MCA_SUCCESS:
            print("System Bcast event 'PSETOP_DEFINED' failed ", rc)
        
        return rc

    def finalize_psetop(self, psetop_id):
        psetop = self.run_service("GET", "GRAPH_EDGE", psetop_id)
        psetop.run_service("SET", "PSETOP_STATUS", MCAPSetopModule.PSETOP_STATUS_FINALIZED)
        psets = psetop.run_service("GET", "OUTPUT")
        #print("FINALIZING PSETOP: "+psetop.run_service("GET", "GID"))

        for pset in psets:
            procs = pset.run_service("GET", "PROCS")
            for proc in procs:
                if proc.run_service("GET", "PROC_STATUS") == MCAProcModule.PROC_STATUS_LAUNCH_REQUESTED:
                   proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_RUNNING) 
                elif proc.run_service("GET", "PROC_STATUS") == MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED:
                   proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_TERMINATED) 

        if psetop.run_service("GET", "PSETOP_OP") == MCAPSetopModule.PSETOP_OP_SUB:
            pset = psetop.run_service("GET", "INPUT")[0]
            procs = pset.run_service("GET", "PROCS")
            for proc in procs:
                if proc.run_service("GET", "PROC_STATUS") != MCAProcModule.PROC_STATUS_TERMINATED:
                   proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_TERMINATED) 

        return DYNRM_MCA_SUCCESS

    def print_system(self):
        print("=============================")
        print("=========== SYSTEM ==========")
        print("=============================")

        topo_graph = self.run_service("GET", "TOPOLOGY_GRAPH")
        if None == topo_graph:
            print("===== NO TOPOLOGY GRAPH =====")
        else:
            topo_graph.run_service("PRINT", "TOPOLOGY_GRAPH")
            
        pset_graphs = self.run_service("GET", "PSET_GRAPHS")
        for pset_graph in pset_graphs:
            task_graph = pset_graph.run_service("GET", "TASK")
            task_graph.run_service("PRINT", "TASK_GRAPH")
            pset_graph.run_service("PRINT", "PSET_GRAPH")


        print("=============================")
        print("=============================")
        print("=============================")

        return DYNRM_MCA_SUCCESS



    def add_core(self, core):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        return hw_graph.run_service("UPDATE", "GRAPH", [core])

    def add_node(self, node):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        return hw_graph.run_service("UPDATE", "GRAPH", [node])

    def add_cores(self, cores):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        return hw_graph.run_service("UPDATE", "GRAPH", cores)

    def add_nodes(self, nodes):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        return hw_graph.run_service("UPDATE", "GRAPH", nodes)


    def get_core_ids(self):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return []
        cores = hw_graph.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
        return [c.run_service("GET", "GID") for c in cores]

    def get_node_ids(self):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return []
        nodes = hw_graph.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
        return [n.run_service("GET", "GID") for n in nodes]

    def get_core(self, id):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return None
        return hw_graph.run_service("GET", "GRAPH_VERTEX", id)

    def get_node(self, id):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return []
        return hw_graph.run_service("GET", "GRAPH_VERTEX", id)


    def get_cores(self):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return []
        return hw_graph.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCACoreModule))

    def get_nodes(self):
        hw_graph = self.run_component_service(MCAGraphComponent, "GET", "GRAPH", self._get_topology_graph_name())
        if None == hw_graph:
            return []
        return hw_graph.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    def get_node(self, id):
        return self.run_service("GET", "GRAPH_VERTEX", id)

    def get_node(self, id):
        return self.run_service("GET", "GRAPH_VERTEX", id)

    def remove_core(self, id):
        core = self.run_service("GET", "GRAPH_VERTEX", id)
        core.run_service("SET", "STATUS", MCAVertexModule.MCA_VERTEX_STATUS_INVALID)
        return self.run_service("UPDATE", "GRAPH", [core])

    def remove_node(self, id):
        node = self.run_service("GET", "GRAPH_VERTEX", id)
        node.run_service("SET", "STATUS", MCAVertexModule.MCA_VERTEX_STATUS_INVALID)
        return self.run_service("UPDATE", "GRAPH", [node])


