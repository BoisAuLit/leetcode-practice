from typing import List
from collections import deque, defaultdict

"""
Time: O(n+m)
Space: O(n+m)
"""

class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # Store all edges in 'graph'.
        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        # Store all the nodes to be visited in 'queue'.
        seen = [False] * n
        seen[source] = True
        queue = deque([source])
    
        while queue:
            curr_node = queue.popleft()
            if curr_node == destination:
                return True

            # For all the neighbors of the current node, if we haven't visit it before,
            # add it to 'queue' and mark it as visited.
            for next_node in graph[curr_node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    queue.append(next_node)
        
        return False


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
