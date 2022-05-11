from data_structures.Complete_graphs import *  # type: ignore
from data_structures.graph import Graph  # type: ignore
import os
from data_structures import Complete_graphs  # type: ignore


from typing import List, Tuple
import math
import numpy as np


def triangular_inequality(graph:CompleteGraph, node1, node2, node_intermediate):
    first_intermediate_distance: float = graph.getDistance(node1, node_intermediate)
    intermediate_second_distance: float = graph.getDistance(node_intermediate, node2)
    first_second_distance: float = graph.getDistance(node1, node2)
    return (
        first_intermediate_distance
        + intermediate_second_distance
        - first_second_distance
    )


def inizialization(graph:CompleteGraph, starting_node, node_not_in_path)->int:
    maximum_distance = np.max(graph.Distances[starting_node-1])
    farthest_node = (np.where(graph.Distances[starting_node-1] == maximum_distance))[0]
    return farthest_node[0]

def selection(graph:CompleteGraph, nodes_not_in_path, final_path)->int:

    maximumDistance = 0  # lower bound for maximum distance possible
    farthest_node = 0    # this will hold the farthest distanced node

    for new_node in nodes_not_in_path:
        biggest_distance = 0
        for visited_node in final_path:
            distance = graph.getDistance(visited_node, new_node)

            if distance > biggest_distance:
                biggest_distance= distance

        if biggest_distance > maximumDistance:
            maximumDistance = biggest_distance
            farthest_node = new_node


    return farthest_node

def insertion(graph:CompleteGraph, node, final_path):
    final_path_tuple = [(final_path[final_path.index(x) - 1], x) for x in final_path[1:]]
    
    nearest_edge = ()
    minimumDistance = float("+Infinity")
    for (node1, node2) in final_path_tuple:
        distance = triangular_inequality(graph, node1, node2, node)
        if distance < minimumDistance:
            minimumDistance = distance
            nearest_edge = (node1, node2)
    
    return nearest_edge

        

def farthest_insertion(graph:CompleteGraph)->float:
    final_path: List[int] = []
    nodes_not_in_path: List[int] = list(graph.getNodes())
    starting_node = list(graph.getNodes())[0]
    nodes_not_in_path.remove(starting_node)
    
    second_node = inizialization(graph, starting_node, nodes_not_in_path)
    final_path.append(starting_node)
    final_path.append(second_node)
    nodes_not_in_path.remove(second_node)

    while len(nodes_not_in_path)>0:
        next_node = selection(graph, nodes_not_in_path, final_path)

        (node1, node2) = insertion(graph, next_node, final_path)
        index_node1 = final_path.index(node1)
        index_node2 = final_path.index(node2)

        first_part = final_path[:index_node1+1]
        second_part = final_path[index_node2:]
        final_path = first_part + [next_node] + second_part

        
        nodes_not_in_path.remove(next_node)

    
    final_path_tuple = [(final_path[final_path.index(x) - 1], x) for x in final_path[1:]]
    final_path_tuple.append((final_path[-1], starting_node))
    print(final_path_tuple)
    total_weight: float = 0.00
    for (n1, n2) in final_path_tuple:
        total_weight += graph.getDistance(n1, n2)

    return total_weight
