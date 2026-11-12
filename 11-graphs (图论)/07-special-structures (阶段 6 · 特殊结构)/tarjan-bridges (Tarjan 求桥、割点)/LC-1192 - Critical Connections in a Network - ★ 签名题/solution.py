"""LC-1192 - Critical Connections in a Network

阶段 6 · 特殊结构 · Tarjan 求桥 ★ 签名题
题目在问：删掉哪些连线会让网络断开，把这些"桥"全部找出来
点是什么：服务器 0..n-1   边是什么：connections 里的无向连线（题目保证连通、无重边）
和签名题比改了哪一行：本题就是签名题
核心画面：DFS 给每个点盖时间戳 disc；low[v] = v 的子树不走父边能回到的最早时间戳；
    low[v] > disc[u] 说明 v 那边绕不回 u 或更早的祖先，(u, v) 就是桥
"""
import sys
from typing import List

##################################################################################################
##### ! Solution 1: Tarjan 求桥（递归版）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：最清楚的写法，面试默认写这个；n 到 1e5 要先调递归上限
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        sys.setrecursionlimit(max(10000, 2 * n))  # ! 链状图递归深度 = n，默认 1000 不够

        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)

        disc = [-1] * n  # ! 第几个被访问到（时间戳），-1 = 还没来过
        low = [0] * n  # ! 不走父边，从 u 的子树能回到的最早时间戳
        timer = 0
        bridges = []

        def dfs(u: int, parent: int) -> None:
            nonlocal timer
            disc[u] = low[u] = timer
            timer += 1
            for v in adj[u]:
                if v == parent:  # ! 不走回父边（无重边时记父节点就够；有重边要记边 id）
                    continue
                if disc[v] == -1:  # ! 树边：先递归，再用孩子的 low 更新自己
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:  # ! v 的子树绕不回 u 或更早 → (u, v) 是桥
                        bridges.append([u, v])
                else:  # ! 回边：v 是祖先，能回到 disc[v] 这么早
                    low[u] = min(low[u], disc[v])

        dfs(0, -1)  # ! 题目保证连通，从 0 出发一次就够
        return bridges


##################################################################################################
##### ! Solution 2: Tarjan 求桥（迭代版，显式栈）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：不想碰递归上限时；ptr[u] 记录"递归暂停在第几个邻居"，弹栈时才把 low 交给父亲
##################################################################################################


class Solution_2:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)

        disc = [-1] * n
        low = [0] * n
        parent = [-1] * n
        ptr = [0] * n  # ! ptr[u] = u 已经看过几个邻居，相当于递归里的"断点"
        bridges = []

        disc[0] = low[0] = 0
        timer = 1
        stack = [0]
        while stack:
            u = stack[-1]
            if ptr[u] < len(adj[u]):  # ! 还有邻居没看：看一个，指针往前挪
                v = adj[u][ptr[u]]
                ptr[u] += 1
                if v == parent[u]:
                    continue
                if disc[v] == -1:  # ! 树边：进栈 = 递归下去
                    parent[v] = u
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append(v)
                else:  # ! 回边
                    low[u] = min(low[u], disc[v])
            else:  # ! 邻居看完 = 递归返回：把 low 交给父亲，顺便判桥
                stack.pop()
                p = parent[u]
                if p != -1:
                    low[p] = min(low[p], low[u])
                    if low[u] > disc[p]:
                        bridges.append([p, u])
        return bridges


##################################################################################################
##### ! Solution 3: 暴力，删一条边测连通（baseline）
##### ! 时间复杂度: O(E · (V + E))   空间复杂度: O(V + E)
##### ! 适用：只用来理解题意和验证 Tarjan；E 到 1e5 会超时
##################################################################################################


class Solution_3:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)

        def connected_without(a: int, b: int) -> bool:  # ! 不走 (a, b) 这条边，从 0 还能不能走遍全图
            seen = [False] * n
            seen[0] = True
            stack = [0]
            count = 1
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if (u == a and v == b) or (u == b and v == a):
                        continue
                    if not seen[v]:
                        seen[v] = True
                        count += 1
                        stack.append(v)
            return count == n

        return [[u, v] for u, v in connections if not connected_without(u, v)]


s = Solution_1()
n = 4
connections = [[0, 1], [1, 2], [2, 0], [1, 3]]
result = s.criticalConnections(n, connections)
print(result)  # [[1, 3]]

n = 2
connections = [[0, 1]]
result = s.criticalConnections(n, connections)
print(result)  # [[0, 1]]
