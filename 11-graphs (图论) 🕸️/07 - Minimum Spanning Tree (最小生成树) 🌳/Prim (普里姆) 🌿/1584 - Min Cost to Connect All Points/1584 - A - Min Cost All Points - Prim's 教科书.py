from typing import List
import heapq

"""
Time: O(N²log(N))
Space: O(N²)
"""


class Solution:
    def get_cost(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
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
                        *points[curr_node], *points[next_node]
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
