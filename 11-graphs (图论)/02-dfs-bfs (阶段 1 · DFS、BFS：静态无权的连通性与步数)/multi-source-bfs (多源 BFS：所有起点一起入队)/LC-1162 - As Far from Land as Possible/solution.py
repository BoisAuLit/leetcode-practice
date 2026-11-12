"""LC-1162 - As Far from Land as Possible

阶段 1 · 多源 BFS(所有起点一起入队) ○ 核心变体
题目在问：n x n 网格 1 是陆地 0 是海，找离最近陆地最远的那个海洋格，返回这个曼哈顿距离；全陆或全海返回 -1
点是什么：一个格子   边是什么：上下左右相邻(每走一步距离 +1，正好就是曼哈顿距离)
和签名题比改了哪一行：994 把所有烂橘子一起入队，层数 = 分钟数；
    本题把所有陆地一起入队，BFS 一层层往外扩，最后一层的层号就是答案(最远的海洋格一定在最后一层)。
    542 要每个格子的距离，本题只要最大值，所以不用 dist 数组，数层数就够。
"""
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

##################################################################################################
##### ! Solution 1: 多源 BFS，按层扩，答案 = 最后一层的层号
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)  (队列)
##### ! 适用：994 / 542 的多源模板，"最远 = 最后一层"
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxDistance(self, grid: List[List[int]]) -> int:
        n = len(grid)
        queue = deque((r, c) for r in range(n) for c in range(n) if grid[r][c] == 1)  # ! 多源：所有陆地一起入队
        if len(queue) == 0 or len(queue) == n * n:
            return -1  # ! 全海 / 全陆

        level = -1  # 陆地那层算第 0 层，所以从 -1 起数
        while queue:
            level += 1
            for _ in range(len(queue)):  # ! 按层弹：弹完一整层，level 才 +1
                r, c = queue.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                        grid[nr][nc] = 1  # ! 标记已访问：海变陆
                        queue.append((nr, nc))
        return level  # ! 最后一层弹完 queue 空了，此时 level 就是最远距离


##################################################################################################
##### ! Solution 2: 两遍 DP(左上扫一遍、右下扫一遍)
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)  (dist 数组)
##### ! 适用：曼哈顿距离的经典 DP 替代，不用队列；542 也能这么写
##################################################################################################


class Solution_2:
    def maxDistance(self, grid: List[List[int]]) -> int:
        n = len(grid)
        INF = 10**9
        dist = [[0 if grid[r][c] == 1 else INF for c in range(n)] for r in range(n)]  # ! 陆地 0，海 INF

        # ! 第一遍：左上 → 右下，只看上、左两个方向的邻居
        for r in range(n):
            for c in range(n):
                if r > 0:
                    dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1)
                if c > 0:
                    dist[r][c] = min(dist[r][c], dist[r][c - 1] + 1)

        # ! 第二遍：右下 → 左上，只看下、右两个方向的邻居；两遍合起来覆盖所有曼哈顿路径
        for r in range(n - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                if r < n - 1:
                    dist[r][c] = min(dist[r][c], dist[r + 1][c] + 1)
                if c < n - 1:
                    dist[r][c] = min(dist[r][c], dist[r][c + 1] + 1)

        best = max(max(row) for row in dist)
        return -1 if best == 0 or best >= INF else best  # ! 0 = 全陆，INF = 全海


s = Solution_1()
grid = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
result = s.maxDistance(grid)
print(result)  # 2
