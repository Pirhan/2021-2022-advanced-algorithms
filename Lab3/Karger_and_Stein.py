import math, copy
import numpy as np
from typing import *
from data_structures.graph import Graph


def Karger(G: Graph, k : int)-> float:

    minimumDistance = float("+Infinity")  # Useful for the comparison
    for _ in range(k):
        # Passing a copy and not a reference  
        t = Recursive_Contract(G.getD_W())   # Passing a copy of the object G instead of its reference
        if t < minimumDistance :
            minimumDistance = t
    return minimumDistance

def Random_Select(C: List[float]):

        if C[-1] == 0: print("Error in",C)
        
        r = np.random.randint(0, C[-1]-1) # Pick the last edge value

        edge_found_index = binarySearch(r, C)   # This is the edge founded, achived as just an index

        if edge_found_index is None: 
            print(C , r)
            assert(False)

        return edge_found_index


def binarySearch(r : int, C: List[float]):
    mid = 0
    start = 0
    end = len(C)

    while (start <= end):
        
        mid = (start + end) // 2

        if C[mid - 1] <= r and C[mid] > r:
            return mid

        if r < C[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return None



def Edge_Select(G: Tuple[List[float], np.matrix]) -> Tuple:

    (D,W) = G

    # Creating the comulative weight on D
    C_D = [sum(D[:i]) for i in range(1, len(D)+1)] 
    u = Random_Select(C_D)

    # Creating the comulative weights on W
    C_W = [sum((W[u])[:i]) for i in range(1, len(D)+1)]  
    v = Random_Select(C_W)

    return (u,v)

def Contract_Edge(G: Tuple[List[float], np.matrix], u : int, v: int):
    (D,W) = G
    D[u] += D[v] - 2 * W[u,v]
    D[v] = 0
    W[u,v] = W[v,u] = 0

    # Picking the vertices in D different from u and v positive
    V = [D.index(n) for n in D if n != u or n != v or n != 0] 

    for w in V: # V[0] is 0. It is an additional element that should be neglected

        W[u, w] += W[v, w]
        W[w, u] += W[w, v]
        W[v, w] = W[w, v] = 0


def Contract(G:Tuple[List[float], np.matrix], k:int):
    (D_,W_) = G
  

    V = [n for n in D_ if n != 0]   # len(V) corresponds to the number of vertices remaning in D

    for _ in range(len(V) - k): # Strating form 1. Adding 1 to the upper range

        (u,v) = Edge_Select((D_,W_))
        Contract_Edge((D_,W_), u, v)

    return (D_,W_)


def Recursive_Contract(G:Graph):
    (D,W) = G
    V = [n for n in D if n != 0]   # Number of vertices remaning in D
    if len(V) <= 6:

        # Contracting G to 2 vertices
        (D_1,W_1) = Contract(G,2)

        # Check if there are only two occurrences other than 0. 
        # This means that in the matrix there is the same repeated value 
        # for the pair of vertices associated with it (W [a, b] = W [b, a] = value).
        positions = np.where(W_1 != 0)
        if len(positions)!=2 : assert(False)

        # Returning the value which corresponds to the only value different form 0 in the matrix
        return np.max(W_1)

    t = math.ceil((len(V)/math.sqrt(2))+1)
    
    outputs : List[float] = []
    G_i = Contract(G, t)
    for _ in range(2):
        (D_i,W_i) = G_i
        outputs.append(Recursive_Contract((D_i[:], W_i.copy())))
    
    return min(outputs)



    