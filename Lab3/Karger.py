import numpy as np
from typing import *
from data_structures.graph import Graph


def Karger(G: Graph, k : int)-> float:
    minimumDistance = float("+Infinity")  # Useful for the comparison
    for i in range(1, k + 1 ):
        t = Full_Contraction(G)
        if t < minimumDistance :
            minimumDistance = t
    return int(minimumDistance)

def comulative_weights(G : Graph):
        Comulative : List[int] 
        n_nodes = len(G.getNodes())

        for k in range(1, n_nodes + 1):
            Comulative.append(G.getRowWeight(k))
        return Comulative

def binarySearch(G : Graph, r : int, Comulative: List[int]):
        low = 0
        hight = len(G.getNodes()) - 1

        # Repeat until the pointers low and high meet each other
        while low <= high:

            mid = low + (high - low)//2

            if array[mid] == r:
                return mid

            elif array[mid] < r:
                low = mid + 1

            else:
                high = mid - 1

        return None 



def Random_Select(G : Graph)->int:
    
    Comulative : List[int] = comulative_weights(G)
    r = np.random.randint(comulative_weights(G)[len(G.getNodes()) - 1])
    
    edge_found_index = binarySearch(G, r, Comulative)   # This is the edge fouded, achived as just an index
    
    if edge_found_index is None: assert(True)

    return edge_found_index



