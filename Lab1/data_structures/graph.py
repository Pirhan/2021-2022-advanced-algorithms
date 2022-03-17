class load_graph_AL:
    """
    load the graph from the txt file and computes the adjacency lists
    """
    def _init_(self):
        self.nodes = {}
        self.edges = set()
    
    
    def inizialize(self, filename):
        """ Builds the adiacency lists from the txt file"""
        edges = {}
        nodes = set()
        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                v1 = int(line.split()[0])
                v2 = int(line.split()[1])
                c = int(line.split()[2])
                edges[(v1, v2)] = c
                nodes.add(v1)
                nodes.add(v2)
        self.edges = edges
        self.nodes = nodes
    #################
        def test_graph(graph, lines, nodes):
            """
            This is only a test function on the load_graphs() correctness
            """
            discovered = set()
            for (n1, n2) in graph:
                if n1 != n2:
                    discovered.add(n1)
                    discovered.add(n2)
            if len(nodes) != len(discovered) or len(lines)-1 != len(graph):
                return "Failed"   
            return "Passed"
    ###################

        assert(test_graph(edges, lines, nodes) == "Passed")             # Makes sure that everything is ok
        return "OK"   
    
    def get_nodes(self):
        return self.nodes.copy()    # FIXME

    def get_edges(self):
        return self.edges.copy()    # FIXME
                