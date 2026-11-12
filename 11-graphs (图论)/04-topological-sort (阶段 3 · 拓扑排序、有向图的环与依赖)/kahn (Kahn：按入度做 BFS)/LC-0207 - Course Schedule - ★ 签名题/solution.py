"""LC-0207 - Course Schedule

合并自 2 个解法文件:
  1. 0207 - A - Course Schedule - DFS 3-state cycle detection.py
  2. 0207 - B - Course Schedule - BFS - Kahn.py

阶段 3 · 拓扑排序 · Kahn（按入度做 BFS）★ 签名题
题目在问：课程有先修关系，能否全部修完（= 有向图里有没有环）
点是什么：一门课   边是什么：b -> a（先修完 b 才能修 a）
和签名题比改了哪一行：本题就是签名题；入度为 0 的进队列，出队个数 < n 就有环
"""

from typing import List

from collections import defaultdict

from collections import defaultdict, deque


# ============================================================================
# Solution 1: DFS_3_state_cycle_detection    (原文件: 0207 - A - Course Schedule - DFS 3-state cycle detection.py)
# ============================================================================

##################################################################################################
##### ! Solution 1: 三色 DFS 判环（UNVISITED / VISITING / VISITED）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   V = numCourses, E = len(prerequisites)
##### ! 适用：只问"有没有环"、或顺便要后序（210）；递归深度最坏 = V（2000），LeetCode 已调高上限，本地跑大链用 Solution 3
##################################################################################################


class Solution_1_DFS_3_state_cycle_detection:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        next_courses = defaultdict(list)
        for a, b in prerequisites:
            next_courses[b].append(a)
        UNVISITED = 0
        VISITING = 1
        VISITED = 2
        states = [UNVISITED] * numCourses

        def acyclic(course):
            if states[course] == VISITING:
                return False
            if states[course] == VISITED:
                return True
            states[course] = VISITING
            for neigh in next_courses[course]:
                if not acyclic(neigh):
                    return False
            states[course] = VISITED
            return True

        return all(acyclic(c) for c in range(numCourses))

# ============================================================================
# Solution 2: Kahn    (原文件: 0207 - B - Course Schedule - BFS - Kahn.py)
# ============================================================================

##################################################################################################
##### ! Solution 2: Kahn（按入度做 BFS）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：签名题写法；要"出队顺序"（210）、要"分层"（1136）都从它改一行
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2_Kahn:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        next_courses = defaultdict(list)
        indegree = [0] * numCourses
        for a, b in prerequisites:
            next_courses[b].append(a)
            indegree[a] += 1
        q = deque()
        for c in range(numCourses):
            if indegree[c] == 0:
                q.append(c)
        seen = 0
        while q:
            c = q.popleft()
            indegree[c] = -100
            seen += 1
            for neigh in next_courses[c]:
                indegree[neigh] -= 1
                if indegree[neigh] == 0:
                    q.append(neigh)
        return seen == numCourses


##################################################################################################
##### ! Solution 3: 三色 DFS 迭代版（显式栈，和 Solution 1 同一个思路）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：不想碰递归上限时；栈里存 (点, 下一个要看的邻居下标)，模拟"回到这一层接着 for"
##################################################################################################


class Solution_3:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        next_courses = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            next_courses[b].append(a)

        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * numCourses

        for start in range(numCourses):
            if color[start] != WHITE:
                continue
            color[start] = GRAY
            stack = [(start, 0)]  # ! (点, 下一个要看的邻居下标)
            while stack:
                u, i = stack[-1]
                if i == len(next_courses[u]):
                    color[u] = BLACK  # ! 邻居全看完了，出栈时涂黑
                    stack.pop()
                    continue
                stack[-1] = (u, i + 1)
                v = next_courses[u][i]
                if color[v] == GRAY:
                    return False  # ! 碰到还在栈上的灰点 = 有环
                if color[v] == WHITE:
                    color[v] = GRAY
                    stack.append((v, 0))
        return True


s = Solution_2_Kahn()
numCourses = 2
prerequisites = [[1, 0]]
result = s.canFinish(numCourses, prerequisites)
print(result)  # True

prerequisites = [[1, 0], [0, 1]]
result = s.canFinish(numCourses, prerequisites)
print(result)  # False
