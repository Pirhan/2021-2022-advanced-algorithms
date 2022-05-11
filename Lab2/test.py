from data_structures.Complete_graphs import * # type: ignore
import os
import geopy.distance  # type: ignore
from Two_approximate import *


def main():

    foldername: str = "tsp_dataset"
    for filename in os.listdir(foldername):
        
        if filename != "ch150.tsp": continue
        Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        Result = TwoApproximate(Graph)
        print(Result)


    """print(
        "Geopy distance =>\t",
        geopy.distance.distance((16.47, 96.10), (21.52, 95.59)).km,
    )"""

if __name__ == "__main__":
    main()
