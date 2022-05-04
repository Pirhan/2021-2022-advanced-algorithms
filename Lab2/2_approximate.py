from data_structures.EUC_graph import Graph_EUC
from data_structures.GEO_graph import Graph_GEO
from data_structures.unionfind import UnionFind
from data_structures.graph import Graph

def Efficient_Kruskal(G) -> None:
    """
    This is a function that implements the Kruskal's algorithm 
    implemented using the "Disjoint Set Union" data structure, 
    which allows to achieve the time complexity of O(M * log(N)).
    """
    A = Graph()
    # Not an array because we need to store the weight associated to the edge
    
    U = UnionFind()
    U.Initialize(G.getNodes())
    
    edges = G.getAllEdges()
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