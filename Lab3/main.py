import gc, os, math
from time import perf_counter_ns
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore

from data_structures.graph import *

from Karger import Karger


def measureTime(Graphs, Function, Weights, Time):
    print(Function)
    temp_time = 0  # List of times
    iterations = 10  # Iterations
    current: int = 1  # Progress bar's counter
    start_time_bar = perf_counter_ns()
    end_time = 0
    for graph in Graphs:
        Result = []
        temp_time = []

        gc.disable()

        for _ in range(iterations):
           

            start_time = perf_counter_ns()

            Result = Function(graph,1)  # Function call FIXME setting k

            end_time = perf_counter_ns()

            temp_time.append(end_time - start_time)

            # Prints a progress bar for the specific function
            progress_bar(current, (len(Graphs) * iterations), perf_counter_ns() - start_time_bar)
            current += 1

        gc.enable()
        Time.append(sum(temp_time) / iterations)
        Weights.append(Result)
    print("\n")
    return Time, Weights


def progress_bar(progress: int, total: int, current_time) -> None:
    # Progress bar

    percent = 100 * (progress / float(total))  # Obtaining the percent
    bar = "█" * int(percent) + "_" * (100 - int(percent))  # Building the bar
    current_time = current_time / 10**6  # Conversion to ms
    print(f"\r|{bar}|{percent:.2f}% - {current_time:.2f} ms", end="\r")


def print_to_file(
    Output_nearest_neighbour,
    Times,
    Times_Minimum_Cut,
    Path_File,
):
    saving_data_nearest_neighbour = []
    saving_data_nearest_neighbour.append(("Solution", "Run times", "Run times minimim cut"))
    for i in range(len(Output_nearest_neighbour)):
        saving_data_nearest_neighbour.append(
            (   
                Output_nearest_neighbour[i],
                Times[i],
                Times_Minimum_Cut[i],
            )
        )

    mat = np.matrix(saving_data_nearest_neighbour)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv(Path_File, sep="\t", header=False, index=False)


def functionExecution(
    Graphs, Function, FilePath: str
) -> None:
    Output: List[int] = []
    Times: List[float] = []
    measureTime(Graphs, Function, Output, Times)

    
    print_to_file(Output, Times, Times, FilePath)           # FIXME The second Times needs to be releated to the minimum cut search

    graph_sizes = sorted([graph.dimension for graph in Graphs])
    pyplot(graph_sizes, sorted(Times), Function.__name__)
   

def pyplot(graphs_sizes, times_Function, Function):
    ################## pyplot ##################
       
    C = int(times_Function[-1]/graphs_sizes[-1]**2* math.log2(n)**3) # Takes the last elements as reference
    reference = [n**2 * math.log2(n)**3 *  C for n in graphs_sizes]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, times_Function)
    plt.title(Function)
    plt.legend(["Reference", Function])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('RESULTS/PLOTS/' + Function + '.png')
    plt.close()


def main():

    Graphs: List[float] = []
    foldername = "dataset"
    optimal_sol = []
    for filename in os.listdir(foldername):  
        G = Graph.initialize_from_file(foldername + "/" + filename)
        Graphs.append(G)  # we don't need to understand the graph type
    

    functionExecution(Graphs, Karger, "RESULTS/KARGER.csv")
    
    

if __name__ == "__main__":
    main()
