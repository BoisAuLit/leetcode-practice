from typing import List
from collections import deque


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph) # n is the number of vertices
        """
        For each inner array
        - 1st element is the current node
        - 2nd element is the path up until current node
        """
        queue = deque([[0, [0]]])
        results = []

        while queue:
            node, path_so_far = queue.popleft()
            if node == n - 1:
                results.append(path_so_far)
                continue
            for next_node in graph[node]:
                queue.append([next_node, path_so_far + [next_node]])
        return results


s = Solution()
graph = [[1, 2], [3], [3], []]
result = s.allPathsSourceTarget(graph)
print(result)
