from heapq import heappop, heappush, heapify
from typing import Tuple, List


#  using the heapq library, which is a minheap
#  -> need to convert the weights (from positive to negative)
#  to make the minheap a maxheap
#  this property is an invariant of the underlying
#  heap (ie all weights must be negative in the heap
#  positive "to the user"
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
        heappush(self.heap, (weightNegative, vertex))

    def remove(self, vertex: int, weight: int) -> None:
        index: int = 0
        #  recall that the vertex is in the position 1 of the tuple
        while index < len(self.heap) and self.heap[index][1] != vertex:
            index += 1
        #  trick to remove an arbitrary element
        #  from the heap without requiring
        #  an explicit remove
        # (which for some reason cannot make it working
        self.heap[index] = self.heap[-1]
        #  recall that pop remove the last element
        #  of the list considered
        self.heap.pop()
        #  since we are tampering with the underlying
        #  data structure, a re-heapification is required
        # also it removes duplicates which allows us to remove the duplicate inserted by
        #  self.heap[index] = self.heap[-1]
        #  completing the removal
        heapify(self.heap)

    # weightToAdd is passed as positive
    # transparent from the user
    def increaseKey(self, vertex: int, weightToAdd: int) -> None:
        #  since weight it's recorded as negative value
        #  we convert it to positive in order to
        #  make the sum weight += weightToAdd  correct (recall that all weightToAdd are positive)
        weight: int = self.findFromVertex(vertex=vertex)[0] * (-1)
        self.remove(vertex=vertex, weight=weight)
        weight += weightToAdd
        # replace with the new element
        # recall that self.push take care of
        # converting from positive to negative the weight passed
        self.push(vertex=vertex, weight=weight)

    # returns the pair vertex, weight
    def findFromVertex(self, vertex: int) -> Tuple[int, int]:
        heapAsList: List[Tuple[int, int]] = list(self.heap)
        #  recall that vertex is in the second position of the tuple(ie index 1) not the first
        item = [item for item in heapAsList if item[1] == vertex]
        return item[
            0
        ]  # just return the first in case there are multiple occurrence of same vertex

    # should not happen btw

    #  required for for all cycle inside
    #  stMinimumCut
    def findVertex(self, vertex: int) -> bool:
        item: Tuple[int, int] = self.findFromVertex(vertex=vertex)
        if len(item) > 0:
            return True
        else:
            return False

    #  only for testing purpose
    def all(self) -> List[Tuple[int, int]]:
        return self.heap
