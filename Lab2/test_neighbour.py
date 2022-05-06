from data_structures.Complete_graphs import * # type: ignore
import os
import nearest_neighbour
from typing import List


def main():

    foldername: str = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        if filename == "eil51.tsp":
            Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
            Result: List[int] = nearest_neighbour.nearestNeighbour(graph=Graph)
            print(Result)


if __name__ == "__main__":
    main()
