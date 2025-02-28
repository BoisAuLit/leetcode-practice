from typing import List
import math

"""
Time: O(E²log(E))
Space: O(E²)
"""


class Solution:
    def get_cost(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        mst_cost = 0
        edges_used = 0

        # Track nodes which are visited.
        visited = [False] * n

        min_dist = [math.inf] * n
        min_dist[0] = 0

        while edges_used < n:
            curr_min_edge = math.inf
            curr_node = -1

            # Pick least weight node which is not in MST.
            for node in range(n):
                if not visited[node] and curr_min_edge > min_dist[node]:
                    curr_min_edge = min_dist[node]
                    curr_node = node

            mst_cost += curr_min_edge
            edges_used += 1
            visited[curr_node] = True

            # Update adjacent nodes of current node.
            for next_node in range(n):
                weight = self.get_cost(*points[curr_node], *points[next_node])
                if not visited[next_node] and weight < min_dist[next_node]:
                    min_dist[next_node] = weight

        return mst_cost


s = Solution()

# Test case 1: Expecting 20
points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]

# Test case 2: Expecting 18
# points = [[3, 12], [-2, 5], [-4, 1]]

# Test case 3: Expecting 0
# points = [[10, 10]]

# Test case 4: Expecting 4
# points = [[0, 0], [2, 2]]

result = s.minCostConnectPoints(points)
print(result)
