from heapq import heappop, heappush, heapify
from typing import Tuple, List, Optional


#  using the heapq library, which is a minheap
#  -> need to convert the weights (from positive to negative)
#  to make the minheap a maxheap
#  this property is an invariant of the underlying
#  heap (ie all weights must be negative in the heap
#  positive "to the user")
class maxHeap:
    # also the order must be (weight, node)
    def __init__(self) -> None:
        self.heap: List[Tuple[int, List[int]]] = []

    # order of return is node weight
    def pop(self) -> Tuple[List[int], int]:
        # required to provide the tuple as
        # node, weight instead as
        # weight, node (as stored)
        # remember that weight are stored
        # negatively -> a (-1) multiplication
        # is required to make them positive
        res: Tuple[int, List[int]] = heappop(self.heap)
        return (res[1], (-1) * res[0])

    # in the algorithms the push is done
    # node, weight so i present the same order
    # under the hood the order is reversed
    # since the heap orders tuples on the first
    # component only
    def push(self, node: List[int], weight: int) -> None:
        weightNegative: int = weight * (-1)
        heappush(self.heap, (weightNegative, node))

    def remove(self, node: List[int], weight: int) -> None:
        index: int = 0
        #  recall that the node is in the position 1 of the tuple
        while index < len(self.heap) and node != self.heap[index][1]:
            index += 1
        #  trick to remove an arbitrary element
        #  from the heap without requiring
        #  an explicit remove
        # (which for some reason i cannot make it work)
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
    # node is a node adjacent to
    def increaseKey(self, node: int, weightToAdd: int) -> None:
        weightNode: Optional[Tuple[int, List[int]]] = self.findFromVertex(node=node)
        if weightNode is None:
            return
        else:
            weight: int = weightNode[0] * (-1)
            # remove the previous pair(weight, node)
            # to make room for the new updated weight tuple
            self.remove(node=weightNode[1], weight=weight)
            weight += weightToAdd
            # replace with the new element
            # recall that self.push take care of
            # converting from positive to negative the weight passed
            self.push(node=weightNode[1], weight=weight)

    # weightToAdd is passed as positive
    # transparent from the user
    def increaseKeyFromNodes(self, node: List[int], weightToAdd: int) -> None:
        #  since weight it's recorded as negative value
        #  we convert it to positive in order to
        #  make the sum weight += weightToAdd  correct (recall that all weightToAdd are positive)
        weightNode: Optional[Tuple[int, List[int]]] = self.findFromVertices(node=node)
        if weightNode is None:
            return
        else:
            weight: int = weightNode[0] * (-1)
            # remove the previous pair(weight, node)
            # to make room for the new updated weight tuple
            self.remove(node=node, weight=weight)
            weight += weightToAdd
            # replace with the new element
            # recall that self.push take care of
            # converting from positive to negative the weight passed
            self.push(node=node, weight=weight)

    def findFromVertex(self, node: int) -> Optional[Tuple[int, List[int]]]:
        heapAsList: List[Tuple[int, List[int]]] = list(self.heap)
        #  recall that node is in the second position of the tuple(ie index 1) not the first
        # return only the first
        result: List[Tuple[int, List[int]]] = [item for item in heapAsList if node in item[1]]
        if len(result) == 0:
            return None
        return result[0]

    # returns the pair node, weight
    def findFromVertices(self, node: List[int]) -> Optional[Tuple[int, List[int]]]:
        heapAsList: List[Tuple[int, List[int]]] = list(self.heap)
        #  recall that node is in the second position of the tuple(ie index 1) not the first
        # return only the first
        result: List[Tuple[int, List[int]]] = [item for item in heapAsList if item[1] == node]
        if len(result) == 0:
            return None
        return result[0]

    # should not happen btw

    def findVertex(self, node: int) -> bool:
        item: Optional[Tuple[int, List[int]]] = self.findFromVertex(node=node)
        if item is None:
            return False
        return True

    #  required for for all cycle inside
    #  stMinimumCut
    def findVertices(self, node: List[int]) -> bool:
        item: Optional[Tuple[int, List[int]]] = self.findFromVertices(node=node)
        if item is None:
            return False
        return True

    #  required for loop in stMinimumCut
    def isEmpty(self) -> bool:
        return len(self.heap) == 0

    # avoid to do the for loops inside the
    # while stMinimumCut if the number of remaining element inside the priority queue is less or equal of one since it's pointless
    # to update keys when the number of element
    # which needs to be picked is one
    def moreThenOneElement(self) -> bool:
        return len(self.heap) > 1

    #  only for testing purpose
    def all(self) -> List[Tuple[int, List[int]]]:
        return self.heap
