"""LC-1059 - All Paths from Source Lead to Destination

合并自 2 个解法文件:
  1. 1059 - A - All Paths Source Lead to Destination - DFS 3-state (WHITE-GRAY-BLACK).py
  2. 1059 - B - All Paths Source Destination - ⭐️ DFS 教科书.py
"""

from typing import List

from collections import defaultdict


# ============================================================================
# Solution 1: DFS_3_state_WHITE_GRAY_BLACK    (原文件: 1059 - A - All Paths Source Lead to Destination - DFS 3-state (WHITE-GRAY-BLACK).py)
# ============================================================================

n_1 = 4

edges_1 = [[0, 1], [0, 2], [1, 3], [2, 3]]

source_1 = 0

destination_1 = 3

class Solution_1_DFS_3_state_WHITE_GRAY_BLACK:
    WHITE = 0 # Unvisited
    GRAY = 1 # Itself and its descendants are being processed
    BLACK = 2 # 

    def leadsToDestination(
        self, n_1: int, edges_1: List[List[int]], source_1: int, destination_1: int
    ) -> bool:
        graph = defaultdict(list)
        for x, y in edges_1:
            graph[x].append(y)

        # ! Initially, all nodes are WHITE
        return self.leadsToDest(graph, source_1, destination_1, [Solution_1_DFS_3_state_WHITE_GRAY_BLACK.WHITE] * n_1)

    def leadsToDest(self, graph, node, dest, states):
        # If the state is GRAY, this is a backward edge and hence, it creates a Loop.
        if states[node] is not Solution_1_DFS_3_state_WHITE_GRAY_BLACK.WHITE:
            return states[node] == Solution_1_DFS_3_state_WHITE_GRAY_BLACK.BLACK

        # If this is a leaf node, it should be equal to the destination_1.
        if not graph[node]:
            return node == dest

        # Now, we are processing this node. So we mark it as GRAY.
        states[node] = Solution_1_DFS_3_state_WHITE_GRAY_BLACK.GRAY

        for next_node in graph[node]:
            # If we get a `false` from any recursive call on the neighbors, we short circuit and return from there.
            if not self.leadsToDest(graph, next_node, dest, states):
                return False

        # Recursive processing done for the node. We mark it BLACK.
        states[node] = Solution_1_DFS_3_state_WHITE_GRAY_BLACK.BLACK
        return True

# ============================================================================
# Solution 2: DFS    (原文件: 1059 - B - All Paths Source Destination - ⭐️ DFS 教科书.py)
# ============================================================================

n_2 = 4

edges_2 = [[0, 1], [0, 2], [1, 3], [2, 3]]

source_2 = 0

destination_2 = 3

class Solution_2_DFS:
    def leadsToDestination(
        self, n_2: int, edges_2: List[List[int]], source_2: int, destination_2: int
    ) -> bool:
        g = defaultdict(set)
        visited = defaultdict(int)
        for [x, y] in edges_2:
            g[x].add(y)

        def dfs(node):
            if visited[node] == 1:
                return True
            elif visited[node] == -1:
                return False
            elif len(g[node]) == 0:
                return node == destination_2
            else:
                visited[node] = -1
                for child in g[node]:
                    if not dfs(child):
                        return False
                visited[node] = 1
                return True

        return dfs(source_2)


if __name__ == "__main__":

    # --- Solution 1: DFS_3_state_WHITE_GRAY_BLACK ---
    s = Solution_1_DFS_3_state_WHITE_GRAY_BLACK()
    result = s.leadsToDestination(n_1, edges_1, source_1, destination_1)
    print(result)

    # --- Solution 2: DFS ---
    s = Solution_2_DFS()
    result = s.leadsToDestination(n_2, edges_2, source_2, destination_2)
    print(result)
