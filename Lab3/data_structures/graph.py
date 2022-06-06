# from typing import *
from typing import List, Set, Tuple, Dict
import numpy as np  # type:ignore
import copy


class Graph:
    def __init__(self, n) -> None:
        self.nodes: Set[int] = set()
        self.edges: Dict[Tuple[int, int], float] = {}
        self.dimension = n

    def addEdge(self, node1: int, node2: int, weight: int) -> None:
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.edges[(node1, node2)] = weight

    def getW(self):
        return self.W

    def getD_W(self):
        D_ = self.D.copy()
        W_ = [array.copy() for array in self.W]
        return (D_,W_)

    #  get weight of a pair of nodes, required by stoer wagner
    #  node index start from 1 and not 0
    def getWeight(self, node1: int, node2: int) -> int:
        if node1 in self.nodes and node2 in self.nodes:
            return self.W[node1][node2]
        else:
            return 0

    def set_D_W(self):
        # Builds the weights matrix and build the comulative weight list
        n_nodes = self.dimension
        # Creating W
        W_: np.matrix = np.zeros((n_nodes + 1, n_nodes + 1))  # Strarting from 0
        W = W_.tolist()
        #W = [list(W_[i])[:] for i in range(len(list(W_[0])))]
        for edge in self.getEdges().items():
            ((node1, node2), weight) = edge
            W[node1][node2] = weight
            W[node2][node1] = weight

        self.W = W
        # Nodes are starting from 1
        # W is a matrix and we are accessing to the column relative to u
        self.D = [0] + [sum(W[u]) for u in sorted(list(self.getNodes()))]

    def cutWeight(self, cut1: List[int]) -> int:
        # returns the weight of the cut
        # since the set of nodes is splitted in 2
        # cut1 is enough to compute the nodes belonging to each cut
        # ie cut1 will contain the nodes of the first partition, where all other nodes will be on the second partition
        # idea:
        # get the array weight for all nodes in cut1
        # it will be an array of arrays
        # for each of these nested array
        # compute the sum of the weight only for those vertex which does not belong to cut1
        # return the sum of this partial sum
        # nodesInCut contains only the list of nodes weight of the first cut
        partialSum: int = 0
        #  also check if node exists(required in stoerWagner when computing stMinimumCut for smaller graph)
        for nodeInCut1 in cut1[0]:  # type: ignore
            for nodeInCut2 in cut1[1]:  # type: ignore
                partialSum += self.getWeight(nodeInCut1, nodeInCut2)
        return partialSum

    def adjacentNodes(self, node: int) -> List[int]:
        # get the row of nodes adjacent to node
        # it will contain only the weights
        # associate for each weight of a node it's index
        # return only nodes where the weight is greater then 0 for the moment try to see if this is enough
        # if node does not belong anymore to the graph return the empty list
        if node not in self.nodes:
            return []
        rowEdges: List[int] = self.getD_W()[1][
            node
        ]  # should be equivalent to self.getRowEdges(node=node)
        return [
            vertex
            for vertex, weight in enumerate(rowEdges)
            if weight > 0 and (vertex) in self.nodes
        ]
        # adds one just because vertex index seem to start from 1 instead of 0

    def removeNodes(self, toRemove: List[int]) -> None:
        # remove nodes which does not belong to
        # the graph anymore
        # required by GlobalMiniumCut when computing
        # the second cut
        # node passed are 1-start nodes (ie node start from 1)
        # node 1,2,3 .. etc
        # remove from node only for the moment try to see if this is enough
        if len(toRemove) < 0:
            return
        self.nodes = set([x for x in self.nodes if x not in toRemove])

    def getEdges(self):
        return self.edges

    def getNodes(self) -> List[int]:
        return list(self.nodes)

    @staticmethod
    def initialize_from_file(filename: str):
        """Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file

            starting_line = lines[0]
            n_nodes = int(starting_line.split()[0])

            graph = Graph(n_nodes)

            for line in lines[1:]:
                node_1 = int(line.split()[0])
                node_2 = int(line.split()[1])
                # weight = float(line.split()[2])
                weight = int(
                    line.split()[2]
                )  # all weights seem to be int in the dataset

                graph.addEdge(node_1, node_2, weight)

            graph.set_D_W()
            file.close()
        return graph
