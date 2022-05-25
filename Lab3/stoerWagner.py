from typing import Tuple, List, Optional
from data_structures.graph import Graph
from data_structures.maxheap import maxHeap


def globalMinimumCut(graph: Graph) -> Tuple[List[int], List[int]]:
    # where first component are vertex,
    # second component are edges
    # third component is the weight function
    nodes: List[int] = graph.getNodes()
    if len(nodes) == 2:
        return ([nodes[0]], [nodes[1]])
    else:
        (C1, s, t) = stMinimumCut(graph=graph)
        C2 = globalMinimumCut(graph=graph)  # G minus s and t
        # so we need to update the graph in some way
        # remove the s t nodes
        # and remove all the edges which connects to them?
        if graph.cutWeight(C1) <= graph.cutWeight(C2):
            return C1
        else:
            return C2


def stMinimumCut(graph: Graph) -> Tuple[Tuple[List[int], List[int]], int, int]:
    # where first component are vertex,
    # second component are edges
    # third component is the weight function
    priorityQueue = maxHeap()  # empty list at the beginning
    for vertex in graph[0]:
        vertexKey: int = 0
        priorityQueue.heappush(priorityQueue, (vertex, vertexKey))
    s: Optional[int] = None
    t: Optional[int] = None
    while not priorityQueue.isEmpty():
        u: int = priorityQueue.pop()[
            0
        ]  # recall that the vertex in the priorityQueue is provided as the first vertex also u is the vertex with maximum weight
        s = t
        t = u
        for adjacent in graph.adjacentNodes(node=u):
            if priorityQueue.findVertex(vertex=adjacent):
                weightUV: int = graph.getWeight(node1=u, node2=adjacent)
                assert weightUV > 0
                priorityQueue.increaseKey(vertex=adjacent, weightToAdd=weightUV)

    firstPartition: List[int] = graph.getNodes()
    #  if for some reason s and t are underfined
    #  raise some error
    assert s is not None and t is not None
    firstPartition.remove(t)
    return ((firstPartition, [t]), s, t)
