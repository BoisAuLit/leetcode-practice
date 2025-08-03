from typing import List


class UnionFind:
    def __init__(self, n):
        self.rank = [1] * n
        self.root = list(range(n))
        self.count = n

    def find(self, x: int) -> int:
        if self.root[x] == x:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> None:
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

    def getCount(self):
        return self.count

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort(key=lambda x: x[0])
        unionFind = UnionFind(n)
        for timestamp, x, y in logs:
            unionFind.union(x, y)
            if unionFind.getCount() == 1:
                return timestamp

        return -1


s = Solution()

# Test case 1: Expecting 20190301
logs = [
    [20190101, 0, 1],
    [20190104, 3, 4],
    [20190107, 2, 3],
    [20190211, 1, 5],
    [20190224, 2, 4],
    [20190301, 0, 3],
    [20190312, 1, 2],
    [20190322, 4, 5],
]
n = 6

# Test case 2: Expecting 8
logs = [[9, 3, 0], [0, 2, 1], [8, 0, 1], [1, 3, 2], [2, 2, 0], [3, 3, 1]]
n = 4

result = s.earliestAcq(logs, n)
print(result)
