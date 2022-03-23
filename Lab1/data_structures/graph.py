class load_graph_AL:
    # [[]], dict in order to support an unordered set of keys
    Adj_list = {}

    # dict containing the edges with a tuple of nodes as key and the weight as value 
    edges = {}

    # set containing the nodes discovered
    nodes = set()

    """
    load the graph from the txt file and computes the adjacency lists
    """
    def inizialize(self, filename):
        """ Builds the adiacency lists from the txt file"""
        # dict containing the edges with a tuple of nodes as key and the weight as value 
        edges = {}

        # set containing the nodes discovered
        nodes = set()

        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                v1 = int(line.split()[0])   # First node 
                v2 = int(line.split()[1])   # Second node 
                c = int(line.split()[2])    # Weight
                edges[(v1, v2)] = c  
                nodes.add(v1)
                nodes.add(v2)
                
                keys = self.Adj_list.keys()       # keys are [1,3,2,...] an unordered set
                
                # In order to create the adiacency list we need to store all the pairs forming the keys of the tuples
                # linked with the two nodes
                if v1 not in  keys:
                    self.Adj_list[v1] = []        # For each node in AL we instantiate an empty array
                if v2 not in keys:
                    self.Adj_list[v2] = []
                
                # Adding the tuple to the adiacency list
                (self.Adj_list[v1]).append((v1,v2))   
                (self.Adj_list[v2]).append((v1,v2))

            ############# Testing ############
            first_line = lines[0].split()
            assert(len(nodes) == int(first_line[0]))
            assert(len(edges) == int(first_line[1]))
            #################################


        self.edges = edges
        self.nodes = nodes
        
    
    def get_nodes(self):
        return self.nodes.copy()    # FIXME

    def get_edges(self):
        return self.edges.copy()    # FIXME
    
    def get_AL(self):
        return self.AL.copy()       # FIXME
                