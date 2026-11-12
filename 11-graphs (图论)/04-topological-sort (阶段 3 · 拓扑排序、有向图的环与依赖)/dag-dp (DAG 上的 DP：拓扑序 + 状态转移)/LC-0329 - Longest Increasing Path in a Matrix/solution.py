"""NC - Longest Increasing Path in Matrix (= LC-0329)

阶段 3 · 拓扑排序 · DAG 上的 DP（拓扑序 + 状态转移）○ 核心
题目在问：网格里最长的严格递增路径有几个格子（只能上下左右走）
点是什么：一个格子   边是什么：相邻且严格变大 a -> b（b > a），天然无环，网格就是 DAG
和签名题比改了哪一行：记忆化 DFS 就是 DAG 上的 DP；Kahn 版把 207 的"入度"换成"出度"（出度 0 = 路径终点），按层剥，层数就是答案
"""
from typing import List
from functools import lru_cache
from collections import deque


##################################################################################################
##### ! Solution 1: 记忆化 DFS（DAG 上的 DP：dp(x, y) = 从 (x, y) 出发最长能走几格）
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)   每格只算一次，各看 4 个邻居
##### ! 适用：面试首选、最短；递归深度最坏 = m · n（4e4），LeetCode 已调高上限
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution（三种都是 O(mn)，并列时选最常考、最短的这个）
##################################################################################################


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


##################################################################################################
##### ! Solution 2: 按值从大到小排序后 DP（排序就是一种拓扑序）
##### ! 时间复杂度: O(m · n · log(m · n))   空间复杂度: O(m · n)
##### ! 适用：想完全不递归；值大的先算，读邻居时它一定已经算好
##################################################################################################


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


##################################################################################################
##### ! Solution 3: Kahn 按出度剥层（出度 0 的格子 = 递增路径的终点，先剥）
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)
##### ! 适用：不递归、不排序；剥了几层答案就是几；和 1136 一模一样，只是入度换成出度
##################################################################################################


class Solution_3:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))

        # ! 出度 = 周围有几个更大的格子；出度 0 就是递增路径的终点
        outdeg = [[0] * n for _ in range(m)]
        for x in range(m):
            for y in range(n):
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] > matrix[x][y]:
                        outdeg[x][y] += 1

        q = deque((x, y) for x in range(m) for y in range(n) if outdeg[x][y] == 0)
        layers = 0
        while q:
            layers += 1  # ! 剥一层：这一层每个格子出发的最长路径长度都 = layers
            for _ in range(len(q)):
                x, y = q.popleft()
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    # ! 反着走：邻居比我小，说明它有一条边指向我；我被剥了，它出度减 1
                    if 0 <= nx < m and 0 <= ny < n and matrix[nx][ny] < matrix[x][y]:
                        outdeg[nx][ny] -= 1
                        if outdeg[nx][ny] == 0:
                            q.append((nx, ny))
        return layers


s = Solution_2_Iterative()
matrix = [[5, 5, 3], [2, 3, 6], [1, 1, 1]]
matrix = [[1, 2, 3], [2, 1, 4], [7, 6, 5]]
result = s.longestIncreasingPath(matrix)
print(result)
