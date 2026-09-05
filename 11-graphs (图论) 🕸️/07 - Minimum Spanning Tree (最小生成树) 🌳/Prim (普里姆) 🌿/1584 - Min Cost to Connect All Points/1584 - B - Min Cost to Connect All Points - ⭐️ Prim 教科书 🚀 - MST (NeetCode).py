from typing import List
import heapq

"""
Time: O(E²log(E))
Space: O(E²)
"""


class Solution:
    def distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
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
                        *points[node], *points[next_node]
                    )
                    heapq.heappush(heap, (next_cost, next_node))

        return result


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
