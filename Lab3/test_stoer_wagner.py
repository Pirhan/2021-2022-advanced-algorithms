from data_structures.graph import Graph  # type: ignore
from stoerWagner import globalMinimumCut
from os import listdir


def test():
    directory: str = "dataset"
    counter: int = 0
    for filename in sorted(listdir(directory)):
        if counter == 1:
            break
        aGraph = Graph.initialize_from_file(filename=directory + "/" + filename)
        cut = globalMinimumCut(graph=aGraph)
        print(cut)
        counter += 1


test()
