"""LC-1136 - Parallel Courses

阶段 3 · 拓扑排序 · 按层（轮数 = 学期数）○ 核心
题目在问：每学期可修任意多门没有先修限制的课，最少几学期修完，有环返回 -1
点是什么：一门课（1..n）   边是什么：prevCourse -> nextCourse
和签名题比改了哪一行：207 的 while queue 里套一层 for _ in range(len(queue))，剥完一层 semesters += 1；出队数 < n 就是有环
"""
from typing import List
from collections import defaultdict, deque


##################################################################################################
##### ! Solution 1: Kahn 按层剥（一层 = 一个学期）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)   E = len(relations)
##### ! 适用：问"最少几轮"的依赖题；同一层的课互不依赖，可以同一学期一起修
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        in_degree = [0] * (n + 1)

        graph = defaultdict(list)
        for x, y in relations:
            graph[x].append(y)
            in_degree[y] += 1
        queue = deque(i for i, d in enumerate(in_degree) if d == 0 and i != 0)

        semesters = 0
        orders = [0] * n
        index = 0
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                orders[index] = node
                index += 1
                for nei in graph[node]:
                    in_degree[nei] -= 1
                    if in_degree[nei] == 0:
                        queue.append(nei)
            semesters += 1

        if index != n:
            return -1
        return semesters


##################################################################################################
##### ! Solution 2: 记忆化 DFS 求最长路 + 三色判环
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：把"学期数"看成 DAG 最长路的点数；递归深度最坏 = n（5000），LeetCode 已调高上限
##################################################################################################


class Solution_2:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        graph = [[] for _ in range(n + 1)]
        for x, y in relations:
            graph[x].append(y)

        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * (n + 1)
        longest = [0] * (n + 1)  # ! longest[u] = 从 u 出发（含 u）最多还要修几门

        def dfs(u: int) -> int:
            # ! 返回 0 当哨兵表示发现环（真实长度至少是 1）
            if color[u] == GRAY:
                return 0
            if color[u] == BLACK:
                return longest[u]
            color[u] = GRAY
            best = 1
            for v in graph[u]:
                d = dfs(v)
                if d == 0:
                    return 0
                best = max(best, 1 + d)
            color[u] = BLACK
            longest[u] = best
            return best

        ans = 0
        for u in range(1, n + 1):
            d = dfs(u)
            if d == 0:
                return -1
            ans = max(ans, d)
        return ans  # ! 最长链有几门课，就要几个学期


# Test case 1: Expecting 2
# s = Solution()
# n = 3
# relations = [[1, 3], [2, 3]]
# result = s.minimumSemesters(n, relations)
# print(result)


# Test case 2: Expecting -1
s = Solution()
n = 3
relations = [[1,2],[2,3],[3,1]]
result = s.minimumSemesters(n, relations)
print(result)
