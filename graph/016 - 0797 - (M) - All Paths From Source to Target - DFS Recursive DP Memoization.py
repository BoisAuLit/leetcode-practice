from typing import List

"""
Time: O(2ᴺ⋅N)
Space: O(2ᴺ⋅N)
"""


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        source = 0
        target = len(graph) - 1
        memo = dict()

        def dfs(node: int) -> List[List[int]]:
            if node == target:
                return [[target]]
            if node in memo:
                return memo[node]
            paths = []
            for next_node in graph[node]:
                paths.extend([node] + path for path in dfs(next_node))
            memo[node] = paths
            return paths

        return dfs(source)


s = Solution()

# Test case 1: Expecting [[0,1,3],[0,2,3]]
graph = [[1, 2], [3], [3], []]

# Test case 2: Expecting [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
graph = [[4, 3, 1], [3, 2, 4], [3], [4], []]

result = s.allPathsSourceTarget(graph)
print(result)
