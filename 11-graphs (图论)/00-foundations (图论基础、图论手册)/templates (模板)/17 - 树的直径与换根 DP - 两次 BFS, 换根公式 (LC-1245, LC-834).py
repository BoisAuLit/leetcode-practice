"""
树的直径与换根 DP: 两次 BFS, 换根公式

画面:   直径: 随便站一个点, 找离它最远的人 A; 再从 A 出发找最远的人 B; A 到 B 就是树上最长的一条路。
        换根: 先以 0 为根算出 "所有点到 0 的距离和"; 把根挪到邻居 v 时, v 那边的 size[v] 个点各近了 1,
        另一边 n - size[v] 个点各远了 1, 所以答案只差一个公式, 不用重算。
动作:   直径 ① 随便挑一点 BFS 找最远点 A
             ② 从 A 再 BFS 找最远点 B, 距离就是直径
        换根 ③ 第一遍 DFS (后序): 算 size[u] 和 down[u] (子树内各点到 u 的距离和), ans[root] = down[root]
             ④ 第二遍 DFS (先序): ans[v] = ans[u] - size[v] + (n - size[v])
动作对代码: 见下面 # ! 注释
签名题: LC-1245 Tree Diameter (两次 BFS); LC-834 Sum of Distances in Tree (换根)
决策句: 树上 "最远两点" 用两次 BFS; "以每个点为根时的某个量" 且暴力是 O(n^2) 时用换根, 把 "根从 u 挪到 v 答案怎么变" 写成一个公式。
改一行: 直径和 03 BFS 比, 只是多跑一次, 第二次的起点换成第一次的最远点。
        换根和 02 DFS 比, 多了一遍自顶向下的 DFS, 核心就 ④ 那一行公式; 公式随题换, 骨架不变。
        LC-310 Minimum Height Trees: 直径的中点 (一个或两个) 就是答案。
"""
from collections import deque
from typing import List, Tuple
import sys

sys.setrecursionlimit(10 ** 6)


def bfs_farthest(adj: List[List[int]], src: int) -> Tuple[int, int]:
    """返回 (离 src 最远的点, 距离)"""
    dist = [-1] * len(adj)
    dist[src] = 0
    queue = deque([src])
    far = src
    while queue:
        u = queue.popleft()
        if dist[u] > dist[far]:
            far = u
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    return far, dist[far]


def tree_diameter(edges: List[List[int]]) -> int:
    """LC-1245: 点数 = 边数 + 1"""
    n = len(edges) + 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    a, _ = bfs_farthest(adj, 0)                         # ! ① 随便挑一点, 找最远点 A
    _, d = bfs_farthest(adj, a)                         # ! ② 从 A 再找最远点, 距离就是直径
    return d


def sum_of_distances_in_tree(n: int, edges: List[List[int]]) -> List[int]:
    """LC-834: ans[u] = 所有点到 u 的距离和"""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    size = [1] * n
    ans = [0] * n

    def down(u: int, parent: int) -> None:              # ! ③ 后序: 先算子树, 再汇总到 u
        for v in adj[u]:
            if v != parent:
                down(v, u)
                size[u] += size[v]
                ans[u] += ans[v] + size[v]              # 子树里每个点到 u 都比到 v 多 1

    def reroot(u: int, parent: int) -> None:            # ! ④ 先序: 父答案已定, 推出子答案
        for v in adj[u]:
            if v != parent:
                ans[v] = ans[u] - size[v] + (n - size[v])   # ! ④ 换根公式: 子树近 1, 其余远 1
                reroot(v, u)

    down(0, -1)
    reroot(0, -1)
    return ans


if __name__ == "__main__":
    print(tree_diameter([[0, 1], [0, 2]]))                                  # 2
    print(tree_diameter([[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]]))          # 4
    print(sum_of_distances_in_tree(6, [[0, 1], [0, 2], [2, 3], [2, 4], [2, 5]]))   # [8, 12, 6, 10, 10, 10]
