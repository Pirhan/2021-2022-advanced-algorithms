from data_structures.graph import Graph
from data_structures.Complete_graphs import *
from Two_approximate import TwoApproximate
from nearest_neighbour import nearestNeighbour
from typing import List, Dict, Tuple, Set
from time import perf_counter_ns
import gc
import os
import pandas as pd
import numpy as np

Optimal_solutions : Dict[str,float] = {
"burma14.tsp":3323,
"ulysses16.tsp":6859,
"ulysses22.tsp":7013,
"eil51.tsp":426,
"berlin52.tsp":7542,
"kroD100.tsp":21294,
"kroA100.tsp":21282,
"ch150.tsp":6528,
"gr202.tsp":40160,
"gr229.tsp":134602,
"pcb442.tsp":50778,
"d493.tsp":35002,
"dsj1000.tsp":18659688,
}

def measureTime(Graphs, Function, Weights, Time):
    temp_time = 0
    for c_graph in Graphs:
        print(Function, "\t=>\t", Graphs.index(c_graph) + 1)
        gc.disable()
        Result = []
        temp_time = []
        iterations = 1
        for _ in range(iterations):
            start_time = perf_counter_ns()

            Result = Function(c_graph)  # Function call

            end_time = perf_counter_ns()
            
            temp_time.append(end_time - start_time)
        
        gc.enable()
        Time.append(sum(temp_time)/iterations)
        Weights.append(Result)

    return Time, Weights

def main():
    CompGraphs : List[float] = [] 
    foldername = "tsp_dataset"
    optimal_sol = []
    for filename in sorted(os.listdir(foldername)):
        optimal_sol.append(Optimal_solutions.get(filename)) # Possible None
        CompGraph = CompleteGraph.initialize_from_file(foldername + "/" + filename)
        CompGraphs.append(CompGraph) # we don't need to understand the type of graph
    
    Output_two_approximate = []
    Output_nearest_neighbour = []
    #....

    Times_two_approximate = []
    Times_nearest_neighbour = []
    #....
    
    measureTime(CompGraphs, TwoApproximate, Output_two_approximate, Times_nearest_neighbour)
    measureTime(CompGraphs, nearestNeighbour, Output_nearest_neighbour, Times_nearest_neighbour)
    #....TODO Add the other function
    
    Error_calculated_two_approximate = []
    Error_calculated_nearest_neighbour = []
    #....

    for index, optimalError in enumerate(optimal_sol):   # They are in the same order
        Error_calculated_two_approximate.append((Output_two_approximate[index] - optimalError) / optimalError)
        Error_calculated_nearest_neighbour.append((Output_nearest_neighbour[index] - optimalError) / optimalError)
        #....

    saving_data_twoApprox = []
    saving_data_twoApprox.append(("Solution", "Run times", "Error"))
    for i in range(len(CompGraphs)):
        saving_data_twoApprox.append((Output_two_approximate[i], Times_two_approximate[i], Error_calculated_twoApprox[i]))

    mat = np.matrix(saving_data_twoApprox)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/TWOAPPROX.csv", sep="\t", header=False, index=False)

    saving_data_nearest_neighbour= []
    saving_data_tnearest_neighbour.append(("Solution", "Run times", "Error"))
    for i in range(len(CompGraphs)):
        saving_data_nearest_neighbour.append((Output_nearest_neighbour[i], Times_nearest_neighbour[i], Error_calculated_nearest_neighbour[i]))

    mat = np.matrix(saving_data_nearest_neighbour)
    df = pd.DataFrame(data=mat.astype(str))
    df.to_csv("RESULTS/NEAREST_NEIGHBOUR.csv", sep="\t", header=False, index=False)


if __name__ == "__main__":
    main()
