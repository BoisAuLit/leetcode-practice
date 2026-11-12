"""LC-2976 - Minimum Cost to Convert String I

Level 1 · 01 标准加法最短路 —— 把"字符替换"建模成最短路
题目在问：把 source 一个字符一个字符换成 target，每条替换规则 x -> y 有代价，求总最小代价，不行返回 -1
点是什么：26 个小写字母   边是什么：一条规则 original[i] -> changed[i]，权 = cost[i]（有向、可以有重边）
和签名题 743 比改了哪一行：一行都没改。难点全在建模：
      "字符 a 变成 b 最少花多少" = 26 个点的图上 a 到 b 的最短路；逐位求和就是答案

坑：
  - 图是有向的（a->b 便宜不代表 b->a 便宜），邻接表只加一条边
  - 规则里有重边，Dijkstra 本身能处理；用 Floyd 写则必须 min 一下
  - source[i] == target[i] 时代价是 0，但"绕一圈回来"不可能更便宜，dist[c][c] = 0 自然成立
  - 只要有一位到不了就整体 -1，不要把 inf 加进答案
  - 总代价最大 1e5 * 1e6 = 1e11，Python 无所谓，C++/Java 要用 long long
"""

from heapq import heappop, heappush
from typing import List

A = 26


##################################################################################################
##### ! Solution 1: 对 26 个字母各跑一遍标准 Dijkstra
##### ! 时间复杂度: O(26 * (E log 26) + L)   空间复杂度: O(26^2 + E)，L = len(source)
##### ! 适用：点少边多的全源最短路；和 743 同一个模板，体现"把问题翻译成图"才是本题考点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumCost(self, source: str, target: str, original: List[str],
                    changed: List[str], cost: List[int]) -> int:
        adj = [[] for _ in range(A)]
        for o, c, w in zip(original, changed, cost):
            adj[ord(o) - 97].append((ord(c) - 97, w))  # ! 有向边，只加一条

        def dijkstra(src: int) -> List[float]:
            dist = [float("inf")] * A
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:
                    continue
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heappush(heap, (d + w, v))
            return dist

        dist = [dijkstra(c) for c in range(A)]
        total = 0
        for s, t in zip(source, target):
            d = dist[ord(s) - 97][ord(t) - 97]
            if d == float("inf"):
                return -1  # ! 有一位换不过去，整体就是 -1
            total += d
        return total


##################################################################################################
##### ! Solution 2: Floyd-Warshall（26 个点的全源最短路）
##### ! 时间复杂度: O(26^3 + E + L)   空间复杂度: O(26^2)
##### ! 适用：★ 点数固定且很小时代码最短；26^3 = 17576，比建 26 个堆还快
##################################################################################################


class Solution_2:
    def minimumCost(self, source: str, target: str, original: List[str],
                    changed: List[str], cost: List[int]) -> int:
        INF = float("inf")
        d = [[INF] * A for _ in range(A)]
        for i in range(A):
            d[i][i] = 0
        for o, c, w in zip(original, changed, cost):
            x, y = ord(o) - 97, ord(c) - 97
            d[x][y] = min(d[x][y], w)  # ! 重边取最小，这一步不能省

        for k in range(A):
            dk = d[k]
            for i in range(A):
                dik = d[i][k]
                if dik == INF:
                    continue
                row = d[i]
                for j in range(A):
                    if dik + dk[j] < row[j]:
                        row[j] = dik + dk[j]

        total = 0
        for s, t in zip(source, target):
            w = d[ord(s) - 97][ord(t) - 97]
            if w == INF:
                return -1
            total += w
        return total


##################################################################################################
##### ! Solution 3: 只对 source 里真正出现过的字母跑 Dijkstra（按需 + 记忆化）
##### ! 时间复杂度: O(k * E log 26 + L)，k = source 里不同字母数   空间复杂度: O(26^2 + E)
##### ! 适用：源字母很少时省掉大半的 Dijkstra；工程上"别算用不到的东西"的习惯
##################################################################################################


