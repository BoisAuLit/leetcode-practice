from typing import List
from collections import deque


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        m = len(heights)
        n = len(heights[0])
        pacific = [(0, y) for y in range(n)] + [(x, 0) for x in range(1, m)]
        atlantic = [(m - 1, y) for y in range(n)] + [(x, n - 1) for x in range(m - 1)]

        def dfs(points):
            q = deque(points)
            seen = set(points)
            while q:
                x, y = q.popleft()
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen and heights[nx][ny] >= heights[x][y]:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            return seen

        return list(dfs(pacific) & dfs(atlantic))


s = Solution()
# fmt: off
input_ = [
  [4,2,7,3,4],
  [7,4,6,4,7],
  [6,3,5,3,6]
]
# fmt: on
result = s.pacificAtlantic(input_)
print(result)
