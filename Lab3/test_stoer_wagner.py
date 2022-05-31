from data_structures.graph import Graph  # type: ignore
from stoerWagner import stoerWagner
from os import listdir


def test():
    directory: str = "dataset"
    counter: int = 0
    for filename in sorted(listdir(directory)):
        if counter == 5:
            break
        aGraph = Graph.initialize_from_file(filename=directory + "/" + filename)
        cut = stoerWagner(graph=aGraph)
        print("filename", filename)
        print(cut)
        counter += 1


test()
