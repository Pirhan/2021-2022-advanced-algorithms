from data_structures.Complete_graphs import *  # type: ignore

from typing import List, Tuple


def first_circuit(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int
) -> int:  # only the minimal distance vertex required here since we can build the the first partial circuit with just that
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    for node in not_in_path:
        if node != current_pick:  # maybe useless?
            current_distance: float = graph.getDistance(current_pick, node)
            if current_distance < minimum:
                minimum = current_distance
                minimum_node = node
    #  we care of the minimum node only, weight is unneded
    return minimum_node


def triangular_inequality(
    graph: CompleteGraph,
    first_node_in_edge: int,
    intermediate_node: int,
    second_node_in_edge: int,
) -> float:
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
    index_first_node_edge_to_be_replaced: int = -1
    for first_end_edge in partial_circuit[:-1]:  # upto the last but one
        second_end_edge: int = partial_circuit[partial_circuit.index(first_end_edge) + 1]
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
                index_first_node_edge_to_be_replaced = partial_circuit.index(
                    first_end_edge
                )
    return (minimum_node, index_first_node_edge_to_be_replaced)


def getTotalWeight(Graph: CompleteGraph, cycle: List[int]):  # type: ignore
    total_weight: float = 0
    node1 = cycle[0]
    for node2 in cycle[1:]:

        total_weight += Graph.getDistance(node1, node2)
        node1 = node2

    return total_weight


# still working on it WORK IN PROGRESS
# no guarantee!!


def cheapest_insertion(graph: CompleteGraph) -> List[int]:
    #  initialization
    all_nodes: List[int] = list(graph.getNodes())  # must be indexable
    initial_pick: int = all_nodes[0]  # convention: start from 0
    path: List[int] = [initial_pick]
    not_in_path: List[int] = all_nodes[
        1:
    ]  # all other nodes still does not belong to path
    nearest_neighbour: int = first_circuit(
        graph=graph, not_in_path=not_in_path, current_pick=initial_pick
    )
    # also second end of first partial circuit now belongs to the path
    not_in_path.remove(nearest_neighbour)
    path += [nearest_neighbour]

    #  nearest_neighbour with smaller weight
    #  partial_circuit: List[Tuple[int, int]] = [(initial_pick, nearest_neighbour)]
    #  no need of explicit partial_circuit
    #  we will do with final path
    #  ie let [1,2,3] a partial circuit
    #  then the list of edges will be (1,2),(2,3)
    #  ie generate an edge with (i, i + 1) for i < len(partial_circuit) - 2
    while len(not_in_path) > 0:  # continue to iterate until no more nodes must be added
        new_node, index_first_node_edge_to_be_replaced = selection(
            graph=graph, partial_circuit=path, not_in_path=not_in_path
        )
        path[
            index_first_node_edge_to_be_replaced:index_first_node_edge_to_be_replaced
        ] = [new_node]  # insert new node in between
        not_in_path.remove(new_node)
    path += [initial_pick]  # add the initial node to close the cycle
    # return getTotalWeight(graph, path)
