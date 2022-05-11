from data_structures.Complete_graphs import * # type: ignore
import os
from farthest_insertion import farthest_insertion
from data_structures import Complete_graphs
def main():

    foldername: str = "tsp_dataset"
    for filename in os.listdir(foldername):

        #  this requires to me more then 15 minutes if the
        # dsj1000 is used (using pypy, python not tested)
        if filename != "gr229.tsp":
            continue
        Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        Result = farthest_insertion(Graph)
        print(Result)


if __name__ == "__main__":
    main()
