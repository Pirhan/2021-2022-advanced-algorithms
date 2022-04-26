from data_structures.graph import Graph
from data_structures.unionFind import UnionFind
from heapq import *

def Efficient_Kruskal(G: Graph) -> None:
    """
    This is a function that implements the Kruskal's algorithm 
    implemented using the "Disjoint Set Union" data structure, 
    which allows to achieve the time complexity of O(M * log(N)).
    """
    A = Graph() # Not an array because we need to store the weight associated to the edge
    
    U = UnionFind()
    U.Initialize(G.nodes)

    edges = G.edges
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    
    for edge in sort_edges_keys:
        (v,w) = edge
        if v == w: continue
        if U.Find(v) != U.Find(w):              # No path v-w in A
            A.addEdge(edge, edges.get(edge))    # Adding weight in order to print it and test it later
            U.Union(v, w)

    A.nonDiscendingOrderGraph_Keys()
    
    return A.total_Weight()



def Prim_Heap(G: Graph):
    """
    This is a function that implements the Prim's algorithm, 
    which allows to achieve the time complexity of O(M * log(N)).
    """   

    Total_weight = 0    # The weight of the MST obtained

    Q = []              # This is the list uset to build the heap  
    
    visited = []        # Contains all the visited nodes
    heappush(Q,[0,1])   # [0,1] indicates a first weight of 0 and node 1 as starting node
                        # In this way we don't need to use key and Phi as data structures
    
    
    while len(Q)!=0:

        weight, node = heappop(Q)    # Extract the minimum edge incident [weignt, node], it pops the elements too 
                                    # This is the weight of a visited edge. It does not create cycles so let's add it to the final MST

        if node in visited:         # node already visited
            continue

        visited.append(node)        # Node non visited. Adding it to the final MST
        
        Total_weight += weight      # Adding the edge's weight to the final MST weight


        for v in G.getAdjacentNodes(node):                      # for each v adiacent to node
            weight = G.edges.get((node, v))                     # Taking the weight of the node
            if weight == None: 
                weight = G.edges.get((v, node))
            if v not in visited:
                heappush(Q,[weight,v])                          # Adding a new [w,v] to Q if v in not visited yet

    return Total_weight
