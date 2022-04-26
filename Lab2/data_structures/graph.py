class Graph:
    
    def __init__(self) -> None:
        self.Adj_list = {}          # [[]], dict in order to support an unordered set of keys
        self.nodes = set()          # set containing the nodes discovered
        self.edges = {}             # dict containing the edges with a tuple of nodes as key and the weight as value                      
        

    def addEdge(self, edge: tuple, weight: int) -> None:
        (v, u) = edge 
        self.nodes.add(v)
        self.nodes.add(u)
        edges = list(self.edges.keys())
        if edge not in edges:
            self.edges[edge] = weight
        else: return
                                                                         
        if v not in list(self.Adj_list.keys()) : self.Adj_list[v] = []  
        if u not in list(self.Adj_list.keys()) : self.Adj_list[u] = [] 
        (self.Adj_list[v]).append(edge)
        (self.Adj_list[u]).append(edge)

    def removeEdge(self, edge: tuple) -> None:
        (u, w) = edge 
        self.edges.pop((edge))
        (self.Adj_list[u]).remove(edge)
        (self.Adj_list[w]).remove(edge)        

    def total_Weight(self):
        return sum(self.edges.values())

    # Returns all the nodes incident to node
    def getAdjacentNodes(self, node : int) -> list:
        nodes = set()
        if node in self.nodes:
            for (u, v) in list((self.Adj_list)[node]):
                if node == u: nodes.add(v)
                else: nodes.add(u)                   # if node == v
        return list(nodes)
    
    # Returns all the edges with node 
    def getAdjacentEdges(self, node: int) -> list:
        edges = set()
        for list_edges in list(self.Adj_list[node]):
            edges.add(list_edges)
        return list(edges)

    # Orders the graph in non discending order of keys
    def nonDiscendingOrderGraph_Keys(self):
        self.edges = dict(sorted(self.edges.items(), key = lambda item: item[0]))
    
    # Orders the graph in non discending order of values
    def nonDiscendingOrderGraph_Values(self):
        self.edges = dict(sorted(self.edges.items(), key = lambda item: item[1]))


    def isCycle(self):
        """
        Based on Breadth-first search (BFS) to explore every vertex which is reachable from v. 
        The overall complexity is O(m+n), with m and n being the number of edges and vertices respectively.
        """
        
        Visited = []
    
        # initially all vertices are unexplored
        L = { v: -1 for v in self.nodes }
    
        for v in self.nodes:
    
            # v has already been explored; move on
            if L[v] != -1:
                continue
    
            # take v as a starting vertex
            L[v] = 0                # start by selecting some unexplored vertex v of G
            Visited.append(v)
    
            # as long as Q is not empty
            while len(Visited) > 0:
    
                # get the next vertex u of Q that must be looked at
                u = Visited.pop(0)
    
                Adjacents = self.getAdjacentNodes(u)
    
                for adj in Adjacents:
                    # if z is being found for the first time
                    if L[adj] == -1:
                        L[adj] = L[u] + 1
                        Visited.append(adj)
                    elif L[adj] >= L[u]:
                        return True
        return False

    def inizialize(self, filename):
        """ Builds the adiacency lists from the txt file"""
        
        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                v1 = int(line.split()[0])   # First node 
                v2 = int(line.split()[1])   # Second node 
                w = int(line.split()[2])    # Weight
                
                self.addEdge((v1,v2), w)

        ############# Testing ############
        first_line = lines[0].split()
        assert(len(self.nodes) == int(first_line[0]))
        assert(len(self.edges) == int(first_line[1])) 
        

    def PrintGraph(self, FunctionName,  OriginalGraph = None):
        total_weight = 0
        for weight in list(self.edges.values()):
            total_weight += weight

        if OriginalGraph != None:
            #OriginalGraph = Graph()
            if len(self.nodes) == len(OriginalGraph.nodes):
                print(FunctionName)
                print(self.edges)
                print("The number of nodes in the MST is: ", len(self.nodes), " Total weight is: ", total_weight)
            else: 
                print(FunctionName + " => Failed","---- n. nodes = ", len(self.nodes))
                print(self.edges)
        else: print(self.edges)


        
    