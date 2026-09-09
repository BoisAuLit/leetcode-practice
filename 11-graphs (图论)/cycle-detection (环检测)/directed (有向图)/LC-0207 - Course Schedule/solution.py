"""LC-0207 - Course Schedule

合并自 2 个解法文件:
  1. 0207 - A - Course Schedule - DFS 3-state cycle detection.py
  2. 0207 - B - Course Schedule - BFS - Kahn.py
"""

from typing import List

from collections import defaultdict

from collections import defaultdict, deque


# ============================================================================
# Solution 1: DFS_3_state_cycle_detection    (原文件: 0207 - A - Course Schedule - DFS 3-state cycle detection.py)
# ============================================================================

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
