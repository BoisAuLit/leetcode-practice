"""LC-0130 - Surrounded Regions

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 边界优先（从边界反向 DFS）○ 核心
题目在问：被 X 四面包围的 O 全部改成 X；碰到边界的 O 连通块不算被包围
点是什么：一个格子   边是什么：上下左右相邻的 O
和签名题比改了哪一行：和 417 一样从边界反向出发，但只有一条海岸（四条边）；标记到的 O 是安全的，没标到的 O 改 X
"""
# https://leetcode.com/problems/surrounded-regions/
# https://neetcode.io/problems/surrounded-regions/question?list=neetcode150

from collections import deque


##################################################################################################
##### ! Solution 1: 从边界 O 出发 BFS 反向标记
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：四条边上的 O 一起入队（多源 BFS），不怕递归深度
##################################################################################################


class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        q = deque()
        # 1. 把边界上的 O 全部入队并标记为 #
        for i in range(m):
            for j in range(n):
                if (i in (0, m - 1) or j in (0, n - 1)) and board[i][j] == "O":
                    board[i][j] = "#"
                    q.append((i, j))
        # 2. 从边界 O 出发,把所有连通的 O 都标成 #(这些是"安全"的)
        while q:
            i, j = q.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] == "O":
                    board[ni][nj] = "#"
                    q.append((ni, nj))
        # 3. 剩下的 O 都是被包围的 → X;# 还原成 O
        for i in range(m):
            for j in range(n):
                board[i][j] = "O" if board[i][j] == "#" else "X"




s = Solution()
# fmt: off
board = [
    ["X","X","X","X"],
    ["X","O","O","X"],
    ["X","X","O","X"],
    ["X","O","X","X"]
]
# fmt:on
s.solve(board)
for i in range(len(board)):
    print(board[i])
