"""LC-1584 - Min Cost to Connect All Points

合并自 2 个解法文件:
  1. 1584 - A - Min Cost All Points - Prim's 教科书.py
  2. 1584 - B - Min Cost to Connect All Points - ⭐️ Prim 教科书 🚀 - MST (NeetCode).py
"""

from typing import List

import heapq


# ============================================================================
# Solution 1: Prim_s    (原文件: 1584 - A - Min Cost All Points - Prim's 教科书.py)
# ============================================================================

# Time: O(N²log(N))
# Space: O(N²)

points_1 = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

class Solution_1_Prim_s:
    def get_cost(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points_1: List[List[int]]) -> int:
        n = len(points_1)
        visited = [False] * n

        """
        1st item is the edge weight.
        - Here we choose vertice 0 as starting point

        2nd item is the next vertice.
        - From the beginning to vertice 0, the distance is zero)
        """
        heap = [(0, 0)]

        # This is the total edge weights sum of the current
        # minimum spanning being constructed.
        result = 0
        edges = 0
        while edges < n:
            cost, curr_node = heapq.heappop(heap)
            if visited[curr_node]:
                continue
            visited[curr_node] = True
            result += cost
            edges += 1

            # Here we are adding all the edges of the current node
            for next_node in range(n):
                if not visited[next_node]:
                    next_cost = self.get_cost(
                        *points_1[curr_node], *points_1[next_node]
                    )
                    heapq.heappush(heap, (next_cost, next_node))

        return result

# ============================================================================
# Solution 2: MST_NeetCode    (原文件: 1584 - B - Min Cost to Connect All Points - ⭐️ Prim 教科书 🚀 - MST (NeetCode).py)
# ============================================================================

# Time: O(E²log(E))
# Space: O(E²)

points_2 = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

class Solution_2_MST_NeetCode:
    def distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points_2: List[List[int]]) -> int:
        n = len(points_2)
        visited = [False] * n
        
        heap = [(0, 0)] # [edge_weight, next_vertice]

        # This is the total edge weights sum of the current
        # minimum spanning being constructed.
        result = 0
        edges = 0
        while edges < n:
            cost, node = heapq.heappop(heap)
            if visited[node]:
                continue
            visited[node] = True
            result += cost
            edges += 1

            # Here we are adding all the edges of the current node
            for next_node in range(n):
                if not visited[next_node]:
                    next_cost = self.distance(
                        *points_2[node], *points_2[next_node]
                    )
                    heapq.heappush(heap, (next_cost, next_node))

        return result


if __name__ == "__main__":

    # --- Solution 1: Prim_s ---
    s = Solution_1_Prim_s()
    result = s.minCostConnectPoints(points_1)
    print(result)

    # --- Solution 2: MST_NeetCode ---
    s = Solution_2_MST_NeetCode()
    result = s.minCostConnectPoints(points_2)
    print(result)
