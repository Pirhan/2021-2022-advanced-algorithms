from typing import List, Dict, Tuple, KeysView
import math
import numpy as np


class CompleteGraph:
    def __init__(self) -> None:
        self.nodes: Dict[int, Tuple[float, float]] = {}  # key = index; value = (x,y)
        self.dimension: int = 0
        self.Distances: np.matrix = None # type: ignore

    def add_node(self, index: int, value1: float, value2: float):
        self.nodes[index] = (value1, value2)

    def getCoordinates(self, index: int) -> tuple:

        (x, y) = self.nodes.get(index) # type: ignore
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

    def toMatrix(self):
        for first_index, node1 in enumerate(self.getNodes()):
            for second_index, node2 in enumerate(self.getNodes()):
                if node1 == node2:
                    continue
                self.Distances[first_index, second_index] = self.computeDistance(
                    node1, node2
                )  # child class function

    @staticmethod
    def initialize_from_file(filename: str) -> CompleteGraph:
        """Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            start = 0

            end = 0
            for index, line in enumerate(lines):
                if line.startswith("DIMENSION"):
                    graph_dimension = int(
                        line.split()[1]
                    )  # could be useful when deciding if repeat or not an algorithm if the problem instance is small
                if line.startswith("EDGE_WEIGHT_TYPE"):
                    graph_type = line.split()[1]
                if line.startswith("NODE_COORD_SECTION"):
                    start = index
                if line.startswith("EOF"):
                    end = index

            if graph_type == "EUC_2D":
                Comp_graph = Graph_EUC()
            if graph_type == "GEO":
                Comp_graph = Graph_GEO() # type: ignore

            Comp_graph.dimension = graph_dimension
            for line in lines[start + 1 : end]:

                node: int = int(line.split()[0])
                x_coord: float = float(line.split()[1])
                y_coord: float = float(line.split()[2])

                Comp_graph.add_node(node, x_coord, y_coord)

            n_nodes = len(Comp_graph.getNodes())

            Comp_graph.Distances = np.zeros( # type: ignore
                (n_nodes, n_nodes)
            )  # Inizialization of Distances matrix 
            Comp_graph.toMatrix()  # Filling np.matrix

            file.close()
        return Comp_graph

    def getDistance(self, index_n1: int, index_n2: int) -> float:

        return self.Distances[index_n1 - 1, index_n2 - 1]


class Graph_EUC(CompleteGraph):
    def computeDistance(self, index_n1: int, index_n2: int) -> float:
        n1_x, n1_y = self.getCoordinates(index_n1)
        n2_x, n2_y = self.getCoordinates(index_n2)

        return math.sqrt((n1_x - n2_x) ** 2 + (n1_y - n2_y) ** 2)

    def computeDistanceLineToPoint(self, node1, node2, target_node) -> float:
        (x_node1, y_node1) = self.nodes.get(node1)  # type: ignore
        (x_node2, y_node2) = self.nodes.get(node2)  # type: ignore
        (x_target_node, y_target_node) = self.nodes.get(target_node)    # type: ignore
        
        current_distance = abs(
            ((x_node2 - x_node1) * (y_node1 - y_target_node))
            - ((x_node1 - x_target_node) * (y_node2 - y_node1))
        ) / math.sqrt(
            ((x_node2 - x_node1) ** 2) + ((y_node2 - y_node1) ** 2)
        )

        return current_distance


class Graph_GEO(CompleteGraph):
    def add_node(self, index: int, coordinate_x: float, coordinate_y: float):
        self.nodes[index] = (coordinate_x, coordinate_y)

    def getLatLong(self, index: int) -> Tuple[float, float]:

        (latitude, longitude) = self.nodes.get(index)   # type: ignore
        return latitude, longitude

    def getLatLongInRadiant(self, index: int) -> Tuple[float, float]:

        (latitude, longitude) = self.nodes.get(index)   # type: ignore
        return Graph_GEO.toRadiant(latitude), Graph_GEO.toRadiant(longitude)

    def computeDistance(self, node_x: int, node_y: int) -> int:

        RRR: float = 6378.388
        latitude_x_rad, longitude_x_rad = self.getLatLongInRadiant(node_x)
        latitude_y_rad, longitude_y_rad = self.getLatLongInRadiant(node_y)

        q1: float = math.cos(longitude_x_rad - longitude_y_rad)
        q2: float = math.cos(latitude_x_rad - latitude_y_rad)
        q3: float = math.cos(latitude_x_rad + latitude_y_rad)
        return (int)(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

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

    # Returns a Dict contianing the distance between all nodes

    def getDistance_2(self, node_x: int, node_y: int) -> float:
        """Solution from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude/43211266#43211266"""
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

    def computeDistanceLineToPoint(self, node1, node2, target_node) -> float:
        # https://www.movable-type.co.uk/scripts/latlong.html

        def get_bearing(lat1, long1, lat2, long2):
            dLon = (long2 - long1)
            x = math.cos(Graph_GEO.toRadiant(lat2)) * math.sin(Graph_GEO.toRadiant(dLon))
            y = math.cos(Graph_GEO.toRadiant(lat1)) * math.sin(Graph_GEO.toRadiant(lat2)) - math.sin(Graph_GEO.toRadiant(lat1)) * math.cos(Graph_GEO.toRadiant(lat2)) * math.cos(Graph_GEO.toRadiant(dLon))
            brng = np.arctan2(x,y)
            brng = np.degrees(brng)

            return brng
        
        
        
        lat1, lon1 = self.getCoordinates(node1)
        lat2, lon2 = self.getCoordinates(node2)
        latt, lont = self.getCoordinates(target_node)
        
        RRR: float = 6378.388 # Approximate radius earth 

        angular_distance_node1_target_node = self.getDistance(node1, target_node)/RRR
        bearing_n1_nTarget = get_bearing(lat1, lon1, latt, lont)
        bearing_n1_n2 = get_bearing(lat1, lon1, lat2, lon2)

        angular_cross_track_distance = math.asin(math.sin(angular_distance_node1_target_node)*math.sin(bearing_n1_nTarget-bearing_n1_n2)) * RRR
        along_track_distance = math.acos(math.cos(angular_distance_node1_target_node)/math.cos(angular_cross_track_distance/RRR)) * RRR

        return along_track_distance