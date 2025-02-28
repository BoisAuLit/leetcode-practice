from typing import List


class Solution:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(self, x: int, y: int, grid: List[List[str]]) -> None:
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == "1":
            grid[x][y] = "0"
            for dx, dy in self.directions:
                x1, y1 = x + dx, y + dy
                self.dfs(x1, y1, grid)

    def numIslands(self, grid: List[List[str]]) -> int:
        count = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == "1":
                    count += 1
                    self.dfs(x, y, grid)
        return count


s = Solution()

# fmt: off
# Test case 1: expecting 1
# grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]

# Test case 2: Expecting 3
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

# fmt: on

result = s.numIslands(grid)
print(result)
