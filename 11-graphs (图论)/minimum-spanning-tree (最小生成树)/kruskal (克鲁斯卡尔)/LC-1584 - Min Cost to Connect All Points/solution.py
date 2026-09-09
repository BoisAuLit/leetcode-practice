"""LC-1584 - Min Cost to Connect All Points

合并自 2 个解法文件:
  1. 1584 - A - Min Cost All Points - Kruskal's 教科书.py
  2. 1584 - B - Min Cost to Connect All Points - ⭐️ Kruskal 教科书 🐢 - MST (NeetCode).py
"""

from typing import List


# ============================================================================
# Solution 1: Kruskal_s    (原文件: 1584 - A - Min Cost All Points - Kruskal's 教科书.py)
# ============================================================================

# Time complexity: O(N²·logN)
# Space complexity: O(N²)

points_1 = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

class UnionFind_1:
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

class Solution_1_Kruskal_s:
    def get_manh_dist(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points_1: List[List[int]]) -> int:
        n = len(points_1)
        edges = []

        # We need to find the minimum edges of all, so we must calculate
        # all the manhattan distance first
        for i in range(n - 1):
            for j in range(i + 1, n):
                edge_weight = self.get_manh_dist(*points_1[i], *points_1[j])
                # 点只用 index 表示, i 代表第1个点, j 代表第二个点
                edges.append((edge_weight, i, j))

        # Sorting algorithm in python use first element in inner array by default
        edges.sort()
        uf = UnionFind_1(n)
        for edge in edges:
            if uf.union(*edge):
                return uf.get_dist()

        # Returning 0 is important, in case there's only 1 point.
        return 0

# ============================================================================
# Solution 2: MST_NeetCode    (原文件: 1584 - B - Min Cost to Connect All Points - ⭐️ Kruskal 教科书 🐢 - MST (NeetCode).py)
# ============================================================================

# Time: O(ElogE)
# Space: O(E)

points_2 = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

points_2 = [[3, 12], [-2, 5], [-4, 1]]

points_2 = [[10, 10]]

class UnionFind_2:
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

class Solution_2_MST_NeetCode:
    def distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points_2: List[List[int]]) -> int:
        n = len(points_2)
        edges = []
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                distance = self.distance(*points_2[i], *points_2[j])
                edges.append((distance, i, j))
        edges.sort(key=lambda x: x[0])
        unionFind = UnionFind_2(n)
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


if __name__ == "__main__":

    # --- Solution 1: Kruskal_s ---
    s = Solution_1_Kruskal_s()
    result = s.minCostConnectPoints(points_1)
    print(result)

    # --- Solution 2: MST_NeetCode ---
    s = Solution_2_MST_NeetCode()
    result = s.minCostConnectPoints(points_2)
    print(result)
