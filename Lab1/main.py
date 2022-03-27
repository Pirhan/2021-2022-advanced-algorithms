import os
from data_structures.graph import Graph
import algorithms
from time import perf_counter_ns
import gc
import matplotlib.pyplot as plt

def measureTime(Graphs: list, Function):
    Time = []
    MSTs = []
    temp_time = 0
    for Graph in Graphs:
        gc.disable()
        start_time = perf_counter_ns()

        temp_time = Function(Graph)        # Function call

        end_time = perf_counter_ns()
        gc.enable()
        MSTs.append(temp_time)
        Time.append(end_time-start_time)

    sum_times += (end_time - start_time)/len(Graphs)
    
    #avg_time = int(round(sum_times/num_instances))
    return Time, MSTs

def main():
    
    Graphs = []
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        graph = Graph()
        graph.inizialize(foldername + "//" + filename)
        Graphs.append(graph)

    """ graph = Graph()
    graph.inizialize(foldername + "//" + 'input_random_01_10.txt') """

    algorithms.Efficient_Kruskal(graph)
    print("_"*30)
    algorithms.Kruskal(graph)
    print("_"*30)
    algorithms.Prim_Heap(graph)

    graphs_sizes = [len(graph.get_nodes()) for graph in Graphs]
    run_times_Prim, MSTs_Weights_Prim = measureTime(Graphs, algorithms.Prim_Heap)
    run_times_Kruskal, MSTs_Weights_Kruscal = measureTime(Graphs, algorithms.Kruskal)
    run_times_Kruskal_efficient, MSTs_Weights_Kruscal_efficient = measureTime(Graphs, algorithms.Efficient_Kruska)

    reference = [69 * size for size in len(Graph)]
    plt.plot(graphs_sizes, run_times_Prim)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.plot(graphs_sizes, run_times_Kruskal_efficient)
    plt.plot(graphs_sizes, reference)
    plt.legend(["Prim","Kruscal", "Kruskal_Efficient", "69 * N"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.show()
    
    
if __name__ == '__main__':
    main()