"""LC-1724 - Checking Existence of Edge Length Limited Paths II

阶段 5 · 最小生成树与 Kruskal 过程 · 第 3 层: 瓶颈路径与阈值连通 (用 Kruskal 的过程, 不要树) △ 扩展 (会员题)
题目在问：1697 的在线版: 先给图, 之后查询 [p, q, limit] 一条条来 (只走长度 < limit 的边 p、q 通不通), 不能攒着一起答
点是什么：n 个点 (0..n-1)   边是什么：[u, v, dis]
和签名题比改了哪一行：1697 能离线是因为可以把查询按 limit 排序; 在线做不到, 于是把 Kruskal 过程"录下来":
                     边按长度升序 union, 并查集不做路径压缩, 每个点记下"我是在长度几的边上被挂到父亲下面的" (attach 权);
                     查询时 p、q 沿着 attach < limit 的父指针往上爬, 爬到同一个点就通
"""
from math import inf
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并, 和 1135 / 1584 一样 (Solution 2 建重构树时用)
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
##### ! Solution 1: 不压缩路径的并查集 + 每个点记 attach 权, 查询时双指针往上爬
##### ! 时间复杂度: 建图 O(E log E + E log n), 每次查询 O(log n)   空间复杂度: O(n)
##### ! 适用：在线的"只用 < limit 的边通不通"; 按 size 合并保证树高 O(log n), 所以爬几步就到
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class DistanceLimitedPathsExist_1:
    def __init__(self, n: int, edgeList: List[List[int]]):
        self.parent = list(range(n))
        self.attach = [inf] * n  # attach[x] = x 被挂到 parent[x] 下面时那条边的长度; 根是 inf (永远爬不上去)
        size = [1] * n
        for u, v, w in sorted(edgeList, key=lambda e: e[2]):  # ! Kruskal 过程: 边按长度升序逐条接
            ru, rv = self._find(u), self._find(v)
            if ru == rv:
                continue
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            self.parent[rv] = ru  # ! 按 size 合并 (树高 O(log n)); 不做路径压缩, 否则 attach 的含义就被压没了
            self.attach[rv] = w
            size[ru] += size[rv]

    def _find(self, x: int) -> int:  # 只找根, 不压缩 (这就是为什么不能直接用模块级的 UnionFind)
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def query(self, p: int, q: int, limit: int) -> bool:
        # ! 从任何点往上走, 路上的 attach 权只增不减 (先挂上去的一定是更短的边),
        # ! 所以"沿着 attach < limit 的指针能爬到的最高点" = 只用 < limit 的边时这个点所在派的代表
        while p != q:
            if self.attach[p] > self.attach[q]:  # ! 总是抬 attach 更小的那个 (它离自己的代表更远)
                p, q = q, p
            if self.attach[p] >= limit:  # 两个都爬不动了还不相等 -> 不通
                return False
            p = self.parent[p]
        return True


##################################################################################################
##### ! Solution 2: Kruskal 重构树 + 倍增
##### ! 时间复杂度: 建树 O(E log E + n log n), 每次查询 O(log n)   空间复杂度: O(n log n)
##### ! 适用：想把"沿 attach 往上爬"做成严格 O(log n) 的倍增; 重构树是瓶颈路径类问题的通用武器
##################################################################################################


class DistanceLimitedPathsExist_2:
    def __init__(self, n: int, edgeList: List[List[int]]):
        total = 2 * n - 1  # 最多 n 个叶子 (原图的点) + n-1 个内部点 (每次成功合并新建一个)
        par = [-1] * total  # 重构树上的父亲, 没有就 -1
        self.wt = [0] * total  # 内部点的权 = 合并它两个孩子的那条边的长度 (叶子用不到)
        uf = UnionFind(n)
        top = list(range(n))  # top[并查集的根] = 这一派在重构树上目前的最高点
        cur = n
        for u, v, w in sorted(edgeList, key=lambda e: e[2]):  # ! 还是 Kruskal 过程
            ru, rv = uf.find(u), uf.find(v)
            if ru == rv:
                continue
            par[top[ru]] = par[top[rv]] = cur  # ! 新建内部点 cur, 两派的最高点都挂到它下面
            self.wt[cur] = w
            uf.union(ru, rv)
            top[uf.find(ru)] = cur
            cur += 1

        # ! 倍增表: up[k][x] = x 往上 2^k 步的祖先. 叶子到根的权只增不减, 所以"权 < limit 的祖先"是一段前缀
        self.up = [par]
        for _ in range(1, max(1, total.bit_length())):
            prev = self.up[-1]
            self.up.append([-1 if prev[x] == -1 else prev[prev[x]] for x in range(total)])

    def _lift(self, x: int, limit: int) -> int:  # 爬到权 < limit 的最高祖先
        for k in range(len(self.up) - 1, -1, -1):
            a = self.up[k][x]
            if a != -1 and self.wt[a] < limit:
                x = a
        return x

    def query(self, p: int, q: int, limit: int) -> bool:
        return self._lift(p, limit) == self._lift(q, limit)  # ! 爬到同一个点 = 只用 < limit 的边连通


obj = DistanceLimitedPathsExist_1(6, [[0, 2, 4], [0, 3, 2], [1, 2, 3], [2, 3, 1], [4, 5, 5]])
result = [obj.query(2, 3, 2), obj.query(1, 3, 3), obj.query(2, 0, 3), obj.query(0, 5, 6)]
print(result)  # [True, False, True, False]
