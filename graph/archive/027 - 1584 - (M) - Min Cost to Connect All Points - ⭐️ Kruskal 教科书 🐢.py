from typing import List

"""
Time: O(ElogE)
Space: O(E)
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
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


class Solution:
    def get_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                distance = self.get_distance(*points[i], *points[j])
                edges.append((distance, i, j))
        edges.sort(key=lambda x: x[0])
        unionFind = UnionFind(n)
        total_cost = 0
        count_edges = 0
        for cost, x, y in edges:
            if unionFind.connected(x, y):
                continue
            unionFind.union(x, y)
            total_cost += cost
            count_edges += 1
            if count_edges == n - 1:
                return total_cost
        return total_cost


s = Solution()

# Test case 1: Expecting 20
points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

# Test case 2: Expecting 18
points = [[3, 12], [-2, 5], [-4, 1]]

# Test case 3: Expecting 0
points = [[10, 10]]
result = s.minCostConnectPoints(points)
print(result)
