from typing import List
import heapq
from collections import defaultdict


class UnionFind:
    def __init__(self, n: int, wells: List[int], pipes: List[List[int]]):
        self.root = list(range(n))
        self.cost = wells
        self.pipes = [(x - 1, y - 1, z) for x, y, z in pipes]
        self.pipes.sort(key=lambda x: x[2])
        for x, y, pipe_cost in self.pipes:
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
            # If establishing a pipe is more expensive than digging wells at both houses,
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


class Solution:
    def minCostToSupplyWater(
        self, n: int, wells: List[int], pipes: List[List[int]]
    ) -> int:
        unionFind = UnionFind(n, wells, pipes)
        return unionFind.get_cost()


class Solution2:
    def minCostToSupplyWater(
        self, n: int, wells: List[int], pipes: List[List[int]]
    ) -> int:
        edges = defaultdict(list)

        for x, y, cost in pipes:
            edges[x].append((cost, y))
            edges[y].append((cost, x))

        for index, cost in enumerate(wells):
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

            if len(visited) == n:
                return total_cost

            for cost, next_house in edges[house]:
                if next_house not in visited:
                    heapq.heappush(heap, (cost, next_house))

        return total_cost

s = Solution()

# Test case 1: Expecting 3
n = 3
wells = [1, 2, 2]
pipes = [[1, 2, 1], [2, 3, 1]]

# Test case 2: Expecting 2
n = 2
wells = [1, 1]
pipes = [[1, 2, 1], [1, 2, 2]]


result = s.minCostToSupplyWater(n, wells, pipes)
print(result)
