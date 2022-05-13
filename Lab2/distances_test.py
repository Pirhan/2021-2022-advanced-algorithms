from typing import List, Dict, Tuple, KeysView
from geopy.distance import geodesic as GD
from geopy.distance import great_circle as GRC
import math
def main():
    def toRadiant(
        value: float,
    ) -> float:
        PI: float = 3.141592
        deg: int = (int)(value)
        minimum: float = (
            value - deg
        )  # min is also a function -> bit confusing -> renamed to minimum

        return PI * (deg + 5.0 * minimum / 3.0) / 180.0


    def getDistance(node_x: Tuple[float, float], node_y: Tuple[float,float]) -> int:

        RRR: float = 6378.388
        (lat_x, lon_x) = node_x
        (lat_y, lon_y) = node_y
        latitude_x, longitude_x = toRadiant(lat_x), toRadiant(lon_x)
        latitude_y, longitude_y = toRadiant(lat_y), toRadiant(lon_y)
        q1: float = math.cos(longitude_x - longitude_y)
        q2: float = math.cos(latitude_x - latitude_y)
        q3: float = math.cos(latitude_x + latitude_y)
        return (int)(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

    # Returns a Dict contianing the distance between all nodes

    def getDistance_2(node_x: Tuple[float, float], node_y: Tuple[float, float]) -> float:
       
        # approximate radius of earth in km
        approximate_radius_earth: float = 6373.0

        (lat_x, lon_x) = node_x
        (lat_y, lon_y) = node_y
        latitude_x, longitude_x = toRadiant(lat_x), toRadiant(lon_x)
        latitude_y, longitude_y = toRadiant(lat_y), toRadiant(lon_y)
        dlon: float = longitude_y - longitude_x
        dlat: float = latitude_y - latitude_x

        versine: float = (
            math.sin(dlat / 2) ** 2
            + math.cos(latitude_x) * math.cos(latitude_y) * math.sin(dlon / 2) ** 2
        )  # half of versine of an angle
        haversine_distance: float = 2 * math.atan2(
            math.sqrt(versine), math.sqrt(1 - versine)
        )  # haversine distance, computes the versine of an angle, required for computing the haversine distance

        return approximate_radius_earth * haversine_distance

    def geopy(node_x: Tuple[float, float], node_y: Tuple[float, float])->float:
      
        return geopy.distance.distance(node_x, node_y)


    Coordinate_x = (16.47, 96.10)
    Coordinate_y = (21.52, 95.59)
    print("TSPLIB FAQ: ", getDistance(Coordinate_x, Coordinate_y), "km")
    print("Heversine: ", getDistance_2(Coordinate_x, Coordinate_y), "km")
    print("Geopy: ", GD(Coordinate_x, Coordinate_y))
    print("Geopy great cycle: ", GRC(Coordinate_x, Coordinate_y))

if __name__ == "__main__":
    main()