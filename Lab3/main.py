import gc
import os
import math
import sys
from time import perf_counter_ns
from typing import List  # Dict unused
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from multiprocessing import Process  # type: ignore

from data_structures.graph import *  # type: ignore

from Karger_and_Stein import Karger_and_Stein
from stoerWagner import stoerWagner


def measureTime(Graphs: List[Graph], Function, Weights, Time, Discovery_time):
    # Prints the function name
    if Proc:
        print(Function)

    K: List[Tuple[int, int]] = []
    temp_time = 0  # List of times

    if Function.__name__ == "stoerWagner":
        iterations = 3
    else:
        iterations = 1  # Iterations

    current: int = 1  # Progress bar's counter
    start_time_bar = perf_counter_ns()
    end_time = 0
    for graph in Graphs:
        Results = []
        temp_time = []
        discovered_times = []
        gc.disable()

        for _ in range(iterations):

            start_time = perf_counter_ns()

            Result, D_time = Function(graph)

            end_time = perf_counter_ns()
            Results.append(Result)
            discovered_times.append(D_time - start_time)
            temp_time.append(end_time - start_time)
            # Prints a progress bar for the specific function
            progress_bar(
                current,
                (len(Graphs) * iterations),
                perf_counter_ns() - start_time_bar,
                Function.__name__,
            )
            current += 1

        gc.enable()
        Time.append(sum(temp_time) / iterations)
        Weights.append(min(Results))

        Discovery_time.append(discovered_times[Results.index(min(Results))])
    print("\n")
    return Time, Weights


def progress_bar(progress: int, total: int, current_time, name) -> None:
    if Proc:
        current_time = current_time / 10**6  # Conversion to ms
        print(f"Function {name}: {progress}/{total} - {current_time}")
    else:
        percent = 100 * (progress / float(total))  # Obtaining the percent
        bar = "???" * int(percent) + "_" * (100 - int(percent))  # Building the bar
        current_time = current_time / 10**6  # Conversion to ms
        print(f"\r|{bar}|{percent:.2f}% - {current_time:.2f} ms", end="\r")


def print_to_file(
    Output,
    Times,
    Discovery_Minimum_Cut,
    Path_File,
):
    saving_data = []
    saving_data.append(("Solution", "Run times", "Run times minimim cut"))
    for i in range(len(Output)):
        saving_data.append((Output[i], Times[i], Discovery_Minimum_Cut[i]))

        mat = np.matrix(saving_data)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv(Path_File, sep="\t", header=False, index=False)


def functionExecution(Graphs, Function, FilePath: str) -> None:
    Output: List[int] = []
    Times: List[float] = []
    Discovery: List[float] = []
    measureTime(Graphs, Function, Output, Times, Discovery)

    print_to_file(Output, Times, Discovery, FilePath)

    graph_sizes = [graph.dimension for graph in Graphs]
    graph_edge_sized = [len(list(G.getEdges().keys())) for G in Graphs]
    pyplot(graph_sizes, graph_edge_sized, sorted(Times), Function.__name__)


def pyplot(graphs_sizes, graph_edge_sized, times_Function, Function):
    ################## pyplot ##################
    if Function == "stoerWagner":
        C = int(
            times_Function[-1]
            / (
                graph_edge_sized[-1] * graphs_sizes[-1]
                + graphs_sizes[-1] ** 2 * math.log2(graphs_sizes[-1])
            )
        )  # Takes the last elements as reference
        reference = [
            (graph_edge_sized[i] * n + n**2 * math.log2(n)) * C
            for i, n in enumerate(graphs_sizes)
        ]
    else:
        C = int(
            times_Function[-1]
            / (graphs_sizes[-1] ** 2 * math.log2(graphs_sizes[-1]) ** 3)
        )  # Takes the last elements as reference
        reference = [n**2 * math.log2(n) ** 3 * C for n in graphs_sizes]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, times_Function)
    plt.title(Function)
    plt.legend(["Reference", Function])
    plt.ylabel("run time (ns)")
    plt.xlabel("size")
    plt.savefig("RESULTS/PLOTS/" + Function + ".png")
    plt.close()


def main():
    global Proc
    Proc = False
    print(sys.argv)
    if sys.argv[1] == "-p":
        Proc = True
    Graphs: List[Graph] = []
    foldername = "dataset"
    
    for filename in sorted(os.listdir(foldername)):  # Use [:x] to set a limit

        G = Graph.initialize_from_file(foldername + "/" + filename)
        Graphs.append(G)

    if Proc:
        P1 = Process(
            target=functionExecution,
            args=(Graphs, Karger_and_Stein, "RESULTS/KARGER_STEIN.csv"),
        )

        P2 = Process(
            target=functionExecution,
            args=(Graphs, stoerWagner, "RESULTS/STOER_WAGNER.csv"),
        )

        processes = [P1, P2]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    else:
        functionExecution(Graphs, Karger_and_Stein, "RESULTS/KARGER_STEIN.csv")
        functionExecution(Graphs, stoerWagner, "RESULTS/STOER_WAGNER.csv")


if __name__ == "__main__":
    main()
