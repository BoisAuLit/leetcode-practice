"""LC-1631 - Path With Minimum Effort

阶段 4 · 带权最短路 · 瓶颈路径(relax 改 max 或 min) ○ 核心
题目在问：从左上到右下，路径上"相邻两格高度差"的最大值最小是多少
点是什么：每个格子   边是什么：上下左右相邻，边权 = 两格高度差(门槛写在边上)
和签名题(743)比改了哪一行：relax 从 d + w 改成 max(d, w)；堆里存的是"到这格为止路上最大的高度差"
三种解法都要会说：① Dijkstra 改 relax  ② Kruskal 过程 + 并查集看左上右下何时连通  ③ 二分答案 + BFS 检查通不通
"""
from typing import List, Tuple
import heapq
from collections import deque  # Solution_3 用

"""
cost == max_height_diff along optimal path
"""


##################################################################################################
##### ! Solution 1: Dijkstra 改 relax 为 max(d, w)
##### ! 时间复杂度: O(m·n · log(m·n))   空间复杂度: O(m·n)
##### ! 适用：单起点单终点的最小瓶颈路径，三种解法里代码最短
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
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


##################################################################################################
##### ! Solution 2: Kruskal 过程 + 并查集 (不要树，只看左上和右下何时连通)
##### ! 时间复杂度: O(m·n · log(m·n))   空间复杂度: O(m·n)   边数约 2·m·n，瓶颈是排序
##### ! 适用：多组查询 / 离线 / 要反着时间走时用这套；门槛从小到大涨，第一次连通的那条边权就是答案
##################################################################################################


class UnionFind:
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


class Solution_2:
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


##################################################################################################
##### ! Solution 3: 二分答案 + BFS 检查通不通
##### ! 时间复杂度: O(m·n · log(maxH))   空间复杂度: O(m·n)   maxH ≤ 1e6，约 20 次 BFS
##### ! 适用：答案单调("x 够了 x+1 一定也够")就能二分；面试能把三种解法的取舍说清楚是加分项
##################################################################################################


class Solution_3:
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


# Test case 1: Expect 0
# s = Solution()
# heights = [
#     [1, 2, 1, 1, 1],
#     [1, 2, 1, 2, 1],
#     [1, 2, 1, 2, 1],
#     [1, 2, 1, 2, 1],
#     [1, 1, 1, 2, 1],
# ]
# result = s.minimumEffortPath(heights)
# print(result)

# Test case 2: Expect 2
s = Solution()
heights = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
result = s.minimumEffortPath(heights)
print(result)
