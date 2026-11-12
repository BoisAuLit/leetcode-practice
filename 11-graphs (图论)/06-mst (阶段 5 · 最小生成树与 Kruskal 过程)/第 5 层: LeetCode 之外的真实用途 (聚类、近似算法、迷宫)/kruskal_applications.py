"""第 5 层: MST 在 LeetCode 之外的真实用途（可运行 demo）

这一层没有 LeetCode 题，但面试聊项目、以后做 AI / RAG 都会用到。
三个用途共用同一个 Kruskal：排序 + 并查集 + 只要不成环的边。区别只在"什么时候停"和"边权是什么"。

    1. 单链接聚类 (single-linkage)：Kruskal 跑到剩 k 派就停  → k 个簇
    2. TSP 2 倍近似：先建 MST，再沿树做先序遍历         → 不超过最优 2 倍的回路
    3. 随机迷宫：给每道墙一个随机权重跑 Kruskal         → 没有环、处处可达的迷宫

跑一下：python3 kruskal_applications.py
"""
from itertools import combinations
from math import dist
import random


class UnionFind:  # 和题库里的模板一个字都不改：路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n  # ! 还剩几派，聚类要靠它决定什么时候停

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
        self.count -= 1
        return True


# ==================================================================================================
# ! 用途 1: 单链接层次聚类 —— Kruskal 在"剩 k 派"时停下
# ! 它保证的是"不同簇之间的最小距离尽量大"，因为砍掉的恰好是 MST 上最长的 k-1 条边。
# ! 做 embedding 去重、文档聚类时是基础方法之一：点换成向量，距离换成余弦距离即可。
# ==================================================================================================


def single_linkage(points: list[tuple[float, ...]], k: int) -> list[list[int]]:
    """把 points 分成 k 个簇，返回每个簇的下标列表。"""
    n = len(points)
    if k >= n:
        return [[i] for i in range(n)]
    edges = sorted((dist(points[i], points[j]), i, j) for i, j in combinations(range(n), 2))
    uf = UnionFind(n)
    for _, i, j in edges:
        if uf.count == k:  # ! 唯一的改动：不是跑到剩 1 派，而是剩 k 派就收手
            break
        uf.union(i, j)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(uf.find(i), []).append(i)
    return sorted(groups.values())


def mst_edges(points: list[tuple[float, ...]]) -> list[tuple[float, int, int]]:
    """完整跑完 Kruskal，返回 MST 的 n-1 条边（按权重升序）。"""
    n = len(points)
    uf = UnionFind(n)
    kept = []
    for w, i, j in sorted((dist(points[i], points[j]), i, j) for i, j in combinations(range(n), 2)):
        if uf.union(i, j):
            kept.append((w, i, j))
    return kept


# ==================================================================================================
# ! 用途 2: TSP 的 2 倍近似 —— 沿 MST 做先序遍历
# ! TSP 要最短的、经过所有点一次的回路，没有快速精确解。但：
# !   MST 总长 <= 最优回路（回路去掉一条边就是一棵生成树，而 MST 是最便宜的生成树）
# !   沿 MST 每条边走两次得到一条闭合散步，长度 = 2 * MST <= 2 * 最优
# !   先序遍历相当于把重复经过的点跳过，三角不等式保证跳过不会更长
# ==================================================================================================


def tsp_two_approx(points: list[tuple[float, ...]]) -> tuple[list[int], float]:
    """返回 (回路的访问顺序, 回路总长)，总长保证 <= 2 * 最优。"""
    n = len(points)
    if n <= 1:
        return list(range(n)), 0.0
    children: list[list[int]] = [[] for _ in range(n)]
    for _, i, j in mst_edges(points):
        children[i].append(j)
        children[j].append(i)
    tour, seen, stack = [], [False] * n, [0]
    while stack:  # ! 先序遍历（迭代版），每个点第一次被访问时记进回路
        u = stack.pop()
        if seen[u]:
            continue
        seen[u] = True
        tour.append(u)
        for v in reversed(children[u]):
            if not seen[v]:
                stack.append(v)
    total = sum(dist(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n))
    return tour, total


# ==================================================================================================
# ! 用途 3: 随机迷宫 —— 给每道墙一个随机权重跑 Kruskal
# ! 格子是点，相邻格之间的"墙"是边。Kruskal 留下的 n-1 条边就是要打通的墙：
# ! 生成树没有环（迷宫无回路）且连通（任意两格都走得到），正是一张迷宫该有的样子。
# ==================================================================================================


def random_maze(rows: int, cols: int, seed: int | None = None) -> set[frozenset[int]]:
    """返回要打通的墙的集合，每道墙是 frozenset({格子编号 a, 格子编号 b})。"""
    rng = random.Random(seed)
    walls = []
    for r in range(rows):
        for c in range(cols):
            u = r * cols + c
            if c + 1 < cols:
                walls.append((rng.random(), u, u + 1))
            if r + 1 < rows:
                walls.append((rng.random(), u, u + cols))
    walls.sort()  # ! 权重是随机数，所以"最便宜的边"就是"随机挑一道墙"
    uf = UnionFind(rows * cols)
    return {frozenset((u, v)) for _, u, v in walls if uf.union(u, v)}


def draw_maze(rows: int, cols: int, opened: set[frozenset[int]]) -> str:
    out = ["+" + "---+" * cols]
    for r in range(rows):
        mid, bot = "|", "+"
        for c in range(cols):
            u = r * cols + c
            right_open = c + 1 < cols and frozenset((u, u + 1)) in opened
            down_open = r + 1 < rows and frozenset((u, u + cols)) in opened
            mid += "   " + (" " if right_open else "|")
            bot += ("   " if down_open else "---") + "+"
        out += [mid, bot]
    return "\n".join(out)


# ==================================================================================================
# ! 做不到的事，一起记住
# !   有向图的"最小生成树"叫最小树形图，要用朱-刘 / Edmonds，Prim 和 Kruskal 都不适用
# !   MST 上两点间的路径不是最短路（它保证的是瓶颈最小，不是总和最小），要最短得用 Dijkstra
# !   限制度数的生成树、Steiner tree（只连通指定的几个点）都是 NP-hard，MST 只能给近似
# ==================================================================================================


if __name__ == "__main__":
    pts = [(0.0, 0.0), (0.4, 0.2), (0.1, 0.5), (5.0, 5.0), (5.3, 4.8), (9.0, 0.0)]

    print("用途 1: 单链接聚类，k = 3")
    print("  ", single_linkage(pts, 3))  # [[0, 1, 2], [3, 4], [5]]
    edges = mst_edges(pts)                       # MST 的 n-1 条边，升序
    uf = UnionFind(len(pts))
    for _, i, j in edges[:-2]:                   # ! 砍掉最贵的 2 条 = 分成 3 个簇
        uf.union(i, j)
    cut = {}
    for i in range(len(pts)):
        cut.setdefault(uf.find(i), []).append(i)
    print("   砍掉 MST 最贵的 2 条边：", sorted(cut.values()),
          "→ 和聚类结果一致" if sorted(cut.values()) == single_linkage(pts, 3) else "→ 不一致")

    print("\n用途 2: TSP 2 倍近似")
    tour, total = tsp_two_approx(pts)
    print(f"   回路 {tour}  总长 {total:.3f}  (MST 总长 {sum(w for w, _, _ in mst_edges(pts)):.3f})")

    print("\n用途 3: 随机迷宫 6 x 10")
    print(draw_maze(6, 10, random_maze(6, 10, seed=42)))
