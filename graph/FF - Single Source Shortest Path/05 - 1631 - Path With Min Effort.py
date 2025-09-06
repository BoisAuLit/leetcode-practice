from typing import List, Tuple
import heapq

"""
cost == max_height_diff along optimal path
"""


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])
        visited = [[False] * n for _ in range(m)]

        # Each cell stores the max_height_diff along the optimal path
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # cost, x, y

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def get_neigbs(x: int, y: int) -> List[Tuple[int, int, int]]:
            cost = dist[x][y]
            neigbs = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < m and 0 <= ny < n):
                    continue

                # ! 2️⃣ Skip visited nodes optimization
                if visited[nx][ny]:
                    continue
                new_cost = abs(heights[nx][ny] - heights[x][y])
                """
                The new cost is the maximum between
                - the previous max height diff along the optimal path
                and
                - the new height diff (from (x, y) --> (nx, ny))
                """
                neigbs.append((max(new_cost, cost), nx, ny))
            return neigbs

        while heap:
            cost, x, y = heapq.heappop(heap)

            # ! 1️⃣ Skip stale entries optimization
            if dist[x][y] < cost:
                continue

            # ! 3️⃣ Stop early optimization
            if x == m - 1 and y == n - 1:
                return cost

            visited[x][y] = True

            for new_cost, nx, ny in get_neigbs(x, y):
                if new_cost < dist[nx][ny]:
                    dist[nx][ny] = new_cost
                    heapq.heappush(heap, (new_cost, nx, ny))
        return -1


# Test case 1: Expect 0
# s = Solution()
# heights = [
#     [1, 2, 1, 1, 1],
#     [1, 2, 1, 2, 1],
#     [1, 2, 1, 2, 1],
#     [1, 2, 1, 2, 1],
#     [1, 1, 1, 2, 1],
# ]
# result = s.minimumEffortPath(heights)
# print(result)

# Test case 2: Expect 2
s = Solution()
heights = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
result = s.minimumEffortPath(heights)
print(result)
