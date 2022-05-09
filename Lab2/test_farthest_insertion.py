from data_structures.Complete_graphs import * # type: ignore
import os
from farthest_insertion import farthest_insertion
from data_structures import Complete_graphs
def main():

    foldername: str = "tsp_dataset"
    for filename in os.listdir(foldername):

        if filename != "burma14.tsp":
            continue
        Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        Result = farthest_insertion(Graph)
        print(Result)


if __name__ == "__main__":
    main()