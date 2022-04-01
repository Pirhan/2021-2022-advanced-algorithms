from operator import index
import os, math
from data_structures.graph import Graph
import algorithms
from time import perf_counter_ns
import gc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from multiprocessing import Process


def measureTime(Graphs: list, Function, MSTs, Time):
    temp_time = 0
    for Graph in Graphs:
        print(Function, "\t=>\t", Graphs.index(Graph) + 1)
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
        #if count == 40: break 
        #count += 1
        graph = Graph()
        graph.inizialize(foldername + "//" + filename)
        Graphs.append(graph)
        Graphs_names.append(filename)
        print(filename, "\t=>\tOK")

    graphs_sizes = [len(graph.get_nodes()) for graph in Graphs]

    MSTs_Weights_Prim = [] 
    MSTs_Weights_Kruskal = []
    MSTs_Weights_Kruscal_Efficient = []
    run_times_Prim = []
    run_times_Kruskal_Efficient = []
    run_times_Kruskal = []
    
    # Run the algorithms and computes all the measurements
    # param Multiprocess = True/False 
    run(Graphs, MSTs_Weights_Prim, MSTs_Weights_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Prim, run_times_Kruskal, run_times_Kruskal_Efficient, False)

    
    graph_data = []                         # Obtaining data for the graphs references
    for graph in Graphs:
        n_nodes = len(graph.get_nodes())
        n_edges = len(list(graph.get_edges().keys()))
        graph_data.append((n_nodes, n_edges))

       
    pyplot_Kruskal(graphs_sizes, run_times_Kruskal, graph_data)

    pyplot_Kruskal_Efficient(graphs_sizes, run_times_Kruskal_Efficient, graph_data)

    pyplot_Prim(graphs_sizes, run_times_Prim, graph_data)

    pyplot_Complete(graphs_sizes, run_times_Prim, run_times_Kruskal, run_times_Kruskal_Efficient)

    data_to_file(Graphs, Graphs_names, MSTs_Weights_Prim, MSTs_Weights_Kruskal, MSTs_Weights_Kruscal_Efficient)




def run(Graphs, MSTs_Weights_Prim, MSTs_Weights_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Prim, run_times_Kruskal, run_times_Kruskal_Efficient, Multiprocess = True):
    if Multiprocess == False:
        ############## No processs ##############
        measureTime(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim)
        measureTime(Graphs, algorithms.Kruskal, MSTs_Weights_Kruskal, run_times_Kruskal)
        measureTime(Graphs, algorithms.Efficient_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Kruskal_Efficient)
        ########################################
    else:
        ############## processs ##############
        MSTs_Weights_Kruskal_1 = []
        MSTs_Weights_Kruskal_2 = []
        MSTs_Weights_Kruskal_3 = []
        MSTs_Weights_Kruskal_4 = []
        run_times_Kruskal_1 = [] # Kruskal on 1-39  graphs
        run_times_Kruskal_2 = [] # Kruskal on 40-52 graphs
        run_times_Kruskal_3 = [] # Kruskal on 53-62 graphs
        run_times_Kruskal_4 = [] # Kruskal on 63-68 graphs
       
        Prim_process = Process(target=measureTime, args=(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim))
        Kruskal_process_1 = Process(target=measureTime, args=(Graphs[:40], algorithms.Kruskal, MSTs_Weights_Kruskal_1, run_times_Kruskal_1))
        Kruskal_process_2 = Process(target=measureTime, args=(Graphs[40:53], algorithms.Kruskal, MSTs_Weights_Kruskal_2, run_times_Kruskal_2))
        Kruskal_process_3 = Process(target=measureTime, args=(Graphs[53:63], algorithms.Kruskal, MSTs_Weights_Kruskal_3, run_times_Kruskal_3))
        Kruskal_process_4 = Process(target=measureTime, args=(Graphs[63:], algorithms.Kruskal, MSTs_Weights_Kruskal_4, run_times_Kruskal_4))
        Kruskal_Efficient_process = processing.process(target=measureTime, args=(Graphs, algorithms.Efficient_Kruskal, MSTs_Weights_Kruscal_Efficient, run_times_Kruskal_Efficient))
        processs = [Prim_process, Kruskal_process_1, Kruskal_process_2, Kruskal_process_3, Kruskal_process_4, Kruskal_Efficient_process]
        for process in processs:
            process.start()
        
        for process in processs:
            process.join() 

        run_times_Kruskal.append(run_times_Kruskal_1 + run_times_Kruskal_2 + run_times_Kruskal_3 + run_times_Kruskal_4)
        MSTs_Weights_Kruskal.append(MSTs_Weights_Kruskal_1 + MSTs_Weights_Kruskal_2 + MSTs_Weights_Kruskal_3 + MSTs_Weights_Kruskal_4)

        #####################################

def data_to_file(Graphs, Graphs_names, MSTs_Weights_Prim, MSTs_Weights_Kruskal, MSTs_Weights_Kruscal_Efficient):
    """ Extracts all the weights computed by the algorithms, writing them in a .csv file """
    
    table = [["File name", "Prim", "Kruskal", "Kruskal Efficient"]]

    for i in range(len(Graphs)):
        table.append([Graphs_names[i], MSTs_Weights_Prim[i], MSTs_Weights_Kruskal[i],  MSTs_Weights_Kruscal_Efficient[i]])

    mat = np.matrix(table)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv('weights.csv', sep='\t', header=False, index=False)


def pyplot_Complete(graphs_sizes, run_times_Prim, run_times_Kruskal, run_times_Kruskal_Efficient):
    ############# pyplot Total ##############
    plt.plot(graphs_sizes, run_times_Prim)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.plot(graphs_sizes, run_times_Kruskal_Efficient)
    plt.title("N = " + str(graphs_sizes[-1]) + "    Single process")
    plt.legend(["Prim","Kruscal", "Kruskal_Efficient"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('All.png')
    plt.close()


def pyplot_Prim(graphs_sizes, run_times_Prim, graph_data):
    ############# pyplot Prim ##############
    reference = [n_e * math.log(n_n) * 10**6 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Prim)
    plt.title("Prim => O(m*log(n))")
    plt.legend(["Reference", "Prim"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Prim.png')
    plt.close()
    #####################################################

def pyplot_Kruskal_Efficient(graphs_sizes, run_times_Kruskal_Efficient, graph_data):
    ############# pyplot Efficient Kruskal ##############

    reference = [n_e * math.log(n_n) * 10**6 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Kruskal_Efficient)
    plt.title("Kruscal Efficient => O(m*log(n))")
    plt.legend(["Reference", "Kruskal_Efficient"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Kruskal_Efficient.png')
    plt.close()

    #####################################################

def pyplot_Kruskal(graphs_sizes, run_times_Kruskal, graph_data):
    ################## pyplot Kruskal ##################

    reference = [n_n * n_e * 10**6 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.title("Kruscal => O(n*m)")
    plt.legend(["Reference", "Kruskal"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Kruskal.png')
    plt.close()

    #####################################################
    
    
    
if __name__ == '__main__':
    main()