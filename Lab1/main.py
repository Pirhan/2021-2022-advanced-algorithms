import os
from data_structures.graph import load_graph_AL
import algorithms
from time import perf_counter_ns
import gc


def main():
    
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        graph = load_graph_AL()
        #print(filename, " => ", graph.inizialize(foldername + "//" + filename))
    graph = load_graph_AL()
    graph.inizialize(foldername + "//" + 'input_random_01_10.txt')
    print(algorithms.Efficient_Kruskal(graph))
    print("_"*30)
    print(algorithms.Kruskal(graph))
    print("_"*30)
    print(algorithms.Prim_Heap(graph))
    
    
if __name__ == '__main__':
    main()