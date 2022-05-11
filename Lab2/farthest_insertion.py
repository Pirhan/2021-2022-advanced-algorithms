from data_structures.Complete_graphs import *  # type: ignore
from data_structures.graph import Graph  # type: ignore
import os
from data_structures import Complete_graphs  # type: ignore


from typing import List, Tuple
import math
import numpy as np


def triangular_inequality(graph: CompleteGraph, node1, node2, node_intermediate) -> float:  # type: ignore
    # Computes the triangular inequality
    first_intermediate_distance: float = graph.getDistance(node1, node_intermediate)
    intermediate_second_distance: float = graph.getDistance(node_intermediate, node2)
    first_second_distance: float = graph.getDistance(node1, node2)
    return (
        first_intermediate_distance
        + intermediate_second_distance
        - first_second_distance
    )


def inizialization(graph: CompleteGraph, starting_node, node_not_in_path) -> int:  # type: ignore
    # Pick the maximum distance between the starting_node and the others, then returns the relative node
    maximum_distance = np.max(graph.Distances[starting_node - 1])
    farthest_node = (np.where(graph.Distances[starting_node - 1] == maximum_distance))[
        0
    ]  # Obtaining the corresponding node. np.where returns a list of array having that specific distance form starting_node
    # Pick the first array containing the node
    return farthest_node[0]  # Extracting the node from the array


def selection(graph: CompleteGraph, nodes_not_in_path, final_path) -> int:  # type: ignore

    maximumDistance = 0  # lower bound for maximum distance possible
    farthest_node = 0  # this will hold the farthest distanced node

    for new_node in nodes_not_in_path:
        biggest_distance = 0  # Will contain the biggest distance founded between this node and the path
        for visited_node in final_path:
            distance = graph.getDistance(
                visited_node, new_node
            )  # Distance between this node and visited_node

            if distance > biggest_distance:
                biggest_distance = distance  # If the new distance is bigger than the previous, store it

        if (
            biggest_distance > maximumDistance
        ):  # If the biggest distance computed form the node and the path is founded, store it
            maximumDistance = biggest_distance
            farthest_node = new_node  # This can be the node we are searching

    return farthest_node


def insertion(graph: CompleteGraph, node, final_path):  # type: ignore
    final_path_tuple = [
        (final_path[final_path.index(x) - 1], x) for x in final_path[1:]
    ]  # Es. from [1,2,4,5] to [(1,2),(2,4),(4,5)]

    nearest_edge: Tuple[int, int] = (0, 0)  # Empty tuple
    minimumDistance = float("+Infinity")  # Useful for the comparison
    for (node1, node2) in final_path_tuple:
        distance = triangular_inequality(
            graph, node1, node2, node
        )  # Computing the triangular_inequality
        if distance < minimumDistance:
            minimumDistance = distance  # If this distance is smaller than the "global" one, than store it as the current minimumDistance
            nearest_edge = (node1, node2)  # Candidate edge

    return nearest_edge


def farthest_insertion(graph: CompleteGraph) -> float:  # type: ignore
    final_path: List[int] = []  # This list will contain the final path
    nodes_not_in_path: List[int] = list(graph.getNodes())  # Initially = N
    starting_node = list(graph.getNodes())[0]  # Pick the first node as starting node
    nodes_not_in_path.remove(starting_node)  # N - starting_node

    second_node = inizialization(
        graph, starting_node, nodes_not_in_path
    )  # Pick the farthest node form the starting node
    final_path.append(starting_node)  # Adding starting node to the final path
    final_path.append(second_node)  # Adding second node to final path
    nodes_not_in_path.remove(
        second_node
    )  # Removing the second node from the list of non in path

    while len(nodes_not_in_path) > 0:
        next_node = selection(
            graph, nodes_not_in_path, final_path
        )  # Pick the farthest node form the path

        (node1, node2) = insertion(
            graph, next_node, final_path
        )  # Using the tri_ineq search for the nearest edge
        index_node1 = final_path.index(
            node1
        )  # Obtaining the index corresponding to the node
        index_node2 = final_path.index(node2)

        first_part = final_path[
            : index_node1 + 1
        ]  # Splitting the path in order to add the new node in the nearest edge
        second_part = final_path[index_node2:]
        final_path = (
            first_part + [next_node] + second_part
        )  # Recomposing the final path

        nodes_not_in_path.remove(next_node)

    final_path_tuple = [
        (final_path[final_path.index(x) - 1], x) for x in final_path[1:]
    ]  # Again Es. from [1,2,4,5] to [(1,2),(2,4),(4,5)], this is needed to compute the total_weight
    final_path_tuple.append(
        (final_path[-1], starting_node)
    )  # Adding the starting node to the end of the path
    # print(final_path_tuple)
    total_weight: float = 0.00
    for (n1, n2) in final_path_tuple:
        total_weight += graph.getDistance(n1, n2)  # Computing the sum of the weights

    return total_weight
