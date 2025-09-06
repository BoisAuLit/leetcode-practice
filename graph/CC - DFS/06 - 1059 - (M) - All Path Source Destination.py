from typing import List
from collections import defaultdict


class Solution:
    WHITE = 0 # Unvisited
    GRAY = 1 # Itself and its descendants are being processed
    BLACK = 2 # 

    def leadsToDestination(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        graph = defaultdict(list)
        for x, y in edges:
            graph[x].append(y)

        # ! Initially, all nodes are WHITE
        return self.leadsToDest(graph, source, destination, [Solution.WHITE] * n)

    def leadsToDest(self, graph, node, dest, states):
        # If the state is GRAY, this is a backward edge and hence, it creates a Loop.
        if states[node] is not Solution.WHITE:
            return states[node] == Solution.BLACK

        # If this is a leaf node, it should be equal to the destination.
        if not graph[node]:
            return node == dest

        # Now, we are processing this node. So we mark it as GRAY.
        states[node] = Solution.GRAY

        for next_node in graph[node]:
            # If we get a `false` from any recursive call on the neighbors, we short circuit and return from there.
            if not self.leadsToDest(graph, next_node, dest, states):
                return False

        # Recursive processing done for the node. We mark it BLACK.
        states[node] = Solution.BLACK
        return True


# # Expect False
# s = Solution()
# n = 3
# edges = [[0, 1], [0, 2]]
# source = 0
# destination = 2
# result = s.leadsToDestination(n, edges, source, destination)
# print(result)

# Expect True
s = Solution()
n = 4
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
source = 0
destination = 3
result = s.leadsToDestination(n, edges, source, destination)
print(result)
