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

def Random_Select(G : Graph):
    
    def comulative_weights(G : Graph):
        Comulative : List[int] 
        n_nodes = len(G.getNodes())

        for k in range(1, n_nodes + 1):
            Comulative.append(G.getRowWeight(k))
        return Comulative

    def binarySearch(G : Graph, r : int, Comulative: List[int], current : int= 0):
        n_nodes = len(G.getNodes()) - 1
        
        while current <= (n_nodes): 
    
            mid = current + (n_nodes - current) // 2
    
            # Check if x is present at mid
            if (Comulative[mid] <= r) and (r < Comulative[middle + 1]):
                return mid
    
            # If x is greater, ignore left half
            elif arr[mid] < x:
                current = mid + 1
    
            # If x is smaller, ignore right half
            else:
                n_nodes = mid - 1
    
        # If we reach here, then the element
        # was not present
        return None


    r = np.random.randint(comulative_weights(G)[len(G.getNodes()) - 1])
    # TODO - Continue

