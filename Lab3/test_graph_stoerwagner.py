from data_structures.graph import Graph  # type: ignore
from typing import List


def testGetWeightUtil(graph: Graph, node1: int, node2: int, assertValue: int) -> None:
    aWeight: int = graph.getWeight(node1=node1, node2=node2)
    print("weight", aWeight)
    assert aWeight == assertValue


def testGetWeight(graph: Graph):
    print("in test getWeight")
    testGetWeightUtil(graph=graph, node1=1, node2=2, assertValue=9091)
    testGetWeightUtil(graph=graph, node1=3, node2=8, assertValue=51)
    testGetWeightUtil(graph=graph, node1=5, node2=5, assertValue=0)
    print("out test getWeight")


def testGetWeightAfterRemove(graph: Graph):
    print("in test getWeight after Remove")
    testGetWeightUtil(graph=graph, node1=1, node2=2, assertValue=0)
    testGetWeightUtil(graph=graph, node1=3, node2=8, assertValue=0)
    testGetWeightUtil(graph=graph, node1=9, node2=10, assertValue=0)
    testGetWeightUtil(graph=graph, node1=10, node2=9, assertValue=0)

    print("out test getWeight afterRemove")


def testCutWeightUtil(graph: Graph, cut: List[int], assertValue: int):
    weight: int = graph.cutWeight(cut1=cut, nodes=graph.getNodes())
    print("cut weight", weight)
    assert weight == assertValue


def testCutWeight(graph: Graph):
    print("in test cutWeight")
    testCutWeightUtil(graph=graph, cut=[1], assertValue=9091)
    testCutWeightUtil(graph=graph, cut=[2], assertValue=22986)
    testCutWeightUtil(graph=graph, cut=[2, 3], assertValue=21600)
    testCutWeightUtil(graph=graph, cut=[2, 3, 4], assertValue=25488)
    print("out test cutWeight")


def testCutWeightAfterRemove(graph: Graph):
    print("in test cutWeight afterRemove")
    testCutWeightUtil(graph=graph, cut=[1], assertValue=0)
    testCutWeightUtil(graph=graph, cut=[2], assertValue=0)
    testCutWeightUtil(graph=graph, cut=[2, 3], assertValue=0)
    testCutWeightUtil(graph=graph, cut=[9], assertValue=5961)
    print("out test cutWeight afterRemove")


def testAdjacentNodes(graph: Graph):
    print("in test adjacentNodes")
    adjacent: List[int] = graph.adjacentNodes(node=1)
    print(adjacent)
    assert 2 in adjacent
    adjacent = graph.adjacentNodes(node=6)
    print(adjacent)
    assert 5 in adjacent and 7 in adjacent and 10 in adjacent
    adjacent = graph.adjacentNodes(node=9)
    print(adjacent)
    assert 10 in adjacent and 8 in adjacent and 10 in adjacent and 2 in adjacent
    print("out test adjacentNodes")


def testAdjacentNodesAfterRemove(graph: Graph):
    print("in test adjacentNodes after remove")
    adjacent: List[int] = graph.adjacentNodes(node=1)
    print(adjacent)
    assert len(adjacent) == 0
    adjacent = graph.adjacentNodes(node=6)
    print(adjacent)
    assert 5 in adjacent and 7 in adjacent
    adjacent = graph.adjacentNodes(node=9)
    print(adjacent)
    assert 8 in adjacent
    print("out test adjacentNodes after remove")


def testRemoveNodes(graph: Graph):
    print("in test removeNodes")
    print(graph.getNodes())
    toRemove: List[int] = [1]
    print("toRemove", toRemove)
    graph.removeNodes(toRemove)
    print(graph.getNodes())
    toRemove = [1, 2, 3]
    print("toRemove", toRemove)
    graph.removeNodes(toRemove=toRemove)
    print(graph.getNodes())
    toRemove = [10]
    print("toRemove", toRemove)
    graph.removeNodes(toRemove=toRemove)
    print(graph.getNodes())
    print("out test removeNodes")


def main():
    aGraph = Graph.initialize_from_file(filename="dataset/input_random_01_10.txt")
    testGetWeight(graph=aGraph)
    testAdjacentNodes(graph=aGraph)
    testCutWeight(graph=aGraph)
    testRemoveNodes(graph=aGraph)
    testAdjacentNodesAfterRemove(graph=aGraph)
    testGetWeightAfterRemove(graph=aGraph)
    testCutWeightAfterRemove(graph=aGraph)


main()
