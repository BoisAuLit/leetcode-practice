"""
📌 信号→模式: 矩阵最长递增路径 → 严格递增保证 DAG，记忆化 DFS；迭代版按值降序填表
📅 首次: 2026-09-05 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
from functools import lru_cache


class Solution_1_Recursive:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])

        @lru_cache(maxsize=None)
        def dp(x: int, y: int) -> int:
            res = 1
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] > matrix[x][y]:
                    res = max(res, 1 + dp(nx, ny))
            return res

        return max(dp(x, y) for x in range(m) for y in range(n))


class Solution_2_Iterative:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dp = [[1] * n for _ in range(m)]  # 第1+2步：每格至少是自己，全 1

        cells = sorted(  # 第4步：生成计算顺序
            ((matrix[x][y], x, y) for x in range(m) for y in range(n)),
            reverse=True,  # 值从大到小
        )

        for val, x, y in cells:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] > val:
                    dp[x][y] = max(dp[x][y], 1 + dp[nx][ny])  # 第3步：读的邻居值更大，必已算好

        return max(max(row) for row in dp)


s = Solution_2_Iterative()
matrix = [[5, 5, 3], [2, 3, 6], [1, 1, 1]]
matrix = [[1, 2, 3], [2, 1, 4], [7, 6, 5]]
result = s.longestIncreasingPath(matrix)
print(result)
