from typing import List
from collections import defaultdict

"""
Time: O(V+E)
Space: O(n+m)

! All nodes are from 0 to N-1
"""



class Solution:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        # ! Define the seen array 👁️👁️👁️​
        seen = [False] * n

        # ! ​‌‌‌The source vertice is always first seen 💰​
        seen[source] = True

        # ! Construct the graph 🏗️
        # ! (Use adjacency list to create a dict representing the graph)
        graph = defaultdict(list)
        for a, b in edges:
            # ! Since it is an un-directed graph, the connection is mutual ⬅️ ➡️
            graph[a].append(b)
            graph[b].append(a)

        # ! Define the DFS algorithm 🔢
        def dfs(node: int) -> bool:
            if node == destination:
                return True

            # ! Iterate over all the unvisited neighbors 🔄
            for next_node in graph[node]:

                # ! Only if the neighbor node is not seen yet will we iterate it 🙈
                if not seen[next_node]:
                    # ! Mark the neighbor node as seen
                    seen[next_node] = True 

                    # ! If in the nested iteration we found the result, then we stop early
                    if dfs(next_node):
                        return True
            # ! If we arrive at this place, it means that no valid path is found
            return False

        return dfs(source)


s = Solution()

# Test case 1: Expecting True
n = 3
edges = [[0, 1], [1, 2], [2, 0]]
source = 0
destination = 2

# Test case 2: Expecting False
n = 6
edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
source = 0
destination = 5

# Test case 3: Expecting True
n = 6
edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]
source = 0
destination = 5

result = s.validPath(n, edges, source, destination)
print(result)
