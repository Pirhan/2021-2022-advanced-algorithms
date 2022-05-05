from typing import List, Dict, Tuple, KeysView
import math

class CompleteGraph:
    def __init__(self) -> None:
        self.nodes: Dict[int, Tuple[float, float]] = {}  # key = index; value = (x,y)

    def add_node(self, index: int, value1: float, value2: float):
        self.nodes[index] = (value1, value2)

    def getCoordinates(self, index: int) -> tuple:
        (x, y) = self.nodes.get(index)
        return x, y

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

class Graph_EUC(CompleteGraph):

    def getDistance(self, index_n1: int, index_n2: int) -> float:
        n1_x, n1_y = self.getCoordinates(index_n1)
        n2_x, n2_y = self.getCoordinates(index_n2)

        return math.sqrt((n1_x - n2_x) ** 2 + (n1_y - n2_y) ** 2)

class Graph_GEO(CompleteGraph):

    def add_node(self, index: int, coordinate_x: float, coordinate_y: float):
        self.nodes[index] = (
            Graph_GEO.toRadiant(coordinate_x),
            Graph_GEO.toRadiant(coordinate_y),
        )

    def getLatLong(self, index: int) -> Tuple[float, float]:
        (latitude, longitude) = self.nodes.get(index)
        return latitude, longitude

    @staticmethod
    def toRadiant(
        value: float,
    ) -> float:
        PI: float = 3.141592
        deg: int = (int)(value)
        minimum: float = (
            value - deg
        )  # min is also a function -> bit confusing -> renamed to minimum

        return PI * (deg + 5.0 * minimum / 3.0) / 180.0

    def getDistance(self, node_x: int, node_y: int) -> int:

        RRR: float = 6378.388
        latitude_x, longitude_x = self.getLatLong(node_x)
        latitude_y, longitude_y = self.getLatLong(node_y)
        q1: float = math.cos(longitude_x - longitude_y)
        q2: float = math.cos(latitude_x - latitude_y)
        q3: float = math.cos(latitude_x + latitude_y)
        return (int)(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

    # Returns a Dict contianing the distance between all nodes


    def getDistance_2(self, node_x: int, node_y: int) -> float:
        """ Solution from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude/43211266#43211266"""
        # approximate radius of earth in km
        approximate_radius_earth: float = 6373.0

        lat1, lon1 = self.getLatLong(node_x)
        lat2, lon2 = self.getLatLong(node_y)
        dlon: float = lon2 - lon1
        dlat: float = lat2 - lat1

        versine: float = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )  # half of versine of an angle
        haversine_distance: float = 2 * math.atan2(
            math.sqrt(versine), math.sqrt(1 - versine)
        )  # haversine distance, computes the versine of an angle, required for computing the haversine distance

        return approximate_radius_earth * haversine_distance
