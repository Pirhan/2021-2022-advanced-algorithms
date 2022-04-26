from data_structures.graph import Graph
import algorithms as algorithms

from time import perf_counter_ns
import gc
import os
import pandas as pd
import numpy as np


def measureTime(Graphs, Function, MSTs, Time):
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
    foldername = "tsp_dataset"
    for filename in sorted(os.listdir(foldername)):
        graph = Graph()
        graph.initialize_from_file(foldername + "//" + filename)
        Graphs.append(graph)
        Graphs_names.append(filename)
        print(filename, "\t=>\tOK")

    # no calls to the run algorithms for the moment
    # Run the algorithms and computes all the measurements
    # param Multiprocess = True/False
    # run(
    #  Graphs,
    #    MSTs_Weights_Prim,
    #    MSTs_Weights_Kruskal,
    #    MSTs_Weights_Kruscal_Efficient,
    #    run_times_Prim,
    #    run_times_Kruskal,
    #    run_times_Kruskal_Efficient,
    # )

    # graph_data = []  # Obtaining data for the graphs references
    # for graph in Graphs:
    #    n_nodes = len(graph.nodes)
    #    n_edges = len(list(graph.edges.keys()))
    #    graph_data.append((n_nodes, n_edges))


def run(
    Graphs,
    MSTs_Weights_Prim,
    MSTs_Weights_Kruskal,
    MSTs_Weights_Kruscal_Efficient,
    run_times_Prim,
    run_times_Kruskal,
    run_times_Kruskal_Efficient,
):
    # WARNING Don't let Kruskal run on the entire graph dataset. It takes too long.

    measureTime(Graphs, algorithms.Prim_Heap, MSTs_Weights_Prim, run_times_Prim)
    measureTime(Graphs, algorithms.Kruskal, MSTs_Weights_Kruskal, run_times_Kruskal)
    measureTime(
        Graphs,
        algorithms.Efficient_Kruskal,
        MSTs_Weights_Kruscal_Efficient,
        run_times_Kruskal_Efficient,
    )

    saving_data_Prim = []
    for i in range(len(Graphs)):
        saving_data_Prim.append((run_times_Prim[i], MSTs_Weights_Prim[i]))

    mat = np.matrix(saving_data_Prim)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/Prim.csv", sep="\t", header=False, index=False)

    saving_data_Kruskal_Eff = []
    for i in range(len(Graphs)):
        saving_data_Kruskal_Eff.append(
            (run_times_Kruskal_Efficient[i], MSTs_Weights_Kruscal_Efficient[i])
        )

    mat = np.matrix(saving_data_Kruskal_Eff)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/Kruskal_Eff.csv", sep="\t", header=False, index=False)

    saving_data_Kruskal = []
    for i in range(len(Graphs)):
        saving_data_Kruskal.append((run_times_Kruskal[i], MSTs_Weights_Kruskal[i]))

    mat = np.matrix(saving_data_Kruskal)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/Kruskal.csv", sep="\t", header=False, index=False)

    data_to_file(
        Graphs, MSTs_Weights_Prim, MSTs_Weights_Kruskal, MSTs_Weights_Kruscal_Efficient
    )


def data_to_file(
    Graphs,
    MSTs_Weights_Prim,
    MSTs_Weights_Kruskal,
    MSTs_Weights_Kruscal_Efficient,
):
    """Extracts all the weights computed by the algorithms, writing them in a .csv file"""

    table = [["Prim", "Kruskal", "Kruskal Efficient"]]

    difference = len(MSTs_Weights_Kruskal) < len(Graphs)
    if difference > 0:  # Adding empty fields to the table
        for _ in range(difference):
            MSTs_Weights_Kruskal.append(None)

    for i in range(len(Graphs)):
        table.append(
            [
                MSTs_Weights_Prim[i],
                MSTs_Weights_Kruskal[i],
                MSTs_Weights_Kruscal_Efficient[i],
            ]
        )

    mat = np.matrix(table)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/weights.csv", sep="\t", header=False, index=False)


if __name__ == "__main__":
    main()
