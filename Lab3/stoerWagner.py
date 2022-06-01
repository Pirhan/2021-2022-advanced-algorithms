from typing import Tuple, List, Optional
from data_structures.graph import Graph  # type: ignore
from data_structures.maxheap import maxHeap  # type: ignore
from time import perf_counter_ns


def minusT(nodes: List[List[int]], t: List[int]) -> List[List[int]]:
    return [item for item in nodes if item != t]


#  required by cutWeight
def flatten(
    toFlatten: Tuple[List[List[int]], List[List[int]]]
) -> Tuple[List[int], List[int]]:
    firstComponent = [node for sublist in toFlatten[0] for node in sublist]
    secondComponent = [node for sublist in toFlatten[1] for node in sublist]

    return (firstComponent, secondComponent)


#  when the algorithms says G / {s, t} it actually means this
#  ie remove s, t _and_ replace with a new supernode which contains both
def mergeNodes(
    nodes: List[List[int]], node1ToMerge: List[int], node2ToMerge: List[int]
) -> List[List[int]]:
    nodeToAdd: List[int] = node1ToMerge + node2ToMerge
    nodes.remove(node1ToMerge)
    nodes.remove(node2ToMerge)
    nodes += [nodeToAdd]
    return nodes


def stoerWagner(graph: Graph) -> Tuple[int, int]:
    nodes: List[List[int]] = [[item] for item in graph.getNodes()]
    # vertex can be merged together so i use a list
    # of int instead of simple int to do that
    discovery_time: int = 0
    minimumCut: Tuple[List[List[int]], List[List[int]]] = globalMinimumCut(
        graph=graph, nodes=nodes
    )
    discovery_time = perf_counter_ns()
    minimumCutWeight: int = graph.cutWeight(cut1=flatten(toFlatten=minimumCut))
    return minimumCutWeight, discovery_time


#  nodes, edges and weight function are inside the graph already, no need to pass them as parameters
# returns the a pair of first partition, second partition, both are list of nodes
def globalMinimumCut(
    graph: Graph, nodes: List[List[int]]
) -> Tuple[List[List[int]], List[List[int]]]:
    if len(nodes) == 2:
        return ([nodes[0]], [nodes[1]])  # type: ignore
    else:
        (firstCut, nodeFirstPartition, nodeSecondPartition) = stMinimumCut(
            graph=graph, nodes=nodes
        )
        firstCutWeight: int = graph.cutWeight(
            cut1=flatten(toFlatten=firstCut)
        )  # do here to avoid node removal issues
        mergeNodes(
            nodes=nodes,
            node1ToMerge=nodeFirstPartition,
            node2ToMerge=nodeSecondPartition,
        )
        #  merge of the two nodes is required, not just removal
        secondCut: Tuple[List[List[int]], List[List[int]]] = globalMinimumCut(
            graph=graph, nodes=nodes
        )  # graph minus nodeFirstPartition and nodeSecondPartition
        secondCutWeight: int = graph.cutWeight(flatten(toFlatten=secondCut))
        if firstCutWeight <= secondCutWeight:
            return firstCut
        else:
            return secondCut


# returns a pair which contains the first(all nodes without t) and second partition (only t) and the node t and s
def stMinimumCut(
    graph: Graph, nodes: List[List[int]]
) -> Tuple[Tuple[List[List[int]], List[List[int]]], List[int], List[int]]:
    priorityQueue = maxHeap()  # empty list at the beginning
    for node in nodes:
        priorityQueue.push(node=node, weight=0)
    s: Optional[List[int]] = None
    t: Optional[List[int]] = None
    while not priorityQueue.isEmpty():
        u: List[int] = priorityQueue.pop()[
            0
        ]  # recall that the node in the priorityQueue is provided as the first node also u is the node with maximum weight
        s = t
        t = u
        #  no need to do the cycle that updates the priorityQueue if
        #  the number of remaining element is only one
        #  since it will be picked at the next round anyway
        if priorityQueue.moreThenOneElement():
            for (
                singleNode
            ) in u:  # unpack the u which is a list of node / supernode , one by one
                #  example u = [1,2,3] -> inside an iteration single node will be 1 then 2 then 3
                #  this makes the following operations simpler
                for adjacent in graph.adjacentNodes(node=singleNode):
                    #  the following operation finds a single node inside a supernode
                    if priorityQueue.findVertex(node=adjacent):
                        weightUV: int = graph.getWeight(
                            node1=singleNode, node2=adjacent
                        )
                        #  as findVertex this operation is able to update the weight
                        #  of supernodes given one of it's component
                        #  example adjacent = 1, supernode = [1,2] -> then increaseKey is able
                        #  to increment the key of [1,2] since 1 is contained in it
                        priorityQueue.increaseKey(node=adjacent, weightToAdd=weightUV)

    #  since t and s are Optional -> they could be None
    #  if they were None there is some problem in the algorithm implementation
    if t is not None and s is not None:
        return ((minusT(nodes=nodes, t=t), [t]), s, t)
    raise BaseException()
