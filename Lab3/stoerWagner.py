from typing import Tuple, List, Optional
from data_structures.graph import Graph  # type: ignore
from data_structures.maxheap import maxHeap  # type: ignore


#  nodes, edges and weight function are inside the graph already, no need to pass them as parameters
# returns the a pair of first partition, second partition, both are list of nodes
def globalMinimumCut(graph: Graph) -> Tuple[List[int], List[int]]:
    nodes: List[int] = graph.getNodes()
    if len(nodes) == 2:
        return ([nodes[0]], [nodes[1]])
    else:
        (firstCut, nodeFirstPartition, nodeSecondPartition) = stMinimumCut(graph=graph)
        graph.removeNodes(toRemove=[nodeFirstPartition, nodeSecondPartition])
        secondCut: Tuple[List[int], List[int]] = globalMinimumCut(
            graph=graph
        )  # graph minus nodeFirstPartition and nodeSecondPartition

        if graph.cutWeight(firstCut) <= graph.cutWeight(secondCut):
            return firstCut
        else:
            return secondCut


# returns a pair which contains the first(all nodes without t) and second partition (only t) and the node t and s
def stMinimumCut(graph: Graph) -> Tuple[Tuple[List[int], List[int]], int, int]:
    priorityQueue = maxHeap()  # empty list at the beginning
    for node in graph.getNodes():
        priorityQueue.push(node=node, weight=0)
    s: Optional[int] = None
    t: Optional[int] = None
    while not priorityQueue.isEmpty():
        print("START PHASE")
        u: int = priorityQueue.pop()[
            0
        ]  # recall that the node in the priorityQueue is provided as the first node also u is the node with maximum weight
        s = t
        t = u
        print("u", u, "s", s, "t", t)
        for adjacent in graph.adjacentNodes(node=u):
            print("adjacent to u", adjacent)
            if priorityQueue.findVertex(node=adjacent):
                weightUV: int = graph.getWeight(node1=u, node2=adjacent)
                print("weightUV", weightUV)
                priorityQueue.increaseKey(node=adjacent, weightToAdd=weightUV)
                print("priorityQueue after update", priorityQueue.all())
        print("END PHASE")

    firstPartition: List[int] = graph.getNodes()
    #  if for some reason s and t are underfined
    #  raise some error
    assert s is not None and t is not None
    print("s", s, "t", t)
    firstPartition.remove(t)
    return ((firstPartition, [t]), s, t)
