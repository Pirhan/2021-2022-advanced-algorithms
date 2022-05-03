import math
from typing import List

class Graph_GEO:

    def __init__(self)->None:
        self.nodes = {}     # key = index; value = (longitude, latitude)

    def add_node(self,index, coordinate_x, coordinate_y):
        self.nodes[index] = (Graph_GEO.toRadiant(coordinate_x), Graph_GEO.toRadiant(coordinate_y))

    def getLL(self, index):
        (longitude, latitude) = self.nodes.get(index)
        return longitude, latitude
    
    def toRadiant(value):
        PI = 3.141592
        deg = (int)(value)
        min = value - deg

        return PI * (deg + 5.0 * min / 3.0) / 180.0


    def getDistance(self, node_x, node_y):

        RRR = 6378.388
        longitude_x, latitude_x = self.getLL(node_x)
        longitude_y, latitude_y = self.getLL(node_y)
        q1 = math.cos(longitude_x - longitude_y)
        q2 = math.cos(latitude_x - latitude_y)
        q3 = math.cos(latitude_x + latitude_y)
        return (int)(RRR * math.acos(0.5 * ((1.0 + q1)*q2 - (1.0 - q1)*q3)) + 1.0)
    
    def getDistance_2(self, node_x, node_y):
        """ Solution from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude/43211266#43211266"""
        # approximate radius of earth in km
        R = 6373.0

        lon1, lat1 = self.getLL(node_x)
        lon2, lat2 = self.getLL(node_y)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def initialize_from_file(self, filename: str) -> None:
        """ Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            start = 0 
            end = 0
            for index, line in enumerate(lines):
                if line.startswith("NODE_COORD_SECTION"):
                    start = index
                if line.startswith("EOF"):
                    end = index
            
            for line in lines[start + 1 : end]:

                index : int = int(line.split()[0])
                x_coord: float = float(line.split()[1])
                y_coord: float = float(line.split()[2])
                
                self.add_node(index, x_coord, y_coord)



        