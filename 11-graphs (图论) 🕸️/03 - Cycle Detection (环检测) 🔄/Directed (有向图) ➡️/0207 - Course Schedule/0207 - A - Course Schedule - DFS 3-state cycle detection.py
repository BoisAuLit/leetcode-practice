"""
📌 信号→模式: 课程能否修完 = 有向图无环 → DFS 三色标记（VISITING 再遇即环）
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
from collections import defaultdict


class Solution:
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
