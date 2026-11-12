"""LC-2290 - Minimum Obstacle Removal to Reach Corner

Level 1 · 04 网格建图与特殊边权 —— 0/1 权的网格最短路
题目在问：网格里 1 是障碍，从 (0,0) 走到 (m-1,n-1) 最少要移走几个障碍
点是什么：格子 (r, c)   边是什么：上下左右；进入一格的代价 = grid[nr][nc]（0 或 1）
和签名题 743 比改了哪一行：一行都没改，relax 还是 d + w，只是 w 只能是 0 或 1，
      而且图不是给出来的邻接表，是"网格隐式建图"：邻居靠四方向算，不用先建 adj

坑：
  - 代价在"进入的格子"上，不在边上；起点那格就算是障碍也不用移（题目保证 grid[0][0] = 0）
  - 权只有 0/1 时 0-1 BFS 用双端队列就能做到 O(mn)，比堆快一个 log；但模板要多记一个
  - dist 要开成二维数组，别用 set 当 visited：0 权边会让同一格以更低代价再次被更新
"""

from collections import deque
from heapq import heappop, heappush
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


##################################################################################################
##### ! Solution 1: 标准 Dijkstra（堆），权就是 grid 值
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：复用 743 的模板，不用额外记忆；网格题先想"点是格子、边是四方向"就套得上
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
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


##################################################################################################
##### ! Solution 2: 0-1 BFS（双端队列）
##### ! 时间复杂度: O(mn)   空间复杂度: O(mn)
##### ! 适用：★ 渐进更快（没有 log）；边权只有 0 和 1 时专用：0 放队头、1 放队尾，队列天然有序
##################################################################################################


class Solution_2:
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


if __name__ == "__main__":
    cases = [
        ([[0, 1, 1], [1, 1, 0], [1, 1, 0]], 2),
        ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0),
        ([[0]], 0),
        ([[0, 1, 1], [1, 1, 1], [1, 1, 0]], 3),   # 只能硬拆
    ]
    for sol in (Solution_1(), Solution_2()):
        for grid, want in cases:
            got = sol.minimumObstacles([row[:] for row in grid])
            assert got == want, f"{type(sol).__name__} {grid}: got {got}, want {want}"
    print("2 个解法全过")
