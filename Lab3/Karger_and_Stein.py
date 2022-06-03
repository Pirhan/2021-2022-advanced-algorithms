import math
import numpy as np
from typing import List, Tuple
from data_structures.graph import Graph  # type:ignore
from time import perf_counter_ns


def Karger_and_Stein(G: Graph, k: int = 0) -> float:
    # This is the main function of the alghoritm and calls
    # Recursive_Contract which returns the minumum cut found.
    # main sets k which is equal to log(n) ^ 2

    minimumDistance = float("+Infinity")  # Useful for the comparison
    discovery_time = 0
    # Setting k = n
    if k == 0: k = int(math.log2(G.dimension)**2)  
    for _ in range(k):

        # Passing a copy and not a reference
        (D, W) = G.getD_W()
        # W = [list(W_[i])[:] for i in range(len(list(W_[0])))]

        # Passing a copy of the object G instead of its reference
        t = Recursive_Contract((D, W))
        if t < minimumDistance:
            minimumDistance = t

            # Taking the current time, which corresponds to the time
            # when the minimum cut was found
            discovery_time = perf_counter_ns()

        
    return minimumDistance, discovery_time

def Random_Select(C: List[float]):

    if C[-1] == 0:
        print("Error in", C)

    # np.random.randint: 0 is included and C[-1] is excluded
    r = np.random.randint(0, int(C[-1])-1)  # Pick the last edge value

    edge_found_index = binarySearch(
        r, C
    )  # This is the edge founded, achived as just an index

    if edge_found_index is None:
        print(C, r)
        assert False

    return edge_found_index


def binarySearch(r: int, C: List[float]):
    mid = 0
    start = 0
    end = len(C)

    while start <= end:

        mid = (start + end) // 2

        if C[mid - 1] <= r and C[mid] > r:
            return mid

        if r < C[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return None


def Edge_Select(G: Tuple[List[float], List[List[float]]]) -> Tuple:

    (D, W) = G

    # Creating the comulative weight on D
    C_D = [sum(D[:i]) for i in range(1, len(D) + 1)]
    u = Random_Select(C_D)

    # Creating the comulative weights on W
    C_W = [sum((W[u])[:i]) for i in range(1, len(D) + 1)]
    v = Random_Select(C_W)

    return (u, v)


def Contract_Edge(G: Tuple[List[float], List[List[float]]], u: int, v: int):
    (D, W) = G

    D[u] += D[v] - 2 * W[u][v]
    D[v] = 0
    W[u][v] = W[v][u] = 0

    # Picking the vertices in D different from u and v positive
    V = [index for index, n in enumerate(D) if n != u or n != v or n != 0]
    for w in V:  # V[0] is 0. It is an additional element that should be neglected

        W[u][w] += W[v][w]
        W[w][u] += W[w][v]
        W[v][w] = W[w][v] = 0

    #return (D, W)


def Contract(G: Tuple[List[float], List[List[float]]], k: int):
    (D_, W_) = G

    D = D_.copy()
    W = [array.copy() for array in W_]
    # len(V) corresponds to the number of vertices remaning in D
    V = [n for n in D if n != 0]

    for _ in range(len(V) - k):  # Strating form 1. Adding 1 to the upper range

        (u, v) = Edge_Select((D, W))
        Contract_Edge((D, W), u, v)

    return (D, W)


def Recursive_Contract(G: Tuple[List[float], List[List[float]]]):
    (D, W) = G
    V = [n for n in D if n != 0]  # Number of vertices remaning in D
    if len(V) <= 6:

        # Contracting G to 2 vertices
        (_, W_1) = Contract(G, 2)

        # The matrix now contains only two value different from 0
        #
        return max(max(W_1))

    Results: List[int] = []
    t = math.ceil((len(V) / math.sqrt(2)) + 1)
    (D_, W_) = Contract(G, t)
    for _ in range(2):
        D = D_.copy()
        W = [array.copy() for array in W_]
        
        Results.append(Recursive_Contract((D,W)))

    return min(Results)
