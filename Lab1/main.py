import os
from data_structures.graph import load_graph_AL

def main():
    
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        graph = load_graph_AL()
        print(filename, " => ", graph.inizialize(foldername + "//" + filename))
    
if __name__ == '__main__':
    main()