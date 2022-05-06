from data_structures.Complete_graphs import *  # type: ignore

from typing import List


def computeSmallestNeighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int
) -> int:  # return the index of the smallest_neighbour
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    #  TODO see if it is possible to precompute the distance between each node
    #  at graph initialization
    for node in not_in_path:
        if node != current_pick and graph.getDistance(current_pick, node) < minimum:

            minimum = graph.getDistance(current_pick, node)
            minimum_node = node
    return minimum_node


#  TODO collapse into nearestNeighbour, since it's a oneliner
def removeNode(from_s: List[int], what: int) -> None:
    """ remove the neighbour to the set of the element in te path. this is done with side effects"""
    from_s.remove(what)

def getTotalWeight(Graph: CompleteGraph, cycle : List):
    total_weight: float = 0

    node1 = cycle[0]
    total_weight
    for node2 in cycle[1:]:
        total_weight += Graph.getDistance(node1, node2)
        node1 = node2

    return total_weight

def nearestNeighbour(graph: CompleteGraph) -> List[int]:
    """ computes the tsp using nearest_neighbour heuristic"""
    all_nodes: List[int] = list(
        graph.getNodes()
    )  # keyview not indexable -> convert it into list
    current_pick: int = all_nodes[0]  # initialization, first selection
    not_in_path: List[int] = all_nodes[1:]
    final_path: List[int] = [current_pick]
    while (
        len(not_in_path) > 0
    ):  # inside this loop, end when there are no more nodes to add to the path
        smallest_neighbour: int = computeSmallestNeighbour(
            graph=graph, not_in_path=not_in_path, current_pick=current_pick
        )  # selection
        final_path += [
            smallest_neighbour
        ]  # insertion, last element is the new element of the path
        removeNode(
            from_s=not_in_path, what=smallest_neighbour
        )  # side effects here, not_in_path has one element less(smallest_neighbour
        current_pick = smallest_neighbour  # update the current_pick to reflect the path after the update

    # following some simple testing function
    # sorted_final_path = final_path.sort()
    # print("f path", sorted_final_path)
    # print("len", len(final_path))
    return getTotalWeight(graph, final_path)  # ordered by insertion

