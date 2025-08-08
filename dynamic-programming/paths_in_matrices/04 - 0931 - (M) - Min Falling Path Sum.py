from typing import List
from functools import lru_cache
import math


class Solution_Top_Down_Memoization:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        @lru_cache(None)
        def dp(i: int, j: int) -> int:
            if j < 0 or j >= n:
                return math.inf
            if i == m - 1:
                return matrix[i][j]
            return matrix[i][j] + min(
                dp(i + 1, j - 1), dp(i + 1, j), dp(i + 1, j + 1)
            )

        return min(dp(0, j) for j in range(n))


class Solution:
    """
    Time complexity: O(m·n)
    Space complexity: O(m))
    """

    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        dp = matrix[-1][:]

        def elem(j: int) -> int:
            return dp[j] if 0 <= j <= n - 1 else math.inf

        for i in range(m - 2, -1, -1):
            temp = [0] * n
            for j in range(n):
                temp[j] = matrix[i][j] + min(elem(j - 1), dp[j], elem(j + 1))
            dp = temp
        return min(dp)


s = Solution()
matrix = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
result = s.minFallingPathSum(matrix)
print(result)
