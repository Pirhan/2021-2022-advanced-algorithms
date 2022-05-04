from typing import List, Dict, Tuple
class Graph:

    def __init__(self)->None:
        self.nodes : List[int] = []
        self.edges : Dict[Tuple[int, int], float]

    def addEdge(self, node1 : int, node2 : int, weight)->None:
        if node1 in self.nodes and node2 in self.nodes:
            return
        if node1 not in self.nodes: self.nodes.append(node1)
        if node2 not in self.nodes: self.nodes.append(node2)
        self.edges[(node1, node2)] = weight

    def getNodes(self) -> List[int]:
        return self.nodes

    def getEdges(self) -> Dict[Tuple[int, int], float]:
        return self.edges