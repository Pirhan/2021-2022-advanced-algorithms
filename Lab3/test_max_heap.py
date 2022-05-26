from data_structures.maxheap import maxHeap


def pushPop() -> None:
    v = maxHeap()
    v.push(node=1, weight=100)
    print(v.all())
    v.push(node=2, weight=200)
    print(v.all())
    v.push(node=3, weight=300)
    print(v.all())
    popped = v.pop()
    print(v.all(), popped)
    popped = v.pop()
    print(v.all(), popped)
    popped = v.pop()
    print(v.all(), popped)


def increaseKey() -> None:
    v = maxHeap()
    v.push(node=1, weight=100)
    v.push(node=2, weight=200)
    v.push(node=3, weight=300)
    v.increaseKey(node=1, weightToAdd=200)
    popped = v.pop()
    print(v.all(), popped)
    popped = v.pop()
    print(v.all(), popped)

    print(v.all())


def main():
    pushPop()
    increaseKey()


main()
