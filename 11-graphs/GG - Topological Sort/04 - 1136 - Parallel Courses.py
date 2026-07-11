from typing import List
from collections import defaultdict, deque


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
