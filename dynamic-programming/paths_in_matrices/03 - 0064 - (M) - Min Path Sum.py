from typing import List

"""
Time complexity: O(m·n)
Space complexity: O(m)
"""


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        dp = [0] * m
        dp[-1] = grid[-1][-1]
        for i in range(m - 2, -1, -1):
            dp[i] = dp[i + 1] + grid[i][-1]

        for j in range(n - 2, -1, -1):
            dp[-1] += grid[-1][j]
            for i in range(m - 2, -1, -1):
                dp[i] = grid[i][j] + min(dp[i], dp[i + 1])
        return dp[0]


s = Solution()
grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
result = s.minPathSum(grid)
print(result)
