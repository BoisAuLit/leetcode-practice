"""LC-0210 - Course Schedule II

合并自 2 个解法文件:
  1. 0210 - A - Course Schedule II - DFS TopSort (reversed post-order) - 教科书 📚.py
  2. 0210 - B - Course Schedule II - BFS - Kahn - 教科书 📚.py
"""

from typing import List

from collections import defaultdict

from collections import defaultdict, deque


# ============================================================================
# Solution 1: DFS_TopSort_reversed_post_order    (原文件: 0210 - A - Course Schedule II - DFS TopSort (reversed post-order) - 教科书 📚.py)
# ============================================================================

# DFS 解法的本质:
# - 我沿着 dependency graph 往下走, 会不会绕回当前 DFS Path
# - UNVISITED -> VISITING -> VISITED
# - 倘若遇到 VISITING, 那就是有 cycle
#
# --------------------------------------------------
#
# - 这个 DFS 解法的普适性更偏“图遍历” (UNVISITED, VISITING, VISITED)
# - 这个概念不是 Topological Sort 专属的。
# - 它是一个非常通用的 directed DFS cycle detection 模板。

class Solution_1_DFS_TopSort_reversed_post_order:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        # 1 -> [2, 3], 只有先学完 1, 才能学 2, 3
        next_courses = defaultdict(list)

        for a, b in prerequisites:
            next_courses[b].append(a)

        UNVISITED = 0  # 从来没有 DFS 过
        VISITING = 1  ## 当前正在 DFS path 上
        VISITED = 2  ### 已经完整 DFS 完毕，并且确认安全

        states = [UNVISITED] * numCourses

        postorder = []

        def acyclic(course):
            if states[course] == VISITING:  # The course was previously being visited, and is visited again
                return False
            if states[course] == VISITED:  # The course has been visisted and there's no cycles ahead
                return True

            states[course] = VISITING

            for next_course in next_courses[course]:
                if not acyclic(next_course):
                    return False

            states[course] = VISITED
            postorder.append(course)
            return True

        # 图可能有多个 disconnected components，
        # 所以不能只从 Course 0 开始 DFS。
        #
        # 必须确保每一门课都被检查到。
        for course in range(numCourses):
            if not acyclic(course):
                return []

        # postorder 是反向拓扑顺序，
        # reverse 后才是 prerequisite -> course 的正确顺序。
        return postorder[::-1]

# ============================================================================
# Solution 2: Kahn    (原文件: 0210 - B - Course Schedule II - BFS - Kahn - 教科书 📚.py)
# ============================================================================

# BFS/Khan 的本质:
# - 现在哪些课程已经没有 prerequisite, 可以立即学?
# - 不断地更新所有 nodes 的 indegree
#
# ⭐⁉️ indegree[course] 表示还有多少 prerequisite 没完成。
# ➡️ 当它变成 0, 这门课就可以开始。
# ✅ 完成一门课以后，它后面的课程分别少一个 prerequisite。
#
# --------------------------------------------------
#
# BFS/Kahn 的普适性更偏“dependency / scheduling”

class Solution_2_Kahn:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        next_courses = defaultdict(list)

        # remaining_prerequisites[course]
        # = course 还有多少 prerequisite 尚未完成
        indegree = [0] * numCourses

        for a, b in prerequisites:
            next_courses[b].append(a)
            indegree[a] += 1

        q = deque()  # 当前已经没有任何 prerequisite，可以立刻学习的课程。

        for course in range(numCourses):
            if indegree[course] == 0:
                q.append(course)

        order = []

        while q:
            # 这门课所有 prerequisites 都已经完成，
            # 所以现在正式完成它。
            course = q.popleft()

            order.append(course)

            # course 完成以后，
            # 它后面的每一门课都少了一个 prerequisite。
            for neigh in next_courses[course]:
                indegree[neigh] -= 1

                # 如果最后一个 prerequisite 也完成了，
                # next_course 现在被“解锁”。 🔐
                if indegree[neigh] == 0:
                    q.append(neigh)

        # 如果所有课程都成功进入 topological_order，
        # 说明没有 cycle。
        #
        # 如果有 cycle：
        # cycle 中的课程会互相等待，
        # remaining_prerequisites 永远无法变成 0，
        # 所以无法进入 queue。
        return order if len(order) == numCourses else []
