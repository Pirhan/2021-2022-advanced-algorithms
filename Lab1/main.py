import os

# cythonized code start import
from graph_compiled import Graph
import algorithms_compiled as algorithms

# cythonized code end import
from time import perf_counter_ns
import gc
import pandas as pd
import numpy as np
from multiprocessing import Process


def measureTime(Graphs: list, Function, MSTs, Time):
    temp_time = 0
    for a_graph in Graphs:
        print(Function, "\t=>\t", Graphs.index(a_graph) + 1)
        gc.disable()
        start_time = perf_counter_ns()

        temp_time = Function(a_graph)  # Function call

        end_time = perf_counter_ns()
        gc.enable()
        MSTs.append(temp_time)
        Time.append(end_time - start_time)

    return Time, MSTs


def main():

    Graphs = []
    Graphs_names = []
    foldername = "mst_dataset"
    for filename in sorted(
        os.listdir(foldername)
    ):  # now generation of graph from file is in order(ouput from print more clear, sorted)
        graph = Graph()
        graph.inizialize(foldername + "//" + filename)
        Graphs.append(graph)
        Graphs_names.append(filename)
        print(filename, "\t=>\tOK")

    # graphs_sizes = [len(graph.get_nodes()) for graph in Graphs]

    MSTs_Weights_Prim = []
    MSTs_Weights_Kruskal = []
    MSTs_Weights_Kruscal_Efficient = []
    run_times_Prim = []
    run_times_Kruskal_Efficient = []
    run_times_Kruskal = []

    # Run the algorithms and computes all the measurements
    # param Multiprocess = True/False
    run(
        Graphs,
        MSTs_Weights_Prim,
        MSTs_Weights_Kruskal,
        MSTs_Weights_Kruscal_Efficient,
        run_times_Prim,
        run_times_Kruskal,
        run_times_Kruskal_Efficient,
        True,
    )

    graph_data = []  # Obtaining data for the graphs references
    for graph in Graphs:
        n_nodes = len(graph.get_nodes())
        n_edges = len(list(graph.get_edges().keys()))
        graph_data.append((n_nodes, n_edges))


def run(
    Graphs,
    MSTs_Weights_Prim,
    MSTs_Weights_Kruskal,
    MSTs_Weights_Kruscal_Efficient,
    run_times_Prim,
    run_times_Kruskal,
    run_times_Kruskal_Efficient,
    Multiprocess=True,
):
    # WARNING Don't let Kruskal run on the entire graph dataset. It takes too long.

    if Multiprocess is False:
        ############## No processs ##############
        measureTime(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim)
        measureTime(
            Graphs, algorithms.Kruskal, MSTs_Weights_Kruskal, run_times_Kruskal
        )  # Graphs[:50] requires 4 hours to compute
        measureTime(
            Graphs,
            algorithms.Efficient_Kruskal,
            MSTs_Weights_Kruscal_Efficient,
            run_times_Kruskal_Efficient,
        )
        ########################################
    else:
        ############## processs ##############
        MSTs_Weights_Kruskal_1 = []
        MSTs_Weights_Kruskal_2 = []
        MSTs_Weights_Kruskal_3 = []
        MSTs_Weights_Kruskal_4 = []
        MSTs_Weights_Kruskal_5 = []
        run_times_Kruskal_1 = []  # Kruskal on 1-39  graphs
        run_times_Kruskal_2 = []  # Kruskal on 40-52 graphs
        run_times_Kruskal_3 = []  # Kruskal on 53-59 graphs
        run_times_Kruskal_4 = []  # Kruskal on 60-64 graphs
        run_times_Kruskal_5 = []  # Kruskal on 65-68 graphs

        Prim_process = Process(
            target=measureTime,
            args=(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim),
        )
        Kruskal_process_1 = Process(
            target=measureTime,
            args=(
                Graphs[:40],
                algorithms.Kruskal,
                MSTs_Weights_Kruskal_1,
                run_times_Kruskal_1,
            ),
        )
        Kruskal_process_2 = Process(
            target=measureTime,
            args=(
                Graphs[40:53],
                algorithms.Kruskal,
                MSTs_Weights_Kruskal_2,
                run_times_Kruskal_2,
            ),
        )
        Kruskal_process_3 = Process(
            target=measureTime,
            args=(
                Graphs[53:60],
                algorithms.Kruskal,
                MSTs_Weights_Kruskal_3,
                run_times_Kruskal_3,
            ),
        )
        Kruskal_process_4 = Process(
            target=measureTime,
            args=(
                Graphs[60:65],
                algorithms.Kruskal,
                MSTs_Weights_Kruskal_4,
                run_times_Kruskal_4,
            ),
        )
        Kruskal_process_5 = Process(
            target=measureTime,
            args=(
                Graphs[65:],
                algorithms.Kruskal,
                MSTs_Weights_Kruskal_5,
                run_times_Kruskal_5,
            ),
        )
        Kruskal_Efficient_process = Process(
            target=measureTime,
            args=(
                Graphs,
                algorithms.Efficient_Kruskal,
                MSTs_Weights_Kruscal_Efficient,
                run_times_Kruskal_Efficient,
            ),
        )
        process = [
            Prim_process,
            Kruskal_process_1,
            Kruskal_process_2,
            Kruskal_process_3,
            Kruskal_process_4,
            Kruskal_process_5,
            Kruskal_Efficient_process,
        ]

        for proc in process:
            proc.start()

        for proc in process:
            proc.join()

        run_times_Kruskal.append(
            run_times_Kruskal_1
            + run_times_Kruskal_2
            + run_times_Kruskal_3
            + run_times_Kruskal_4
        )
        MSTs_Weights_Kruskal.append(
            MSTs_Weights_Kruskal_1
            + MSTs_Weights_Kruskal_2
            + MSTs_Weights_Kruskal_3
            + MSTs_Weights_Kruskal_4
        )

        ################################
    saving_data_Prim = []
    for i in range(len(Graphs)):
        saving_data_Prim.append((run_times_Prim[i], MSTs_Weights_Prim[i]))

    mat = np.matrix(saving_data_Prim)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("Prim.csv", sep="\t", header=False, index=False)

    saving_data_Kruskal = []
    for i in range(len(Graphs)):  # Use range(50)
        saving_data_Kruskal.append((run_times_Kruskal[i], MSTs_Weights_Kruskal[i]))

    mat = np.matrix(saving_data_Kruskal)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("Kruskal.csv", sep="\t", header=False, index=False)

    saving_data_Kruskal_Eff = []
    for i in range(len(Graphs)):
        saving_data_Kruskal_Eff.append(
            (run_times_Kruskal_Efficient[i], MSTs_Weights_Kruscal_Efficient[i])
        )

    mat = np.matrix(saving_data_Kruskal_Eff)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("Kruskal_Eff.csv", sep="\t", header=False, index=False)

    #####################################


def data_to_file(
    Graphs,
    Graphs_names,
    MSTs_Weights_Prim,
    MSTs_Weights_Kruskal,
    MSTs_Weights_Kruscal_Efficient,
):
    """Extracts all the weights computed by the algorithms, writing them in a .csv file"""

    table = [["File name", "Prim", "Kruskal", "Kruskal Efficient"]]

    for i in range(len(Graphs)):
        table.append(
            [
                Graphs_names[i],
                MSTs_Weights_Prim[i],
                MSTs_Weights_Kruskal[i],
                MSTs_Weights_Kruscal_Efficient[i],
            ]
        )

    mat = np.matrix(table)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("weights.csv", sep="\t", header=False, index=False)


if __name__ == "__main__":
    main()
