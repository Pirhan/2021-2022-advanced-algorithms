import gc
import os
from time import perf_counter_ns
from typing import Dict, List

import numpy as np
import pandas as pd  # type: ignore

from data_structures.Complete_graphs import *  # type: ignore
from nearest_neighbour import nearestNeighbour
from Two_approximate import TwoApproximate
from cheapest_insertion import cheapest_insertion

Optimal_solutions: Dict[str, float] = {
    "burma14.tsp": 3323,
    "ulysses16.tsp": 6859,
    "ulysses22.tsp": 7013,
    "eil51.tsp": 426,
    "berlin52.tsp": 7542,
    "kroD100.tsp": 21294,
    "kroA100.tsp": 21282,
    "ch150.tsp": 6528,
    "gr202.tsp": 40160,
    "gr229.tsp": 134602,
    "pcb442.tsp": 50778,
    "d493.tsp": 35002,
    "dsj1000.tsp": 18659688,
}


def measureTime(Graphs, Function, Weights, Time):
    print(Function)
    temp_time = 0  # List of times
    iterations = 1  # Iterations
    current: int = 1  # Progress bas's counter
    start_time_bar = perf_counter_ns()
    end_time = 0
    for c_graph in Graphs:
        Result = []
        temp_time = []

        gc.disable()

        for _ in range(iterations):
           

            start_time = perf_counter_ns()

            Result = Function(c_graph)  # Function call

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
    Times_nearest_neighbour,
    Error_calculated_nearest_neighbour,
    Path_File,
):
    saving_data_nearest_neighbour = []
    saving_data_nearest_neighbour.append(("Solution", "Run times", "Error"))
    for i in range(len(Output_nearest_neighbour)):
        saving_data_nearest_neighbour.append(
            (
                Output_nearest_neighbour[i],
                Times_nearest_neighbour[i],
                Error_calculated_nearest_neighbour[i],
            )
        )

    mat = np.matrix(saving_data_nearest_neighbour)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv(Path_File, sep="\t", header=False, index=False)


def functionExecution(
    CompGraphs, optimal_sol: List[float], Function, FilePath: str
) -> None:
    Output: List[int] = []
    Times: List[float] = []
    measureTime(CompGraphs, Function, Output, Times)

    Error_calculated = []
    for index, optimalError in enumerate(optimal_sol):
        Error_calculated.append((Output[index] - optimalError) / optimalError)
    print_to_file(Output, Times, Error_calculated, FilePath)


def main():
    CompGraphs: List[float] = []
    foldername = "tsp_dataset"
    optimal_sol = []
    for filename in os.listdir(foldername):  # [:3]
        optimal_sol.append(Optimal_solutions.get(filename))  # Possible None
        CompGraph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        CompGraphs.append(CompGraph)  # we don't need to understand the type of graph

    functionExecution(CompGraphs, optimal_sol, TwoApproximate, "RESULTS/TWOAPPROX.csv")
    functionExecution(
        CompGraphs, optimal_sol, nearestNeighbour, "RESULTS/NEAREST_NEIGHBOUR.csv"
    )
    functionExecution(CompGraphs, optimal_sol, cheapest_insertion, "RESULTS/CHEAPEST_INSERTION.csv")
    # ....TODO Add the other function


if __name__ == "__main__":
    main()
