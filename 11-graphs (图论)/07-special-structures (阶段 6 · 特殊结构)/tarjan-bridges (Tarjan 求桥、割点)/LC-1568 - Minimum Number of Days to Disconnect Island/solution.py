"""LC-1568 - Minimum Number of Days to Disconnect Island

阶段 6 · 特殊结构 · Tarjan 求桥、割点 △ 扩展
题目在问：最少把几格陆地变成水，才能让网格不再"恰好 1 个岛"（0 个或 ≥ 2 个都算断开）
点是什么：一格陆地   边是什么：上下左右相邻的两格陆地
和签名题比改了哪一行：1192 找"桥"（删一条边就断），这里找"割点"（删一个格子就断）；
    而且答案只可能是 0 / 1 / 2：任何岛挑一个角落格，它最多 2 个陆地邻居，删掉这 2 个邻居它就孤立了
    特判：岛只有 1 格 → 删它变 0 个岛，1 天；只有 2 格 → 删 1 格还剩 1 个岛，要 2 天
"""
import sys
from typing import List

##################################################################################################
##### ! Solution 1: 数岛 + 枚举删一格再数岛
##### ! 时间复杂度: O((m·n)^2)   空间复杂度: O(m·n)
##### ! 适用：面试默认答案；网格最多 30x30，900 次数岛完全跑得动，不用写 Tarjan
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minDays(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def count_islands() -> int:  # ! 标准数岛（迭代 DFS），每次调用 O(m·n)
            seen = [[False] * n for _ in range(m)]
            count = 0
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 1 and not seen[i][j]:
                        count += 1
                        seen[i][j] = True
                        stack = [(i, j)]
                        while stack:
                            r, c = stack.pop()
                            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1 and not seen[nr][nc]:
                                    seen[nr][nc] = True
                                    stack.append((nr, nc))
            return count

        if count_islands() != 1:  # ! 本来就不是 1 个岛 → 0 天
            return 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0  # ! 试着删掉这一格
                    if count_islands() != 1:  # ! 变 0 个岛（它是唯一一格）或 ≥ 2 个岛 → 1 天
                        grid[i][j] = 1
                        return 1
                    grid[i][j] = 1  # ! 还原
        return 2  # ! 删一格都不行 → 删两格一定行


##################################################################################################
##### ! Solution 2: Tarjan 求割点
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：追求线性；有割点 → 1 天，没有 → 2 天；根的判法不同（≥ 2 个 DFS 孩子才算割点）
##################################################################################################


class Solution_2:
    def minDays(self, grid: List[List[int]]) -> int:
        sys.setrecursionlimit(10000)  # ! 最多 900 格，蛇形岛递归深度能到 900，默认 1000 太险
        m, n = len(grid), len(grid[0])
        land = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]
        if not land:
            return 0  # ! 0 个岛，本来就断开

        disc = [[-1] * n for _ in range(m)]
        low = [[0] * n for _ in range(m)]
        timer = 0
        has_cut = False

        def dfs(r: int, c: int, pr: int, pc: int) -> None:
            nonlocal timer, has_cut
            disc[r][c] = low[r][c] = timer
            timer += 1
            children = 0
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if not (0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1):
                    continue
                if (nr, nc) == (pr, pc):  # ! 不走回父边
                    continue
                if disc[nr][nc] == -1:  # ! 树边
                    children += 1
                    dfs(nr, nc, r, c)
                    low[r][c] = min(low[r][c], low[nr][nc])
                    if pr != -1 and low[nr][nc] >= disc[r][c]:  # ! 非根：孩子绕不到比我更早 → 我是割点（是 >=，桥是 >）
                        has_cut = True
                else:  # ! 回边
                    low[r][c] = min(low[r][c], disc[nr][nc])
            if pr == -1 and children >= 2:  # ! 根：有 ≥ 2 个 DFS 孩子才是割点
                has_cut = True

        dfs(land[0][0], land[0][1], -1, -1)
        if timer != len(land):  # ! 一次 DFS 没走遍所有陆地 → 本来就 ≥ 2 个岛
            return 0
        if len(land) <= 2:  # ! 1 格：删它就剩 0 个岛，1 天；2 格：删 1 格还是 1 个岛，2 天
            return len(land)
        return 1 if has_cut else 2


s = Solution_1()
grid = [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
result = s.minDays(grid)
print(result)  # 2

grid = [[1, 1]]
result = s.minDays(grid)
print(result)  # 2
