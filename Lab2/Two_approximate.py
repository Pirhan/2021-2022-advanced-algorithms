from data_structures.unionfind import UnionFind
from data_structures.graph import Graph
from data_structures.Complete_graphs import * # type: ignore


def Efficient_Kruskal(G:CompleteGraph):
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
    A.orderEdges()
    return A

def DFS_Traversal(graph : Graph, visited = [], node = None):
    if node == None: node = graph.getNodes()[0]
    if node not in visited:
        visited.append(node)
        for adj in graph.getAdjacentNodes(node):
            DFS_Traversal(graph, visited, adj)
            
    return visited + [graph.getNodes()[0]]

def getTotalWeight(Graph: CompleteGraph, cycle : List):
    total_weight: float = 0
    node1 = cycle[0]
    for node2 in cycle[1:]:
        
        total_weight += Graph.getDistance(node1, node2)
        node1 = node2
    
    return total_weight

def TwoApproximate(Graph):
    Result = Efficient_Kruskal(Graph)
    print("\n\n", Result.getNodes(),"\n\n")
    Cycle = DFS_Traversal(Result) # This is a list
    print("Cycle in: => ", Cycle)
    return getTotalWeight(Graph, Cycle)

