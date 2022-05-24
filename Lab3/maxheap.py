from heapq import heappop, heappush, heapify
from typing import Tuple, List


#  using the heapq library, which is a minheap
#  -> need to convert the weights (from positive to negative)
#  to make the minheap a maxheap
class maxHeap:
    def __init__(self) -> None:
        #  keep it simple, provide only this as
        #  initializer, and add element only
        #  with the push
        self.heap: List[Tuple[int, int]] = []

    # order of return is weight, vertex
    def pop(self) -> Tuple[int, int]:
        # required to provide the tuple as
        # vertex, weight instead as
        # weight, vertex (as stored)
        # remember that weight are stored
        # negatively -> a (-1) multiplication
        # is required to make them positive
        res: Tuple[int, int] = heappop(self.heap)
        return (res[1], (-1) * res[0])

    # in the algorithms the push is done
    # vertex, weight so i present the same order
    # under the hood the order is reversed
    # since the heap orders tuples on the first
    # component only
    def push(self, vertex: int, weight: int) -> None:
        weightNegative: int = weight * (-1)
        heappush(self.heap, [weightNegative, vertex])

    def remove(self, vertex: int, weight: int) -> None:
        heap_as_list: List[Tuple[int, int]] = list(self.heap)
        #  for some reason the list remove does not work
        # so the following solution
        self.heap = [item for item in heap_as_list if item[0] != weight and item[1] != vertex]
        heapify(self.heap)

    # see newkey is passed as positive
    # transparent from the user
    def increaseKey(self, vertex: int, newkey: int) -> None:
        keyNegative: int = (-1) * newkey
        weight_node_to_update: int = self.find_from_vertex(vertex=vertex)[0]
        self.remove(vertex=vertex, weight=weight_node_to_update)
        print("new key negative", keyNegative)
        print("current key", weight_node_to_update)
        weight_node_to_update -= keyNegative
        # replace with the new element
        self.push(vertex=vertex, weight=weight_node_to_update)

    # returns the pair vertex, weight
    def find_from_vertex(self, vertex: int) -> Tuple[int, int]:
        heapAsList: List[Tuple[int, int]] = list(self.heap)
        #  recall that vertex is in the second position of the tuple(ie index 1) not the first
        item = [item for item in heapAsList if item[1] == vertex]
        return item[
            0
        ]  # just return the first in case there are multiple occurrence of same vertex

    # should not happen btw

    #  required for for all cycle inside
    #  stMinimumCut
    def find_vertex(self, vertex: int) -> bool:
        item: Tuple[int, int] = self.find_from_vertex(vertex=vertex)
        if len(item) > 0:
            return True
        else:
            return False

    #  only for testing purpose
    def all(self) -> List[Tuple[int, int]]:
        return self.heap
