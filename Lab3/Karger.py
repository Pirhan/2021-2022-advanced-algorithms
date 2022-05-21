import math
import numpy as np
from typing import *
from data_structures.graph import Graph




def Random_Select(C: List[float]):
    print(C[-1])
    r = np.random.randint(C[- 1])
    
    edge_found_index = binarySearch(r, C)   # This is the edge fouded, achived as just an index
    
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

    def comulative_weights(D: List[float]):
        Comulative : List[int] = []
        n_nodes = len(D)
        
        # Supposing that k can not be more than n_nodes
        for i in range (n_nodes):
            Comulative.append(sum(D[:i+1])) # Starting from 0
        return Comulative
    
    (D,W) = G
    C_D = comulative_weights(D)
    u = Random_Select(C_D)
    C_W = comulative_weights(W[u-1])     # To check 
    v = Random_Select(C_W)

    return (u,v)

def Contract_Edge(G, u : int, v: int):
    (D,W) = G
    D[u -1] += D[v-1] - (2 * W[u-1,v-1])
    D[v-1] = 0
    W[u-1, v-1] = 0
    W[v-1, u-1] = 0

    temp_nodes = [n for n in range(len(D)) if (n != u and n != v)]
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
    for _ in range(2):
        newG = Contract((D,W), t)
        list_w.append(Recursive_Contract(newG))
    return min(list_w)


def Karger(G: Graph, k : int)-> float:
    minimumDistance = float("+Infinity")  # Useful for the comparison
    for i in range(k):
        t = Recursive_Contract((G.getD().copy(), G.getW().copy()))
        if t < minimumDistance :
            minimumDistance = t
    return minimumDistance
