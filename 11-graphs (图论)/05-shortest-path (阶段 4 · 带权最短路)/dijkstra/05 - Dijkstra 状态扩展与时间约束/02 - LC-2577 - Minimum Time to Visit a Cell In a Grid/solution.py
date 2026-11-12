"""LC-2577 - Minimum Time to Visit a Cell In a Grid

阶段 4 · Dijkstra + 状态扩展 △ 扩展
题目在问：从左上走到右下最早什么时候能到；每格有最早可进入时刻 grid[r][c]，走一步 1 秒，可以来回踱步等待
点是什么：格子 (r, c)，状态是 (到达时刻, r, c)   边是什么：上下左右，权 1，但到达时刻要抬到 grid[nr][nc] 并对齐奇偶
和签名题比改了哪一行：743 的 relax 是 d + w；这里是 max(t + 1, grid[nr][nc] + 奇偶修正)，另加一个开局卡死判定
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Dijkstra with parity-adjusted waiting
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：到达时刻单调不减、边权非负但依赖"当前时刻"的最短路；只有这一种标准写法，
##### ! 区别只在奇偶修正怎么写（暴力按时刻 BFS 只用来做验证，mn · maxT 太大）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumTime(self, grid: List[List[int]]) -> int:
        # ! 开局卡死：t=0 站在 (0,0)，t=1 只能进 (0,1) 或 (1,0)；两个都进不去就永远走不出去（连踱步的地方都没有）
        if grid[0][1] > 1 and grid[1][0] > 1:
            return -1
        m, n = len(grid), len(grid[0])

        # ! 等待靠踱步：只要走出过第一步，就能在"当前格 <-> 上一格"之间来回走（上一格的门槛早就过了）
        # ! 所以从时刻 t 的 (r,c) 出发，到邻居的时刻只能是 t+1, t+3, t+5 ...，奇偶性是锁死的
        # ! 邻居门槛 g：若 t+1 >= g 直接进；否则抬到 g，g 和 t+1 奇偶不同就再多等 1 秒
        dist = [[inf] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # (到达时刻, r, c)
        while heap:
            t, r, c = heappop(heap)
            if r == m - 1 and c == n - 1:
                return t
            if t > dist[r][c]:  # 作废票
                continue
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n:
                    g = grid[nr][nc]
                    nt = t + 1
                    if nt < g:  # ! 来早了：抬到 g，再按奇偶补 1；(g - nt) % 2 就是"奇偶不同"的 0/1
                        nt = g + (g - nt) % 2
                    if nt < dist[nr][nc]:
                        dist[nr][nc] = nt
                        heappush(heap, (nt, nr, nc))
        return -1  # 题目保证 m, n >= 2，过了开局判定就一定能到，这行只是兜底


s = Solution_1()
grid = [[0, 1, 3, 2], [5, 1, 2, 5], [4, 3, 8, 6]]
result = s.minimumTime(grid)
print(result)  # 7

grid = [[0, 2, 4], [3, 2, 1], [1, 0, 4]]
result = s.minimumTime(grid)
print(result)  # -1
