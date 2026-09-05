from typing import List
from collections import deque, defaultdict

"""
Time: O(V+E)
Space: O(n+m)
"""


class Solution:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        """
        We initialize a stack with the source element

        Stack operations
        1. To add element to the queue, we use stack.append() ❇️
        2. To remove element from the queue, we use stack.pop() ❌
        """
        stack = deque([source])
        
        """
        ! The following three operations are exactly the same as the DFS recursive one
        ! 1. Declare a seen array
        ! 2. Mark the source node as seen
        ! 3. Construct the graph dictionary (two-way)
        """
        seen = [False] * n
        seen[source] = True
        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        # ! As long as stack is not empty, we keep looping 🔄
        while stack:
            node = stack.pop()

            # ! This part is exactly the same as the DFS recursive one
            if node == destination:
                return True
            
            # ! This part is almost the same as the DFS recursive one
            for next_node in graph[node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    # * Only this part is different from the DFS recursive one
                    stack.append(next_node)

        # ! If we arrive at this place, it means that no valid path is found
        return False


s = Solution()

# Test case 1: Expecting True
n = 3
edges = [[0, 1], [1, 2], [2, 0]]
source = 0
destination = 2

# Test case 2: Expecting False
# n = 6
# edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
# source = 0
# destination = 5

# Test case 3: Expecting True
# n = 6
# edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]
# source = 0
# destination = 5

result = s.validPath(n, edges, source, destination)
print(result)
