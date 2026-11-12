"""LC-0847 - Shortest Path Visiting All Nodes（第二轮自主新增）

阶段 0 · 状态图 BFS —— **把「访问过哪些点」压成一个位掩码**
题目在问：无向连通图，从任意点出发，访问**所有**点的最短路径长度。
         可以重复经过点和边。

为什么新增它（它补的是哪个缺口）：
  本模板原有的 LC-0752 / LC-1293 的状态是「位置 + 一个标量资源」。
  这道题的状态是「位置 + **一个集合**」，集合用**位掩码**表示 ——
  这是状态压缩（Bitmask）最经典的入口，也是通往状压 DP 的桥。
  本专题原本没有练到「状态里带一个集合」这件事。

点是什么：**`(当前所在点 u, 已访问点集 mask)`**，共 `n · 2^n` 个状态。
边是什么：从 u 走到邻居 v，mask 多点亮一位 ⟹ `(v, mask | 1<<v)`。

决定性观察：
  1. **为什么可以重复经过点**：题目允许，而且这正是为什么不能只做简单 DFS ——
     最优路径可能来回穿过某个枢纽点。把 mask 放进状态后，
     「同一个点带不同的已访问集合」是不同状态，重复经过自然被允许。
  2. **多源起点**：从任意点出发都可以 ⟹ 把**所有** `(i, 1 << i)` 一起入队
     （这就是多源 BFS），而不是对每个起点各跑一次 BFS（那样会多一个 n 倍）。
  3. 终止条件：`mask == (1 << n) - 1`，即所有位都点亮了。
  4. 每条边代价都是 1 ⟹ **BFS 就是最短路**，不需要 Dijkstra。

```python
full = (1 << n) - 1
q = deque((i, 1 << i, 0) for i in range(n))      # 多源
seen = {(i, 1 << i) for i in range(n)}
while q:
    u, mask, d = q.popleft()
    if mask == full: return d
    for v in graph[u]:
        nm = mask | (1 << v)
        if (v, nm) not in seen:
            seen.add((v, nm)); q.append((v, nm, d + 1))
```

复杂度：状态数 **O(n · 2^n)**，每个状态最多 n 条边
      ⟹ 时间 O(n² · 2^n)，空间 O(n · 2^n)。
      题目限制 n ≤ 12，所以 12² · 4096 ≈ 60 万，完全可行。
      **这类题的 n 很小就是在暗示状态压缩。看到 n ≤ 20 就该想到位掩码。**

这是 **TSP（旅行商问题）** 的一个变体 —— 它本身是 NP-hard，
所以指数级复杂度是预期的，不要试图找多项式算法。

和 LC-0752 Open the Lock 的对照：

| | LC-0752 | LC-0847 |
|---|---|---|
| 状态 | 4 位锁的字符串 | `(位置, 已访问集合)` |
| 状态数 | 10⁴ | n · 2^n |
| 起点 | 单源 `"0000"` | **多源**（任意点都行） |
| 终止 | 到达 target | mask 全亮 |

边界：
  - n == 1 → 0（一个点，什么都不用走）
  - 链状图（必须来回走）
  - 星形图（枢纽点会被重复经过多次）
  - 完全图 → n - 1 步
"""

from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: 多源 BFS，状态 = (当前点, 已访问点的位掩码)
##### ! 时间复杂度: O(n^2 · 2^n)   空间复杂度: O(n · 2^n)
##### ! 适用：「必须访问全部 / 一个子集」的最短路；n ≤ 20 就该想到位掩码
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        n = len(graph)
        if n == 1:
            return 0
        full = (1 << n) - 1
        # ! 多源：从每个点各起一个状态，一起入队
        q = deque((i, 1 << i, 0) for i in range(n))
        seen = {(i, 1 << i) for i in range(n)}
        while q:
            u, mask, dist = q.popleft()
            if mask == full:
                return dist
            for v in graph[u]:
                nm = mask | (1 << v)         # ! 点亮 v 这一位
                if (v, nm) not in seen:      # ! 去重必须按 (点, 集合) 二元组
                    seen.add((v, nm))
                    q.append((v, nm, dist + 1))
        return 0


##################################################################################################
##### ! Solution 2: 状压 DP（Floyd 预处理两点最短路 + 枚举访问顺序的 DP）
##### ! 时间复杂度: O(n^3 + n^2 · 2^n)   空间复杂度: O(n · 2^n)
##### ! 适用：说明本题就是 TSP；dp[mask][u] = 访问完 mask 且停在 u 的最短长度
##################################################################################################


class Solution_2:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        n = len(graph)
        if n == 1:
            return 0
        INF = float("inf")
        # ! Floyd：任意两点最短距离（图无权，等价于 BFS，但 n 很小直接 Floyd 更短）
        d = [[INF] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
            for j in graph[i]:
                d[i][j] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
        full = (1 << n) - 1
        dp = [[INF] * n for _ in range(1 << n)]
        for i in range(n):
            dp[1 << i][i] = 0
        for mask in range(1 << n):
            for u in range(n):
                if dp[mask][u] == INF:
                    continue
                for v in range(n):
                    if mask >> v & 1:
                        continue
                    nm = mask | (1 << v)
                    if dp[mask][u] + d[u][v] < dp[nm][v]:
                        dp[nm][v] = dp[mask][u] + d[u][v]
        return int(min(dp[full]))


if __name__ == "__main__":
    import random

    cases = [([[1, 2, 3], [0], [0], [0]], 4),
             ([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4),
             ([[]], 0),
             ([[1], [0]], 1),
             ([[1, 2], [0, 2], [0, 1]], 2)]
    for graph, want in cases:
        a = Solution_1().shortestPathLength([r[:] for r in graph])
        b = Solution_2().shortestPathLength([r[:] for r in graph])
        assert a == b == want, (graph, a, b, want)
        print(f"{graph} -> {a}")

    def rand_connected(n):
        """随机生成一个连通无向图（先造生成树再随机加边）。"""
        adj = [set() for _ in range(n)]
        for v in range(1, n):
            u = random.randint(0, v - 1)
            adj[u].add(v); adj[v].add(u)
        for _ in range(random.randint(0, n)):
            a, b = random.sample(range(n), 2) if n >= 2 else (0, 0)
            if a != b:
                adj[a].add(b); adj[b].add(a)
        return [sorted(s) for s in adj]

    for _ in range(400):
        n = random.randint(1, 7)
        graph = rand_connected(n)
        a = Solution_1().shortestPathLength([r[:] for r in graph])
        b = Solution_2().shortestPathLength([r[:] for r in graph])
        assert a == b, (graph, a, b)
    print("随机对拍 400 组通过 ✓（多源位掩码 BFS == Floyd + 状压 DP）")
