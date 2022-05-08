from data_structures.Complete_graphs import *  # type: ignore

from typing import List


def computeSmallestNeighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int  # type: ignore
) -> int:  # return the index of the smallest_neighbour
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    for node in not_in_path:
        current_distance: float = graph.getDistance(current_pick, node)
        if current_distance < minimum:

            minimum = current_distance
            minimum_node = node
    return minimum_node


def getTotalWeight(Graph: CompleteGraph, cycle: List):  # type: ignore
    total_weight: float = 0

    node1 = cycle[0]
    for node2 in cycle[1:]:
        total_weight += Graph.getDistance(node1, node2)
        node1 = node2

    return total_weight


def nearestNeighbour(graph: CompleteGraph) -> List[int]:  # type: ignore
    """ computes the tsp using nearest_neighbour heuristic"""
    all_nodes: List[int] = list(
        graph.getNodes()
    )  # keyview not indexable -> convert it into list
    current_pick: int = all_nodes[0]  # initialization, first selection
    not_in_path: List[int] = all_nodes[1:]
    final_path: List[int] = [current_pick]
    while (
        len(not_in_path) > 1
    ):  # inside this loop, end when there are no more nodes to add to the path
        smallest_neighbour: int = computeSmallestNeighbour(
            graph=graph, not_in_path=not_in_path, current_pick=current_pick
        )  # selection
        final_path += [
            smallest_neighbour
        ]  # insertion, last element is the new element of the path
        not_in_path.remove(smallest_neighbour)

        current_pick = smallest_neighbour  # update the current_pick to reflect the path after the update
        # add the remaining node not in the path and initial node to close the cycle
    final_path += [not_in_path[0], all_nodes[0]]
    # following some simple testing function
    # sorted_final_path = final_path.sort()
    # print("f path", sorted_final_path)
    # print("len", len(final_path))
    return getTotalWeight(graph, final_path)  # ordered by insertion
