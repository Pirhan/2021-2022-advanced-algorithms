# interface class requried for external visibility of cython classes (ie calling from regular python code) 

cdef class UnionFind:
    cpdef void Initialize(self, set nodes)
    cpdef int Find(self, int x)
    cpdef void Union(self, int x, int y)
    

    
