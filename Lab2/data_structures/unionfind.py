from typing import Dict
class UnionFind:

    parent : Dict[int,int] = {}
    size : Dict[int,int] = {}    # stores the depth of trees using memory n

    def Initialize(self, nodes):
        # create `n` disjoint sets (one for each node)
        for i in nodes:
            self.parent[i] = i
            self.size[i] = 1
 
    # Find the root of the set in which element `x` belongs
    def Find(self, x):
        # if `k` is not the root
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x]) # Recursive call
        return self.parent[x]

    # Perform the Find method iteratively
    def Find_it(self, x):

        while(self.parent[x] != x):
            x = self.parent[x]
        return self.parent[x]
 
    # Perform Union of two subsets
    def Union(self, x, y):
        # find the root of the sets in which elements `x` and `y` belongs
        i, j = self.Find(x), self.Find(y)
 
        # if `x` and `y` are present in the same set
        if i == j:
            return
 
        # Always attach a smaller depth tree under the root of the deeper tree.
        if self.size[i] >= self.size[j]:
            self.parent[j] = i
            self.size[i] += self.size[j]
        else:
            self.parent[i] = j
            self.size[j] += + self.size[i]