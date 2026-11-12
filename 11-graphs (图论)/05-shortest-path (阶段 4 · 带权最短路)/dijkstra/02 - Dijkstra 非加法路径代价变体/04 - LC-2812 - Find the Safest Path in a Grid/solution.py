"""LC-2812 - Find the Safest Path in a Grid

阶段 4 · Dijkstra + 状态扩展 △ 扩展
题目在问：从左上到右下，路径安全度 = 路径上各格到最近小偷的曼哈顿距离的最小值，求安全度最大的那条路
点是什么：格子 (r, c)   边是什么：上下左右；格子的权 = 安全度（先用多源 BFS 算出来）
和签名题比改了哪一行：先用 994 的多源 BFS 把"离最近小偷多远"填进每格；再把 743 的 relax 从 d + w 改成 min(d, safe[nr][nc])、
堆改大根堆（存负数），就是 1102 的最大最小值路径。另两种解法：二分安全度 + BFS、按安全度从高到低加格子的并查集（778 的三件套）
"""

from collections import deque
from heapq import heappop, heappush
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def safeness_grid(grid: List[List[int]]) -> List[List[int]]:
    # ! 多源 BFS：所有小偷同时入队，距离 0，一圈圈往外扩；无障碍网格上 BFS 距离就是曼哈顿距离
    n = len(grid)
    safe = [[-1] * n for _ in range(n)]
    q = deque()

    # ! 小偷和他们自己的距离是 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                safe[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and safe[nr][nc] == -1:
                safe[nr][nc] = safe[r][c] + 1
                q.append((nr, nc))
    return safe


##################################################################################################
##### ! Solution 1: Multi-source BFS + Dijkstra maximin (max-heap)
##### ! 时间复杂度: O(n^2 log n)   空间复杂度: O(n^2)
##### ! 适用：最大最小值路径的标准写法；relax 改 min、堆改大根堆，一遍出答案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        safe = safeness_grid(grid)
        # ! best[r][c]：到这格为止，所有路径里"一路上的最小安全度"的最大值；大根堆按它弹
        best = [[-1] * n for _ in range(n)]
        best[0][0] = safe[0][0]
        heap = [(-safe[0][0], 0, 0)]  # 存负数当大根堆
        while heap:
            neg, r, c = heappop(heap)
            d = -neg
            if r == n - 1 and c == n - 1:  # 第一次弹到终点就是答案
                return d
            if d < best[r][c]:  # 作废票
                continue
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    nd = min(d, safe[nr][nc])  # ! relax：路径安全度 = 一路上的最小值
                    if nd > best[nr][nc]:
                        best[nr][nc] = nd
                        heappush(heap, (-nd, nr, nc))
        return 0


##################################################################################################
##### ! Solution 2: Binary search on safeness + BFS
##### ! 时间复杂度: O(n^2 log n)   空间复杂度: O(n^2)
##### ! 适用："答案 s 可行则 s-1 也可行"的题都能二分；每次用只踩 safe >= s 的格子做一遍普通 BFS
##################################################################################################


class Solution_2:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        safe = safeness_grid(grid)

        def can(s: int) -> bool:  # 只踩安全度 >= s 的格子，能不能从起点走到终点
            if safe[0][0] < s or safe[n - 1][n - 1] < s:
                return False
            seen = [[False] * n for _ in range(n)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == n - 1 and c == n - 1:
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and safe[nr][nc] >= s:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        # ! s = 0 时所有格子都能踩，一定可行；找最大的可行 s
        lo, hi = 0, min(safe[0][0], safe[n - 1][n - 1])
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


##################################################################################################
##### ! Solution 3: Union-Find, add cells in decreasing safeness
##### ! 时间复杂度: O(n^2 α(n^2))   空间复杂度: O(n^2)
##### ! 适用：778 的"Kruskal 过程不要树"：按安全度从高到低一批批放格子，起点终点第一次连通时的安全度就是答案
##################################################################################################


class UnionFind:  # 和 1135 完全一样
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
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        safe = safeness_grid(grid)
        buckets = [[] for _ in range(2 * n)]  # 安全度最大 2n-2，按安全度分桶省掉排序
        for r in range(n):
            for c in range(n):
                buckets[safe[r][c]].append((r, c))

        uf = UnionFind(n * n)
        added = [[False] * n for _ in range(n)]
        for s in range(2 * n - 1, -1, -1):  # ! 安全度从高到低，一整批放完再检查
            for r, c in buckets[s]:
                added[r][c] = True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and added[nr][nc]:
                        uf.union(r * n + c, nr * n + nc)
            if added[0][0] and added[n - 1][n - 1] and uf.find(0) == uf.find(n * n - 1):
                return s
        return 0


s = Solution_1()
grid = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
print(s.maximumSafenessFactor(grid))  # 0

grid = [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
print(s.maximumSafenessFactor(grid))  # 2

grid = [[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
print(s.maximumSafenessFactor(grid))  # 2
