"""LC-1631 - Path With Minimum Effort

Level 1 · 02 非加法路径代价变体 —— minimax（最小化路径上的最大值）
题目在问：从左上走到右下，一条路的"体力" = 相邻两格高度差的最大值；求体力最小的那条路
点是什么：格子 (r, c)   边是什么：上下左右，权 = |heights[r][c] - heights[nr][nc]|
和签名题 743 比改了哪一行：只改了 relax —— d + w 变成 max(d, w)。
      Greedy 框架、堆、dist、作废票全都不动，这就是"非加法代价"的全部含义

和同层三道题的区别（必须说得清）：
  - 1631 minimax：门槛在**边**上（高度差），relax = max(d, w)，小根堆
  - 0778 minimax：门槛在**格子**上（水位），relax = max(d, grid[nr][nc])，小根堆
  - 1514 乘法  ：代价沿路径**相乘**求最大，relax = d * w，大根堆（不是 minimax！）
  - 2812 maximin：先多源 BFS 算安全度，再 relax = min(d, safe)，大根堆

坑：
  - 起点的标签是 0（还没走过任何一条边），不是 heights[0][0]
  - 1x1 的网格答案是 0
  - "最小化最大值"的三件套：Dijkstra 改 relax / 二分答案 + BFS / 按边权排序的并查集
"""

import heapq  # ! 原来写的是 from collections import heapq —— heapq 是独立模块，不在 collections 里，会 ImportError
from collections import deque
from typing import List, Tuple


##################################################################################################
##### ! Solution 1: Dijkstra minimax（relax 改成 max）
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：minimax 的标准写法，一遍出答案；面试里先写这个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])
        visited = [[False] * n for _ in range(m)]

        # Each cell stores the max_height_diff along the optimal path
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # cost, x, y

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def get_neigbs(x: int, y: int) -> List[Tuple[int, int, int]]:
            prev_height_diff = dist[x][y]
            neigbs = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < m and 0 <= ny < n):
                    continue
                if visited[nx][ny]:
                    continue
                new_height_diff = abs(heights[nx][ny] - heights[x][y])
                neigbs.append((max(new_height_diff, prev_height_diff), nx, ny))
            return neigbs

        while heap:
            height_diff, x, y = heapq.heappop(heap)

            if dist[x][y] < height_diff:
                continue

            if x == m - 1 and y == n - 1:
                return height_diff

            visited[x][y] = True

            for new_height_diff, nx, ny in get_neigbs(x, y):
                if new_height_diff < dist[nx][ny]:
                    dist[nx][ny] = new_height_diff
                    heapq.heappush(heap, (new_height_diff, nx, ny))
        return -1


##################################################################################################
##### ! Solution 2: 二分体力值 + BFS 检查连通
##### ! 时间复杂度: O(mn log(max_diff))   空间复杂度: O(mn)
##### ! 适用："体力 e 能过，e+1 一定也能过"的单调性；值域小于格子数时比 Dijkstra 还快
##################################################################################################


class Solution_2:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])

        def can(limit: int) -> bool:  # ! 只走高度差 <= limit 的边，左上能不能到右下
            seen = [[False] * n for _ in range(m)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == m - 1 and c == n - 1:
                    return True
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and not seen[nr][nc]
                            and abs(heights[nr][nc] - heights[r][c]) <= limit):
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        lo, hi = 0, max(max(row) for row in heights) - min(min(row) for row in heights)
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 3: 按边权从小到大加边的并查集（Kruskal 过程，不要树）
##### ! 时间复杂度: O(mn log(mn))   空间复杂度: O(mn)
##### ! 适用：★ 离线 / 多次查询时最佳；"第一次连通时那条边的权"就是瓶颈，和 778 同一个套路
##################################################################################################


class UnionFind:  # ! 和 1135 的模板一个字都不改
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
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        edges = []
        for r in range(m):
            for c in range(n):
                if r + 1 < m:
                    edges.append((abs(heights[r + 1][c] - heights[r][c]), r * n + c, (r + 1) * n + c))
                if c + 1 < n:
                    edges.append((abs(heights[r][c + 1] - heights[r][c]), r * n + c, r * n + c + 1))
        edges.sort()  # ! 边权从小到大，一条条接上去

        uf = UnionFind(m * n)
        for w, a, b in edges:
            uf.union(a, b)
            if uf.find(0) == uf.find(m * n - 1):  # ! 左上和右下刚连通，这条边的权就是瓶颈
                return w
        return 0  # 1x1：一条边都不用


