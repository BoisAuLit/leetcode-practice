from typing import List


"""
Time complexity: O(N²·logN)
Space complexity: O(N²)
"""


class UnionFind:
    def __init__(self, n):
        self.root = list(range(n))
        self.rank = [1] * n
        self.n = n
        self.edges_count = 0
        self.dist = 0

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    # Return value means finished or not
    def union(self, edge_weight: float, x: int, y: int) -> bool:
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
            self.dist += edge_weight
            self.edges_count += 1
            return self.edges_count == self.n - 1
        return False

    def get_dist(self) -> float:
        return self.dist


class Solution:
    def get_manh_dist(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []

        # We need to find the minimum edges of all, so we must calculate
        # all the manhattan distance first
        for i in range(n - 1):
            for j in range(i + 1, n):
                edge_weight = self.get_manh_dist(*points[i], *points[j])
                # 点只用 index 表示, i 代表第1个点, j 代表第二个点
                edges.append((edge_weight, i, j))

        # Sorting algorithm in python use first element in inner array by default
        edges.sort()
        uf = UnionFind(n)
        for edge in edges:
            if uf.union(*edge):
                return uf.get_dist()

        # Returning 0 is important, in case there's only 1 point.
        return 0


s = Solution()
points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
result = s.minCostConnectPoints(points)
print(result)
