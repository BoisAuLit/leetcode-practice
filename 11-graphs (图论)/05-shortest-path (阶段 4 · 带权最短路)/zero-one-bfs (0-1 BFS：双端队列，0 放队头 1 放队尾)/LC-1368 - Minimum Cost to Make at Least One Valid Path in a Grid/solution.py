"""LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid

阶段 4 · 0-1 BFS (双端队列，0 放队头 1 放队尾) ○ 核心题
题目在问：每格有个默认箭头 (1 右 2 左 3 下 4 上)，顺着箭头走不花钱，改一格的箭头花 1，从左上走到右下最少花多少
点是什么：一个格子   边是什么：往四个方向各走一步，顺箭头的那条权 0，其他三条权 1
和签名题比改了哪一行：743 的堆换成 deque：边权只有 0 和 1，权 0 的邻居放队头、权 1 的放队尾，
  队列里的 dist 就始终不减，相当于免费的优先队列，省掉 log
"""
from collections import deque
from heapq import heappop, heappush
from math import inf
from typing import List

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))  # ! 下标 k 对应 grid 值 k + 1：1 右 2 左 3 下 4 上

##################################################################################################
##### ! Solution 1: 0-1 BFS (deque，0 放队头 1 放队尾)
##### ! 时间复杂度: O(mn)   空间复杂度: O(mn)
##### ! 适用：边权只有 0 / 1 的最短路，比 Dijkstra 少一个 log，是这题的标准解
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0)])

        while dq:
            r, c = dq.popleft()
            d = dist[r][c]  # 弹出时读当前最好的 dist (同一格可能在队列里出现多次，后弹的直接没法更新)
            for k, (dr, dc) in enumerate(DIRS, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    w = 0 if grid[r][c] == k else 1  # ! 顺着箭头走 0 元，否则改箭头 1 元
                    if d + w < dist[nr][nc]:
                        dist[nr][nc] = d + w
                        if w == 0:
                            dq.appendleft((nr, nc))  # ! 0 放队头：和队头一样近，马上处理
                        else:
                            dq.append((nr, nc))  # ! 1 放队尾：比队头远 1，排到后面

        return dist[m - 1][n - 1]


##################################################################################################
##### ! Solution 2: Dijkstra (743 原样，边权 0 / 1)
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：通用写法，不用记 deque 的技巧；0-1 BFS 就是把这里的堆换成了双端队列
##################################################################################################


class Solution_2:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # (花费, r, c)

        while heap:
            d, r, c = heappop(heap)
            if (r, c) == (m - 1, n - 1):
                return d
            if d > dist[r][c]:  # 作废票
                continue
            for k, (dr, dc) in enumerate(DIRS, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nd = d + (0 if grid[r][c] == k else 1)  # ! relax 写 d + w，w 是 0 或 1
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heappush(heap, (nd, nr, nc))

        return -1  # 网格总能到右下角 (最多每格都改一次)，不会走到这里


s = Solution_1()
grid = [[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]
result = s.minCost(grid)
print(result)  # 3

grid = [[1, 1, 3], [3, 2, 2], [1, 1, 4]]
result = s.minCost(grid)
print(result)  # 0

grid = [[1, 2], [4, 3]]
result = s.minCost(grid)
print(result)  # 1


##################################################################################################
##### ! Solution Alt: Dijkstra（优先队列）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid
##### ! 变体目录　：dijkstra/04 - Dijkstra 网格建图与特殊边权/变体 · 02 - LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid
##### ! 为什么这样定主次：边权只有 0/1 ⟹ 0-1 BFS 是 O(V+E) 的最优解法；Dijkstra 版多一个 log，作为对照保留
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from collections import deque


from heapq import heappop, heappush


from typing import List


class Solution_1_Alt:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]
        while heap:
            d, r, c = heappop(heap)
            if r == m - 1 and c == n - 1:
                return d
            if d > dist[r][c]:
                continue
            for k in range(1, 5):
                dr, dc = DIRS[k]
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nd = d + (0 if grid[r][c] == k else 1)  # ! 顺箭头免费，否则花 1 改箭头
                    if nd < dist[nr][nc]:
                        dist[nr][nc] = nd
                        heappush(heap, (nd, nr, nc))
        return dist[m - 1][n - 1]


class Solution_2_Alt:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0)])
        while dq:
            r, c = dq.popleft()
            for k in range(1, 5):
                dr, dc = DIRS[k]
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    w = 0 if grid[r][c] == k else 1
                    if dist[r][c] + w < dist[nr][nc]:
                        dist[nr][nc] = dist[r][c] + w
                        (dq.appendleft if w == 0 else dq.append)((nr, nc))
        return dist[m - 1][n - 1]
