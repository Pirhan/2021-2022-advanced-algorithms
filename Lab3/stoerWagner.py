from typing import Tuple, List, Optional
from data_structures.graph import Graph  # type: ignore
from data_structures.maxheap import maxHeap  # type: ignore


def minusT(nodes: List[List[int]], t: List[int]) -> List[List[int]]:
    return [item for item in nodes if item != t]


def flatten(
    toFlatten: Tuple[List[List[int]], List[List[int]]]
) -> Tuple[List[int], List[int]]:
    firstComponent = [node for sublist in toFlatten[0] for node in sublist]
    secondComponent = [node for sublist in toFlatten[1] for node in sublist]

    return (firstComponent, secondComponent)


def mergeNodes(
    nodes: List[List[int]], node1ToMerge: List[int], node2ToMerge: List[int]
) -> List[List[int]]:
    nodeToAdd: List[int] = node1ToMerge + node2ToMerge
    nodes.remove(node1ToMerge)
    nodes.remove(node2ToMerge)
    nodes += [nodeToAdd]
    return nodes


def stoerWagner(graph: Graph) -> Tuple[List[List[int]], List[List[int]]]:
    nodes: List[List[int]] = [[item] for item in graph.getNodes()]
    # vertex can be merged together so i use a list
    # of int instead of simple int to do that
    minimumCut: Tuple[List[List[int]], List[List[int]]] = globalMinimumCut(
        graph=graph, nodes=nodes
    )
    print("minimumCut", minimumCut)
    print("minimumCut weight", graph.cutWeight(cut1=flatten(minimumCut)))
    return minimumCut


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
        if priorityQueue.moreThenOneElement():
            for singleNode in u:
                for adjacent in graph.adjacentNodes(node=singleNode):
                    if priorityQueue.findVertex(node=adjacent):
                        weightUV: int = graph.getWeight(
                            node1=singleNode, node2=adjacent
                        )
                        priorityQueue.increaseKey(node=adjacent, weightToAdd=weightUV)

    if t is not None and s is not None:
        return ((minusT(nodes=nodes, t=t), [t]), s, t)
    raise BaseException()
