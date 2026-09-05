from typing import List
from collections import defaultdict, deque


class Solution:
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