class Solution_3:
    def minimumCost(self, source: str, target: str, original: List[str],
                    changed: List[str], cost: List[int]) -> int:
        adj = [[] for _ in range(A)]
        for o, c, w in zip(original, changed, cost):
            adj[ord(o) - 97].append((ord(c) - 97, w))

        memo: dict[int, List[float]] = {}

        def dist_from(src: int) -> List[float]:
            if src in memo:  # ! 同一个起点只算一次
                return memo[src]
            dist = [float("inf")] * A
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:
                    continue
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heappush(heap, (d + w, v))
            memo[src] = dist
            return dist

        total = 0
        for s, t in zip(source, target):
            if s == t:
                continue
            d = dist_from(ord(s) - 97)[ord(t) - 97]
            if d == float("inf"):
                return -1
            total += d
        return total


if __name__ == "__main__":
    cases = [
        ("abcd", "acbe", ["a", "b", "c", "c", "e", "d"], ["b", "c", "b", "e", "b", "e"],
         [2, 5, 5, 1, 2, 20], 28),
        ("aaaa", "bbbb", ["a", "c"], ["c", "b"], [1, 2], 12),      # a->c->b 比直接便宜
        ("abcd", "abce", ["a"], ["e"], [10000], -1),
        ("ab", "ab", ["a"], ["b"], [1], 0),                        # 本来就一样，0 代价
    ]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for s, t, o, c, w, want in cases:
            got = sol.minimumCost(s, t, o[:], c[:], w[:])
            assert got == want, f"{type(sol).__name__} {s}->{t}: got {got}, want {want}"
    print("3 个解法全过")


##################################################################################################
##### ! Solution Alt: Floyd-Warshall（全源最短路）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：dijkstra/01 - Dijkstra 标准加法最短路/04 - LC-2976 - Minimum Cost to Convert String I
##### ! 变体目录　：floyd (Floyd：所有点对，点 ≤ 100)/变体 · LC-2976 - Minimum Cost to Convert String I
##### ! 为什么这样定主次：同 LC-1334：Floyd 作为参考实现保留
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from heapq import heappop, heappush


from math import inf


from typing import List


class Solution_1_Alt:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        K = 26
        dist = [[inf] * K for _ in range(K)]
        for i in range(K):
            dist[i][i] = 0
        for a, b, c in zip(original, changed, cost):
            u, v = ord(a) - 97, ord(b) - 97
            if c < dist[u][v]:  # ! 有向、重边取最小；不要直接覆盖
                dist[u][v] = c

        for k in range(K):  # 1334 的三层循环原样搬过来
            dk = dist[k]
            for i in range(K):
                dik = dist[i][k]
                if dik == inf:
                    continue
                di = dist[i]
                for j in range(K):
                    if dik + dk[j] < di[j]:
                        di[j] = dik + dk[j]

        total = 0
        for a, b in zip(source, target):  # 逐位查表
            if a == b:
                continue
            d = dist[ord(a) - 97][ord(b) - 97]
            if d == inf:  # ! 有一位改不过去，整体失败
                return -1
            total += d
        return total


class Solution_2_Alt:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        K = 26
        adj = [[] for _ in range(K)]
        for a, b, c in zip(original, changed, cost):
            adj[ord(a) - 97].append((ord(b) - 97, c))  # 重边不用去，Dijkstra 自己会挑小的

        def dijkstra(src: int) -> List[int]:
            dist = [inf] * K
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heappop(heap)
                if d > dist[u]:  # 作废票
                    continue
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heappush(heap, (d + w, v))
            return dist

        table = [dijkstra(i) for i in range(K)]  # ! 26 次 Dijkstra 拼成和 Floyd 一样的表
        total = 0
        for a, b in zip(source, target):
            if a == b:
                continue
            d = table[ord(a) - 97][ord(b) - 97]
            if d == inf:
                return -1
            total += d
        return total
