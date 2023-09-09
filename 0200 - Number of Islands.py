from typing import List


class Solution:
    """
    Time complexity: O(M x N)
    Space complexity: O(M x N)
    """

    def expandIslands(self, x: int, y: int, grid: List[List[str]]) -> None:
        if (
            (not 0 <= x < len(grid))
            or (not 0 <= y < len(grid[0]))
            or grid[x][y] == "0"
        ):
            return
        grid[x][y] = "0"
        for a, b in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            self.expandIslands(x + a, y + b, grid)

    def numIslands(self, grid: List[List[str]]) -> int:
        count = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == "1":
                    count += 1
                    self.expandIslands(x, y, grid)
        return count


s = Solution()

# Expecting 1
input_ = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"],
]

# Expecting 3
input_ = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]


result = s.numIslands(input_)
print(result)
print(input_)

"""

"""
