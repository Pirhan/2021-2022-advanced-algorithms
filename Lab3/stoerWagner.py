from typing import Tuple, List, Optional
from data_structures import graph


def globalMinimumCut(graph) -> Tuple[List[int], List[int]]:
    # where first component are vertex,
    # second component are edges
    # third component is the weight function
    if len(graph[0]) == 2:
        return (list(graph[0][0]), list(graph[0][1]))
    else:
        return ([], [])


def stMinimumCut(graph) -> Tuple[List[int], int, int, int]:
    # where first component are vertex,
    # second component are edges
    # third component is the weight function
    priorityQueue: List[Tuple[int, int]] = []  # empty list at the beginning
    for vertex in graph[0]:
        vertexKey: int = 0
        heappush(priorityQueue, (vertex, vertexKey))
    s: Optional[int] = None
    t: Optional[int] = None
    while len(priorityQueue) > 0:
        u = extractMax(priorityQueue)
        s = t
        t = u
        for adjacent in range(10):
            if adjacent in priorityQueue:
                newKey = adjacent[key] + weight(u, adjacent)
                IncreaseKey(priorityQueue, adjacent, newKey)
    return None
