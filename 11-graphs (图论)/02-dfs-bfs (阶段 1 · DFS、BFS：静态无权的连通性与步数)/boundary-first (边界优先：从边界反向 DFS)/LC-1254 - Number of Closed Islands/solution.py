"""LC-1254 - Number of Closed Islands

阶段 1 · 边界优先(从边界反向 DFS) ○ 核心变体
题目在问：0 是陆地、1 是水，四周全被水围住(不碰网格边界)的岛有几个
点是什么：一个格子   边是什么：上下左右相邻且同为 0
和签名题比改了哪一行：417 从海岸线反向 DFS 标记"能流到海的格子"；
    本题同样先从四条边上的 0 出发，把"碰到边界的岛"整个淹成 1，剩下的 0 再按 200 数岛就是答案。
    注意本题 0 是陆地、1 是水，和 200 反过来。
"""
import sys
from collections import deque
from typing import List

sys.setrecursionlimit(10**5)  # ! 网格最多 100x100 = 1e4 格，蛇形岛递归深度能到 1e4，Solution_1/2 需要放开

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

##################################################################################################
##### ! Solution 1: 边界优先 DFS 淹掉，再数岛
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)  (递归栈)
##### ! 适用：417/130 同款套路，两步分开写最不容易错
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def closedIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def flood(r: int, c: int) -> None:
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != 0:
                return
            grid[r][c] = 1  # ! 淹掉：陆地改成水，兼当 visited
            for dr, dc in DIRS:
                flood(r + dr, c + dc)

        # ! 第一步：边界优先，四条边上的 0 全淹掉(它们所在的岛一定不 closed)
        for r in range(m):
            flood(r, 0)
            flood(r, n - 1)
        for c in range(n):
            flood(0, c)
            flood(m - 1, c)

        # ! 第二步：剩下的 0 全是 closed island，按 200 数岛
        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    count += 1
                    flood(r, c)
        return count


##################################################################################################
##### ! Solution 2: 一遍 DFS，返回"这座岛有没有碰到边界"
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)
##### ! 适用：想一次遍历搞定时；坑在于不能用 and 短路，必须把整座岛走完
##################################################################################################


class Solution_2:
    def closedIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(r: int, c: int) -> bool:
            if r < 0 or r >= m or c < 0 or c >= n:
                return False  # ! 走出了网格 = 这座岛碰到了边界
            if grid[r][c] == 1:
                return True
            grid[r][c] = 1
            closed = True
            for dr, dc in DIRS:
                closed &= dfs(r + dr, c + dc)  # ! 用 &= 不用 and：四个方向都要走完，不能短路
            return closed

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0 and dfs(r, c):
                    count += 1
        return count


##################################################################################################
##### ! Solution 3: 边界优先 + BFS(无递归)
##### ! 时间复杂度: O(m · n)   空间复杂度: O(m · n)  (队列)
##### ! 适用：网格很大、不想碰递归深度时；逻辑和 Solution 1 完全一样
##################################################################################################


class Solution_3:
    def closedIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def flood(sr: int, sc: int) -> None:
            if grid[sr][sc] != 0:
                return
            grid[sr][sc] = 1
            queue = deque([(sr, sc)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0:
                        grid[nr][nc] = 1
                        queue.append((nr, nc))

        for r in range(m):
            flood(r, 0)
            flood(r, n - 1)
        for c in range(n):
            flood(0, c)
            flood(m - 1, c)

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    count += 1
                    flood(r, c)
        return count


s = Solution_1()
grid = [
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0],
]
result = s.closedIsland(grid)
print(result)  # 2
