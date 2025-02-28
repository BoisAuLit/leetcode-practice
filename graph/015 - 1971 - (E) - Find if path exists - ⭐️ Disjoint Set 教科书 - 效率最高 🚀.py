from typing import List

"""
Time complexity: O(m⋅α(n))

The amortized complexity for performing m union find operations is O(m⋅α(n)) 
time where α is the Inverse Ackermann Function.
To sum up, the overall time complexity is O(m⋅α(n)).

========================================================================

Space complexity: O(n)

We used two arrays root and rank to save the root and rank 
of each node in the DSU data structure, each of them takes O(n) space.
To sum up, the overall time complexity is O(n).
"""


class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n

    def find(self, x: int) -> int:
        if self.root[x] == x:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> None:
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[x] > self.rank[y]:
                self.root[rootY] = rootX
            elif self.rank[x] < self.rank[y]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1


class Solution:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        unionFind = UnionFind(n)
        for x, y in edges:
            unionFind.union(x, y)
        return unionFind.find(source) == unionFind.find(destination)
