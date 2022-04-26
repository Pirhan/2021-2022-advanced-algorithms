from typing import List


class Graph:
    def __init__(self) -> None:
        self.Adj_list = {}  # [[]], dict in order to support an unordered set of keys
        self.nodes = set()  # set containing the nodes discovered
        self.edges = (
            {}
        )  # dict containing the edges with a tuple of nodes as key and the weight as value

    def addEdge(self, edge: tuple, weight: int) -> None:
        (v, u) = edge
        self.nodes.add(v)
        self.nodes.add(u)
        edges = list(self.edges.keys())
        if edge not in edges:
            self.edges[edge] = weight
        else:
            return

        if v not in list(self.Adj_list.keys()):
            self.Adj_list[v] = []
        if u not in list(self.Adj_list.keys()):
            self.Adj_list[u] = []
        (self.Adj_list[v]).append(edge)
        (self.Adj_list[u]).append(edge)

    def total_Weight(self):
        return sum(self.edges.values())

    # Returns all the nodes incident to node
    def getAdjacentNodes(self, node: int) -> list:
        nodes = set()
        if node in self.nodes:
            for (u, v) in list((self.Adj_list)[node]):
                if node == u:
                    nodes.add(v)
                else:
                    nodes.add(u)  # if node == v
        return list(nodes)

    # Returns all the edges with node
    def getAdjacentEdges(self, node: int) -> list:
        edges = set()
        for list_edges in list(self.Adj_list[node]):
            edges.add(list_edges)
        return list(edges)

    # Orders the graph in non discending order of keys
    def nonDiscendingOrderGraph_Keys(self):
        self.edges = dict(sorted(self.edges.items(), key=lambda item: item[0]))

    # Orders the graph in non discending order of values
    def nonDiscendingOrderGraph_Values(self):
        self.edges = dict(sorted(self.edges.items(), key=lambda item: item[1]))

    def skip_prelude(self, lines: List[str]) -> int:
        """ skip all data before the vertex for now"""
        index: int = 0
        # iterate over all string which are not vertex data
        while not (
            lines[index].startswith("NODE_COORD_SECTION")
        ):  # keep going if we are not in the section of vertex, NB: prelude of each file can be different
            print(
                lines[index], index
            )  # do something with it, see if type coordinates is needed (euclidean or georaphic)
            index += 1
        #  list[index] now contains "NODE_COORD_SECTION" skip this one too
        print(lines[index])
        index += 1
        return index

    def initialize_from_file(self, filename: str) -> None:
        """ Builds the graph from the filename"""
        with open(file=filename) as file:
            lines: List[str] = file.readlines()  # all lines of the file
            index: int = self.skip_prelude(lines=lines)
            print("skipped prelude", index)
            while not (lines[index]).startswith("EOF"):
                #  parse
                # following line not needed at the moment
                # edge_id : float = float(line.split()[0])  # float for now, probably need to be converted to int in the future
                print(lines[index])
                line = lines[index]
                x_coord: float = float(line.split()[1])
                y_coord: float = float(line.split()[2])
                #  add
                self.addEdge((x_coord, y_coord), 0)
                # weight null for the moment, change it later?
                index += 1

        return

    def inizialize(self, filename):
        """ Builds the adiacency lists from the txt file"""

        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                v1 = int(line.split()[0])  # First node
                v2 = int(line.split()[1])  # Second node
                w = int(line.split()[2])  # Weight

                self.addEdge((v1, v2), w)

        ############# Testing ############
        first_line = lines[0].split()
        assert len(self.nodes) == int(first_line[0])
        assert len(self.edges) == int(first_line[1])

    def PrintGraph(self, FunctionName, OriginalGraph=None):
        total_weight = 0
        for weight in list(self.edges.values()):
            total_weight += weight

        if OriginalGraph != None:
            # OriginalGraph = Graph()
            if len(self.nodes) == len(OriginalGraph.nodes):
                print(FunctionName)
                print(self.edges)
                print(
                    "The number of nodes in the MST is: ",
                    len(self.nodes),
                    " Total weight is: ",
                    total_weight,
                )
            else:
                print(FunctionName + " => Failed", "---- n. nodes = ", len(self.nodes))
                print(self.edges)
        else:
            print(self.edges)
