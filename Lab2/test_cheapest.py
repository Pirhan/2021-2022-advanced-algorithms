from data_structures.Complete_graphs import *  # type: ignore
import os
import cheapest_insertion
from typing import List


def main():

    foldername: str = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        #if filename == "burma14.tsp":
        Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        Result: List[int] = cheapest_insertion.cheapest_insertion(graph=Graph)
        print("filename:", filename, "->", Result)


if __name__ == "__main__":
    main()
