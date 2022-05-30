import gc, os, math
from time import perf_counter_ns
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore

from data_structures.graph import *

from Karger_and_Stein import Karger


def measureTime(Graphs : List[Graph], Function, Weights, Time, Discovery_time):
    print(Function)
    temp_time = 0  # List of times
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
            
            if Function.__name__=="Karger":
                # This will give us a probability of 1-1/n for Karger and Stain
                n = len(graph.getEdgesList())
                Result, D_time = Function(graph, int(n * math.log(n)/(n - 1)))  
            else:
                Result, D_time = Function(graph)

            end_time = perf_counter_ns()
            Results.append(Result)
            discovered_times.append(D_time - start_time)
            temp_time.append(end_time - start_time)

            # Prints a progress bar for the specific function
            progress_bar(
                current, (len(Graphs) * iterations), perf_counter_ns() - start_time_bar
            )
            current += 1

        gc.enable()
        Time.append(sum(temp_time) / iterations)
        Weights.append(min(Results))
        #print(len(Weights), len(Discovery_time))
        Discovery_time.append(discovered_times[Results.index(min(Results))])
    print("\n")
    return Time, Weights


def progress_bar(progress: int, total: int, current_time) -> None:
    # Progress bar

    percent = 100 * (progress / float(total))  # Obtaining the percent
    bar = "█" * int(percent) + "_" * (100 - int(percent))  # Building the bar
    current_time = current_time / 10 ** 6  # Conversion to ms
    print(f"\r|{bar}|{percent:.2f}% - {current_time:.2f} ms", end="\r")


def print_to_file(
    Output,
    Times,
    Discovery_Minimum_Cut,
    Path_File,
):
    saving_data = []
    saving_data.append(
        ("Solution", "Run times", "Run times minimim cut")
    )
    for i in range(len(Output)):
        saving_data.append(
            (Output[i], Times[i], Discovery_Minimum_Cut[i])
        )

        mat = np.matrix(saving_data)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv(Path_File, sep="\t", header=False, index=False)


def functionExecution(Graphs, Function, FilePath: str) -> None:
    Output: List[int] = []
    Times: List[float] = []
    Discovery : List[float] = []
    measureTime(Graphs, Function, Output, Times, Discovery)

    print_to_file(
        Output, Times, Discovery, FilePath
    )  # FIXME The second Times needs to be releated to the minimum cut search

    graph_sizes = sorted([graph.dimension for graph in Graphs])
    pyplot(graph_sizes, sorted(Times), Function.__name__)


def pyplot(graphs_sizes, times_Function, Function):
    ################## pyplot ##################
    C = int(
        times_Function[-1] / (graphs_sizes[-1] ** 2 * math.log2(graphs_sizes[-1]) ** 3)
    )  # Takes the last elements as reference
    reference = [n ** 2 * math.log2(n) ** 3 * C for n in graphs_sizes]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, times_Function)
    plt.title(Function)
    plt.legend(["Reference", Function])
    plt.ylabel("run time (ns)")
    plt.xlabel("size")
    plt.savefig("RESULTS/PLOTS/" + Function + ".png")
    plt.close()


def main():

    Graphs: List[float] = []
    foldername = "dataset"
    optimal_sol = []
    for filename in sorted(os.listdir(foldername)): # Use [:x] to set a limit 

        G = Graph.initialize_from_file(foldername + "/" + filename)
        Graphs.append(G)  
        

    functionExecution(Graphs, Karger, "RESULTS/KARGER_STEIN.csv")
    #functionExecution(Graph, function_name, "RESULTS/STOER_WAGNER")

if __name__ == "__main__":
    main()
