"""
并查集: 路径减半 + 按 size 合并, union 返回 bool

画面:   班里几拨人各认一个老大; 两拨人握手就让小拨改认大拨的老大;
        问两个人是不是一伙, 各自追到老大比一比就行。
动作:   ① 认老大 (find: 一路往上追, 顺手把路缩短)
        ② 握手 (union: 老大相同说明早是一伙, 返回 False; 不同就把小拨挂到大拨下, 返回 True)
        ③ 数拨数 (count 初始 n, 每次握手成功 -1)
动作对代码: 见下面 # ! 注释
签名题: LC-323 Number of Connected Components (块数 = n - 成功合并次数)
        LC-684 Redundant Connection (union 返回 False 的那条边就是多余边, 它会成环)
        LC-305 Number of Islands II (动态加格子: 新格子先 +1, 每次成功合并 -1)
决策句: 边一条条加进来, 中途要回答 "有几块 / 是不是一伙 / 这条边会不会成环" 就用它; 图一开始就定好且只问一次, 02 DFS 更短。
改一行: 和 02 DFS 数连通块比, 不遍历图, 只对每条边做一次 union; 答案从 "倒了几桶颜料" 变成 "n 减成功合并次数"。
        LC-721 Accounts Merge: union 完后按 find(x) 分组输出。
        LC-990 Satisfiability of Equality Equations: 先把所有 == 做 union, 再对每个 != 检查 find 是否相同。
"""
from typing import List


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))                    # 一开始每个人认自己当老大
        self.size = [1] * n
        self.count = n                                  # ! ③ 数拨数: 一开始各自一拨

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]    # ! ① 路径减半: 每走一步把自己挂到爷爷下面
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                # ! ② 早是一伙: 这条边多余 (加上就成环)
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                             # ! 按 size: 保证 ra 是大拨
        self.parent[rb] = ra                            # ! ② 小拨挂到大拨下
        self.size[ra] += self.size[rb]
        self.count -= 1                                 # ! ③ 握手成功, 拨数 -1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


def count_components(n: int, edges: List[List[int]]) -> int:
    """LC-323: 块数 = n - 成功合并次数"""
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count


def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """LC-684: 1-indexed, 第一条让 union 失败的边就是答案"""
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):                          # ! ② 返回 False = 两头早已连通 = 这条边成环
            return [u, v]
    return []


def num_islands2(m: int, n: int, positions: List[List[int]]) -> List[int]:
    """LC-305: 每放一个格子, 回答当前岛数"""
    uf = UnionFind(m * n)
    land = set()
    count = 0
    res = []
    for r, c in positions:
        idx = r * n + c
        if idx in land:
            res.append(count)
            continue
        land.add(idx)
        count += 1                                      # ! 新格子先算一座新岛
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and nr * n + nc in land:
                if uf.union(idx, nr * n + nc):          # ! 和邻居合并成功, 岛数 -1
                    count -= 1
        res.append(count)
    return res


if __name__ == "__main__":
    print(count_components(5, [[0, 1], [1, 2], [3, 4]]))                    # 2
    print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))              # [2, 3]
    print(num_islands2(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]))             # [1, 1, 2, 3]
