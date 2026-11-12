"""
Kruskal: 排序 + 并查集

画面:   所有线按价钱排队, 从最便宜的开始逐条审批: 两头已经连通的线驳回 (买了会成环), 否则买下。
        买够 n - 1 条就停; 线审完了还没买够, 说明图本来就不连通。
动作:   ① 排队 (edges 按 w 排序)
        ② 逐条审批 (union 成功就买, 失败就跳过)
        ③ 记账 (cost += w, used += 1)
        ④ 验收 (used < n - 1 说明图不连通, 返回 -1)
动作对代码: 见下面 # ! 注释
签名题: LC-1584 Min Cost to Connect All Points (给坐标: 先生成 n(n-1)/2 条边再跑)
        LC-1697 Checking Existence of Edge Length Limited Paths (离线阈值查询: 查询也排序, 边按阈值逐步加入)
决策句: 给边列表用 Kruskal; 给坐标 (稠密完全图) 用 13 Prim 数组版更省; 问 "只走权小于 x 的边能否连通" 这类查询, 把查询排序后跑一遍 Kruskal 过程。
改一行: 和 05 并查集比, 只多了 "先按 w 排序" 这一行, 并查集本身不变。
        LC-1697: 不收集 MST, 而是把查询按 limit 排序, 每个查询之前把 w < limit 的边全部 union, 再问 connected。
        LC-1135 Connecting Cities With Minimum Cost: 签名题的 1-indexed 边列表版本。
"""
from typing import List


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


def kruskal(n: int, edges: List[List[int]]) -> int:
    """edges 是 [u, v, w]; 返回 MST 总权, 图不连通返回 -1"""
    uf = UnionFind(n)
    cost, used = 0, 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):   # ! ① 排队
        if uf.union(u, v):                              # ! ② 审批: 两头没连通才买
            cost += w                                   # ! ③ 记账
            used += 1
            if used == n - 1:
                break                                   # 买够了, 后面的线不用看
    return cost if used == n - 1 else -1                # ! ④ 验收


def min_cost_connect_points(points: List[List[int]]) -> int:
    """LC-1584: 坐标 -> 完全图的边列表 -> Kruskal"""
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append([i, j, w])
    return kruskal(n, edges)


def distance_limited_paths_exist(n: int, edge_list: List[List[int]], queries: List[List[int]]) -> List[bool]:
    """LC-1697 离线: 查询按 limit 排序, 边按 w 排序, 双指针逐步 union"""
    uf = UnionFind(n)
    edge_list.sort(key=lambda e: e[2])                  # ! ① 边排队
    order = sorted(range(len(queries)), key=lambda i: queries[i][2])   # ! ① 查询也排队 (记住原下标)
    res = [False] * len(queries)
    i = 0
    for qi in order:
        p, q, limit = queries[qi]
        while i < len(edge_list) and edge_list[i][2] < limit:
            uf.union(edge_list[i][0], edge_list[i][1])  # ! ② 把所有 w < limit 的边加进来
            i += 1
        res[qi] = uf.find(p) == uf.find(q)              # 此时 "连通" 就是 "存在一条每条边都 < limit 的路"
    return res


if __name__ == "__main__":
    print(min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # 20
    print(kruskal(3, [[0, 1, 1]]))                                              # -1
    print(distance_limited_paths_exist(3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]],
                                       [[0, 1, 2], [0, 2, 5]]))                 # [False, True]
