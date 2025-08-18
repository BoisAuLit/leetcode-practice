from typing import List
from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] + grid[n - 1][n - 1] > 0:
            return -1
        if n <= 2:
            return n
        # fmt: off
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # fmt: on
        queue = deque([(0, 0)])
        visited = set([(0, 0)])
        iterations = 1
        while queue:
            for _ in range(len(queue)):
                x, y = queue.popleft()
                for dx, dy in directions:
                    x1, y1 = x + dx, y + dy
                    coords = (x1, y1)
                    if coords == (n - 1, n - 1):
                        return iterations + 1
                    if (
                        not (0 <= x1 <= n - 1 and 0 <= y1 <= n - 1)
                        or (x1, y1) in visited
                        or grid[x1][y1] == 1
                    ):
                        continue
                    visited.add(coords)
                    queue.append(coords)
            iterations += 1
        return -1


s = Solution()

# Test case 1: Expecting 2
# grid = [[0, 1], [1, 0]]

# Test case 2: Expecting 4
grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]

# Test case 3: Expecting -1
# grid = [[1, 0, 0], [1, 1, 0], [1, 1, 0]]

# Test case 4: Expecting -1
# grid = [[0, 1, 1], [1, 1, 1], [1, 1, 0]]

# Test case 5: Expecting
# fmt: off
grid = [
    [0,0,1,1,0,0],
    [0,0,0,0,1,1],
    [1,0,1,1,0,0],
    [0,0,1,1,0,0],
    [0,0,0,0,0,0],
    [0,0,1,0,0,0]]
# fmt: on

result = s.shortestPathBinaryMatrix(grid)
print(result)
