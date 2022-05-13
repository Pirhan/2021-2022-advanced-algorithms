from typing import List, Dict, Tuple, KeysView
import math
import numpy as np


class CompleteGraph:
    def __init__(self) -> None:
        self.nodes: Dict[int, Tuple[float, float]] = {}  # key = index; value = (x,y)
        self.dimension: int = 0  # Number of nodes according to the file
        self.Distances: np.matrix = None  # type: ignore

    def add_node(self, index: int, value1: float, value2: float):
        # Adds the node to the dict setting its value to the its coordinate
        self.nodes[index] = (value1, value2)

    def getCoordinates(self, index: int) -> tuple:
        # Returns the node's coordinate
        (x, y) = self.nodes.get(index)  # type: ignore
        return x, y

    def getNodes(self) -> KeysView[int]:
        # Returns the list of nodes as KeysView.
        return self.nodes.keys()

    # Returns a Dict contianing the distance between all nodes
    def getAllEdges(self) -> Dict[Tuple[int, int], float]:
        # Similar to Distances, returns all the distances beetween the nodes as a dict.

        edges: Dict[Tuple[int, int], float] = {}
        Nodes = self.nodes.keys()

        for Node_1 in Nodes:
            for Node_2 in Nodes:
                if Node_1 == Node_2:
                    continue
                distance = self.getDistance(
                    Node_1, Node_2
                )  # getting the distance beetween Node_1 and Node_2
                edges[
                    (Node_1, Node_2)
                ] = distance  # Stroring the distance in the edges dict as a value

        return edges

    def toMatrix(self):
        # Builds the Distances matrix, filling it with all the distances

        for first_index, node1 in enumerate(self.getNodes()):
            for second_index, node2 in enumerate(self.getNodes()):
                if node1 == node2:
                    continue
                self.Distances[first_index, second_index] = self.computeDistance(
                    node1, node2
                )  # child class function

    @staticmethod
    def initialize_from_file(filename: str):
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

            # Comp_graph is instantiated whith the correct class according to graph_type
            if graph_type == "EUC_2D":
                Comp_graph = Graph_EUC()
            if graph_type == "GEO":
                Comp_graph = Graph_GEO()  # type: ignore

            Comp_graph.dimension = graph_dimension
            for line in lines[start + 1 : end]:

                node: int = int(line.split()[0])  # Taking the node as an integer
                x_coord: float = float(line.split()[1])  # Taking the first coordinate
                y_coord: float = float(line.split()[2])  # Taking the second coordinate

                Comp_graph.add_node(
                    node, x_coord, y_coord
                )  # Adding the node to the nodes data structure

            n_nodes = Comp_graph.dimension  # Taking the number of nodes

            Comp_graph.Distances = np.zeros(  # type: ignore
                (n_nodes, n_nodes)
            )  # Inizialization of Distances matrix
            Comp_graph.toMatrix()  # Filling np.matrix

            file.close()
        return Comp_graph

    def getDistance(self, index_n1: int, index_n2: int) -> float:
        # Return the distance beetween the nodes. All the distances are stored in the Distances np.matrix
        return self.Distances[index_n1 - 1, index_n2 - 1]


class Graph_EUC(CompleteGraph):
    def computeDistance(self, index_n1: int, index_n2: int) -> float:
        # Computes the distance between n1 and n2

        n1_x, n1_y = self.getCoordinates(index_n1)
        n2_x, n2_y = self.getCoordinates(index_n2)

        return math.sqrt((n1_x - n2_x) ** 2 + (n1_y - n2_y) ** 2)

    def computeDistanceLineToPoint(self, node1, node2, target_node) -> float:
        # Computes the shortest distance between an edge and a node non in that edge using: Line defined by two points

        (x_node1, y_node1) = self.nodes.get(node1)  # type: ignore
        (x_node2, y_node2) = self.nodes.get(node2)  # type: ignore
        (x_target_node, y_target_node) = self.nodes.get(target_node)  # type: ignore

        current_distance = abs(
            ((x_node2 - x_node1) * (y_node1 - y_target_node))
            - ((x_node1 - x_target_node) * (y_node2 - y_node1))
        ) / math.sqrt(((x_node2 - x_node1) ** 2) + ((y_node2 - y_node1) ** 2))

        return current_distance


class Graph_GEO(CompleteGraph):
    def getLatLong(self, index: int) -> Tuple[float, float]:
        # Returns the latitude and the longitude of the specific node

        (latitude, longitude) = self.nodes.get(index)  # type: ignore
        return latitude, longitude

    def getLatLongInRadiant(self, index: int) -> Tuple[float, float]:
        # Returns the latitude and the longitude of the specific node in radiant

        (latitude, longitude) = self.nodes.get(index)  # type: ignore
        return Graph_GEO.toRadiant(latitude), Graph_GEO.toRadiant(longitude)

    def computeDistance(self, node_x: int, node_y: int) -> int:
        # Compute the distance betwee node_x and node_y

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
        # This is a static method and returns the value converted in radiant
        PI: float = 3.141592
        deg: int = (int)(value)
        minimum: float = value - deg

        return PI * (deg + 5.0 * minimum / 3.0) / 180.0

    # Returns a Dict contianing the distance between all nodes


    def computeDistanceLineToPoint(self, node1, node2, target_node) -> float:
        # https://www.movable-type.co.uk/scripts/latlong.html

        def get_bearing(lat1, long1, lat2, long2):
            dLon = long2 - long1
            x = math.cos(Graph_GEO.toRadiant(lat2)) * math.sin(
                Graph_GEO.toRadiant(dLon)
            )
            y = math.cos(Graph_GEO.toRadiant(lat1)) * math.sin(
                Graph_GEO.toRadiant(lat2)
            ) - math.sin(Graph_GEO.toRadiant(lat1)) * math.cos(
                Graph_GEO.toRadiant(lat2)
            ) * math.cos(
                Graph_GEO.toRadiant(dLon)
            )
            brng = np.arctan2(x, y)
            brng = np.degrees(brng)

            return brng

        lat1, lon1 = self.getCoordinates(node1)
        lat2, lon2 = self.getCoordinates(node2)
        latt, lont = self.getCoordinates(target_node)

        RRR: float = 6378.388  # Approximate radius earth

        angular_distance_node1_target_node = self.getDistance(node1, target_node) / RRR
        bearing_n1_nTarget = get_bearing(lat1, lon1, latt, lont)
        bearing_n1_n2 = get_bearing(lat1, lon1, lat2, lon2)

        angular_cross_track_distance = (
            math.asin(
                math.sin(angular_distance_node1_target_node)
                * math.sin(bearing_n1_nTarget - bearing_n1_n2)
            )
            * RRR
        )
        along_track_distance = (
            math.acos(
                math.cos(angular_distance_node1_target_node)
                / math.cos(angular_cross_track_distance / RRR)
            )
            * RRR
        )

        return along_track_distance
