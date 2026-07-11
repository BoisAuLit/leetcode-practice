from typing import List


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
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort()
        uf = UnionFind(n)
        for time, x, y in logs:
            uf.union(x, y)
            if uf.getCount() == 1:
                return time
        return -1
