"""LC-1857 - Largest Color Value in a Directed Graph

阶段 3 · DAG 上的 DP（拓扑序 + 状态转移） △ 扩展
题目在问：有向图每个点有颜色，所有路径里"同一种颜色最多出现几次"是多少；图有环返回 -1
点是什么：0..n-1，颜色是 colors[i]   边是什么：[u, v] 是一条 u -> v
和签名题比改了哪一行：207 的 Kahn 出队时多做一步 DP：cnt[v][c] = max(cnt[u][c] for u -> v)，
                     再给自己的颜色 +1；出队个数 < n 就是有环，直接 -1（207 的判环原封不动）
"""
import sys
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: Kahn + DP（cnt[v][c] = 以 v 结尾的路径里颜色 c 最多几个）
##### ! 时间复杂度: O((V + E) * 26)   空间复杂度: O(26 * V + E)
##### ! 适用：DAG 上"路径最值"类 DP，顺带判环；按拓扑序推，轮到 v 时所有前驱的 cnt 都已经最终
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        graph = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v in edges:
            graph[u].append(v)
            indeg[v] += 1

        cnt = [[0] * 26 for _ in range(n)]
        q = deque(v for v in range(n) if indeg[v] == 0)
        seen = 0
        best = 0
        while q:
            u = q.popleft()
            seen += 1
            c = ord(colors[u]) - 97
            cnt[u][c] += 1  # ! 前驱全部处理完了，这时再把自己的颜色加上
            best = max(best, cnt[u][c])  # 以 u 结尾、颜色 = u 的颜色，这就足够覆盖所有路径
            for v in graph[u]:
                cv = cnt[v]
                for k, x in enumerate(cnt[u]):  # 26 种颜色逐个取 max
                    if x > cv[k]:
                        cv[k] = x
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        return best if seen == n else -1  # ! 没出完队 = 有环


##################################################################################################
##### ! Solution 2: 三色 DFS + 记忆化（cnt[u] = 从 u 出发的路径里每种颜色最多几个）
##### ! 时间复杂度: O((V + E) * 26)   空间复杂度: O(26 * V + E)（memo + 递归栈）
##### ! 适用：想从"起点"往后看时；三色判环（灰 = 有环）和 802 一样。n 到 1e5，递归要调 recursionlimit，
##### !       LeetCode 上深链可能吃紧，稳妥还是 Solution 1
##################################################################################################

sys.setrecursionlimit(200000)  # ! 递归深度最坏 = n = 1e5


class Solution_2:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)

        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * n
        cnt = [None] * n

        def dfs(u: int) -> bool:  # 返回 False = 踩到环
            color[u] = GRAY
            res = [0] * 26
            for v in graph[u]:
                if color[v] == GRAY:
                    return False  # ! 灰 = 还在栈上 = 有环
                if color[v] == WHITE and not dfs(v):
                    return False
                for k in range(26):  # 后继的结果取 max
                    if cnt[v][k] > res[k]:
                        res[k] = cnt[v][k]
            res[ord(colors[u]) - 97] += 1  # 再加上自己
            cnt[u] = res
            color[u] = BLACK
            return True

        for u in range(n):
            if color[u] == WHITE and not dfs(u):
                return -1
        return max(max(row) for row in cnt)


s = Solution_1()
colors = "abaca"
edges = [[0, 1], [0, 2], [2, 3], [3, 4]]
result = s.largestPathValue(colors, edges)
print(result)  # 3
