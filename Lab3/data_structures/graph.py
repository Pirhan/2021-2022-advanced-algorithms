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
        return copy.deepcopy((self.D, self.W))

    #  get weight of a pair of nodes, required by stoer wagner
    #  node index start from 1 and not 0
    def getWeight(self, node1: int, node2: int) -> int:
        if node1 in self.nodes and node2 in self.nodes:
            return self.W[node1, node2]
        else:
            return 0

    def set_D_W(self):
        # Builds the weights matrix and build the comulative weight list
        n_nodes = self.dimension
        # Creating W
        W: np.matrix = np.zeros((n_nodes + 1, n_nodes + 1))  # Strarting from 0
        for edge in self.getEdges().items():
            ((node1, node2), weight) = edge
            W[node1, node2] = weight
            W[node2, node1] = weight

        self.W = W
        # Creating D
        D: List[float] = []
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
        # index in W are 0 start based, while in cut are 1-start based
        partialSum: int = 0
        #  also check if node exists(required in stoerWagner when computing stMinimumCut for smaller graph)
        for weightsInCut in [
            weight
            for node, weight in enumerate(self.getW())
            if (node) in self.nodes and (node) in cut1
        ]:  # compute weight of all nodes in cut;
            # sanity check: compute the cut only of nodes which are still in the graph
            for weightInCut in [
                (node, weight)
                for node, weight in enumerate(weightsInCut)
                if node not in cut1 and node in self.nodes and weight > 0
            ]:
                partialSum += weightInCut[1]
        return partialSum

    def adjacentNodes(self, node: int) -> List[int]:
        # get the row of nodes adjacent to node
        # it will contain only the weights
        # associate for each weight of a node it's index
        # return only nodes where the weight is greater then 0 for the moment try to see if this is enough
        # if node does not belong anymore to the graph return the empty list
        if node not in self.nodes:
            return []
        rowEdges: List[int] = self.getD_W()[1][node]  # should be equivalent to self.getRowEdges(node=node)
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
        # remove edges where nodes are involved
        # self.edges = set(
        #    [x for x in self.edges if not (x[0] + 1 in nodes or x[1] + 1 in nodes)]
        # )
        # remove from weight matrix
        # for each node which contains a node in nodes
        # must set it's weight to zero
        # remove from weight nodes
        # index: int = 0
        # while index < len(self.D) - 1:
        #    if index + 1 in nodes:
        #        self.D[index] = 0.0
        #    index += 1

        # pass

    def getEdgesList(self):
        return self.edges

    """ def setWeightedDegree(self):
        D: List[float] = []
        for node in self.getNodes():
            D.append(self.getRowWeight(node))
        self.D = D """

    """ def getRowEdges(self, node: int) -> List[int]:  # int:
        # Returns the array corresponding to the matrix row
        return self.W[node - 1]

    def getRowWeight(self, node: int) -> int:
        # Returns the sum of the matrix row weights
        return sum(self.getRowEdges(node)) """

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
