from data_structures.Complete_graphs import * # type: ignore
import os
import geopy.distance  # type: ignore
from Two_approximate import *


def main():

    foldername: str = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        if filename == "burma14.tsp":
            Graph = Graph_GEO()
            Result = TwoApproximate(Graph, foldername + "/" + filename)
            print(Result)


    """print(
        "Geopy distance =>\t",
        geopy.distance.distance((16.47, 96.10), (21.52, 95.59)).km,
    )"""


if __name__ == "__main__":
    main()
