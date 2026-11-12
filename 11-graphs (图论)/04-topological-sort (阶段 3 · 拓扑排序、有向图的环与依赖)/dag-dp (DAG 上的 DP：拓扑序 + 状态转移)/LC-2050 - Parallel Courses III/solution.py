"""LC-2050 - Parallel Courses III

阶段 3 · DAG 上的 DP（拓扑序 + 状态转移） △ 扩展
题目在问：每门课有时长，没有依赖的课可以同时修，全部修完最少要多少时间
点是什么：课程 1..n（time[i-1] 是课 i 的时长）   边是什么：[prev, next] 是一条 prev -> next
和签名题比改了哪一行：207 的 Kahn 出队时多做一步 DP：finish[v] = max(finish[u] for u -> v) + time[v]；
                     答案 = max(finish)，就是 DAG 上的最长路（关键路径）
"""
import sys
from collections import deque
from functools import lru_cache
from typing import List

##################################################################################################
##### ! Solution 1: Kahn + DP 求最长路
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：DAG 上"最早完成时间 / 最长路"；按拓扑序推，轮到 v 时它所有先修课的 finish 都已经定了
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        graph = [[] for _ in range(n + 1)]
        indeg = [0] * (n + 1)
        for u, v in relations:
            graph[u].append(v)
            indeg[v] += 1

        finish = [0] * (n + 1)  # finish[v] = 课 v 最早什么时候修完
        q = deque()
        for v in range(1, n + 1):
            if indeg[v] == 0:
                q.append(v)
                finish[v] = time[v - 1]  # 没先修，第 0 时刻就开始

        while q:
            u = q.popleft()
            for v in graph[u]:
                finish[v] = max(finish[v], finish[u] + time[v - 1])  # ! 得等最晚修完的那门先修课
                indeg[v] -= 1
                if indeg[v] == 0:  # 先修全到齐，finish[v] 定了
                    q.append(v)

        return max(finish)  # 所有课都修完 = 最晚的那门修完


##################################################################################################
##### ! Solution 2: DFS + 记忆化（自顶向下）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)（memo + 递归栈）
##### ! 适用：顺着"修完 v 要先修完它所有先修"的定义直接写；n 到 5e4，一条链递归就是 5e4 层，要调 recursionlimit
##################################################################################################

sys.setrecursionlimit(100000)  # ! 递归深度最坏 = n = 5e4，默认 1000 会爆


class Solution_2:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        prereq = [[] for _ in range(n + 1)]
        for u, v in relations:
            prereq[v].append(u)  # 反着存：v 的先修课有哪些

        @lru_cache(None)
        def finish(v: int) -> int:
            return time[v - 1] + max((finish(u) for u in prereq[v]), default=0)  # ! 没先修时 max 取 0

        return max(finish(v) for v in range(1, n + 1))


s = Solution_1()
n = 5
relations = [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]]
time = [1, 2, 3, 4, 5]
result = s.minimumTime(n, relations, time)
print(result)  # 12
