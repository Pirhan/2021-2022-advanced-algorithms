from data_structures.graph import Graph
from heapq import heappush
from heapq import heappop
from data_structures.Complete_graphs import *


def Prim_Heap(G: CompleteGraph):
    """
    This is a function that implements the Prim's algorithm,
    which allows to achieve the time complexity of O(M * log(N)).
    """

    total_weight = 0  # The weight of the MST obtained

    Q = []  # This is the list uset to build the heap
    not_in_path = list(G.getNodes())
    visited = []  # Contains all the visited nodes
    heappush(
        Q, [0, 1]
    )  # [0,1] indicates a first weight of 0 and node 1 as starting node
    # In this way we don't need to use key and Phi as data structures

    while len(Q) != 0:

        weight, node = heappop(
            Q
        )  # Extract the minimum edge incident [weignt, node], it pops the elements too
        # This is the weight of a visited edge. It does not create cycles so let's add it to the final MST

        if node in visited:  # node already visited
            continue

        visited.append(node)  # Node non visited. Adding it to the final MST
        not_in_path.remove(node)
        total_weight += weight  # Adding the edge's weight to the final MST weight

        for v in G.getAdjacentNodes(node):  # for each v adiacent to node
            weight = G.edges.get((node, v))  # Taking the weight of the node
            if weight is None:  # flake8 suggestion condition is None instead of equality operator
                weight = G.edges.get((v, node))
            if v not in visited:
                heappush(
                    Q, [weight, v]
                )  # Adding a new [w,v] to Q if v in not visited yet
    print(visited)
    return total_weight
