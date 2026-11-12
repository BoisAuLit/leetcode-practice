"""LC-0778 - Swim in Rising Water

阶段 4 · Dijkstra 家族变体：minimax（最小化路径上的最大值）
题目在问：水位 t 时刻为 t，能踩的格子是 elevation <= t；从左上游到右下角最早是哪一刻
      = 所有路径里，让"路径上的最大 elevation"最小的那条路径，它的最大值就是答案
点是什么：格子 (r, c)   边是什么：上下左右；这题的权在点上（格子的 elevation），不在边上
和签名题比改了哪一行：743 的 relax 是 d + w（总和），这里改成 max(d, grid[nr][nc])（一路上的最大值），
      堆还是小根堆 —— 这就是 minimax。反过来取 min + 大根堆就是 maximin（1102、2812）

三件套（minimax / maximin 的题都是这三个解法）：
  1. Dijkstra 把 relax 改成 max            O(N^2 log N)
  2. 二分答案 t + 只踩 <= t 的格子做 BFS    O(N^2 log N)
  3. 按 elevation 从小到大加格子的并查集    O(N^2 α)  ← 渐进最快

坑：
  - 答案至少是 max(grid[0][0], grid[N-1][N-1])，起点自己的高度也要算进去（二分的 lo 别从 0 开始）
  - 堆里存的是"格子自己的 elevation"，所以弹出来之后要 ans = max(ans, d) 攒着；
    不能直接 return d —— d 只是最后一格的高度，不是整条路的最大值
  - 约束说 grid 是 0..N^2-1 的一个排列，所以解法 3 可以用 elevation 当下标，连排序都省了
"""

import heapq  # ! 原来写的是 from collections import heapq —— heapq 是独立模块，不在 collections 里，会 ImportError
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


##################################################################################################
##### ! Solution 1: Dijkstra minimax (relax 改成 max)
##### ! 时间复杂度: O(N^2 log N)   空间复杂度: O(N^2)
##### ! 适用：minimax / maximin 路径的标准写法，一遍扫完就出答案，不用二分也不用排序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1(object):
    def swimInWater(self, grid):
        N = len(grid)

        seen = {(0, 0)}
        pq = [(grid[0][0], 0, 0)]
        ans = 0
        while pq:
            d, r, c = heapq.heappop(pq)
            ans = max(ans, d)
            if r == c == N-1: return ans
            for cr, cc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
                if 0 <= cr < N and 0 <= cc < N and (cr, cc) not in seen:
                    heapq.heappush(pq, (grid[cr][cc], cr, cc))
                    seen.add((cr, cc))


##################################################################################################
##### ! Solution 2: Binary search on t + BFS
##### ! 时间复杂度: O(N^2 log N)   空间复杂度: O(N^2)
##### ! 适用："t 行则 t+1 也行"的单调性题都能二分；每次只踩 <= t 的格子做一遍普通 BFS
##################################################################################################


class Solution_2:
    def swimInWater(self, grid: List[List[int]]) -> int:
        N = len(grid)

        def can(t: int) -> bool:  # ! 水位 t 时，只踩 elevation <= t 的格子，能不能到右下角
            if grid[0][0] > t:
                return False
            seen = [[False] * N for _ in range(N)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == c == N - 1:
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N and not seen[nr][nc] and grid[nr][nc] <= t:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        # ! lo 从 max(起点, 终点) 开始：这两格非踩不可；hi = N*N-1 一定可行（所有格子都能踩）
        lo, hi = max(grid[0][0], grid[N - 1][N - 1]), N * N - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 3: Union-Find, 按 elevation 从小到大加格子（Kruskal 过程，不要树）
##### ! 时间复杂度: O(N^2 α(N^2))   空间复杂度: O(N^2)
##### ! 适用：★ 渐进最快的解法（没有 log）；"第一次连通时的那一刻"就是答案，MST 瓶颈边的同一个思想
##################################################################################################


class UnionFind:  # ! 和 1135 的模板一个字都不改：路径减半 + 按 size 合并
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution_3:
    def swimInWater(self, grid: List[List[int]]) -> int:
        N = len(grid)
        # ! grid 是 0..N^2-1 的排列，所以 where[e] = 高度为 e 的那个格子，直接按下标取，不用排序
        where = [(0, 0)] * (N * N)
        for r in range(N):
            for c in range(N):
                where[grid[r][c]] = (r, c)

        uf = UnionFind(N * N)
        added = [[False] * N for _ in range(N)]
        for t in range(N * N):  # ! t 就是水位：把高度正好是 t 的那格放进来
            r, c = where[t]
            added[r][c] = True
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N and added[nr][nc]:
                    uf.union(r * N + c, nr * N + nc)
            if added[0][0] and uf.find(0) == uf.find(N * N - 1):
                return t  # ! 起点和终点第一次连通，这一刻的水位就是答案
        return N * N - 1


if __name__ == "__main__":
    cases = [
        ([[0, 2], [1, 3]], 3),
        ([[0, 1, 2, 3, 4],
          [24, 23, 22, 21, 5],
          [12, 13, 14, 15, 16],
          [11, 17, 18, 19, 20],
          [10, 9, 8, 7, 6]], 16),
        ([[0]], 0),
        ([[3, 2], [0, 1]], 3),  # ! 起点就是最高点：答案被起点自己卡住
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for grid, want in cases:
            got = sol.swimInWater([row[:] for row in grid])
            assert got == want, f"{type(sol).__name__} {grid}: got {got}, want {want}"
    print("3 个解法全过")
