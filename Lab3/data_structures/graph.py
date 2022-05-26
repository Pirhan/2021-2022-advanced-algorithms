from typing import *
import numpy as np
class Graph:
    
    def __init__(self, n) -> None:
        self.nodes : Set[int] = set() 
        self.edges : Dict[Tuple[int,int], float] = {}
        self.dimension = n


    def addEdge(self, node1 : int, node2: int, weight: int)->None:
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.edges[node1, node2] = weight 

    def getEdges(self):
        return self.edges

    def getNodes(self)->List[int]:
        return list(self.nodes)

    @staticmethod
    def initialize_from_file(filename: str):
        """Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            
            starting_line = lines[0]
            n_nodes = int(starting_line.split()[0])

            graph = Graph(n_nodes)

            for line in lines[1:]:
                node_1 = int(line.split()[0])
                node_2 = int(line.split()[1])
                weight = float(line.split()[2])

                graph.addEdge(node_1, node_2, weight)
            

            file.close()
        return graph