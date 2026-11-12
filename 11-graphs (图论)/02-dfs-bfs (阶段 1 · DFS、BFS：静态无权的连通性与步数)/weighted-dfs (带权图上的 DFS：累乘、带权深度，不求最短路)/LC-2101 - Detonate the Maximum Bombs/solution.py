"""LC-2101 - Detonate the Maximum Bombs

阶段 1 · 带权图上的 DFS（带权深度，不求最短路） △ 扩展
题目在问：只能手动引爆一个炸弹，连锁反应最多能炸掉几个
点是什么：一个炸弹   边是什么：有向边 i -> j，当 j 的圆心落在 i 的爆炸半径内（距离用平方比较，不开根号）
和签名题比改了哪一行：200 的图是网格现成的，这里要自己按距离建有向图（O(n^2) 两两比）；
    然后从每个点各做一次 DFS 数可达点，取最大。注意是有向图：i 能炸到 j 不代表 j 能炸到 i，
    所以每个起点要用一套新的 visited，不能像数岛那样全局复用
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: 建有向图 + 从每个点 DFS 数可达点
##### ! 时间复杂度: O(n^3)   建图 O(n^2)，每个起点 DFS O(n + E)，E 最多 n^2   空间复杂度: O(n^2)
##### ! 适用：n <= 100，枚举每个起点完全够用；手册点名的解法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        n = len(bombs)
        adj = [[] for _ in range(n)]
        for i, (xi, yi, ri) in enumerate(bombs):
            for j, (xj, yj, _) in enumerate(bombs):
                # ! 有向边 i -> j：j 的圆心在 i 的半径内。坐标到 1e5，平方到 2e10，Python 整数无压力
                if i != j and (xi - xj) ** 2 + (yi - yj) ** 2 <= ri * ri:
                    adj[i].append(j)

        def dfs(u: int, visited: List[bool]) -> int:
            visited[u] = True
            count = 1
            for v in adj[u]:
                if not visited[v]:
                    count += dfs(v, visited)
            return count  # ! 返回从 u 连锁炸掉的个数（含 u 自己）

        ans = 0
        for i in range(n):
            ans = max(ans, dfs(i, [False] * n))  # ! 有向图：每个起点一套新 visited
        return ans


##################################################################################################
##### ! Solution 2: 建有向图 + 从每个点 BFS 数可达点
##### ! 时间复杂度: O(n^3)   空间复杂度: O(n^2)
##### ! 适用：和 DFS 完全等价（只问可达不问步数）；不想碰递归时用队列
##################################################################################################


class Solution_2:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        n = len(bombs)
        adj = [[] for _ in range(n)]
        for i, (xi, yi, ri) in enumerate(bombs):
            for j, (xj, yj, _) in enumerate(bombs):
                if i != j and (xi - xj) ** 2 + (yi - yj) ** 2 <= ri * ri:
                    adj[i].append(j)

        ans = 0
        for i in range(n):
            visited = [False] * n
            visited[i] = True
            queue = deque([i])
            count = 0
            while queue:
                u = queue.popleft()
                count += 1  # ! 弹出一个就是炸掉一个
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
            ans = max(ans, count)
        return ans


s = Solution_1()
bombs = [[2, 1, 3], [6, 1, 4]]
result = s.maximumDetonation(bombs)
print(result)  # 2

bombs = [[1, 1, 5], [10, 10, 5]]
result = s.maximumDetonation(bombs)
print(result)  # 1

bombs = [[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]]
result = s.maximumDetonation(bombs)
print(result)  # 5
