import os
from data_structures.graph import load_graph_AL
import algorithms

def main():
    
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        graph = load_graph_AL()
        print(filename, " => ", graph.inizialize(foldername + "//" + filename))
    graph = load_graph_AL()
    graph.inizialize(foldername + "//" + 'input_random_01_10.txt')
    print(algorithms.Efficient_Kruskal(graph))
    
    
if __name__ == '__main__':
    main()