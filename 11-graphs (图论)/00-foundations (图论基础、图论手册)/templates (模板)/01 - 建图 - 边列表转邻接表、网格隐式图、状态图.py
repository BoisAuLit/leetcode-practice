"""
阶段 0 建图: 边列表转邻接表, 网格隐式图, 状态图

画面:   拿到题先画通讯录: 每个人一页, 页上写他认识谁 (以及关系多重)。
        网格和密码锁不用真的画, 问到谁的邻居时现算就行。
动作:   ① 开本子 (n 页, 编号从 1 开始的多开一格)
        ② 记一笔 (有向记一边, 无向记两边, 带权把 w 一起记)
        ③ 现算邻居 (网格: 上下左右四个格; 状态图: 拨一位)
动作对代码: 见下面 # ! 注释
签名题: LC-1971 Find if Path Exists in Graph (边列表建邻接表 + DFS/BFS)
        LC-752 Open the Lock (状态图: 点 = 四位串, 边 = 拨一位)
决策句: 输入是边列表就建邻接表; 输入是网格或字符串就不建图, 写一个 neighbors 函数代替。
改一行: 无向图和有向图只差 adj[v].append(u) 这一行; 带权和无权只差存 (v, w) 还是 v。
"""
from typing import List, Tuple, Iterator


def build_adj(n: int, edges: List[List[int]], directed: bool = False) -> List[List[int]]:
    adj = [[] for _ in range(n)]                # ! ① 开本子
    for u, v in edges:
        adj[u].append(v)                        # ! ② 记一笔
        if not directed:
            adj[v].append(u)                    # ! 无向图两边都记; 有向图删掉这行
    return adj


def build_adj_weighted(n: int, edges: List[List[int]], directed: bool = True) -> List[List[Tuple[int, int]]]:
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))                   # ! 带权: 把 w 一起记
        if not directed:
            adj[v].append((u, w))
    return adj


def build_adj_1_indexed(n: int, edges: List[List[int]]) -> List[List[int]]:
    adj = [[] for _ in range(n + 1)]            # ! 编号 1..n: 多开一格, 0 号空着不用
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def grid_neighbors(r: int, c: int, rows: int, cols: int) -> Iterator[Tuple[int, int]]:
    # ! ③ 网格是隐式图: 不建表, 要邻居时现算
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:   # ! 越界检查放在生成器里, 调用方不用再写
            yield nr, nc


def lock_neighbors(state: str) -> Iterator[str]:
    # ! ③ 状态图 (LC-752): 点 = 一个四位串, 边 = 某一位拨 +1 或 -1
    for i in range(4):
        d = int(state[i])
        for nd in ((d + 1) % 10, (d - 1) % 10):
            yield state[:i] + str(nd) + state[i + 1:]


if __name__ == "__main__":
    print(build_adj(4, [[0, 1], [1, 2], [2, 0], [3, 2]]))                   # [[1, 2], [0, 2], [1, 0, 3], [2]]
    print(build_adj(4, [[0, 1], [1, 2], [2, 0], [3, 2]], directed=True))    # [[1], [2], [0], [2]]
    print(build_adj_weighted(3, [[0, 1, 5], [1, 2, 7]]))                    # [[(1, 5)], [(2, 7)], []]
    print(build_adj_1_indexed(3, [[1, 2], [2, 3]]))                         # [[], [2], [1, 3], [2]]
    print(list(grid_neighbors(0, 0, 3, 3)))                                 # [(1, 0), (0, 1)]
    print(sorted(lock_neighbors("0000")))
    # ['0001', '0009', '0010', '0090', '0100', '0900', '1000', '9000']
