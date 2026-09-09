"""LC-1168 - Optimize Water Distribution in a Village

合并自 2 个解法文件:
  1. 005 - 1168 - Optimize Water Distribution.py
  2. 1168 - Optimize Water Distribution (stub - TODO re-solve; old Kruskal+Prim solution in archive).py
"""

from typing import List

import heapq

from collections import defaultdict


# ============================================================================
# Solution 1: Optimize_Water_Distribution    (原文件: 005 - 1168 - Optimize Water Distribution.py)
# ============================================================================

n_1 = 3

wells_1 = [1, 2, 2]

pipes_1 = [[1, 2, 1], [2, 3, 1]]

n_1 = 2

wells_1 = [1, 1]

pipes_1 = [[1, 2, 1], [1, 2, 2]]

class UnionFind:
    def __init__(self, n_1: int, wells_1: List[int], pipes_1: List[List[int]]):
        self.root = list(range(n_1))
        self.cost = wells_1
        self.pipes_1 = [(x - 1, y - 1, z) for x, y, z in pipes_1]
        self.pipes_1.sort(key=lambda x: x[2])
        for x, y, pipe_cost in self.pipes_1:
            self.union(x, y, pipe_cost)

    def find(self, x: int) -> int:
        if self.root[x] == x:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int, pipe_cost) -> None:
        rootX = self.find(x)
        rootY = self.find(y)
        wellX_cost = self.cost[rootX]
        wellY_cost = self.cost[rootY]

        # This condition will check if x, y belong to the same group
        # If they do, then we'll quit directly. If not it'll form a cycle.
        if rootX != rootY:
            # If establishing a pipe is more expensive than digging wells_1 at both houses,
            # then it's not worth it to put a pipe between the two houses
            if pipe_cost >= wellX_cost and pipe_cost >= wellY_cost:
                return

            if wellX_cost < wellY_cost:
                self.root[rootY] = rootX
                self.cost[rootY] = pipe_cost
            else:
                self.root[rootX] = rootY
                self.cost[rootX] = pipe_cost

    def get_cost(self) -> int:
        return sum(self.cost)

class Solution_1_Optimize_Water_Distribution:
    def minCostToSupplyWater(
        self, n_1: int, wells_1: List[int], pipes_1: List[List[int]]
    ) -> int:
        unionFind = UnionFind(n_1, wells_1, pipes_1)
        return unionFind.get_cost()

class Solution2:
    def minCostToSupplyWater(
        self, n_1: int, wells_1: List[int], pipes_1: List[List[int]]
    ) -> int:
        edges = defaultdict(list)

        for x, y, cost in pipes_1:
            edges[x].append((cost, y))
            edges[y].append((cost, x))

        for index, cost in enumerate(wells_1):
            edges[0].append((cost, index + 1))

        heap = edges[0]
        heapq.heapify(heap)
        total_cost = 0
        visited = set()

        while heap:
            cost, house = heapq.heappop(heap)

            if house in visited:
                continue
            total_cost += cost
            visited.add(house)

            if len(visited) == n_1:
                return total_cost

            for cost, next_house in edges[house]:
                if next_house not in visited:
                    heapq.heappush(heap, (cost, next_house))

        return total_cost

# ============================================================================
# Solution 2: TODO_re_solve_old_Kruskal_Prim_solution_    (原文件: 1168 - Optimize Water Distribution (stub - TODO re-solve; old Kruskal+Prim solution in archive).py)
# ============================================================================

class Solution_2_TODO_re_solve_old_Kruskal_Prim_solution_:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        pass


if __name__ == "__main__":

    # --- Solution 1: Optimize_Water_Distribution ---
    s = Solution_1_Optimize_Water_Distribution()
    result = s.minCostToSupplyWater(n_1, wells_1, pipes_1)
    print(result)
