"""LC-2421 - Number of Good Paths

阶段 5 · 最小生成树与 Kruskal 过程 · 第 3 层: 瓶颈路径与阈值连通 (用 Kruskal 的过程, 不要树) ○ 核心
题目在问：树上每个点有值, "好路径" = 起点终点值相同 (设为 v) 且路上其他点的值都 <= v; 单个点也算; 一共几条
点是什么：树的 n 个点 (0..n-1), 每点有 vals[i]   边是什么：n-1 条树边
和签名题比改了哪一行：1697 的门槛是"边的长度 < limit", 这里门槛换成"点的值 <= v":
                     点按值升序分批加入, 每点只和值 <= v 的邻居 union, 再对每一派数值恰好 == v 的点 c, 贡献 c(c+1)/2
"""
from collections import Counter, defaultdict
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
##### ! Solution 1: 点按值升序分批加入 + 并查集, 每派数值 == v 的点
##### ! 时间复杂度: O(n log n + n · α(n))   空间复杂度: O(n)
##### ! 适用：门槛写在"点"上而不是边上的阈值连通; 手册里讲的就是这个写法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        groups = defaultdict(list)  # 值 -> 这个值的所有点
        for i, x in enumerate(vals):
            groups[x].append(i)

        uf = UnionFind(n)
        ans = 0
        for v in sorted(groups):  # ! 门槛 v 从小到大升, 一次处理值为 v 的一整批点
            for u in groups[v]:
                for w in adj[u]:
                    if vals[w] <= v:  # ! 只和值 <= v 的邻居合并: 此刻并查集里每一派只含值 <= v 的点
                        uf.union(u, w)
            # ! 同一派里值恰好 == v 的 c 个点, 两两之间的路径全程 <= v, 都是好路径
            cnt = Counter(uf.find(u) for u in groups[v])
            for c in cnt.values():
                ans += c * (c + 1) // 2  # c 个点任选两个 + 每个点自己
        return ans


##################################################################################################
##### ! Solution 2: 边按"两端较大值"排序逐条 union, 每派维护 (最大值, 最大值的个数)
##### ! 时间复杂度: O(n log n + n · α(n))   空间复杂度: O(n)
##### ! 适用：想把门槛挪回"边"上, 写成和 1697 一样的"边排序 + 一个循环"时 (LeetCode 官方题解写法)
##################################################################################################


class Solution_2:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        uf = UnionFind(n)
        mx = vals[:]  # mx[root]  = 这一派里的最大值
        cnt = [1] * n  # cnt[root] = 这一派里值 == mx 的点有几个
        ans = n  # 每个点自己是一条好路径

        # ! 边按 max(两端值) 排序: 处理到门槛 w 的边时, 两边派里所有点的值都 <= w, 且至少一边的最大值 == w
        for u, v in sorted(edges, key=lambda e: max(vals[e[0]], vals[e[1]])):
            ru, rv = uf.find(u), uf.find(v)
            if mx[ru] == mx[rv]:  # ! 两派最大值都 == w: 两边的最大点两两配对, 中间全程 <= w
                ans += cnt[ru] * cnt[rv]
                new_mx, new_cnt = mx[ru], cnt[ru] + cnt[rv]
            elif mx[ru] > mx[rv]:  # 只有一边的最大值是 w, 合并后最大值和个数照抄那一边
                new_mx, new_cnt = mx[ru], cnt[ru]
            else:
                new_mx, new_cnt = mx[rv], cnt[rv]
            uf.union(ru, rv)
            r = uf.find(ru)
            mx[r], cnt[r] = new_mx, new_cnt
        return ans


s = Solution_1()
vals = [1, 3, 2, 1, 3]
edges = [[0, 1], [0, 2], [2, 3], [2, 4]]
result = s.numberOfGoodPaths(vals, edges)
print(result)  # 6
