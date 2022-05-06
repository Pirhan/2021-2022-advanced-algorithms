from data_structures.Complete_graphs import * # type: ignore
import os
import geopy.distance  # type: ignore
from Two_approximate import *
from data_structures import Complete_graphs


def main():

    foldername: str = "tsp_dataset"
    for filename in os.listdir(foldername):
        
        if filename != "ch150.tsp": continue
        Graph = initialize_from_file(foldername + "/" + filename)
        Result = TwoApproximate(Graph)
        print(Result)


    """print(
        "Geopy distance =>\t",
        geopy.distance.distance((16.47, 96.10), (21.52, 95.59)).km,
    )"""

def initialize_from_file(filename: str) -> None:
        """ Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            start = 0

            end = 0
            for index, line in enumerate(lines):
                if line.startswith("DIMENSION"):
                    graph_dimension = int(line.split()[1])  # could be useful when deciding if repeat or not an algorithm if the problem instance is small
                if line.startswith("EDGE_WEIGHT_TYPE"):
                    graph_type = line.split()[1]
                if line.startswith("NODE_COORD_SECTION"):
                    start = index
                if line.startswith("EOF"):
                    end = index
            
            
            if graph_type == "EUC_2D": Comp_graph = Graph_EUC()
            if graph_type == "GEO" : Comp_graph = Graph_GEO()

            Comp_graph.dimension = graph_dimension
            for line in lines[start + 1 : end]:

                node: int = int(line.split()[0])
                x_coord: float = float(line.split()[1])
                y_coord: float = float(line.split()[2])

                Comp_graph.add_node(node, x_coord, y_coord)
                
            file.close()
        return Comp_graph

if __name__ == "__main__":
    main()
