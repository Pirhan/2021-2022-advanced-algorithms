from typing import List, Dict, Tuple, KeysView
import math


class Graph_EUC:
    def __init__(self) -> None:
        self.nodes: Dict[int, Tuple[float, float]] = {}  # key = index; value = (x,y)

    def add_node(self, index: int, value1: float, value2: float):
        self.nodes[index] = (value1, value2)

    def getCoordinates(self, index: int) -> tuple:
        (x, y) = self.nodes.get(index)
        return x, y

    def getDistance(self, index_n1: int, index_n2: int) -> float:
        n1_x, n1_y = self.getCoordinates(index_n1)
        n2_x, n2_y = self.getCoordinates(index_n2)

        return math.sqrt((n1_x - n2_x) ** 2 + (n1_y - n2_y) ** 2)

    def getNodes(self) -> KeysView[int]:
        return self.nodes.keys()

    # Returns a Dict contianing the distance between all nodes
    def getAllEdges(self) -> Dict[Tuple[int, int], float]:

        edges: Dict[Tuple[int, int], float] = {}
        Nodes = self.nodes.keys()

        for Node_1 in Nodes:
            for Node_2 in Nodes:
                if Node_1 == Node_2:
                    continue
                distance = self.getDistance(Node_1, Node_2)
                edges[(Node_1, Node_2)] = distance

        return edges

    def initialize_from_file(self, filename: str) -> None:
        """ Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            start = 0

            end = 0
            for index, line in enumerate(lines):
                if line.startswith("DIMENSION"):
                    self.dimension = int(line.split()[1])  # could be useful when deciding if repeat or not an algorithm if the problem instance is small
                if line.startswith("NODE_COORD_SECTION"):
                    start = index
                if line.startswith("EOF"):
                    end = index

            for line in lines[start + 1 : end]:

                node: int = int(line.split()[0])
                x_coord: float = float(line.split()[1])
                y_coord: float = float(line.split()[2])

                self.add_node(node, x_coord, y_coord)
