from data_structures.maxheap import maxHeap  # type: ignore


def pushPop() -> None:
    print("in push pop")
    v = maxHeap()
    v.push(node=[1], weight=100)
    print(v.all())
    v.push(node=[2], weight=200)
    print(v.all())
    v.push(node=[3], weight=300)
    v.push(node=[3, 4], weight=300)
    print(v.all())
    popped = v.pop()
    print(v.all(), popped)
    popped = v.pop()
    print(v.all(), popped)
    popped = v.pop()
    print(v.all(), popped)
    print("out push pop")


def increaseKey() -> None:
    print("in increase key")
    v = maxHeap()
    v.push(node=[1], weight=100)
    v.push(node=[2], weight=200)
    v.push(node=[3], weight=300)
    v.push(node=[3, 4], weight=100)
    print("node", [1], "current weight", 100, "expected weight", 300)
    v.increaseKey(node=[1], weightToAdd=200)
    print("node", [3, 4], "current weight", 100, "expected weight", 200)
    v.increaseKey(node=[3, 4], weightToAdd=100)
    print(v.all())
    print("out increase key")


def main():
    pushPop()
    increaseKey()


main()
