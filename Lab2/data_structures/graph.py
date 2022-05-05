from typing import List, Dict, Tuple, Set

class Graph:

    def __init__(self)->None:
        self.nodes : Set[int] = set()
        self.edges : Dict[Tuple[int, int], float] = {}
        self.Adj_list : Dict[Tuple[int, int], float] = {}         # [[]], dict in order to support an unordered set of keys


    def addEdge(self, edge: tuple, weight) -> None:
        (v, u) = edge 
        self.nodes.add(v)
        self.nodes.add(u)
        edges = list(self.edges.keys())
        if edge not in edges:
            self.edges[edge] = float(weight)
        else: return
                                                                         
        if v not in list(self.Adj_list.keys()) : self.Adj_list[v] = []  
        if u not in list(self.Adj_list.keys()) : self.Adj_list[u] = [] 
        (self.Adj_list[v]).append(edge)
        (self.Adj_list[u]).append(edge)


    def getNodes(self) -> List[int]:
        return list(self.nodes)

    def getEdges(self) -> Dict[Tuple[int, int], float]:
        return self.edges
    
    def orderEdges(self)->None:
        self.edges = dict(sorted(self.edges.items(), key=lambda item: item[0]))

    def getAdjacentNodes(self, node : int) -> list:
        nodes = set()
        if node in self.nodes:
            for (u, v) in list((self.Adj_list)[node]):
                if node == u: nodes.add(v)
                else: nodes.add(u)                  
        return list(nodes)
