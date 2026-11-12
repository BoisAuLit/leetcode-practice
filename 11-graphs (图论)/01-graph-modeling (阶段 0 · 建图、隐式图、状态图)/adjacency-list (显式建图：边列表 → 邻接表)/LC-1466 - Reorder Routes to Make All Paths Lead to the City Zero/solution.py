"""LC-1466 - Reorder Routes to Make All Paths Lead to the City Zero

阶段 0 · 建图(边列表 → 邻接表) ○ 核心变体
题目在问：树上 n-1 条有向道路，最少反转几条，让每个城市都能开到 0 号城市
点是什么：城市   边是什么：道路，每条存两次并打标记：a→b 原方向记 1，b→a 反向记 0
和签名题比改了哪一行：1971 的邻接表只存邻居；本题存 (邻居, 标记)。
    从 0 出发往外遍历整棵树，走到孩子的那条边如果是"原方向"(背离 0)就必须反转，数这种边即可。
    画面：0 是根，所有车都要往根开；一条边从父指向子就是反的。
"""
import sys
from collections import deque
from typing import List

sys.setrecursionlimit(10**5)  # ! n 到 5e4，链状树递归深度就是 n，Solution_1 需要放开

##################################################################################################
##### ! Solution 1: DFS 递归，从 0 出发数"背离 0"的边
##### ! 时间复杂度: O(n)   空间复杂度: O(n)  (邻接表 + 递归栈)
##### ! 适用：树上单源遍历的标准写法，最短；手册点名的写法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in connections:
            adj[a].append((b, 1))  # ! 从 a 走到 b 用的是原方向 a→b：背离 0，要反转
            adj[b].append((a, 0))  # ! 从 b 走到 a 是逆着原方向：b→a 本来就朝 0，不用动

        def dfs(u: int, parent: int) -> int:
            count = 0
            for v, need_flip in adj[u]:
                if v == parent:  # 树上不走回头路，不需要 visited
                    continue
                count += need_flip + dfs(v, u)
            return count

        return dfs(0, -1)


##################################################################################################
##### ! Solution 2: BFS 迭代，同一张带标记的邻接表
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：不想碰递归深度时的安全版本；第一次到达 v 的那条边就是树边
##################################################################################################


class Solution_2:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in connections:
            adj[a].append((b, 1))
            adj[b].append((a, 0))

        visited = [False] * n
        visited[0] = True
        queue = deque([0])
        count = 0
        while queue:
            u = queue.popleft()
            for v, need_flip in adj[u]:
                if visited[v]:
                    continue
                visited[v] = True
                count += need_flip  # ! 树上每个点只会被到达一次，这条边的标记直接累加
                queue.append(v)
        return count


##################################################################################################
##### ! Solution 3: 无向邻接表 + 有向边集合，遍历时查 (u, v) 在不在集合里
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：另一种常见写法，建图时不打标记，遍历时查原边方向；逻辑一样，多一个 set
##################################################################################################


class Solution_3:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        directed = set()  # ! 原始有向边 (a, b)
        adj = [[] for _ in range(n)]
        for a, b in connections:
            directed.add((a, b))
            adj[a].append(b)
            adj[b].append(a)

        count = 0
        stack = [(0, -1)]  # 显式栈的 DFS，(当前点, 父亲)
        while stack:
            u, parent = stack.pop()
            for v in adj[u]:
                if v == parent:
                    continue
                if (u, v) in directed:  # ! 原边是 u→v，从父指向子，背离 0，要反转
                    count += 1
                stack.append((v, u))
        return count


s = Solution_1()
n = 6
connections = [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]
result = s.minReorder(n, connections)
print(result)  # 3
