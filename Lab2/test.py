from data_structures.GEO_graph import Graph_GEO  # type: ignore
import os
import geopy.distance  # type: ignore
from Two_approximate import *


def main():

    foldername: str = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        if filename == "burma14.tsp":
            Graph = Graph_GEO()
            Graph.initialize_from_file(foldername + "/" + filename)
            Result = Efficient_Kruskal(Graph)
            print(Result.getEdges().items())


    """print(
        "Geopy distance =>\t",
        geopy.distance.distance((16.47, 96.10), (21.52, 95.59)).km,
    )"""


if __name__ == "__main__":
    main()
