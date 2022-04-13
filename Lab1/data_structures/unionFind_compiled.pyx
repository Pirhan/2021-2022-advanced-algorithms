cdef class UnionFind:

    parent: dict = {}
    size: dict = {}      # stores the depth of trees using memory n

    cpdef void Initialize(self, set nodes):
        # create `n` disjoint sets (one for each node)
        for i in nodes:
            self.parent[i] = i
            self.size[i] = 1  
            # start from 1 instead of 0 otherwise
            # the sum of size in the Union operator will sum always 0 -> size not correctly updated
 
    # Find the root of the set in which element `x` belongs
    cpdef int Find(self, int x):
        # if `k` is not the root
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x]) # Recursive call
        return self.parent[x]
 
    # Perform Union of two subsets
    cpdef void Union(self, int x, int y):
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



        
