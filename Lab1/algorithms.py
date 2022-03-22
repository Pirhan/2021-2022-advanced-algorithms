from data_structures.graph import load_graph_AL as Graph
from data_structures.unionFind import UnionFind

def Efficient_Kruskal(G: Graph):

    A = {} # Not an array becouse we need to store the weight associated to the edge
    U = UnionFind()
    U.Initialize(G.get_nodes())
    edges = G.get_edges()
    sort_edges = dict(sorted(edges.items(), key=lambda item: item[1])) # In nondecrising order of weight
    sort_edges_keys = sort_edges.keys() # Getting the keys 
    
    for edge in sort_edges_keys:
        (v,w) = edge

        if U.Find(v) != U.Find(w): # No path v-w in A
            A[edge] = edges.fromkeys(edge) # Adding weight in order to print it and test it later
            U.Union(v, w)
    return A
