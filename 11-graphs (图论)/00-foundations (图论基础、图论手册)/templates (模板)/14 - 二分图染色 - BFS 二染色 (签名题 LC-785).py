"""
二分图染色: BFS 二染色

画面:   给每个人发红蓝帽子, 规定有边相连的两人颜色必须不同: 从一个人开始发红, 他的朋友全发蓝,
        朋友的朋友发红... 发到某人时发现他已经戴着和邻居同色的帽子, 就分不开了。
动作:   ① 挑没帽子的人 (color == -1, 每个连通块都要起一次)
        ② 发帽子入队 (color[s] = 0)
        ③ 给邻居发反色 (color[v] = 1 - color[u], 入队)
        ④ 查冲突 (邻居已有帽子且 color[v] == color[u] 就返回 False)
动作对代码: 见下面 # ! 注释
签名题: LC-785 Is Graph Bipartite?
决策句: 题目问 "能否分成两组, 组内没有边 / 有冲突关系的人不能同组" 就是二分图; 图可能不连通, 外层要对每个点起一次。
改一行: 和 03 BFS 比, visited 数组换成 color 数组 (-1 / 0 / 1), 多了一行 "邻居同色就 False"。
        LC-886 Possible Bipartition: 先把 dislikes 建成邻接表 (1-indexed), 然后一模一样。
        LC-1042 Flower Planting With No Adjacent: 颜色从 2 种变 4 种, 贪心挑没被邻居用过的, 不需要判冲突。
"""
from collections import deque
from typing import List


def is_bipartite(graph: List[List[int]]) -> bool:
    n = len(graph)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue                                    # ! ① 每个没帽子的人都起一次 (图可能不连通)
        color[s] = 0
        queue = deque([s])                              # ! ② 发帽子入队
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]             # ! ③ 发反色
                    queue.append(v)
                elif color[v] == color[u]:
                    return False                        # ! ④ 同色冲突
    return True


def possible_bipartition(n: int, dislikes: List[List[int]]) -> bool:
    """LC-886: 1-indexed, 先建邻接表"""
    adj = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)
    return is_bipartite(adj)                            # 0 号空着, 孤立点不影响结果


if __name__ == "__main__":
    print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))               # True
    print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))         # False
    print(possible_bipartition(4, [[1, 2], [1, 3], [2, 4]]))            # True
    print(possible_bipartition(3, [[1, 2], [1, 3], [2, 3]]))            # False