if __name__ == "__main__":
    cases = [
        ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
        ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
        ([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]], 0),
        ([[7]], 0),
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for h, want in cases:
            got = sol.minimumEffortPath([row[:] for row in h])
            assert got == want, f"{type(sol).__name__} {h}: got {got}, want {want}"
    print("3 个解法全过")


##################################################################################################
##### ! Solution Alt: 瓶颈路径模板（把 relax 从「加」改成「取 max」）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：dijkstra/02 - Dijkstra 非加法路径代价变体/01 - LC-1631 - Path With Minimum Effort
##### ! 变体目录　：bottleneck-path (瓶颈路径：relax 改 max 或 min)/变体 · LC-1631 - Path With Minimum Effort
##### ! 为什么这样定主次：instructions 把 LC-1631 列在 Dijkstra 子树的「非加法路径代价变体」里作为主学习位置
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from typing import List, Tuple


import heapq


from collections import deque  # Solution_3 用


class Solution_Alt:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])
        visited = [[False] * n for _ in range(m)]

        # Each cell stores the max_height_diff along the optimal path
        dist = [[float("inf")] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # cost, x, y

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def get_neigbs(x: int, y: int) -> List[Tuple[int, int, int]]:
            cost = dist[x][y]
            neigbs = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < m and 0 <= ny < n):
                    continue

                # ! 2️⃣ Skip visited nodes optimization
                if visited[nx][ny]:
                    continue
                new_cost = abs(heights[nx][ny] - heights[x][y])
                """
                The new cost is the maximum between
                - the previous max height diff along the optimal path
                and
                - the new height diff (from (x, y) --> (nx, ny))
                """
                neigbs.append((max(new_cost, cost), nx, ny))
            return neigbs

        while heap:
            cost, x, y = heapq.heappop(heap)

            # ! 1️⃣ Skip stale entries optimization
            if dist[x][y] < cost:
                continue

            # ! 3️⃣ Stop early optimization
            if x == m - 1 and y == n - 1:
                return cost

            visited[x][y] = True

            for new_cost, nx, ny in get_neigbs(x, y):
                if new_cost < dist[nx][ny]:
                    dist[nx][ny] = new_cost
                    heapq.heappush(heap, (new_cost, nx, ny))
        return -1


class UnionFind_Alt:
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


class Solution_2_Alt:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        # ! 造边：只造"右"和"下"两个方向，每对相邻格子恰好一条边；格子 (x, y) 编号 x*n + y
        edges = []
        for x in range(m):
            for y in range(n):
                if x + 1 < m:
                    edges.append((abs(heights[x][y] - heights[x + 1][y]), x * n + y, (x + 1) * n + y))
                if y + 1 < n:
                    edges.append((abs(heights[x][y] - heights[x][y + 1]), x * n + y, x * n + y + 1))
        edges.sort()  # ① 按高度差从小到大排队

        uf = UnionFind(m * n)
        start, end = 0, m * n - 1
        for w, u, v in edges:  # ② 逐条接上，当前边权 w 就是门槛
            uf.union(u, v)  # ③ 不看返回值：不是在建树，只是记连通
            if uf.find(start) == uf.find(end):  # ④ 第一次连通 → 当前门槛就是答案
                return w
        return 0  # 1x1 网格没有边，体力 0


class Solution_3_Alt:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])

        def can(limit: int) -> bool:  # 只走高度差 ≤ limit 的边，左上能不能到右下
            seen = [[False] * n for _ in range(m)]
            seen[0][0] = True
            queue = deque([(0, 0)])
            while queue:
                x, y = queue.popleft()
                if (x, y) == (m - 1, n - 1):
                    return True
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and not seen[nx][ny]:
                        if abs(heights[nx][ny] - heights[x][y]) <= limit:
                            seen[nx][ny] = True
                            queue.append((nx, ny))
            return False

        lo, hi = 0, max(map(max, heights)) - min(map(min, heights))  # 答案一定落在 [0, 全局最大高度差]
        while lo < hi:  # ! 找最小的 limit 使 can(limit) 为真
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
