from data_structures.Complete_graphs import * # type: ignore
import os
from farthest_insertion import farthest_insertion
from data_structures import Complete_graphs
from farthest_insertion_variant import farthest_insertion as f_i_variant
def main():

    foldername: str = "tsp_dataset"
    for filename in os.listdir(foldername):

        #  this requires to me more then 15 minutes if the
        # dsj1000 is used (using pypy, python not tested)
        if filename != "burma14.tsp":
            continue
        Graph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        Result = farthest_insertion(Graph)
        Result1 = f_i_variant(Graph)
        print("Slide version: ", Result, "/tVariant: ", Result1)


if __name__ == "__main__":
    main()
