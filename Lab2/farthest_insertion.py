from data_structures.Complete_graphs import *  # type: ignore
from data_structures.graph import Graph  # type: ignore
import os
from data_structures import Complete_graphs  # type: ignore


from typing import List, Tuple

import numpy as np


def getDistancesMatrix(graph: CompleteGraph):  # type: ignore
    n_nodes = len(graph.getNodes())
    Distances = np.zeros((n_nodes, n_nodes))

    for first_index, node1 in enumerate(graph.getNodes()):
        for second_index, node2 in enumerate(graph.getNodes()):
            if node1 == node2:
                continue
            Distances[first_index, second_index] = graph.getDistance(node1, node2)

    return Distances


def triangular_inequality(node1, node2, node_intermediate, Distances):
    first_intermediate_distance: float = Distances[node1 - 1, node_intermediate - 1]
    intermediate_second_distance: float = Distances[node_intermediate - 1, node2 - 1]
    first_second_distance: float = Distances[node1 - 1, node2 - 1]
    return (
        first_intermediate_distance
        + intermediate_second_distance
        - first_second_distance
    )


def getFarthestNodeFromPath(
    path: List[Tuple[int, int]],
    graph: CompleteGraph,  # type: ignore
    Distances: np.matrix,
    nodes_not_in_path,
) -> (int, Tuple[int, int]):  # type: ignore
    maximumDistance = 0
    current_node = 0

    for new_node in nodes_not_in_path:
        for (node1, node2) in path:
            valueTriIneq = triangular_inequality(node1, node2, new_node, Distances)
            if valueTriIneq > maximumDistance:
                maximumDistance = valueTriIneq
                current_node = new_node
                current_edge = (node1, node2)

    return current_node, current_edge


def pickFarthestInitialNodes(graph: CompleteGraph, Distances: np.matrix):  # type: ignore
    biggestDistance = np.max(Distances)  # Obtaining the maximum distance

    listNodesEdge = np.where(
        Distances == biggestDistance
    )  # Obtaining the incident nodes's index of the corresponding edge

    firstTupleofEdges = listNodesEdge[
        0
    ]  # listNodesEdge contains [(node1,node2),(node2,node1)]
    (listNode1, listNode2) = firstTupleofEdges  # every node is in an array

    return listNode1 + 1, listNode2 + 1


def obtainingPath(path: List[Tuple[int, int]], graph: Complete_graphs):  # type: ignore
    # Returns a list of nodes from the path
    # FIXME Delete this function. This is just a print function, no needed for compute the total weight
    new_graph = Graph()
    for edge in path:
        new_graph.addEdge(edge, 0)

    Cycle: List[int] = []
    current_node = new_graph.getNodes()[0]
    Cycle.append(current_node)
    while len(new_graph.getNodes()) >= (len(Cycle) + 1):
        adjs = [
            node
            for node in new_graph.getAdjacentNodes(current_node)
            if (node != current_node) and (node not in Cycle)
        ]
        Cycle.append(adjs[0])
        current_node = adjs[0]
    return Cycle + [new_graph.getNodes()[0]]


def farthest_insertion(graph: CompleteGraph):  # type: ignore

    final_path: List[Tuple[int, int]] = []  # Will contain the final path

    nodes = list(graph.getNodes())

    Distances = getDistancesMatrix(
        graph
    )  # Obtaining all the distances between the nodes in order to obtain the longhest easly

    # FIRST STEP : Picking the two farthest nodes (This do not consider as first node the graph.getNodes()[0])
    node1, node2 = pickFarthestInitialNodes(graph, Distances)

    final_path.append((node1, node2))
    nodes_not_in_path: List[int] = nodes  #  Obtaining a list of unvisited nodes
    nodes_not_in_path.remove(node1)
    nodes_not_in_path.remove(node2)

    # ....END FIRST STEP

    # SECOND STEP : Picking the farthest node from node_1 and node_2
    third_node, _ = getFarthestNodeFromPath(
        final_path, graph, Distances, nodes_not_in_path
    )
    final_path.append((node1, third_node))
    final_path.append((node2, third_node))
    nodes_not_in_path.remove(third_node)

    # ....END SECOND STEP

    # THIRD STEP : Pick the farthest node from the path and add it in the middle of the closest edge

    while len(nodes_not_in_path) > 0:

        # Obtaining the farthest node and the edge on which it has been calculated
        farthestNode, relativeEdge = getFarthestNodeFromPath(
            final_path, graph, Distances, nodes_not_in_path
        )
        final_path.remove(relativeEdge)  # Removing the current edge
        (
            first_node,
            second_node,
        ) = relativeEdge  # Obtaining the incident nodes of the edge
        final_path.append(
            (first_node, farthestNode)
        )  # Adding a new edge including the new node in the path
        final_path.append((farthestNode, second_node))
        nodes_not_in_path.remove(farthestNode)  # Removing the node from the list

    # ....END THIRD STEP

    total_weight: float = 0.00
    for (n1, n2) in final_path:
        total_weight += Distances[n1 - 1, n2 - 1]

    #print(obtainingPath(final_path, graph))  # FIXME Comment or delete
    return total_weight
