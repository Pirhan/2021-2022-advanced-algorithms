from data_structures.Complete_graphs import * # type: ignore

#  from data_structures.GEO_graph import GEO_graph  # type: ignore

from typing import List


def computeSmallestNeighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int
) -> int:  # return the index of the smallest_neighbour
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    for node in not_in_path:
        if node != current_pick and graph.getDistance(current_pick, node) < minimum:

            minimum = graph.getDistance(current_pick, node)
            minimum_node = node
    return minimum_node


def removeNode(from_s: List[int], what: int) -> None:
    """ remove the neighbour to the set of the element in te path. this is done with side effects"""
    from_s.remove(what)


def nearestNeighbour(graph: CompleteGraph) -> List[int]:
    """ computes the tsp using nearest_neighbour heuristic"""
    all_nodes: List[int] = list(
        graph.getNodes()
    )  # keyview not indexable -> convert it into list
    current_pick: int = all_nodes[0]  # initialization, first selection
    print("current pick", current_pick)
    not_in_path: List[int] = all_nodes[1:]
    final_path: List[int] = [current_pick]
    while (
        len(not_in_path) > 0
    ):  # inside this loop, end when there are no more in the graph
        smallest_neighbour: int = computeSmallestNeighbour(
            graph=graph, not_in_path=not_in_path, current_pick=current_pick
        )  # selection
        final_path += [
            smallest_neighbour
        ]  # insertion, last element is the new element of the path
        removeNode(
            from_s=not_in_path, what=smallest_neighbour
        )  # side effects here, not_in_path has one element less(smallest_neighbour) in_path has one more element(smallest_neighbour)
        current_pick = smallest_neighbour  # update the current_pick to reflect the path after the update

    # sorted_final_path = final_path.sort()
    # print("f path", sorted_final_path)
    # print("len", len(final_path))
    return final_path  # ordered by insertion
