"""
Tarjan 求桥: low[v] > disc[u]

画面:   DFS 进场时给每个点发入场号 disc; low[v] 是 "v 的整棵子树不走父边, 能摸到的最早入场号"。
        如果 v 的子树连一条能回到 u 或 u 祖先的边都没有 (low[v] > disc[u]), 那 u-v 就是唯一通道, 剪了就断: 桥。
动作:   ① 发号 (disc[u] = low[u] = timer, timer += 1)
        ② 往下走 (白点递归, 回来时 low[u] = min(low[u], low[v]))
        ③ 碰回边 (邻居已访问且不是父点: low[u] = min(low[u], disc[v]))
        ④ 判桥 (从 v 回来后 low[v] > disc[u])
动作对代码: 见下面 # ! 注释
签名题: LC-1192 Critical Connections in a Network
决策句: 无向图问 "删哪条边会断" 用它 O(V + E); 不要对每条边删掉再 DFS 一遍, 那是 O(E * (V + E))。
改一行: 和 02 DFS 比, visited 换成 disc 数组, 多一个 low 数组; 关键两行: 回边取 disc[v], 子树回来取 low[v], 再比一比。
        割点 (关节点): 条件改成 low[v] >= disc[u] (根另算: 子树数 >= 2)。
        有重边时要用 "父边编号" 跳过而不是 "父点", 否则重边会被误判成桥 (LC-1192 没有重边)。
"""
from typing import List
import sys

sys.setrecursionlimit(10 ** 6)


def bridges_recursive(n: int, adj: List[List[int]]) -> List[List[int]]:
    disc = [-1] * n
    low = [0] * n
    timer = 0
    res = []

    def dfs(u: int, parent: int) -> None:
        nonlocal timer
        disc[u] = low[u] = timer                        # ! ① 发号
        timer += 1
        for v in adj[u]:
            if v == parent:
                continue                                # 不走父边
            if disc[v] == -1:
                dfs(v, u)                               # ! ② 往下走
                low[u] = min(low[u], low[v])            # ! ② 子树能摸到的最早号, 传回来
                if low[v] > disc[u]:                    # ! ④ 判桥
                    res.append([u, v])
            else:
                low[u] = min(low[u], disc[v])           # ! ③ 回边: 取对方的入场号, 不是 low

    for s in range(n):
        if disc[s] == -1:
            dfs(s, -1)
    return res


def bridges_iterative(n: int, adj: List[List[int]]) -> List[List[int]]:
    """栈里存 (点, 父点, 下一个要看的邻居下标), 模拟递归"""
    disc = [-1] * n
    low = [0] * n
    timer = 0
    res = []
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = timer                        # ! ①
        timer += 1
        stack = [(s, -1, 0)]
        while stack:
            u, parent, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, parent, i + 1)
                v = adj[u][i]
                if v == parent:
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = timer            # ! ①
                    timer += 1
                    stack.append((v, u, 0))             # ! ② 往下走
                else:
                    low[u] = min(low[u], disc[v])       # ! ③ 回边
            else:
                stack.pop()                             # u 的邻居看完了, 相当于递归返回
                if stack:
                    pu = stack[-1][0]
                    low[pu] = min(low[pu], low[u])      # ! ② 传回父点
                    if low[u] > disc[pu]:               # ! ④ 判桥
                        res.append([pu, u])
    return res


def critical_connections(n: int, connections: List[List[int]]) -> List[List[int]]:
    adj = [[] for _ in range(n)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    return bridges_recursive(n, adj)


if __name__ == "__main__":
    conn = [[0, 1], [1, 2], [2, 0], [1, 3]]
    print(critical_connections(4, conn))                                    # [[1, 3]]
    adj = [[] for _ in range(4)]
    for u, v in conn:
        adj[u].append(v)
        adj[v].append(u)
    print(bridges_iterative(4, adj))                                        # [[1, 3]]
    print(bridges_iterative(3, [[1], [0, 2], [1]]))                         # [[1, 2], [0, 1]]
