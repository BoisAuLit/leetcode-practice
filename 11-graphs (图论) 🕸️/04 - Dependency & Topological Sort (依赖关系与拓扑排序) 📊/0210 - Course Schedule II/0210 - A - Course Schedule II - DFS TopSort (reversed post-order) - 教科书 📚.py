from collections import defaultdict
from typing import List


"""
DFS 解法的本质:
- 我沿着 dependency graph 往下走, 会不会绕回当前 DFS Path
- UNVISITED -> VISITING -> VISITED
- 倘若遇到 VISITING, 那就是有 cycle

--------------------------------------------------

- 这个 DFS 解法的普适性更偏“图遍历” (UNVISITED, VISITING, VISITED)
- 这个概念不是 Topological Sort 专属的。
- 它是一个非常通用的 directed DFS cycle detection 模板。
"""
class Solution:
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
