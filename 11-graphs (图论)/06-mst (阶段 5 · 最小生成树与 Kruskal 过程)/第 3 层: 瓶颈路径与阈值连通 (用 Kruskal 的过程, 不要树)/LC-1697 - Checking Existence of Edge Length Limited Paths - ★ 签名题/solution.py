"""LC-1697 - Checking Existence of Edge Length Limited Paths

阶段 5 · 最小生成树与 Kruskal 过程 · 第 3 层: 瓶颈路径与阈值连通 (用 Kruskal 的过程, 不要树) ★ 签名题
题目在问：很多组查询 [p, q, limit], 每组问: 只走长度严格小于 limit 的边, p 和 q 通不通
点是什么：n 个点 (0..n-1)   边是什么：[u, v, dis], 可能有重边
和签名题比改了哪一行：本题就是"离线 + Kruskal 过程"的签名题:
                     查询按 limit 排序, 边按长度排序, 一个指针把所有 < limit 的边 union 进去, 再问并查集 p、q 是否一派
"""
from collections import deque
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并, 和 1135 / 1584 一样
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


##################################################################################################
##### ! Solution 1: 离线 + Kruskal 过程 (查询按 limit 排序, 边按长度排序, 指针逐条 union)
##### ! 时间复杂度: O(E log E + Q log Q + (E + Q) · α(n))   空间复杂度: O(n + Q)
##### ! 适用：很多组"只用 < x 的边通不通"的查询, 且允许先看完所有查询再答 (离线)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        edgeList.sort(key=lambda e: e[2])                                 # ! 边按长度排队
        order = sorted(range(len(queries)), key=lambda i: queries[i][2])  # ! 查询按 limit 排队 (记下标, 答案要放回原位)
        uf = UnionFind(n)
        ans = [False] * len(queries)
        k = 0                                                             # 边加到哪了
        for qi in order:
            p, q, limit = queries[qi]
            while k < len(edgeList) and edgeList[k][2] < limit:           # ! 把所有 < limit 的边接上 (严格小于)
                uf.union(edgeList[k][0], edgeList[k][1])                  # 不用管成不成功, 只是在记录连通性
                k += 1
            ans[qi] = uf.find(p) == uf.find(q)                            # ! 此刻通不通就是答案
        return ans
        # ! 为什么能离线: 门槛 limit 只涨不降, 边只加不拆, 并查集只会合并, 所以指针 k 一路往前, 每条边只加一次


##################################################################################################
##### ! Solution 2: 每个查询单独 BFS, 只走长度 < limit 的边 (慢, 对拍基线)
##### ! 时间复杂度: O(Q · (V + E))   空间复杂度: O(V + E)
##### ! 适用：只有一两个查询时; Q、E 都到 1e5 会超时, 这里只作为理解题意的基线
##################################################################################################


class Solution_2:
    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj = [[] for _ in range(n)]
        for u, v, w in edgeList:
            adj[u].append((v, w))
            adj[v].append((u, w))

        ans = []
        for p, q, limit in queries:
            seen = [False] * n
            seen[p] = True
            dq = deque([p])
            while dq:
                u = dq.popleft()
                for v, w in adj[u]:
                    if w < limit and not seen[v]:  # ! 门槛写在走边的那一行: 长度 >= limit 的边当作不存在
                        seen[v] = True
                        dq.append(v)
            ans.append(seen[q])
        return ans


s = Solution_1()
n = 3
edgeList = [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]]
queries = [[0, 1, 2], [0, 2, 5]]
result = s.distanceLimitedPathsExist(n, edgeList, queries)
print(result)  # [False, True]
