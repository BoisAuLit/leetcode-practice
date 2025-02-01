from typing import List


class Solution:
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def expand_island(self, x: int, y: int, grid: List[List[str]]):
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
            return
        if grid[x][y] == "1":
            grid[x][y] = "0"
            for a, b in self.directions:
                self.expand_island(x + a, y + b, grid)

    def numIslands(self, grid: List[List[str]]) -> int:
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "1":
                    count += 1
                    self.expand_island(i, j, grid)
        return count



s = Solution()

# Test case 1: Expecting 1
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]


# Test case 2: Expecting 3
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

result = s.numIslands(grid)
print(result)

