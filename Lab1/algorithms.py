import graphlib
from data_structures.graph import Graph
from data_structures.unionFind import UnionFind
import heapq

def Efficient_Kruskal(G: Graph):

    A = Graph() # Not an array because we need to store the weight associated to the edge
    
    U = UnionFind()
    U.Initialize(G.get_nodes())

    edges = G.get_edges()
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    
    for edge in sort_edges_keys:
        (v,w) = edge

        if U.Find(v) != U.Find(w): # No path v-w in A
            A.addEdge(edge, edges.get(edge))    # Adding weight in order to print it and test it later
            U.Union(v, w)

    A.nonDiscendingOrderGraph_Keys()
    A.PrintGraph("Efficient_Kruscal", G)
    return A



def Kruskal(G: Graph):
    
    A=Graph()
    edges = G.get_edges()
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    print(sort_edges.keys())

    for edge in list(sort_edges_keys):
        A.addEdge(edge, edges.get(edge))
        if A.isCycle() == True:
            A.removeEdge(edge)  
    
    A.nonDiscendingOrderGraph_Keys()
    A.PrintGraph("Kruscal", G)
    return A


def Prim_Heap(G: Graph):
        
        V = G.get_nodes() 

        # key values used to pick minimum weight edge in cut
        key = []  
         
        # List to store constructed MST
        parent = []
 
        # minHeap represents set E, this is Q
        minHeap = []

        # The final MST will be stored here
        A = Graph()

        # Initialize min heap with all vertices. 
        # Key values of al vertices (except the 0th vertex) is initially infinite
        for node in V:
            key.append(1e7)
            parent.append(None)
            heapq.heappush(minHeap, node)   # Adding all nodes not in the tree (Q <- V)
        heapq.heapify(minHeap)              # Creating the heap (minHeap[0] => shortest distance)

        # Make key value of 0th vertex as 0 so
        # that it is extracted first. 
        key[0] = 0
 
        # Initially size of min heap is equal to V
 
        # In the following loop, min heap contains all nodes
        # not yet added in the MST.
        while len(minHeap) != 0:
 
            # Extract the vertex with minimum distance value
            u = minHeap[0] 
            heapq.heappop(minHeap)

            # Traverse through all adjacent vertices of u
            # (the extracted vertex) and update their
            # distance values
            
            for (node_u, adiacent_n) in list(G.Adj_list.get(u)):
                #weight = G.edges.get((adiacent_n, node_u)) 
                weight = G.edges.get((node_u, adiacent_n))             # Taking the weight of the node
                if adiacent_n in minHeap and weight < key[adiacent_n-1]:
                    key[adiacent_n-1] = weight
                    parent[adiacent_n-1] = u
      
                    A.addEdge((node_u, adiacent_n), weight)      # Building the final MST
        
        A.PrintGraph("Prim_Heap", G)
        return A
    
