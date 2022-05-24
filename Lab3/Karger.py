import math
import numpy as np
from typing import *
from data_structures.graph import Graph




def Random_Select(C: List[float]):

    r = np.random.randint(0, C[- 1])
    
    edge_found_index = binarySearch(r, C)   # This is the edge founded, achived as just an index
    
    if edge_found_index is None: assert(False)

    return edge_found_index

def binarySearch(r : int, C: List[float]):
        low = 0
        high = len(C) - 1
        #print (r, "\t", C)
        # Repeat until the pointers low and high meet each other
        while low <= high:

            mid = low + (high - low)//2

            if C[mid-1] <= r and C[mid] > r:
                return mid
            elif C[mid] < r:
                low = mid + 1
            else:
                high = mid - 1

        return None 

def Edge_Select(G) -> Tuple[int,int]:
    
    (D,W) = G
    C_D = [sum(D[:i]) for i in range (1,len(D)+1)] # Creating the comulative weight on D[i]
    print("C_D: \t", C_D[-1])
    u = Random_Select(C_D)

    C_W = [sum((W[u-1])[:i]) for i in range (1,len(W[u-1])+1)]    # Creating the comulative weights on W[u-1]
    print("C_W: \t", C_W[-1], "\t", u)
    if C_W[-1] == 0: print("\n",C_W)
    v = Random_Select(C_W)

    return (u,v)

def Contract_Edge(G, u : int, v: int):
    (D,W) = G
    D[u -1] += D[v-1] - (2 * W[u-1,v-1])    # This is the only way to obtain a negative value
    D[v-1] = 0
    W[u-1, v-1] = 0
    W[v-1, u-1] = 0

    temp_nodes = [n for n in range(1,len(D)+1) if (n != u or n != v)]
    #print("tn \t", temp_nodes)
    for w in temp_nodes:
        W[u-1, w-1] += W[v-1, w-1]
        W[w-1, u-1] += W[w-1, v-1]
        W[v-1, w-1] = 0
        W[w-1, v-1] = 0

def Contract(G, k):
    (D,W) = G
    n_nodes = len(D)
    for _ in range(n_nodes - k):    # TODO from 1???
        (u,v) = Edge_Select((D,W))
        Contract_Edge((D,W), u, v)
    
    return D, W

def Recursive_Contract(G):
    (D,W) = G
    n_nodes = len(D)
    if n_nodes <= 6:
        (_, new_W) = Contract((D,W),2)
        return new_W[u-1, v-1]


    t = math.ceil(n_nodes/math.sqrt(2)+1)
    list_w = []
    for i in range(2):
        print("Hi: ", i)
        newG = Contract((D.copy(),W.copy()), t)
        list_w.append(Recursive_Contract(newG))
    return min(list_w)


def Karger(G: Graph, k : int)-> float:
    minimumDistance = float("+Infinity")  # Useful for the comparison
    for _ in range(k):
        t = Recursive_Contract((G.getD().copy(), G.getW().copy()))
        if t < minimumDistance :
            minimumDistance = t
    return minimumDistance
