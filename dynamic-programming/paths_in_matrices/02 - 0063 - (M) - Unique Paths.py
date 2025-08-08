from typing import List
from functools import lru_cache


class Solution_Top_Down_Memoization:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        # ! Don't forget this special case
        # ! If destination is an obstacle, then we can never reach there
        if obstacleGrid[m - 1][n - 1] == 1:
            return 0

        @lru_cache(None)
        def dp(x: int, y: int) -> int:
            if x == m - 1 and y == n - 1:
                return 1
            if x >= m or y >= n or obstacleGrid[x][y] == 1:
                return 0
            return dp(x, y + 1) + dp(x + 1, y)

        return dp(0, 0)


class Solution_Bottom_Up_Iteration:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        # ! Don't forget this special case
        # ! If destination is an obstacle, then we can never reach there
        if obstacleGrid[m - 1][n - 1] == 1:
            return 0

        dp = [[0] * n for _ in range(m)]

        # ! 注意, 这里一定要从后往前才可以
        for i in range(m - 1, -1, -1):
            if obstacleGrid[i][-1] == 1:
                break
            dp[i][-1] = 1

        # ! 注意, 这里一定要从后往前才可以
        for j in range(n - 1, -1, -1):
            if obstacleGrid[-1][j] == 1:
                break
            dp[-1][j] = 1

        for j in range(n - 2, -1, -1):
            for i in range(m - 2, -1, -1):
                if obstacleGrid[i][j] == 0:
                    dp[i][j] = dp[i + 1][j] + dp[i][j + 1]

        print(dp)
        return dp[0][0]


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        # ! Don't forget this special case
        # ! If destination is an obstacle, then we can never reach there
        if obstacleGrid[m - 1][n - 1] == 1:
            return 0

        dp = [0] * m
        # ! 注意, 这里一定要从后往前才可以
        for i in range(m - 1, -1, -1):
            # ! 一旦有障碍物, 那么之后的遍历就都有障碍物, 所以提早停止
            if obstacleGrid[i][-1] == 1:
                break
            dp[i] = 1

        for j in range(n - 2, -1, -1):
            # ! If last row has an obstacle,
            # ! then dp[-1] is forever 0 (continuosly blocked)
            if obstacleGrid[-1][j] == 1:
                dp[-1] = 0
            for i in range(m - 2, -1, -1):
                if obstacleGrid[i][j] == 1:
                    # ! 若当前格子里有障碍物, 那么此路必定不通, 所以为 0
                    dp[i] = 0
                else:
                    """
                    若当前格子没有障碍物, 那么我们通过 previous dp[i] 和 previous dp[i+1]
                    来计算当前 dp[i]
                    """
                    dp[i] += dp[i + 1]
        return dp[0]


s = Solution()
obstacleGrid = [[0, 1, 0, 0]]
result = s.uniquePathsWithObstacles(obstacleGrid)
print(result)
