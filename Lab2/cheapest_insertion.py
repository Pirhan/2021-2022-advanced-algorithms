from data_structures.Complete_graphs import *  # type: ignore

from typing import List, Tuple


def compute_nearest_neighbour(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int
) -> int:  # compute the nearest_neighbour, which will be used for initialization of the first circuit, only the minimal distance vertex required here and nothing more
    node_distance_collector: List[Tuple[int, float]] = []

    for node in not_in_path:
        node_distance_collector += [(node, graph.getDistance(current_pick, node))]
    return min(node_distance_collector, key=lambda node_distance: node_distance[1])[0]


def triangular_inequality(
    graph: CompleteGraph,
    first_node_in_edge: int,
    intermediate_node: int,
    second_node_in_edge: int,
) -> float:  # compute the triangular_inequality for three nodes
    first_intermediate_distance: float = graph.getDistance(
        first_node_in_edge, intermediate_node
    )
    intermediate_second_distance: float = graph.getDistance(
        intermediate_node, second_node_in_edge
    )
    first_second_distance: float = graph.getDistance(
        first_node_in_edge, second_node_in_edge
    )
    return (
        first_intermediate_distance
        + intermediate_second_distance
        - first_second_distance
    )


def selection(
    graph: CompleteGraph, partial_circuit: List[int], not_in_path: List[int]
) -> Tuple[
    int, int
]:  # first element = vertex which connection have the best triangular_inequality, second element the first  node which compose the edge that must be replaced
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    index_insertion: int = (
        -1
    )  # this tell us where we must insert the node that have the smallest triangular_inequality value
    for first_end_edge in partial_circuit[:-1]:  # upto the last but one
        #  first_end_edge and second_end_edge
        #  are the first and second element of
        #  the edge that will be compared with the nodes not_in_path
        second_end_edge: int = partial_circuit[
            partial_circuit.index(first_end_edge) + 1
        ]
        for node_not_in_path in not_in_path:
            current_triangular_inequality: float = triangular_inequality(
                graph=graph,
                first_node_in_edge=first_end_edge,
                intermediate_node=node_not_in_path,
                second_node_in_edge=second_end_edge,
            )
            if current_triangular_inequality < minimum:
                minimum = current_triangular_inequality
                minimum_node = node_not_in_path
                index_insertion = partial_circuit.index(
                    second_end_edge, 1
                )  # avoid to look for the first element of the list otherwise the index function will refer to the 0th-element which is wrong since this element is by convention the beginning of the cycle
                # example let v = [1,..n,1] a path
                # if the next insertion happens between  the last (ie=1) and last but one element, the index function by default returns the first occurrence of 1 and not the correct one (ie the second)
    return (minimum_node, index_insertion)


def getTotalWeight(Graph: CompleteGraph, cycle: List[int]):  # type: ignore
    total_weight: float = 0
    node1 = cycle[0]
    for node2 in cycle[1:]:

        total_weight += Graph.getDistance(node1, node2)
        node1 = node2

    return total_weight


def cheapest_insertion(graph: CompleteGraph) -> List[int]:
    #  initialization
    all_nodes: List[int] = list(
        graph.getNodes()
    )  # must be indexable while what returned from getNodes is not
    initial_pick: int = all_nodes[0]  # convention: start from node of index 0
    path: List[int] = [initial_pick]
    not_in_path: List[int] = all_nodes[
        1:
    ]  # all other nodes still does not belong to path
    nearest_neighbour: int = compute_nearest_neighbour(
        graph=graph, not_in_path=not_in_path, current_pick=initial_pick
    )
    # also second end of first partial circuit now belongs to the path
    not_in_path.remove(nearest_neighbour)
    path += [nearest_neighbour]  # builds the first part of the circuit
    new_node, index_insertion = selection(
        graph=graph, partial_circuit=path, not_in_path=not_in_path
    )
    path[index_insertion:index_insertion] = [new_node]  # insert new node in between
    not_in_path.remove(new_node)
    # first circuit build outside the loop
    # i assume that "partial circuit" is sequence of nodes [a,..,a] where the first element and last coincide (ie it is a loop)
    path += [initial_pick]  # close the first circuit
    #  note that this is slightly different from the suggestion provided by the lab slides
    #  because, since we are in a graph (and not in a multigraph),
    #  multiple edges are technically not allowed
    #  so an initial partial circuit requires at least three nodes and not just two
    while len(not_in_path) > 0:  # continue to iterate until no more nodes must be added
        new_node, index_insertion = selection(
            graph=graph, partial_circuit=path, not_in_path=not_in_path
        )
        path[index_insertion:index_insertion] = [new_node]  # insert new node in between
        not_in_path.remove(new_node)
    # return path
    return getTotalWeight(graph, path)