from typing import *
import numpy as np
class Graph:
    
    def __init__(self) -> None:
        self.nodes : Set[int] = set() 
        self.Edges : np.matrix = None

    def addEdge(self, node1 : int, node2: int, weight: int)->None:
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.Edges[node1-1, node2-1] = weight
        
    def getRowEdges(self, node:int)->int:
        # Returns the array corresponding to the matrix row 
        return self.Edges[node-1]

    def getRowWeight(self, node: int)->int:
        # Returns the som of the matrix row weights 
        return sum(getRowEdges(node))

    def getNodes(self)->Set[int]:
        return list(self.nodes)

    @staticmethod
    def initialize_from_file(filename: str):
        """Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            
            starting_line = lines[0]
            n_nodes = starting_line.split()[0]

            graph = Graph()
            graph.Edges = np.zeros((n_nodes, n_nodes))


            for line in lines[1:]:
                node_1 = line.split()[0]
                node_2 = line.split()[1]
                weight = line.split()[2]

                graph.addEdge(node_1, node_2, weight)

            file.close()
        return graph