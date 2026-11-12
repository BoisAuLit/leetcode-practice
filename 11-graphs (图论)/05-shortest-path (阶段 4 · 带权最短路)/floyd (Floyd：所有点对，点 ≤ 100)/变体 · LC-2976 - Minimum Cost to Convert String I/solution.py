"""LC-2976 - Minimum Cost to Convert String I

阶段 4 · Floyd (所有点对，点 ≤ 100) ○ 核心
题目在问：把 source 逐位改成 target 最少花多少；每一位独立，有一位改不了就整体返回 -1
点是什么：26 个小写字母   边是什么：original[i] -> changed[i] 的有向边，权 cost[i]（同一对字母重边取最小）
和签名题比改了哪一行：1334 建表后数"阈值内的点"；这里建表后按位查 dist[s][t] 累加。图固定 26 个点，Floyd 只是 26^3 的常数
"""
from heapq import heappop, heappush
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: Floyd on 26 letters
##### ! 时间复杂度: O(26^3 + m + n)   空间复杂度: O(26^2)      (m = 边数，n = 字符串长度)
##### ! 适用：点数固定且很小、要查任意两点的最短路；写完表之后每一位都是 O(1) 查表
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
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


##################################################################################################
##### ! Solution 2: Dijkstra from each of the 26 letters
##### ! 时间复杂度: O(26 · m log 26 + n)   空间复杂度: O(26^2 + m)
##### ! 适用：想复用 743 的模板时；每个字母当一次源点跑出同一张 26 x 26 的表
##################################################################################################


class Solution_2:
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


s = Solution_1()
source, target = "abcd", "acbe"
original = ["a", "b", "c", "c", "e", "d"]
changed = ["b", "c", "b", "e", "b", "e"]
cost = [2, 5, 5, 1, 2, 20]
result = s.minimumCost(source, target, original, changed, cost)
print(result)  # 28

source, target = "aaaa", "bbbb"
original, changed, cost = ["a", "c"], ["c", "b"], [1, 2]
result = s.minimumCost(source, target, original, changed, cost)
print(result)  # 12

source, target = "abcd", "abce"
original, changed, cost = ["a"], ["e"], [10000]
result = s.minimumCost(source, target, original, changed, cost)
print(result)  # -1
