"""LC-2290 - Minimum Obstacle Removal to Reach Corner

阶段 4 · 0-1 BFS (双端队列，0 放队头 1 放队尾) ○ 核心题
题目在问：0 是空地 1 是障碍，可以把障碍拆掉，从左上走到右下(四方向)最少拆几个
点是什么：一个格子   边是什么：上下左右走一步，进入空地权 0，进入障碍权 1 (拆它)
和签名题比改了哪一行：743 的堆换成 deque，边权就是目标格的 grid 值 (0 或 1)：0 放队头、1 放队尾
"""
from collections import deque
from heapq import heappop, heappush
from math import inf
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

##################################################################################################
##### ! Solution 1: 0-1 BFS (deque，进空地放队头，进障碍放队尾)
##### ! 时间复杂度: O(mn)   空间复杂度: O(mn)
##### ! 适用：边权只有 0 / 1 的最短路，比 Dijkstra 少一个 log，是这题的标准解
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0  # 题目保证左上角是 0
        dq = deque([(0, 0)])

        while dq:
            r, c = dq.popleft()
            d = dist[r][c]  # 弹出时读当前最好的 dist
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    w = grid[nr][nc]  # ! 边权就是目标格的值：空地 0、障碍 1
                    if d + w < dist[nr][nc]:
                        dist[nr][nc] = d + w
                        if w == 0:
                            dq.appendleft((nr, nc))  # ! 0 放队头
                        else:
                            dq.append((nr, nc))  # ! 1 放队尾

        return dist[m - 1][n - 1]


##################################################################################################
##### ! Solution 2: Dijkstra (743 原样，边权 0 / 1)
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：通用写法；0-1 BFS 就是把这里的堆换成了双端队列
##################################################################################################


class Solution_2:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # (拆掉的障碍数, r, c)

        while heap:
            d, r, c = heappop(heap)
            if (r, c) == (m - 1, n - 1):
                return d
            if d > dist[r][c]:  # 作废票
                continue
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nd = d + grid[nr][nc]  # ! relax 写 d + w，w 是目标格的值
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heappush(heap, (nd, nr, nc))

        return -1  # 总能到右下角 (大不了全拆)，不会走到这里


s = Solution_1()
grid = [[0, 1, 1], [1, 1, 0], [1, 1, 0]]
result = s.minimumObstacles(grid)
print(result)  # 2

grid = [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]]
result = s.minimumObstacles(grid)
print(result)  # 0


##################################################################################################
##### ! Solution Alt: Dijkstra（优先队列）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-2290 - Minimum Obstacle Removal to Reach Corner
##### ! 变体目录　：dijkstra/04 - Dijkstra 网格建图与特殊边权/变体 · 01 - LC-2290 - Minimum Obstacle Removal to Reach Corner
##### ! 为什么这样定主次：同 LC-1368：边权 0/1 ⟹ 0-1 BFS 最优
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from collections import deque


from heapq import heappop, heappush


from typing import List


class Solution_1_Alt:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]
        while heap:
            d, r, c = heappop(heap)
            if r == m - 1 and c == n - 1:
                return d  # ! 第一次弹到终点就是答案
            if d > dist[r][c]:
                continue
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nd = d + grid[nr][nc]  # ! relax 还是 d + w，w = 进入这格要不要拆障碍
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heappush(heap, (nd, nr, nc))
        return dist[m - 1][n - 1]


class Solution_2_Alt:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0)])
        while dq:
            r, c = dq.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    w = grid[nr][nc]
                    if dist[r][c] + w < dist[nr][nc]:
                        dist[nr][nc] = dist[r][c] + w
                        # ! 0 权走队头、1 权走队尾 —— 队列里的距离就始终是非降的，等价于堆
                        (dq.appendleft if w == 0 else dq.append)((nr, nc))
        return dist[m - 1][n - 1]
