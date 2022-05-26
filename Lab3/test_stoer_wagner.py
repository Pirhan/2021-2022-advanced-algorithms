from data_structures.graph import Graph  # type: ignore
from stoerWagner import globalMinimumCut
from os import listdir


def test():
    directory: str = "dataset"
    for filename in sorted(listdir(directory)):
        aGraph = Graph.initialize_from_file(filename=directory + "/" + filename)
        cut = globalMinimumCut(graph=aGraph)
        print(cut)


test()
