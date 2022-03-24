import os
from data_structures.graph import Graph
import algorithms
from time import perf_counter_ns
import gc


def main():
    
    foldername = "mst_dataset"
    #for filename in os.listdir(foldername):
        #graph = Graph()
        #print(filename, " => ", graph.inizialize(foldername + "//" + filename))
    graph = Graph()
    graph.inizialize(foldername + "//" + 'input_random_02_10.txt')
    algorithms.Efficient_Kruskal(graph)
    print("_"*30)
    algorithms.Kruskal(graph)
    print("_"*30)
    algorithms.Prim_Heap(graph)
    
    
if __name__ == '__main__':
    main()