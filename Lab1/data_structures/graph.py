from lib2to3.pytree import Node
import string
from xmlrpc.client import Boolean


class Graph:
    # [[]], dict in order to support an unordered set of keys
    Adj_list = {}

    # dict containing the edges with a tuple of nodes as key and the weight as value 
    edges = {}

    # set containing the nodes discovered
    nodes = set()

    # Auxiliary data stucture for cycle detection  
    visited = []

    def __init__(self) -> None:
        pass

    def addEdge(self, edge: tuple, weight: int):
        (v, u) = edge 
        self.nodes.add(v)
        self.nodes.add(u)
        edges = list(self.edges.keys())
        if edge not in edges:
            self.edges[edge] = weight
        
        (self.Adj_list[v]).append(edge)
        (self.Adj_list[u]).append(edge)

    def removeEdge(self, edge: tuple):
        (u, w) = edge 
        print("Ora ", edge)
        print(self.edges.pop((edge)))
        print("Dopo ", list(self.edges.items()))
        (self.Adj_list[u]).remove(edge)
        (self.Adj_list[w]).remove(edge)
        if len((self.Adj_list[u]))==1:
            self.nodes.remove(u)
        if len((self.Adj_list[u]))==1:
            self.nodes.remove(u)
    
    def getAdiacentNodes(self, node : int) -> list:
        nodes = []
        #print(node, " => ",(self.get_AL()).get(node))
        if node in self.nodes:
            for (u, v) in list((self.get_AL())[node]):
                #print((u,v))
                if node == u: nodes.append(v)
                else: nodes.append(u)                   # if node == v
        return nodes
    
    def getAdiacentEdges(self, node: int) -> list:
        edges = []
        if node in self.nodes:
            for edges in list((self.get_AL())[node]):
                for (u, v) in edges:
                    edges.append((u, v))
        return edges

    # Orders the graph in non discending order of keys
    def nonDiscendingOrderGraph_Keys(self):
        self.edges = dict(sorted(self.get_edges().items(), key = lambda item: item[0]))
        return self
    
    # Orders the graph in non discending order of values
    def nonDiscendingOrderGraph_Values(self):
        self.edges = dict(sorted(self.get_edges().items(), key = lambda item: item[1]))
        return self
        

    """ def DetectCycle (A, node : int):

        self.visited[src] = True

        for adj_node in self.adjlist[src]:
            if self.visited[adj_node] == False:
                self.parent[adj_node] = src
                self.DetectCycle (adj_node)
            elif self.parent[src] != adj_node:
                self.cycle_present = True
                return """
    
    def detCycles(self) -> Boolean:
        self.visited = [False] * (len(self.get_nodes()))
        self.parent = [None] * (len(self.get_nodes()))
        
        """ def DetectCycle (self:Graph, node : int) -> False:

            self.visited[node-1] = True

            for adj_node in self.getAdiacentNodes(node):
                if self.visited[adj_node-1] == False:
                    self.parent[adj_node-1] = node
                    DetectCycle (self, adj_node)
                elif self.parent[node-1] != adj_node:
                    return True 
            return False """

        def DFS_Traversal(self, v, visited, parent_node=-1):
 
            # assign current node as
            visited[v] = True
 
            # loop for every edge (v, u)
            for u in self.getAdiacentNodes(v):
 
                # if `u` is not visited
                if not visited[u]:
                    if DFS_Traversal(self, u, visited, v):
                        return True
 
                # if `u` is visited, and `u` is not a parent_node
                elif u != parent_node:
                    # found a back-edge 
                    return True
 
                # No back-edges were found 
                return False
        (u, w) = list(self.get_edges().keys())[0]
        return  DFS_Traversal(self, u, self.visited)



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
        return self.Adj_list.copy()       # FIXME

    
    def PrintGraph(self, FunctionName: string,  OriginalGraph = None):
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


        
    