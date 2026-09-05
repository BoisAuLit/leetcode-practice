from collections import defaultdict, deque
from typing import List



"""
BFS/Khan 的本质:
- 现在哪些课程已经没有 prerequisite, 可以立即学?
- 不断地更新所有 nodes 的 indegree

⭐⁉️ indegree[course] 表示还有多少 prerequisite 没完成。
➡️ 当它变成 0, 这门课就可以开始。
✅ 完成一门课以后，它后面的课程分别少一个 prerequisite。

--------------------------------------------------

BFS/Kahn 的普适性更偏“dependency / scheduling”
"""

class Solution:
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
