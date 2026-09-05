from collections import defaultdict, deque
from typing import List


"""
Time complexity: O(V)
Space Complexity O(V)
"""


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Return all roots of Minimum Height Trees (MHTs) in an undirected tree.

        Algorithm:
          - Build adjacency list and initial degrees.
          - Push all current leaves (degree == 1) into a queue.
          - Iteratively trim leaves level by level until ≤ 2 nodes remain.
          - The remaining 1–2 nodes are the centroids (MHT roots).

        Time:  O(n)
        Space: O(n)
        """
        if n == 1:
            return [0]

        # Build graph and degree array
        graph: dict[int, list[int]] = defaultdict(list)
        degree: List[int] = [0] * n

        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
            degree[u] += 1
            degree[v] += 1

        # Initialize leaves
        queue = deque(i for i, d in enumerate(degree) if d == 1)

        # Trim leaves until at most two nodes remain
        remain = n
        while remain > 2:
            leaves_count = len(queue)
            remain -= leaves_count

            for _ in range(leaves_count):
                leaf = queue.popleft()
                for nei in graph[leaf]:
                    degree[nei] -= 1
                    if degree[nei] == 1:
                        queue.append(nei)

        return list(queue)


s = Solution()
n = 4
edges = [[1, 0], [1, 2], [1, 3]]
result = s.findMinHeightTrees(n, edges)
print(result)
