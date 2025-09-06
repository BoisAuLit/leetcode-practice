from typing import List
from collections import deque, defaultdict


class Solution:
    def findOrder(
        self, numCourses: int, prerequisites: List[List[int]]
    ) -> List[int]:
        in_degree = [0] * numCourses
        graph = defaultdict(list)
        for course, pre in prerequisites:
            in_degree[course] += 1
            graph[pre].append(course)

        queue = deque()
        # Append courses with no prerequisites to the queue
        for course, degree in enumerate(in_degree):
            if degree == 0:
                queue.append(course)

        index = 0 # Position to insert the next element in the order array (result)
        order = [0] * numCourses # Array to store the topsorted elements
        while queue:
            node = queue.popleft()
            order[index] = node
            index += 1
            for neigh in graph[node]:
                in_degree[neigh] -= 1
                if in_degree[neigh] == 0:
                    queue.append(neigh)
        if index != numCourses:
            return []  # It means containing a cycle
        return order


s = Solution()
numCourses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
result = s.findOrder(numCourses, prerequisites)
print(result)
