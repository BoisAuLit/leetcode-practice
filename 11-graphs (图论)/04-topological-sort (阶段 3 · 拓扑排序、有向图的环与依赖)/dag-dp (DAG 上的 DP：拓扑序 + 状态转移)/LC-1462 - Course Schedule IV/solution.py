"""LC-1462 - Course Schedule IV

阶段 3 · DAG 上的 DP（拓扑序 + 状态转移） △ 扩展
题目在问：给先修关系（题目保证无环），多组查询"u 是不是 v 的先修（直接或间接）"
点是什么：课程 0..n-1   边是什么：[u, v] 是一条 u -> v，u 先修
和签名题比改了哪一行：207 的 Kahn 只数出队个数；这里出队时多做一步 DP：
                     anc[v] |= anc[u] | {u}，每个点攒下自己的全部祖先，查询就是一次 in
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: Kahn + 每个点维护祖先集合
##### ! 时间复杂度: O(V * E + Q)（每条边合并一次集合，集合最大 V）   空间复杂度: O(V^2)
##### ! 适用：多组可达性查询、图是 DAG；n 只有 100，集合随便开。想更快可把 set 换成 int 当 bitset：anc[v] |= anc[u] | (1 << u)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        n = numCourses
        graph = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v in prerequisites:
            graph[u].append(v)
            indeg[v] += 1

        anc = [set() for _ in range(n)]  # anc[v] = v 的全部先修（直接 + 间接）
        q = deque(v for v in range(n) if indeg[v] == 0)
        while q:
            u = q.popleft()  # ! u 出队时它的祖先已经攒齐（所有前驱都先出队了）
            for v in graph[u]:
                anc[v] |= anc[u]  # 祖先的祖先也是我的祖先
                anc[v].add(u)
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        return [u in anc[v] for u, v in queries]


##################################################################################################
##### ! Solution 2: Floyd-Warshall 传递闭包
##### ! 时间复杂度: O(V^3 + Q)   空间复杂度: O(V^2)
##### ! 适用：n 很小（<= 100）、不想建队列时的三行写法：i 能到 k 且 k 能到 j，则 i 能到 j
##################################################################################################


class Solution_2:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        n = numCourses
        reach = [[False] * n for _ in range(n)]
        for u, v in prerequisites:
            reach[u][v] = True

        for k in range(n):  # ! 中转点放最外层，和 Floyd 最短路一个套路
            for i in range(n):
                if reach[i][k]:  # i 能到 k，那 k 能到的 i 都能到
                    row_i, row_k = reach[i], reach[k]
                    for j in range(n):
                        if row_k[j]:
                            row_i[j] = True

        return [reach[u][v] for u, v in queries]


##################################################################################################
##### ! Solution 3: DFS + 记忆化（每个点记下自己能到的所有点）
##### ! 时间复杂度: O(V * (V + E) + Q)   空间复杂度: O(V^2)
##### ! 适用：自顶向下的写法；图保证无环所以不用三色，memo 一次算完所有点的可达集合
##################################################################################################


class Solution_3:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        graph = [[] for _ in range(numCourses)]
        for u, v in prerequisites:
            graph[u].append(v)

        memo = {}

        def reach(u: int) -> set:  # u 能到的所有点
            if u not in memo:
                s = set()
                for v in graph[u]:
                    s.add(v)
                    s |= reach(v)  # ! 后继能到的我都能到
                memo[u] = s
            return memo[u]

        return [v in reach(u) for u, v in queries]


s = Solution_1()
numCourses = 3
prerequisites = [[1, 2], [1, 0], [2, 0]]
queries = [[1, 0], [1, 2]]
result = s.checkIfPrerequisite(numCourses, prerequisites, queries)
print(result)  # [True, True]
