from data_structures.graph import load_graph_AL as Graph
from data_structures.unionFind import UnionFind
import heapq

def Efficient_Kruskal(G: Graph):

    A = {} # Not an array because we need to store the weight associated to the edge
    
    U = UnionFind()
    U.Initialize(G.get_nodes())

    edges = G.get_edges()
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    
    for edge in sort_edges_keys:
        (v,w) = edge

        if U.Find(v) != U.Find(w): # No path v-w in A
            A[edge] = edges.get(edge) # Adding weight in order to print it and test it later
            U.Union(v, w)
    
    print("Efficient_Kruscal => OK")
    dict_sorted = dict(sorted(A.items(), key = lambda item: item[0]))
    print_data_G(dict_sorted)
    return dict_sorted

def Kruskal(G: Graph):
    
    Nodes = set()
    A={}
    edges = G.get_edges()
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    for edge in sort_edges_keys:
        (v,w) = edge 
        if v not in Nodes or w not in Nodes: # No path v-w in A
              # This is a set, no need to check before adding it
            Nodes.add(w)
            A[edge] = edges.get(edge) # Adding weight in order to print it and test it later
    
    
    print("Kruscal => OK")
    dict_sorted = dict(sorted(A.items(), key = lambda item: item[0]))
    print_data_G(dict_sorted)
    return dict_sorted


def Prim_Heap(G: Graph):
        
        V = G.get_nodes() 

        # key values used to pick minimum weight edge in cut
        key = []  
         
        # List to store constructed MST
        parent = []
 
        # minHeap represents set E, this is Q
        minHeap = []

        # The final MST will be stored here
        final_G = {}

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
                weight = G.edges.get((node_u, adiacent_n))      # Taking the weight of the node
                if adiacent_n in minHeap and weight < key[adiacent_n-1]:
                    key[adiacent_n-1] = weight
                    parent[adiacent_n-1] = u

                    final_G[(node_u, adiacent_n)] = weight      # Building the final MST
        
        print("Prim_Heap => OK")
        print_data_G(final_G)
        return final_G
    

def print_data_G(Graph: dict):
    total_w = 0
    total_n = set()
    for (node1, node2) in Graph.keys():
        total_n.add(node1)
        total_n.add(node2)
        total_w += Graph.get((node1, node2))

    print("The number of nodes in the MST is: ", len(total_n), " Total weight is: ", total_w)
