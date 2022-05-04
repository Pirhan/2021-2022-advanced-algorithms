from data_structures.EUC_graph import Graph_EUC  # type: ignore
import os
import nearest_neighbour
from typing import List


def main():

    foldername: str = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        if filename == "eil51.tsp":
            Graph = Graph_EUC()
            Graph.initialize_from_file(foldername + "/" + filename)
            Result: List[int] = nearest_neighbour.nearestNeighbour(graph=Graph)
            for i in Result:
                print(i)


if __name__ == "__main__":
    main()
