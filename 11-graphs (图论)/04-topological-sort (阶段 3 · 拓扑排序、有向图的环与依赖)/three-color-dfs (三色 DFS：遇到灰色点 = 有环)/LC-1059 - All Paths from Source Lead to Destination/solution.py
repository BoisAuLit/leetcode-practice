"""LC-1059 - All Paths from Source Lead to Destination

合并自 2 个解法文件:
  1. 1059 - A - All Paths Source Lead to Destination - DFS 3-state (WHITE-GRAY-BLACK).py
  2. 1059 - B - All Paths Source Destination - ⭐️ DFS 教科书.py

阶段 3 · 拓扑排序 · 三色 DFS（遇到灰色点 = 有环）
题目在问：从 source 出发的每一条路都必须在 destination 停下：没环、没有别的死胡同、destination 自己出度为 0
点是什么：一个结点   边是什么：有向边 a -> b
和签名题比改了哪一行：802 的三色 DFS 加两个判断：遇到灰色 = 有环 False；出度为 0 的点必须 == destination
"""

from typing import List

from collections import defaultdict
from collections import deque


# ============================================================================
# Solution 1: DFS_3_state_WHITE_GRAY_BLACK    (原文件: 1059 - A - All Paths Source Lead to Destination - DFS 3-state (WHITE-GRAY-BLACK).py)
# ============================================================================

n_1 = 4

edges_1 = [[0, 1], [0, 2], [1, 3], [2, 3]]

source_1 = 0

destination_1 = 3

##################################################################################################
##### ! Solution 1: 三色 DFS（WHITE / GRAY / BLACK）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)   E = len(edges)
##### ! 适用：官方题解写法；灰 = 还在当前路径上，碰到灰就是环；叶子（出度 0）必须是 destination
##### ! 参数名 n_1/edges_1 是合并时改的，LeetCode 按位置传参所以能跑，粘贴时建议改回 n/edges/source/destination
##################################################################################################


class Solution_1_DFS_3_state_WHITE_GRAY_BLACK:
    WHITE = 0 # Unvisited
    GRAY = 1 # Itself and its descendants are being processed
    BLACK = 2 # 

    def leadsToDestination(
        self, n_1: int, edges_1: List[List[int]], source_1: int, destination_1: int
    ) -> bool:
        graph = defaultdict(list)
        for x, y in edges_1:
            graph[x].append(y)

        # ! Initially, all nodes are WHITE
        return self.leadsToDest(graph, source_1, destination_1, [Solution_1_DFS_3_state_WHITE_GRAY_BLACK.WHITE] * n_1)

    def leadsToDest(self, graph, node, dest, states):
        # If the state is GRAY, this is a backward edge and hence, it creates a Loop.
        if states[node] is not Solution_1_DFS_3_state_WHITE_GRAY_BLACK.WHITE:
            return states[node] == Solution_1_DFS_3_state_WHITE_GRAY_BLACK.BLACK

        # If this is a leaf node, it should be equal to the destination_1.
        if not graph[node]:
            return node == dest

        # Now, we are processing this node. So we mark it as GRAY.
        states[node] = Solution_1_DFS_3_state_WHITE_GRAY_BLACK.GRAY

        for next_node in graph[node]:
            # If we get a `false` from any recursive call on the neighbors, we short circuit and return from there.
            if not self.leadsToDest(graph, next_node, dest, states):
                return False

        # Recursive processing done for the node. We mark it BLACK.
        states[node] = Solution_1_DFS_3_state_WHITE_GRAY_BLACK.BLACK
        return True

# ============================================================================
# Solution 2: DFS    (原文件: 1059 - B - All Paths Source Destination - ⭐️ DFS 教科书.py)
# ============================================================================

n_2 = 4

edges_2 = [[0, 1], [0, 2], [1, 3], [2, 3]]

source_2 = 0

destination_2 = 3

##################################################################################################
##### ! Solution 2: 三色 DFS 精简版（visited: 0 未访问 / -1 在路径上 / 1 已确认安全）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：和 Solution 1 同一思路，更短；邻接表用 set 顺手去掉重边
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution（原文件名里用户标了 ⭐️ 教科书，尊重）
##################################################################################################


class Solution_2_DFS:
    def leadsToDestination(
        self, n_2: int, edges_2: List[List[int]], source_2: int, destination_2: int
    ) -> bool:
        g = defaultdict(set)
        visited = defaultdict(int)
        for [x, y] in edges_2:
            g[x].add(y)

        def dfs(node):
            if visited[node] == 1:
                return True
            elif visited[node] == -1:
                return False
            elif len(g[node]) == 0:
                return node == destination_2
            else:
                visited[node] = -1
                for child in g[node]:
                    if not dfs(child):
                        return False
                visited[node] = 1
                return True

        return dfs(source_2)


##################################################################################################
##### ! Solution 3: 反向图上 Kahn（802 的写法：从 destination 往回传播"安全"）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：不想递归（n、E 到 1e4 时深度可能爆）；一个点所有出边都指向安全点，它才安全
##################################################################################################


class Solution_3:
    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        rev = [[] for _ in range(n)]  # ! 反向邻接表：rev[b] 里是所有指向 b 的点
        outdeg = [0] * n
        for a, b in edges:
            rev[b].append(a)
            outdeg[a] += 1

        if outdeg[destination] != 0:
            return False  # ! 终点必须是死胡同，否则走到了还得继续走

        # ! 安全 = 从它出发每条路都到 destination。一开始只有 destination 安全；
        # ! 别的死胡同（出度 0 但不是终点）和环上的点永远进不了队列
        safe = [False] * n
        safe[destination] = True
        q = deque([destination])
        while q:
            u = q.popleft()
            for p in rev[u]:
                outdeg[p] -= 1  # ! p 的一条出边已经确认安全
                if outdeg[p] == 0:  # ! 所有出边都安全，p 才安全
                    safe[p] = True
                    q.append(p)
        return safe[source]


if __name__ == "__main__":

    # --- Solution 1: DFS_3_state_WHITE_GRAY_BLACK ---
    s = Solution_1_DFS_3_state_WHITE_GRAY_BLACK()
    result = s.leadsToDestination(n_1, edges_1, source_1, destination_1)
    print(result)

    # --- Solution 2: DFS ---
    s = Solution_2_DFS()
    result = s.leadsToDestination(n_2, edges_2, source_2, destination_2)
    print(result)
