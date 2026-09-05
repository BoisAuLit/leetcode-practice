from typing import List
from collections import defaultdict


class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1

    def getCount(self) -> int:
        return self.count

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


class Solution:
    """
    Principle:
    Locate all the letter in the same component.
    Sort letters in ascending order in that component.
    Re-put those sorted letters in the origianl sting.
    """
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        uf = UnionFind(n)
        for x, y in pairs:
            uf.union(x, y)
        components = defaultdict(list)
        for i in range(n):
            components[uf.find(i)].append(i)
        result = [0] * n
        for component_indices in components.values():
            letters = sorted([s[i] for i in component_indices])
            for i, j in enumerate(component_indices):
                result[j] = letters[i]
        return "".join(result)


solution = Solution()
s = "dcab"
pairs = [[0, 3], [1, 2]]
result = solution.smallestStringWithSwaps(s, pairs)
print(result)
