from dyn_rm.mca.base.graph.component.edge import MCAEdgeComponent
from dyn_rm.mca.base.graph.module.edge import MCAEdgeModule

from dyn_rm.mca.base.graph.component.vertex import MCAVertexComponent
from dyn_rm.mca.base.graph.module.vertex import MCAVertexModule

from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule

from dyn_rm.util.constants import *

class MCAGraphModule(MCAVertexModule):

    def __init__(self, parent = None, parent_dir = ".", verbosity = 0, enable_output = False):
        super().__init__(parent = parent, parent_dir = parent_dir, verbosity = verbosity, enable_output = enable_output)
        self.register_component(MCAVertexComponent())
        self.register_component(MCAEdgeComponent())
        self._root = self
        MCAGraphModule.register_base_services(self)
        self.run_service("ADD", "GRAPH_VERTICES", [self])

    @staticmethod    
    def register_base_services(self):
        
        self.register_service("SET", "ROOT", self.get_root)
        self.register_service("GET", "ROOT", self.get_root)
        
        self.register_service("ADD", "GRAPH_VERTICES", self.add_vertices)
        self.register_service("ADD", "GRAPH_EDGES", self.add_edges)

        self.register_service("MAKE", "EDGE", self.make_edge)

        self.register_service("GET", "GRAPH_VERTEX", self.get_graph_vertex)
        self.register_service("GET", "GRAPH_EDGE", self.get_graph_edge)
        self.register_service("GET", "GRAPH_VERTICES", self.get_graph_vertices)
        self.register_service("GET", "ALL_GRAPH_VERTICES", self.get_all_vertices)
        self.register_service("GET", "GRAPH_EDGES", self.get_graph_edges)
        self.register_service("GET", "ALL_GRAPH_EDGES", self.get_all_edges)
        self.register_service("GET", "GRAPH_VERTICES_BY_FILTER", self.get_vertices_by_filter)
        self.register_service("GET", "GRAPH_EDGES_BY_FILTER", self.get_edges_by_filter)
        self.register_service("GET", "GRAPH_EDGES_IN_SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)
        self.register_service("GET", "GRAPH_VERTICES_IN_SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)                
        self.register_service("GET", "SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)

        self.register_service("REMOVE", "GRAPH_VERTICES", self.remove_vertices)
        self.register_service("REMOVE", "GRAPH_EDGES", self.remove_edges)
        self.register_service("REMOVE", "GRAPH_VERTICES_BY_FILTER", self.remove_graph_vertices_by_filter)
        self.register_service("REMOVE", "GRAPH_EDGES_BY_FILTER", self.remove_graph_edges_by_filter)
        self.register_service("REMOVE", "GRAPH_EDGES_IN_SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)
        self.register_service("REMOVE", "GRAPH_VERTICES_IN_SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)                
        self.register_service("REMOVE", "SUBGRAPH_BY_FILTER", self.get_edges_in_subgraph_by_filter)

        self.register_service("UPDATE", "GRAPH", self.update_graph)


    def set_root(self, root):
        rc = self.run_component_service(MCAVertexComponent, "ADD", "VERTEX", root)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        self._root = root
        return DYNRM_MCA_SUCCESS
    
    def get_root(self):
        return self._root


    ##### ADD #####
    def add_vertex(self, vertex, assign_graph = True):
        vertex_name = vertex.run_service("GET", "GID")
        if vertex_name == "MCAGraphObject:/":
            vertex.run_service("SET", "GID", self.run_service("GET", "NEW_GID"))
        rc = self.run_component_service(MCAVertexComponent, "ADD", "VERTEX", vertex)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        if assign_graph:
            vertex.run_service("ADD", "GRAPH", self)
        return DYNRM_MCA_SUCCESS

    def add_edge(self, edge):
        edge_name = edge.run_service("GET", "GID")
        if edge_name == "MCAGraphObject:/":
            edge.run_service("SET", "GID", self.run_service("GET", "NEW_GID"))
        rc = self.run_component_service(MCAEdgeComponent, "ADD", "EDGE", edge)
        if rc != DYNRM_MCA_SUCCESS:
            return rc
        edge.run_service("ADD", "GRAPH", self)
        return DYNRM_MCA_SUCCESS  

    def add_vertices(self, vertices, assign_graph = True):
        for vertex in vertices:
            self.add_vertex(vertex, assign_graph = assign_graph)
        return DYNRM_MCA_SUCCESS

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)
        return DYNRM_MCA_SUCCESS
    
    ##### MAKE #####
    def make_edge(self, input, output):
        gid = self.run_service("GET", "NEW_GID")
        edge = MCAEdgeModule()
        edge.run_service("SET", "INPUT", input)
        edge.run_service("SET", "OUTPUT", output)
        edge.run_service("SET", "GID", gid)

        self.add_edge(edge)

        for v_in in input:
            v_in.run_service("ADD", "OUT_EDGE", edge)
        for v_out in output:
            v_out.run_service("ADD", "IN_EDGE", edge)
        return edge
      

    ##### GET ##### 
    def get_graph_vertex(self, name):
        return self.run_component_service(MCAVertexComponent, "GET", "VERTEX", name) 

    def get_graph_vertices(self, names):
        return self.run_component_service(MCAVertexComponent, "GET", "VERTICES", names)

    def get_all_vertices(self):
        return self.run_component_service(MCAVertexComponent, "GET", "ALL_VERTICES")

    def get_graph_edge(self, name):
        return self.run_component_service(MCAEdgeComponent, "GET", "EDGE", name)
    
    def get_graph_edges(self, names):
        return self.run_component_service(MCAEdgeComponent, "GET", "EDGES", names)

    def get_all_edges(self):
        return self.run_component_service(MCAEdgeComponent, "GET", "ALL_EDGES")

    def get_vertices_by_filter(self, vertex_filter):
        return self.run_component_service(MCAVertexComponent, "GET", "VERTICES_BY_FILTER", vertex_filter)

    def get_edges_by_filter(self, edge_filter):
        return self.run_component_service(MCAEdgeComponent, "GET", "EDGES_BY_FILTER", edge_filter)

    ##### REMOVE #####
    def remove_vertex(self, name):
        vertex = self.run_component_service(MCAVertexComponent, "REMOVE", "VERTEX", name)
        if None != vertex:
            vertex.run_service("REMOVE", "GRAPH", self.get_name())
        return vertex

    def remove_vertices(self, names):
        for name in names:
            self.remove_vertex(name)
        return DYNRM_MCA_SUCCESS

    def remove_edge(self, name):
        return self.run_component_service(MCAEdgeComponent, "REMOVE", "EDGE", name)

    def remove_edges(self, names):
        return self.run_component_service(MCAEdgeComponent, "REMOVE", "EDGES", names)

    def remove_graph_vertices_by_filter(self, vertex_filter):
        return self.run_component_service(MCAEdgeComponent, "REMOVE", "VERTICES_BY_FILTER", vertex_filter)


    def remove_graph_edges_by_filter(self, edge_filter):
        return self.run_component_service(MCAEdgeComponent, "REMOVE", "EDGES_BY_FILTER", edge_filter)


    ##### SUBGRAPHS #####
    def get_vertices_in_subgraph_by_filter(self, name, vertex, vertex_filter):
        if name not in self.graphs:
            return DYNRM_MCA_ERR_NOT_FOUND
        vertices, edges = self.get_subgraph_by_filter(name, vertex, vertex_filter, lambda x: True)
        return vertices

    def get_edges_in_subgraph_by_filter(self, name, vertex, edge_filter):
        if name not in self.graphs:
            return DYNRM_MCA_ERR_NOT_FOUND
        vertices, edges = self.get_subgraph_by_filter(name, vertex, lambda x: True, edge_filter)
        return edges

    # Subgraph Operations
    def get_subgraph_by_filter(self, name, vertex_filter, edge_filter):
        subgraph_vertices = []
        subgraph_edges = [] 
        next_vertices = [vertex]
        next_edges = []
        num_vertices = 1
        while num_vertices > 0:
            num_vertices = len(next_vertices)
            for i in range(num_vertices):
                vertex = next_vertices.pop(0)
                if vertex_filter(vertex):
                    subgraph_vertices.append(vertex)
                    edges = vertex.run_service("GET", "EDGES")
                    for edge in edges:
                        if edge not in subgraph_edges:
                            dir = "OUT" if vertex in edge.run_service("GET", "INPUT") else "IN"
                            next_edges.append((dir, edge))
            num_edges = len(next_edges)
            for i in range(num_edges):
                dir, edge = next_edges.pop(0)
                if edge_filter(edge):
                    subgraph_edges.append(edge)
                    if dir == "OUT":
                        vertices = edge.run_service("GET", "OUTPUT")
                    else: 
                        vertices = edge.run_service("GET", "INPUT")
                    for vertex in vertices:
                        if vertex not in subgraph_vertices:
                            next_vertices.append(vertex)



    def remove_vertices_in_subgraph_by_filter(self, name, vertex, vertex_filter):
        if name not in self.graphs:
            return DYNRM_MCA_ERR_NOT_FOUND
        vertices = self.get_vertices_in_subgraph_by_filter(name, vertex, vertex_filter)
        self.remove_vertices([v.run_service("GET", "GID") for v in vertices]) 
        return DYNRM_MCA_SUCCESS


    def get_edges_in_subgraph_by_filter(self, name, vertex, edge_filter):
        if name not in self.graphs:
            return DYNRM_MCA_ERR_NOT_FOUND
        edges = self.get_edges_in_subgraph_by_filter(name, vertex, edge_filter)
        self.remove_edges([e.run_service("GET", "GID") for e in edges]) 
        return DYNRM_MCA_SUCCESS

    # Subgraph Operations
    def remove_subgraph_by_filter(self, name, vertex, vertex_filter, edge_filter):
        if name not in self.graphs:
            return DYNRM_MCA_ERR_NOT_FOUND
        vertices, edges = self.get_subgraph_by_filter(name, vertex, vertex_filter, edge_filter)
        self.remove_vertices([v.run_service("GET", "GID") for v in vertices]) 
        self.remove_edges([e.run_service("GET", "GID") for e in edges]) 
        return DYNRM_MCA_SUCCESS  



    ###### GRAPH UPDATES #####
    def update_graph(self, objects, update_statuses = True):

        # Nothing to do
        if 0 == len(objects):
            return DYNRM_MCA_SUCCESS            
 
        vertices = dict()
        edges = dict()

        vertices = {v.run_service("GET", "GID"): v  for v in objects if isinstance(v, MCAVertexModule)}
        edges = {e.run_service("GET", "GID"): e for e in objects if isinstance(e, MCAEdgeModule)}

        # Step 0 
        # Add all edges of new/updated vertices which are not in the adapted objects list
        # We need to do this as users could create vertices and add edges via some special API, without knowing about it
        # This only holds for edges pointing to vertices presented in or to be added to the own graph 
        for vertex in vertices.values():
            vertex_edges = vertex.run_service("GET", "IN_EDGES")
            for vertex_edge in vertex_edges:
                if  vertex_edge.run_service("GET", "STATUS") != MCAGraphObjectModule.STATUS_ADD and \
                    vertex_edge.run_service("GET", "STATUS") != MCAGraphObjectModule.STATUS_UPDATE:
                    continue

                # This edge is new, or updated. Check if the one of the output vertices is in the old or new graph
                in_vertex_names = [v.run_service("GET", "GID") for v in vertex_edge.run_service("GET", "INPUT")]
                for name in in_vertex_names:
                    if None != self.get_graph_edge(name) or name in vertices.keys():
                        edges[vertex_edge.run_service("GET", "GID")] = vertex_edge
            
            vertex_edges = vertex.run_service("GET", "OUT_EDGES")
            for vertex_edge in vertex_edges:
                if  vertex_edge.run_service("GET", "STATUS") != MCAGraphObjectModule.STATUS_ADD and \
                    vertex_edge.run_service("GET", "STATUS") != MCAGraphObjectModule.STATUS_UPDATE:
                    continue

                # This edge is new, or updated. Check if the one of the output vertices is in the old or new graph
                out_vertex_names = [v.run_service("GET", "GID") for v in vertex_edge.run_service("GET", "OUTPUT")]
                for name in out_vertex_names:
                    if None != self.get_graph_edge(name) or name in vertices.keys():
                        edges[vertex_edge.run_service("GET", "GID")] = vertex_edge
            
        # Step 1:
        # Make sure that all new vertices/edges refer to the updated version of vertices/edges
        for edge_name in edges.keys():
            input = edges[edge_name].run_service("GET", "INPUT")
            output = edges[edge_name].run_service("GET", "OUTPUT")
            for index in range(len(input)):
                name = input[index].run_service("GET", "GID")
                if name in vertices:
                    edges[edge_name].run_service("SET", "INPUT_AT_INDEX", index, vertices[name])

            for index in range(len(output)):
                name = output[index].run_service("GET", "GID")
                if name in vertices:
                    edges[edge_name].run_service("SET", "OUTPUT_AT_INDEX", index, vertices[name])

        for vertex_name in vertices.keys():
            in_edges = vertices[vertex_name].run_service("GET", "IN_EDGES")
            for edge in in_edges:
                edge_name = edge.run_service("GET", "GID")
                if edge_name in edges.keys():
                    vertices[vertex_name].run_service("REMOVE", "IN_EDGE", edge_name)
                    vertices[vertex_name].run_service("ADD", "IN_EDGE", edges[edge_name])

            out_edges = vertices[vertex_name].run_service("GET", "OUT_EDGES")
            for edge in out_edges:
                edge_name = edge.run_service("GET", "GID")
                if edge_name in edges:
                    vertices[vertex_name].run_service("REMOVE", "OUT_EDGE", edge_name)
                    vertices[vertex_name].run_service("ADD", "OUT_EDGE", edges[edge_name])


        # Step 2: store all adjacent vertices/edges of updated edges/vertices from the old graph
        # We need to make sure that all updates are reflected in the graph
        # ignore vertices/edges not part of the original or updated graph
        old_vertex_edges = dict()
        for vertex_name in vertices.keys():
            old_vertex = self.get_graph_vertex(vertex_name)
            old_vertex_edges[vertex_name] = {"IN_EDGES" : dict(), "OUT_EDGES" : dict()}
            if None == old_vertex:
                continue
            in_edges = old_vertex.run_service("GET", "IN_EDGES")
            for edge in in_edges:
                in_edge_name = edge.run_service("GET", "GID")
                # ########
                if None == self.get_graph_edge(in_edge_name):
                    continue
                old_vertex_edges[vertex_name]["IN_EDGES"][in_edge_name] = edge
            out_edges = old_vertex.run_service("GET", "OUT_EDGES")
            for edge in out_edges:
                out_edge_name = edge.run_service("GET", "GID")
                # ########
                if None == self.get_graph_edge(out_edge_name):
                    continue
                old_vertex_edges[vertex_name]["OUT_EDGES"][out_edge_name] = edge

        old_edge_vertices = dict()
        for edge_name in edges.keys():
            old_edge = self.get_graph_edge(edge_name)
            old_edge_vertices[edge_name] = {"INPUT" : dict(), "OUTPUT" : dict()}
            if old_edge == None:
                continue            
            input_vertices = old_edge.run_service("GET", "INPUT")
            for in_vertex in input_vertices:
                in_vertex_name = in_vertex.run_service("GET", "GID")
                # ########
                if None == self.get_graph_vertex(in_vertex_name):
                    continue
                old_edge_vertices[edge_name]["INPUT"][in_vertex_name] = in_vertex
            output_vertices = old_edge.run_service("GET", "OUTPUT")
            for out_vertex in output_vertices:
                out_vertex_name = out_vertex.run_service("GET", "GID")
                # ########
                if None == self.get_graph_vertex(out_vertex_name):
                    continue
                old_edge_vertices[edge_name]["OUTPUT"][out_vertex_name] = out_vertex

        # Step 3: store all adjacent vertices/edges of updated edges/vertices from the new graph
        # We need to make sure that all updates are reflected in the graph
        new_vertex_edges = dict()
        for new_vertex in vertices.values():
            vertex_name = new_vertex.run_service("GET", "GID")
            new_vertex_edges[vertex_name] = {"IN_EDGES" : dict(), "OUT_EDGES" : dict()}

            # This one will be removed
            if  new_vertex.run_service("GET", "STATUS") == MCAGraphObjectModule.STATUS_DELETE or \
                new_vertex.run_service("GET", "STATUS") == MCAGraphObjectModule.STATUS_INVALID:
                continue

            in_edges = new_vertex.run_service("GET", "IN_EDGES")
            for edge in in_edges:
                in_edge_name = edge.run_service("GET", "GID")
                # #########
                if None == self.get_graph_edge(in_edge_name) and None == edges.get(in_edge_name):
                    continue
                new_vertex_edges[vertex_name]["IN_EDGES"][in_edge_name] = edge
            out_edges = new_vertex.run_service("GET", "OUT_EDGES")
            for edge in out_edges:
                out_edge_name = edge.run_service("GET", "GID")
                # #########
                if None == self.get_graph_edge(out_edge_name) and None == edges.get(out_edge_name):
                    continue
                new_vertex_edges[vertex_name]["OUT_EDGES"][out_edge_name] = edge

        new_edge_vertices = dict()
        for new_edge in edges.values():
            edge_name = new_edge.run_service("GET", "GID")
            new_edge_vertices[edge_name] = {"INPUT" : dict(), "OUTPUT" : dict()}

            # This one will be removed
            if new_edge.run_service("GET", "STATUS") == MCAGraphObjectModule.STATUS_DELETE or \
               new_edge.run_service("GET", "STATUS") == MCAGraphObjectModule.STATUS_INVALID:
                continue

            input_vertices = new_edge.run_service("GET", "INPUT")
            for in_vertex in input_vertices:
                in_vertex_name = in_vertex.run_service("GET", "GID")
                # #########
                if None == self.get_graph_vertex(in_vertex_name) and None == vertices.get(in_vertex_name):
                    continue
                new_edge_vertices[edge_name]["INPUT"][in_vertex_name] = in_vertex
            output_vertices = new_edge.run_service("GET", "OUTPUT")
            for out_vertex in output_vertices:
                out_vertex_name = out_vertex.run_service("GET", "GID")
                # #########
                if None == self.get_graph_vertex(out_vertex_name) and None == vertices.get(out_vertex_name):
                    continue
                new_edge_vertices[edge_name]["OUTPUT"][out_vertex_name] = out_vertex
                # #########

        # Step 4:  Update the graph
        for vertex in vertices.values():
            vertex_status = vertex.run_service("GET", "STATUS")
            if  vertex_status == MCAGraphObjectModule.STATUS_DELETE or \
                vertex_status == MCAGraphObjectModule.STATUS_INVALID:
                if update_statuses:
                    vertex.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_INVALID)
                self.remove_vertex(vertex)
            else:
                if update_statuses:
                    vertex.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_VALID)
                self.add_vertex(vertex)
        for edge in edges.values():
            edge_status = edge.run_service("GET", "STATUS")
            if  edge_status == MCAGraphObjectModule.STATUS_DELETE or \
                edge_status == MCAGraphObjectModule.STATUS_INVALID:
                if update_statuses:
                    edge.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_INVALID)
                self.remove_edge(edge.run_service("GET", "GID"))
            else:
                if update_statuses:
                    edge.run_service("SET", "STATUS", MCAGraphObjectModule.STATUS_VALID)
                self.add_edge(edge)

        # Step 5: Ensure all updates are resembled in adjacent vertices/edges 
        # 5.1: Update edge_ouputs
        for vertex_name in vertices.keys():
            old_in_edges = old_vertex_edges[vertex_name]["IN_EDGES"].values()    
            new_in_edges = new_vertex_edges[vertex_name]["IN_EDGES"].values()
            for old_in_edge in old_in_edges:
                name = old_in_edge.run_service("GET", "GID")
                
                if name not in [e.run_service("GET", "GID") for e in new_in_edges]:
                    # This in_edge is not in the new vertex anymore
                    # remove the vertex from the edge_output if it is still there
                    edge = self.get_graph_edge(name)
                    if None == edge:
                        continue
                    index = edge.run_service("GET", "INDEX_IN_OUTPUT", vertex_name)
                    if index == -1:
                        continue
                    edge.run_service("REMOVE", "OUTPUT_AT_INDEX", index)

                    # If there are no vertices in the output of the edge anymore, remove it
                    if 0 == edge.run_service("GET", "OUTPUT_SIZE"):
                        input = edge.run_service("GET", "INPUT")
                        for v in input:
                            v.run_service("REMOVE", "EDGE", edge.run_service("GET", "GID"))
                        self.run_service("REMOVE", "GRAPH_EDGES", [edge.run_service("GET", "GID")])

            for new_in_edge in new_in_edges:
                name = new_in_edge.run_service("GET", "GID")
                
                if name not in [e.run_service("GET", "GID") for e in old_in_edges]:
                    # This in_edge was not in the old vertex
                    # add the vertex to the edge_output if it is not yet there
                    edge = self.get_graph_edge(name)
                    if None == edge:
                        continue
                    index = edge.run_service("GET", "INDEX_IN_OUTPUT", vertex_name)
                    if index != -1:
                        continue
                    edge.run_service("APPEND", "OUTPUT", vertices[vertex_name])

        # 5.2: Update edge inputs
        for vertex_name in vertices.keys():
            old_out_edges = old_vertex_edges[vertex_name]["OUT_EDGES"].values()
            new_out_edges = new_vertex_edges[vertex_name]["OUT_EDGES"].values()
            for old_out_edge in old_out_edges:
                name = old_out_edge.run_service("GET", "GID")
                
                if name not in [e.run_service("GET", "GID") for e in new_out_edges]:
                    # This out_edge is not in the new vertex anymore
                    # remove the vertex from the edge_input if it is still there
                    edge = self.get_graph_edge(name)
                    if None == edge:
                        continue
                    index = edge.run_service("GET", "INDEX_IN_INPUT", vertex_name)
                    if index == -1:
                        continue
                    edge.run_service("REMOVE", "INPUT_AT_INDEX", index)
                    
                    # If there are no vertices in the input of the edge anymore, remove it
                    if 0 == edge.run_service("GET", "INPUT_SIZE"):
                        # need to remove it from the in_edges of the ouput_vertices
                        output = edge.run_service("GET", "OUTPUT")
                        for v in output:
                            v.run_service("REMOVE", "EDGE", edge.run_service("GET", "GID"))
                        self.run_service("REMOVE", "GRAPH_EDGES", [edge.run_service("GET", "GID")])

            for new_out_edge in new_out_edges:
                name = new_out_edge.run_service("GET", "GID")
                
                if name not in [e.run_service("GET", "GID") for e in old_out_edges]:
                    # This in_edge was not in the old vertex
                    # add the vertex to the edge_output if it is not yet there
                    edge = self.get_graph_edge(name)
                    if None == edge:
                        continue
                    index = edge.run_service("GET", "INDEX_IN_INPUT", vertex_name)
                    if index != -1:
                        continue
                    edge.run_service("APPEND", "INPUT", vertices[vertex_name])

        # 5.3: Update vertex outputs
        for edge_name in edges.keys():
            old_in_vertices = old_edge_vertices[edge_name]["INPUT"].values()
            new_in_vertices = new_edge_vertices[edge_name]["INPUT"].values()
            for old_in_vertex in old_in_vertices:
                name = old_in_vertex.run_service("GET", "GID")
                
                if name not in [v.run_service("GET", "GID") for v in new_in_vertices]:
                    # This in_vertex is not in the new edge anymore
                    # remove the edge from the vertex_out_edges if it is still there
                    vertex = self.get_graph_vertex(name)
                    if None == vertex:
                        continue
                    out_edges_names = [e.run_service("GET", "GID") for e in vertex.run_service("GET", "OUT_EDGES")]
                    if edge_name in out_edges_names:
                        vertex.run_service("REMOVE", "EDGE", edge_name)

            for new_in_vertex in new_in_vertices:
                name = new_in_vertex.run_service("GET", "GID")
                
                if name not in [v.run_service("GET", "GID") for v in old_in_vertices]:
                    # This in_vertex was not in the old edge_output
                    # add the edge to the vertex_output if it is not yet there
                    vertex = self.get_graph_vertex(name)
                    if None == vertex:
                        continue

                    out_edges_names = [e.run_service("GET", "GID") for e in vertex.run_service("GET", "OUT_EDGES")]
                    if edge_name not in out_edges_names:

                        vertex.run_service("ADD", "OUT_EDGE", edges[edge_name])

        # 5.4: Update vertex inputs
        for edge_name in edges.keys():
            old_out_vertices = old_edge_vertices[edge_name]["OUTPUT"].values()
            new_out_vertices = new_edge_vertices[edge_name]["OUTPUT"].values()
            for old_out_vertex in old_out_vertices:
                name = old_out_vertex.run_service("GET", "GID")
                
                if name not in [v.run_service("GET", "GID") for v in new_out_vertices]:
                    # This in_vertex is not in the new edge anymore
                    # remove the edge from the vertex_out_edges if it is still there
                    vertex = self.get_graph_vertex(name)
                    if None == vertex:
                        continue
                    vertex.run_service("REMOVE", "EDGE", edge_name)

            for new_out_vertex in new_out_vertices:
                name = new_out_vertex.run_service("GET", "GID")
                if name not in [v.run_service("GET", "GID") for v in old_out_vertices]:
                    # This in_vertex was not in the old edge_output
                    # add the edge to the vertex_output if it is not yet there
                    vertex = self.get_graph_vertex(name)
                    if None == vertex:
                        continue
                    vertex.run_service("ADD", "IN_EDGE", edges[edge_name])
        
        # 5.5 Finally we need to add all missing connections between vertices/edges in the added subgraph
        for edge_name in edges.keys():
            edge = self.get_graph_edge(edge_name)
            if None == edge:
                continue
            in_vertices = edge.run_service("GET", "INPUT")
            for vertex_name in [v.run_service("GET", "GID") for v in in_vertices]:
                vertex = self.get_graph_vertex(vertex_name)
                if None == vertex:
                    continue
                out_edges_names = [e.run_service("GET", "GID") for e in vertex.run_service("GET", "OUT_EDGES")]
                if edge_name not in out_edges_names:
                    vertex.run_service("ADD", "OUT_EDGE", edge)

            out_vertices = edge.run_service("GET", "OUTPUT")
            for vertex_name in [v.run_service("GET", "GID") for v in out_vertices]:
                vertex = self.get_graph_vertex(vertex_name)
                if None == vertex:
                    continue
                in_edges_names = [e.run_service("GET", "GID") for e in vertex.run_service("GET", "IN_EDGES")]
                if edge_name not in in_edges_names:
                    vertex.run_service("ADD", "IN_EDGE", edge)

        # TODO: Consider order
        for vertex_name in vertices.keys():
            vertex = self.get_graph_vertex(vertex_name)
            if None == vertex:
                continue
            in_edges = vertex.run_service("GET", "IN_EDGES")
            for edge_name in [e.run_service("GET", "GID") for e in in_edges]:
                edge = self.get_graph_vertex(edge_name)
                if None == edge:
                    continue
                out_vertices_names = [v.run_service("GET", "NAME") for v in edge.run_service("GET", "OUTPUT")]
                if vertex_name not in out_vertices_names:
                    edge.run_service("APPEND", "OUTPUT", vertex)
        
        for vertex_name in vertices.keys():
            vertex = self.get_graph_vertex(vertex_name)
            if None == vertex:
                continue
            in_edges = vertex.run_service("GET", "OUT_EDGES")
            for edge_name in [e.run_service("GET", "GID") for e in in_edges]:
                edge = self.get_graph_vertex(edge_name)
                if None == edge:
                    continue
                out_vertices_names = [v.run_service("GET", "NAME") for v in edge.run_service("GET", "INPUT")]
                if vertex_name not in out_vertices_names:
                    edge.run_service("APPEND", "INPUT", vertex)

        # Finally
        # Make sure that all vertices/edges refer to the updated version of vertices/edges
        for edge_name in [e.run_service("GET", "GID") for e in self.get_all_edges()]:
            edge = self.get_graph_edge(edge_name)
            if None == edge:
                continue

            input = edge.run_service("GET", "INPUT")
            output = edge.run_service("GET", "OUTPUT")
            for index in range(len(input)):
                name = input[index].run_service("GET", "GID")
                if name in vertices:
                    edge.run_service("SET", "INPUT_AT_INDEX", index, vertices[name])

            for index in range(len(output)):
                name = output[index].run_service("GET", "GID")
                if name in vertices:
                    edge.run_service("SET", "OUTPUT_AT_INDEX", index, vertices[name])

        for vertex_name in [v.run_service("GET", "GID") for v in self.get_all_vertices()]:
            vertex = self.get_graph_vertex(vertex_name)
            if None == vertex:
                continue

            in_edges = vertex.run_service("GET", "IN_EDGES")
            for edge in in_edges:
                edge_name = edge.run_service("GET", "GID")
                if edge_name in edges.keys():
                    vertex.run_service("REMOVE", "IN_EDGE", edge_name)
                    vertex.run_service("ADD", "IN_EDGE", edges[edge_name])

            out_edges = vertex.run_service("GET", "OUT_EDGES")
            for edge in out_edges:
                edge_name = edge.run_service("GET", "GID")
                if edge_name in edges:
                    vertex.run_service("REMOVE", "OUT_EDGE", edge_name)
                    vertex.run_service("ADD", "OUT_EDGE", edges[edge_name])

        return DYNRM_MCA_SUCCESS

    @staticmethod            
    def get_copy(self, graph_copy):

        graph_copy = MCAVertexModule.get_copy(graph_copy)

        graph_copy.run_service("ADD", "GRAPH_VERTICES", self.run_service("GET_ALL_GRAPH_VERTICES"))
        graph_copy.run_service("ADD", "GRAPH_EDGES", self.run_service("GET_ALL_GRAPH_EDGES"))
        graph_copy.run_service("SET", "ROOT", self.run_service("GET", "ROOT"))

        return graph_copy
        
