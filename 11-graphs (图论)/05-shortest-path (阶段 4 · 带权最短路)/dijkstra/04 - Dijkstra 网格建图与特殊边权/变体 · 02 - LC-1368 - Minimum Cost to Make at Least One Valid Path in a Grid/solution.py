"""LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid

Level 1 · 04 网格建图与特殊边权 —— 方向决定 0/1 权
题目在问：每格有个箭头（1 右 2 左 3 下 4 上），改一格的箭头花 1；最少花多少能让 (0,0) 顺着箭头走到 (m-1,n-1)
点是什么：格子 (r, c)   边是什么：四个方向都能走，顺着箭头走权 0，逆着箭头走权 1（= 改这一格）
和签名题 743 比改了哪一行：一行都没改。关键是看懂"改箭头"等价于"付 1 块钱走一条本来不存在的边"，
      于是一道看起来像 DP / BFS 的题变成了最普通的 0/1 权最短路

坑：
  - 箭头编号是 1..4，不是 0..3；DIRS 前面补一个占位或者整体减一，错一位全盘皆错
  - 代价记在"离开的格子"上（改的是当前格的箭头），不是进入的格子 —— 和 2290 正好相反
  - 一格只改一次就够：改成哪个方向都是 1 块钱，所以四条出边里恰好一条权 0、三条权 1
"""

from collections import deque
from heapq import heappop, heappush
from typing import List

# ! 下标 1..4 对应题目的 右 左 下 上；0 号位占位，省得到处 -1
DIRS = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]


##################################################################################################
##### ! Solution 1: 标准 Dijkstra（堆），顺箭头权 0 逆箭头权 1
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：复用 743 模板；面试里先说这个，再说 0-1 BFS 更快，是最稳的回答顺序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
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


##################################################################################################
##### ! Solution 2: 0-1 BFS（双端队列）
##### ! 时间复杂度: O(mn)   空间复杂度: O(mn)
##### ! 适用：★ 渐进更快（没有 log）；和 2290 一模一样的双端队列，0 放队头 1 放队尾
##################################################################################################


class Solution_2:
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


if __name__ == "__main__":
    cases = [
        ([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]], 3),
        ([[1, 1, 3], [3, 2, 2], [1, 1, 4]], 0),
        ([[1, 2], [4, 3]], 1),
        ([[4]], 0),
    ]
    for sol in (Solution_1(), Solution_2()):
        for grid, want in cases:
            got = sol.minCost([row[:] for row in grid])
            assert got == want, f"{type(sol).__name__} {grid}: got {got}, want {want}"
    print("2 个解法全过")
