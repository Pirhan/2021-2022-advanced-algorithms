from data_structures.graph import Graph  # type: ignore
from stoerWagner import stoerWagner
from os import listdir


#  checked until file dataset/input_random_20_80.txt and everything seems fine
#  ie returns the minimum cut
#  check the from dataset/input_random_21_100.txt onward
def test():
    directory: str = "dataset"
    for filename in sorted(listdir(directory)[:2]):
        print("filename", filename)
        # break
        aGraph = Graph.initialize_from_file(filename=directory + "/" + filename)
        cut = stoerWagner(graph=aGraph)
        print()
        print("cut", cut)
        print()

        #  counter += 1


test()
