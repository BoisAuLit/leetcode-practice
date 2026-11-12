"""LC-0834 - Sum of Distances in Tree

阶段 6 · 特殊结构 · 树上问题（换根 DP） △ 扩展
题目在问：对每个点 i，求它到其他所有点的距离之和，一次全部算出来
点是什么：节点 0..n-1   边是什么：edges 里的无向边（树）
和签名题比改了哪一行：1245 只要一个全局数（直径），这里每个点都要一个答案；
    暴力每个点 BFS 一次是 O(n²)，换根 DP 两遍遍历 O(n)：
    第一遍后序：size[v] = v 的子树大小，顺便算出 ans[root]
    第二遍先序：根从 parent 挪到 child，子树里 size[child] 个点各近 1，其余 n - size[child] 个点各远 1
        ans[child] = ans[parent] - size[child] + (n - size[child])
"""
import sys
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: 换根 DP（迭代版，BFS 序代替递归）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：n 到 3e4，不碰递归上限最稳；BFS 序正着扫 = 先序，倒着扫 = 后序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # ! 第 0 步：以 0 为根 BFS 一遍，记下每个点的 parent 和访问顺序 order
        parent = [-1] * n
        order = []
        seen = [False] * n
        seen[0] = True
        q = deque([0])
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    parent[v] = u
                    q.append(v)

        # ! 第 1 步（后序 = 倒着扫 order，孩子先算完）：size[u] 和 "u 到它子树里所有点的距离和"
        size = [1] * n
        ans = [0] * n
        for u in reversed(order):
            if u == 0:
                continue
            p = parent[u]
            size[p] += size[u]
            ans[p] += ans[u] + size[u]  # ! u 子树里每个点到 p 都比到 u 远 1，共 size[u] 个点
        # ! 扫完 ans[0] 就是根的答案（0 的子树 = 整棵树）

        # ! 第 2 步（先序 = 正着扫 order，父亲先算完）：换根公式
        for u in order:
            if u == 0:
                continue
            p = parent[u]
            ans[u] = ans[p] - size[u] + (n - size[u])  # ! 根从 p 挪到 u：子树里的点近 1，子树外的点远 1
        return ans


##################################################################################################
##### ! Solution 2: 换根 DP（递归版，两个 DFS）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：教科书写法，更好读；链状树递归深度 = n，要先调递归上限
##################################################################################################


class Solution_2:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        sys.setrecursionlimit(max(10000, 2 * n))
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        size = [1] * n
        ans = [0] * n

        def dfs_size(u: int, parent: int) -> None:  # ! 后序：先把孩子算完，再汇总到 u
            for v in adj[u]:
                if v != parent:
                    dfs_size(v, u)
                    size[u] += size[v]
                    ans[u] += ans[v] + size[v]

        def dfs_reroot(u: int, parent: int) -> None:  # ! 先序：u 的答案已定，推给每个孩子
            for v in adj[u]:
                if v != parent:
                    ans[v] = ans[u] - size[v] + (n - size[v])
                    dfs_reroot(v, u)

        dfs_size(0, -1)
        dfs_reroot(0, -1)
        return ans


##################################################################################################
##### ! Solution 3: 暴力，每个点 BFS 一次（baseline）
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：理解题意、验证换根公式；n = 3e4 时 9e8 步会超时
##################################################################################################


class Solution_3:
    def sumOfDistancesInTree(self, n: int, edges: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        ans = [0] * n
        for src in range(n):  # ! 每个点当一次起点，BFS 把距离全加起来
            dist = [-1] * n
            dist[src] = 0
            q = deque([src])
            while q:
                u = q.popleft()
                ans[src] += dist[u]
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)
        return ans


s = Solution_1()
n = 6
edges = [[0, 1], [0, 2], [2, 3], [2, 4], [2, 5]]
result = s.sumOfDistancesInTree(n, edges)
print(result)  # [8, 12, 6, 10, 10, 10]

n = 1
edges = []
result = s.sumOfDistancesInTree(n, edges)
print(result)  # [0]

n = 2
edges = [[1, 0]]
result = s.sumOfDistancesInTree(n, edges)
print(result)  # [1, 1]
