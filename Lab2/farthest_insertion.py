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


def getClosestEdgePath(
   graph: CompleteGraph, path: List[Tuple[int, int]], farthest_node: int
):

    nearest_edge: Tuple[int, int] = ()
    closest_distance = float("+Infinity")

    for (n1, n2) in path:
        distance_computed = triangular_inequality(graph, n1, n2, farthest_node)
        if distance_computed < closest_distance:
            closest_distance = distance_computed
            nearest_edge = (n1, n2)

    return nearest_edge


def getFarthestNodeFromPath(
    graph: Complete_graphs,
    path: List[Tuple[int, int]],
    nodes_not_in_path,
) -> int:  # type: ignore
    
    maximumDistance = 0  # lower bound for maximum distance possible
    farthest_node = 0  # this will hold the farthest distanced node

    for new_node in nodes_not_in_path:

        smallest_distance_found = float("+Infinity")
        for (node1, node2) in path:  

            current_distance = graph.computeDistanceLineToPoint(node1, node2, new_node)
            if current_distance < smallest_distance_found:
                smallest_distance_found = current_distance
                

        if smallest_distance_found > maximumDistance:
            farthest_node = new_node
            maximumDistance = smallest_distance_found
            


    return farthest_node






def pickFarthestInitialNodes(graph: CompleteGraph):  # type: ignore
    biggestDistance = np.max(graph.Distances)  # Obtaining the maximum distance

    listNodesEdge = np.where(
        graph.Distances == biggestDistance
    )  # Obtaining the incident nodes's index of the corresponding edge
    #  there are two edges which satisy this property, since Distances keeps
    #  all the distance(ie distance(i,j) and distance(j,i) for all the nodes in the graph)
    #  this is an array, that's why the need for the two extractions that follow

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

  
    # FIRST STEP : Picking the two farthest nodes (This do not consider as first node the graph.getNodes()[0])
    # does this makes the approximation better? if provably not i would consider to
    # just pick the 0 indexed node
    # also it seems to me that it very computationally intensive
    # since it needs to compute the maximum between all values in the distance matrix
    node1, node2 = pickFarthestInitialNodes(graph)

    # final path stores the edges explicitly
    final_path.append((node1, node2))
    # the nodes not visited is all nodes minus the two element
    # forming the initial edge
    nodes_not_in_path: List[int] = list(graph.getNodes())  # Obtaining a list of unvisited nodes
    nodes_not_in_path.remove(node1)
    nodes_not_in_path.remove(node2)

   
    # ....END FIRST STEP

    # SECOND STEP : Picking the farthest node from node_1 and node_2
    farthest_node = getFarthestNodeFromPath(graph, final_path, nodes_not_in_path)
    final_path.append((node1, farthest_node))
    final_path.append((node2, farthest_node))
    nodes_not_in_path.remove(farthest_node)

    #  Second step must be repeated so it probably needs to go inside the
    #  while loop below
    # ....END SECOND STEP

    # THIRD STEP : Pick the farthest node from the path and add it in the middle of the closest edge

    while len(nodes_not_in_path) > 0:

        # i think that here it could help to split the second and third step
        # of the algorithm (Selection and Insertion) where
        # 1) first you select the node which is farthest from all the other _nodes_
        # from the path (ie triangular_inequality here is not involved)
        # 2) using the farthest node you compute the triangular_inequality
        # examining all the edges (ie pair of nodes) in the circuit
        # example: let the following be the current path [(1,2),(2,3),(3,4),(5,6)],
        # let's say that 7 satisfy
        # the property of being the farthestNode from the path
        # let's say that the edge (2,3) is edge where the triangular_inequality is at minimum
        # ie (2,7) + (7,3) - (2,3) is the minimum between all the edges currently on path
        # then the current circuit should be updated as follows
        # note that insertion should be made in between the path and not at the end
        # [(1,2),(2,7),(7,3),(3,4),(5,6)]

        # Obtaining the farthest node and the edge on which it has been calculated
        farthestNode = getFarthestNodeFromPath(
            graph, final_path, nodes_not_in_path
        )

        closest_edge_to_node = getClosestEdgePath(graph, final_path, farthestNode)

        final_path.remove(closest_edge_to_node)  # Removing the current edge
        (
            first_node,
            second_node,
        ) = closest_edge_to_node  
        # Obtaining the incident nodes of the edge
        # not sure of the following appends since the insertion must be done
        # in between
        # for example consider the case when the relativeEdge is "in the middle"
        # then the following code will append (NB:at the end of the current path)
        # the two new nodes while it should be inserted in the middle (as the slides suggest)
        # example: let the following be the current path [(1,2),(2,3),(3,4),(5,6)],
        # let's say that we need to add a new node, 7 that satisfy
        # the property of being the farthestNode from the path
        # let's say that the edge (2,3) is the edge where the substituion will happen(min triangular_inequality)
        # then following the step below you will have
        # [(1,2),(3,4),(5,6),(2,7),(7,3)], which is incorrect
        final_path.append(
            (first_node, farthestNode)
        )  # Adding a new edge including the new node in the path
        final_path.append((farthestNode, second_node))
        nodes_not_in_path.remove(farthestNode)  # Removing the node from the list

    # ....END THIRD STEP

    total_weight: float = 0.00
    for (n1, n2) in final_path:
        total_weight += graph.getDistance(n1, n2)

    #  print(obtainingPath(final_path, graph))  # FIXME Comment or delete
    return total_weight
