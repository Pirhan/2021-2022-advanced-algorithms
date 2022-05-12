from data_structures.Complete_graphs import *  # type: ignore

from typing import List, Tuple


def computeSmallestNeighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int  # type: ignore
) -> int:  # return the index of the smallest_neighbour
    node_distance_collector: List[Tuple[int, float]] = []

    for node in not_in_path:
        node_distance_collector += [(node, graph.getDistance(current_pick, node))]
    return min(node_distance_collector, key=lambda node_distance: node_distance[1])[0]

""" def computeSmallestNeighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int  # type: ignore
) -> int:  # return the index of the smallest_neighbour
    smmallest_distance : float = float("+Infinity")
    current_nearest_neighbour : int = 0 
    for new_node in not_in_path:
        current_distance = graph.getDistance(current_pick, new_node)
        print(current_distance)
        if current_distance < smmallest_distance:
            smmallest_distance =  current_distance
            current_nearest_neighbour = new_node
    return current_nearest_neighbour """


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
        len(not_in_path) > 0
    ):  # inside this loop, end when there is only one element not in path, will be added outside the cycle
        smallest_neighbour: int = computeSmallestNeighbour(
            graph=graph, not_in_path=not_in_path, current_pick=current_pick
        )  # selection
        final_path += [
            smallest_neighbour
        ]  # insertion, last element is the new element of the path
        not_in_path.remove(smallest_neighbour)

        current_pick = smallest_neighbour  # update the current_pick to reflect the path after the update
        # add the remaining node not in the path and initial node to close the cycle
    final_path.append(all_nodes[0])
    #print(final_path)
    return getTotalWeight(graph, final_path)  # ordered by insertion
