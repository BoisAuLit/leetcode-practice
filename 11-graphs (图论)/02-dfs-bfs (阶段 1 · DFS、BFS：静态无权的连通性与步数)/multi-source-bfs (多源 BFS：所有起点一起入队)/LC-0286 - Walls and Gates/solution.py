"""LC-0286 - Walls and Gates

阶段 1 · 多源 BFS（所有起点一起入队） ○ 核心题
题目在问：每个空房间（INF）到最近的门（0）有几步，墙是 -1；答案原地写回 grid
点是什么：一个格子   边是什么：四方向相邻、不是墙
和签名题比改了哪一行：994 的"所有烂橘子一起入队"换成"所有门一起入队"；格子里的 INF 本身就是 visited，
    扩到谁就把 grid[x][y] + 1 写进去，层数 = 距离，不用另开 dist 数组（和 542 一模一样）
签名：LeetCode 叫 wallsAndGates(rooms)，NeetCode 叫 islandsAndTreasure(grid)，本文件沿用 NeetCode 的名字
"""
from typing import List
from collections import deque
import sys  # Solution 2 的递归 DFS 要抬递归上限


##################################################################################################
##### ! Solution 1: 多源 BFS，所有门一起入队
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)  队列
##### ! 适用：多个起点、无权、求"到最近起点的距离"；每格只进队一次，先到的一定最近
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        m = len(grid)
        n = len(grid[0])

        INF = 2**31 - 1

        q = deque([(x, y) for x in range(m) for y in range(n) if grid[x][y] == 0])

        while q:
            x, y = q.popleft()

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == INF:
                    grid[nx][ny] = grid[x][y] + 1
                    q.append((nx, ny))


##################################################################################################
##### ! Solution 2: 从每个门出发递归 DFS，带距离剪枝（对照用，不推荐）
##### ! 时间复杂度: 最坏远超 O(m · n)，同一格可能被更短的路反复刷小   空间复杂度: O(m · n)  递归栈
##### ! 适用：只为看清"为什么多源 BFS 比逐个起点 DFS 好"：DFS 先到的不一定最近，必须允许回头改小
##################################################################################################


class Solution_2:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        m, n = len(grid), len(grid[0])
        # ! 递归深度最坏 = 格子总数（蛇形走完整张图），默认 1000 不够，手动抬高
        sys.setrecursionlimit(max(sys.getrecursionlimit(), m * n + 100))

        def dfs(x: int, y: int, d: int) -> None:
            # ! 剪枝：越界 / 墙 -1 / 门 0 / 已经有不比 d 大的距离 → 都不进去
            if not (0 <= x < m and 0 <= y < n) or grid[x][y] <= d:
                return
            grid[x][y] = d  # ! 先到的不一定最近：这一步可能是在"改小"之前写过的值
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(x + dx, y + dy, d + 1)

        for x in range(m):
            for y in range(n):
                if grid[x][y] == 0:  # ! 门本身是 0，<= 0 会被剪掉，所以从它的四个邻居以 d = 1 起步
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        dfs(x + dx, y + dy, 1)


s = Solution()
input_ = [
    [2147483647, -1, 0, 2147483647],
    [2147483647, 2147483647, 2147483647, -1],
    [2147483647, -1, 2147483647, -1],
    [0, -1, 2147483647, 2147483647],
]
result = s.islandsAndTreasure(input_)
print(result)
