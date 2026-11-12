"""LC-1293 - Shortest Path in a Grid with Obstacles Elimination

阶段 0 · 状态图 BFS（一个状态就是一个点）
题目在问：网格里从左上走到右下，最多可以**清除 k 个障碍**，求最少步数。

点是什么：**`(行, 列, 已用掉的清除次数)`** —— 不是单纯的 `(行, 列)`。
边是什么：四方向走一步；踩到障碍就多消耗一次清除额度。

决定性观察（这题的全部）：
  1. 如果状态只是 `(r, c)`，就会出错：**同一个格子，带着不同的剩余额度，后续能力完全不同**。
     「用了 3 次清除到达 (r,c)」和「用了 0 次到达 (r,c)」不是同一个状态 ——
     后者显然更有前途。所以必须把**剩余资源压进状态**。
  2. 压进状态之后，每条边的代价又变成 1（走一步就是一步），
     所以**普通 BFS 就够了，不需要 Dijkstra**。这是本题最关键的判断。
  3. visited 也必须按**三元组**去重：`visited[r][c][used]`，
     或者更省的做法 —— 对每个格子只记「到达它时用过的最少次数」，
     新路径的 used 不小于它就剪掉（见 Solution_2）。

和签名题 LC-0752 Open the Lock 的关系：
      两题都是「把一个复合状态当成图上的点」。
      752 的状态是 4 位锁的字符串，本题的状态是 `(r, c, used)`。
      **一旦状态定对了，剩下就是裸 BFS。**

**什么时候可以不做 BFS 直接返回**：
      如果 `k >= rows + cols - 2`，那么清除额度足够多到可以直接走曼哈顿最短路
      ⟹ 直接返回 `rows + cols - 2`。这个剪枝在 k 很大时能省掉整个搜索。

复杂度：状态数 O(rows · cols · (k+1))，每个状态常数条边
      ⟹ **O(rows · cols · k)** 时间和空间。

边界：
  - 起点或终点本身是障碍（题目保证不是，但 1×1 网格要能处理）
  - k = 0（退化成普通网格 BFS）
  - k 足够大（走直线）
  - 无论如何都走不到 → 返回 -1
  - 1×1 网格 → 0 步
"""

from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: 状态 = (r, c, used)，三维 visited，裸 BFS
##### ! 时间复杂度: O(rows · cols · k)   空间复杂度: O(rows · cols · k)
##### ! 适用：所有「带一个可消耗资源的最短路」；资源压进状态后边权恢复成 1 ⟹ BFS 就够
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        rows, cols = len(grid), len(grid[0])
        if rows == 1 and cols == 1:
            return 0
        # ! 额度足够走曼哈顿直线，直接返回
        if k >= rows + cols - 2:
            return rows + cols - 2
        # ! visited[r][c][used]：同一个格子带不同额度是不同状态
        visited = [[[False] * (k + 1) for _ in range(cols)] for _ in range(rows)]
        start_used = grid[0][0]
        if start_used > k:
            return -1
        visited[0][0][start_used] = True
        q = deque([(0, 0, start_used)])
        steps = 0
        while q:
            steps += 1
            for _ in range(len(q)):                 # ! 按层推进，层数 = 步数
                r, c, used = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        continue
                    nu = used + grid[nr][nc]        # ! 踩到障碍就多花一次额度
                    if nu > k or visited[nr][nc][nu]:
                        continue
                    if nr == rows - 1 and nc == cols - 1:
                        return steps
                    visited[nr][nc][nu] = True
                    q.append((nr, nc, nu))
        return -1


##################################################################################################
##### ! Solution 2: 用「到达每个格子时用过的最少次数」剪枝（空间从 O(rck) 降到 O(rc)）
##### ! 时间复杂度: O(rows · cols · k)   空间复杂度: O(rows · cols)
##### ! 适用：同一个格子如果之前用更少额度到过，这次就没前途；是上面三维 visited 的压缩版
##################################################################################################


class Solution_2:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        rows, cols = len(grid), len(grid[0])
        if k >= rows + cols - 2:
            return rows + cols - 2
        INF = float("inf")
        best = [[INF] * cols for _ in range(rows)]   # ! 到达该格用过的最少清除次数
        if grid[0][0] > k:
            return -1
        best[0][0] = grid[0][0]
        q = deque([(0, 0, grid[0][0])])
        steps = 0
        while q:
            steps += 1
            for _ in range(len(q)):
                r, c, used = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        continue
                    nu = used + grid[nr][nc]
                    if nu > k or nu >= best[nr][nc]:   # ! 之前用更少（或相同）额度到过 ⟹ 剪掉
                        continue
                    if nr == rows - 1 and nc == cols - 1:
                        return steps
                    best[nr][nc] = nu
                    q.append((nr, nc, nu))
        return 0 if rows == 1 and cols == 1 else -1


if __name__ == "__main__":
    import random

    cases = [([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1, 6),
             ([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1, -1),
             ([[0]], 0, 0),
             ([[0, 0], [0, 0]], 0, 2),
             ([[0, 1], [1, 0]], 1, 2)]
    for grid, k, want in cases:
        a = Solution_1().shortestPath([r[:] for r in grid], k)
        b = Solution_2().shortestPath([r[:] for r in grid], k)
        assert a == want, (grid, k, a, want)
        assert b == want, (grid, k, b, want)
        print(f"k={k} -> {a}")

    # ! 暴力基准：对「状态 = (r, c, used)」做朴素 BFS（不剪枝），用来对拍
    def brute(grid, k):
        rows, cols = len(grid), len(grid[0])
        if grid[0][0] > k:
            return -1
        seen = {(0, 0, grid[0][0])}
        q = deque([(0, 0, grid[0][0], 0)])
        while q:
            r, c, u, d = q.popleft()
            if (r, c) == (rows - 1, cols - 1):
                return d
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nu = u + grid[nr][nc]
                    if nu <= k and (nr, nc, nu) not in seen:
                        seen.add((nr, nc, nu))
                        q.append((nr, nc, nu, d + 1))
        return -1

    for _ in range(600):
        R, C = random.randint(1, 4), random.randint(1, 4)
        grid = [[random.choice([0, 0, 1]) for _ in range(C)] for _ in range(R)]
        grid[0][0] = 0
        grid[R - 1][C - 1] = 0
        k = random.randint(0, 3)
        w = brute(grid, k)
        a = Solution_1().shortestPath([r[:] for r in grid], k)
        b = Solution_2().shortestPath([r[:] for r in grid], k)
        assert a == w, (grid, k, a, w)
        assert b == w, (grid, k, b, w)
    print("随机对拍 600 组通过 ✓（三维 visited 版 == 最少额度剪枝版 == 朴素状态 BFS）")
