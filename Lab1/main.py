import os
from data_structures.graph import Graph
import algorithms
from time import perf_counter_ns
import gc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading



def measureTime(Graphs: list, Function, MSTs, Time):

    temp_time = 0
    for Graph in Graphs:
        gc.disable()
        start_time = perf_counter_ns()

        temp_time = Function(Graph)        # Function call

        end_time = perf_counter_ns()
        gc.enable()
        MSTs.append(temp_time)
        Time.append(end_time-start_time)

    return Time, MSTs

def main():
    
    Graphs = []
    Graphs_names = []
    foldername = "mst_dataset"
    count = 0
    for filename in os.listdir(foldername):
        if count == 30: break 
        count += 1
        graph = Graph()
        graph.inizialize(foldername + "//" + filename)
        Graphs.append(graph)
        Graphs_names.append(filename)

    graphs_sizes = [len(graph.get_nodes()) for graph in Graphs]

    MSTs_Weights_Prim = [] 
    MSTs_Weights_Kruskal = []
    MSTs_Weights_Kruscal_Efficient = []
    run_times_Prim = []
    run_times_Kruskal = []
    run_times_Kruskal_Efficient = []
    
    ############## No Threads ##############

    measureTime(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim)
    measureTime(Graphs, algorithms.Kruskal, MSTs_Weights_Kruskal, run_times_Kruskal)
    measureTime(Graphs, algorithms.Efficient_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Kruskal_Efficient)

    ########################################

    ############## Threads ##############
    """
    Prim_thread = threading.Thread(target=measureTime, args=(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim))
    Kruskal_thread = threading.Thread(target=measureTime, args=(Graphs, algorithms.Kruskal, MSTs_Weights_Kruskal, run_times_Kruskal))
    Kruskal_Efficient_thread = threading.Thread(target=measureTime, args=(Graphs, algorithms.Efficient_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Kruskal_Efficient))
    threads = [Prim_thread, Kruskal_thread, Kruskal_Efficient_thread]
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join() 
    """

    #####################################

    table = [["File name", "Prim", "Kruskal", "Kruskal Efficient"]]

    for i in range(len(Graphs)):
        table.append([Graphs_names[i], MSTs_Weights_Prim[i], MSTs_Weights_Kruskal[i],  MSTs_Weights_Kruscal_Efficient[i]])

    mat = np.matrix(table)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv('weights.csv', sep='\t', header=False, index=False)

    plt.plot(graphs_sizes, run_times_Prim)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.plot(graphs_sizes, run_times_Kruskal_Efficient)
    plt.title("N = " + str(graphs_sizes[-1]) + "    Multiple threads")
    plt.legend(["Prim","Kruscal", "Kruskal_Efficient"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.show()
    
    
if __name__ == '__main__':
    main()