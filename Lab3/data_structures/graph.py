from typing import *
import numpy as np


class Graph:
    def __init__(self, n) -> None:
        self.nodes: Set[int] = set()
        self.edges: Set[Tuple[int, int]] = set()
        self.W: np.matrix = np.zeros((n, n))
        self.D: List[float] = []

    def addEdge(self, node1: int, node2: int, weight: int) -> None:
        self.nodes.add(node1)
        self.nodes.add(node2)

        self.W[node1 - 1, node2 - 1] = weight
        self.W[node2 - 1, node1 - 1] = weight

    def getEdgesList(self):
        return self.edges

    def setWeightedDegree(self):
        D: List[float] = []
        for node in self.getNodes():
            D.append(self.getRowWeight(node))
        self.D = D

    def getRowEdges(self, node: int) -> int:
        # Returns the array corresponding to the matrix row
        return self.W[node - 1]

    def getRowWeight(self, node: int) -> int:
        # Returns the som of the matrix row weights
        return sum(self.getRowEdges(node))

    def getNodes(self) -> List[int]:
        return list(self.nodes)

    def getW(self):
        return self.W

    def getD(self):
        return self.D

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

            graph.setWeightedDegree()
            file.close()
        return graph
