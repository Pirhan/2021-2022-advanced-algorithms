from data_structures.Complete_graphs import *  # type: ignore

from typing import List, Tuple


def first_circuit(
    graph: CompleteGraph, not_in_path: List[int], current_pick: int
) -> int:  # only the minimal distance vertex required here since we can build the the first partial circuit with just that
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    for node in not_in_path:
        if node != current_pick:  # maybe useless?
            if graph.getDistance(current_pick, node) < minimum:
                minimum = graph.getDistance(current_pick, node)
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
    graph: CompleteGraph, partial_circuit: List[Tuple[int, int]], not_in_path: List[int]
) -> Tuple[
    int, Tuple[int, int]
]:  # first element = vertex which connection have the best triangular_inequality, second element(the tuple) = edge that will be replaced by the new pair of edges
    minimum_node: int = -1
    minimum: float = float("+Infinity")
    edge_to_be_replaced: Tuple[int, int] = (-1, -1)
    for current_edge in partial_circuit:
        for node_not_in_path in not_in_path:
            if (
                triangular_inequality(
                    graph=graph,
                    first_node_in_edge=current_edge[0],
                    intermediate_node=node_not_in_path,
                    second_node_in_edge=current_edge[1],
                )
                < minimum
            ):
                minimum = triangular_inequality(
                    graph=graph,
                    first_node_in_edge=current_edge[0],
                    intermediate_node=node_not_in_path,
                    second_node_in_edge=current_edge[1],
                )
                minimum_node = node_not_in_path
                edge_to_be_replaced = current_edge
    return (minimum_node, edge_to_be_replaced)


def shift_current_circuit(
    current_circuit: List[Tuple[int, int]], index_start_shift: int
) -> None:  # done wit side effects
    # extend current_circuit with the last element of the current_circuit (ie [a,b,c] -> [a,b,c,c]
    current_circuit += [current_circuit[(len(current_circuit)) - 1]]
    #  start the shifting from index_start_shift
    index: int = index_start_shift
    while index < (
        len(current_circuit) - 2
    ):  # iterate (ie shift) up until the last but one element
        current_circuit[index + 1] = current_circuit[index]
        index += 1


def add_to_circuit(
    current_circuit: List[Tuple[int, int]],
    node_to_add: int,
    edge_to_be_replaced: Tuple[int, int],
) -> None:  # done with side effect
    index_edge_to_replace: int = current_circuit.index(edge_to_be_replaced)
    new_edge_left: Tuple[int, int] = (
        edge_to_be_replaced[0],
        node_to_add,
    )  # from previous edge first node to new node
    current_circuit[index_edge_to_replace] = new_edge_left
    #  in order to insert the second edge we must
    #  move up all the previous edges
    #  insert the new_edge_right in the first position
    new_edge_right: Tuple[int, int] = (node_to_add, edge_to_be_replaced[1])
    #  index_edge_to_replace + 1 is the position where the new_edge_right must be put after the new_edge_left (minus error of course :) )
    shift_current_circuit(
        current_circuit=current_circuit, index_start_shift=(index_edge_to_replace + 1)
    )
    current_circuit[index_edge_to_replace + 1] = new_edge_right



# still working on it WORK IN PROGRESS
# no guarantee!!
    # def cheapest_insertion(graph: CompleteGraph) -> List[int]:
    """ computes the tsp using cheapest_insertion heuristic
    all_nodes: List[int] = list(
        graph.getNodes()
    )  # keyview not indexable -> convert it into list
    current_pick: int = all_nodes[0]  # initialization, first selection
    not_in_path: List[int] = all_nodes[1:]
    other_edge_first_circuit: int = first_circuit(graph=graph, not_in_path=not_in_path,current_pick=current_pick)
    circuit: List[Tuple[int, int]] = [(current_pick, other_edge_first_circuit)]  # will be used to build a partial circuit
    #  final_path: List[int] = [current_pick]
    while len(not_in_path) > 0:  # keep going until all nodes are in the path


    return final_path
"""
