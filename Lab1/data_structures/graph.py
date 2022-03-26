from re import U


class Graph:
    
    def __init__(self) -> None:
        self.Adj_list = {}          # [[]], dict in order to support an unordered set of keys
        self.nodes = set()          # set containing the nodes discovered
        self.edges = {}             # dict containing the edges with a tuple of nodes as key and the weight as value                      
        

    def addEdge(self, edge: tuple, weight: int):
        (v, u) = edge 
        self.nodes.add(v)
        self.nodes.add(u)
        edges = list(self.edges.keys())
        if edge not in edges:
            self.edges[edge] = weight
                                                                        # TODO Check why the appends doesnt't work anymore 
        if v not in list(self.get_AL().keys()) : self.Adj_list[v] = []  # Not sure why the statements below doesn't work without
        if u not in list(self.get_AL().keys()) : self.Adj_list[u] = []  # Not sure why the statements below doesn't work without
        (self.Adj_list[v]).append(edge)
        (self.Adj_list[u]).append(edge)

    def removeEdge(self, edge: tuple):
        (u, w) = edge 
        self.edges.pop((edge))
        (self.Adj_list[u]).remove(edge)
        (self.Adj_list[w]).remove(edge)
    
    def get_nodes(self):
        return self.nodes.copy()    # FIXME

    def get_edges(self):
        return self.edges.copy()    # FIXME
    
    def get_AL(self):
        return self.Adj_list.copy()       # FIXME

    # Returns all the nodes incident to node
    def getAdjacentNodes(self, node : int) -> list:
        nodes = set()
        if node in self.nodes:
            for (u, v) in list((self.get_AL())[node]):
                if node == u: nodes.add(v)
                else: nodes.add(u)                   # if node == v
        return list(nodes)
    
    # Returns all the edges with node 
    def getAdjacentEdges(self, node: int) -> list:
        edges = set()
        for list_edges in list(self.get_AL()[node]):
            edges.add(list_edges)
        return list(edges)


    # Orders the graph in non discending order of keys
    def nonDiscendingOrderGraph_Keys(self):
        self.edges = dict(sorted(self.get_edges().items(), key = lambda item: item[0]))
        return self
    
    # Orders the graph in non discending order of values
    def nonDiscendingOrderGraph_Values(self):
        self.edges = dict(sorted(self.get_edges().items(), key = lambda item: item[1]))
        return self

    # Construct the Adjacency list in the version [node] = [adjacent] 
    # TODO try to use this kind of rappresentation from the beginning 
    def getAL_list(self):
        nodes = []
        adj = {}
        for edge in list(self.get_edges().keys()):
            (u, v) = edge
            if u not in nodes:
                adj[u] = []
                nodes.append(u)
            if v not in adj[u]:
                (adj[u]).append(v)
            if v not in nodes:
                adj[v] = []
                nodes.append(v)
            if u not in adj[v]:
                (adj[v]).append(u)
        return adj

    def isCycle(self):

        def find_cycle(graph, start):

            colors = { node : True for node in graph }      # Buolding the set, setting all the nodes to 'Visited'
            colors[start] = False
            stack = [(None, start)] # store edge, but at this point we have not visited one
            while stack:
                (prev, node) = stack.pop()  # get stored edge
                for neighbor in graph[node]:
                    if neighbor == prev:
                        pass # don't travel back along the same edge we came from
                    elif colors[neighbor] == False:
                        return True
                    else: # can't be anything else than WHITE...
                        colors[neighbor] = False
                        stack.append((node, neighbor)) # push edge on stack
            return False

        Adj_List = self.getAL_list()
        return find_cycle(Adj_List, list(Adj_List.keys())[0])

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
            ##################################


        self.edges = edges
        self.nodes = nodes
        

    def PrintGraph(self, FunctionName,  OriginalGraph = None):
        total_weight = 0
        for weight in list(self.get_edges().values()):
            total_weight += weight

        if OriginalGraph != None:
            #OriginalGraph = Graph()
            if len(self.get_nodes()) == len(OriginalGraph.get_nodes()):
                print(FunctionName)
                print(self.get_edges())
                print("The number of nodes in the MST is: ", len(self.get_nodes()), " Total weight is: ", total_weight)
            else: print(FunctionName + " => Failed")
        else: print(self.get_edges())


        
    