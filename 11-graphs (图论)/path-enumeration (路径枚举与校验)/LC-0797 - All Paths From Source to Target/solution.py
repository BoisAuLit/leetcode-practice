"""LC-0797 - All Paths From Source to Target

合并自 7 个解法文件:
  1. 023 - 0797 - A - All Paths from A to B - DFS Recursive Memoization (empty placeholder, superseded).py
  2. 023 - 0797 - B - All Paths from A to B - DFS Recursive Backtracking (empty placeholder, superseded).py
  3. 0797 - A - All Paths A to B - DFS Recursive DP Memoization.py
  4. 0797 - B - All Paths A to B - DFS Recursive Backtracking 🚀.py
  5. 0797 - C - All Paths from A to B - BFS.py
  6. 0797 - D - All Paths from A to B - DFS Iterative Memoization (TODO, empty).py
  7. 0797 - E - All Paths from A to B - DFS Iterative (TODO, empty).py
"""

from typing import List

from collections import deque


# ============================================================================
# Solution 1: DFS_Recursive_Memoization_empty_placehol    (原文件: 023 - 0797 - A - All Paths from A to B - DFS Recursive Memoization (empty placeholder, superseded).py)
# ============================================================================

# ============================================================================
# Solution 2: DFS_Recursive_Backtracking_empty_placeho    (原文件: 023 - 0797 - B - All Paths from A to B - DFS Recursive Backtracking (empty placeholder, superseded).py)
# ============================================================================

# ============================================================================
# Solution 3: DFS_Recursive_DP_Memoization    (原文件: 0797 - A - All Paths A to B - DFS Recursive DP Memoization.py)
# ============================================================================

# Time: O(2ᴺ⋅N)
# Space: O(2ᴺ⋅N)

graph_3 = [[1, 2], [3], [3], []]

graph_3 = [[4, 3, 1], [3, 2, 4], [3], [4], []]

class Solution_3_DFS_Recursive_DP_Memoization:
    def allPathsSourceTarget(self, graph_3: List[List[int]]) -> List[List[int]]:
        source = 0
        target = len(graph_3) - 1
        memo = dict()

        def dfs(node: int) -> List[List[int]]:
            if node == target:
                return [[target]]
            if node in memo:
                return memo[node]
            paths = []
            for next_node in graph_3[node]:
                paths.extend([node] + path for path in dfs(next_node))
            memo[node] = paths
            return paths

        return dfs(source)

# ============================================================================
# Solution 4: DFS_Recursive_Backtracking    (原文件: 0797 - B - All Paths A to B - DFS Recursive Backtracking 🚀.py)
# ============================================================================

# Time: O(2ᴺ⋅N)
# Space: O(N)

class Solution_4_DFS_Recursive_Backtracking:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:

        target = len(graph) - 1
        results = []

        def backtrack(curr_node, path):
            # if we reach the target, no need to explore further.
            if curr_node == target:
                results.append(list(path))
                return
            # explore the neighbor nodes one after another.
            for next_node in graph[curr_node]:
                path.append(next_node)
                backtrack(next_node, path)
                path.pop()
        # kick of the backtracking, starting from the source node (0).
        path = [0]
        backtrack(0, path)

        return results

# ============================================================================
# Solution 5: BFS    (原文件: 0797 - C - All Paths from A to B - BFS.py)
# ============================================================================

graph_5 = [[1, 2], [3], [3], []]

class Solution_5_BFS:
    def allPathsSourceTarget(self, graph_5: List[List[int]]) -> List[List[int]]:
        n = len(graph_5) # n is the number of vertices
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
            for next_node in graph_5[node]:
                queue.append([next_node, path_so_far + [next_node]])
        return results

# ============================================================================
# Solution 6: DFS_Iterative_Memoization_TODO_empty    (原文件: 0797 - D - All Paths from A to B - DFS Iterative Memoization (TODO, empty).py)
# ============================================================================

# ============================================================================
# Solution 7: DFS_Iterative_TODO_empty    (原文件: 0797 - E - All Paths from A to B - DFS Iterative (TODO, empty).py)
# ============================================================================


if __name__ == "__main__":

    # --- Solution 3: DFS_Recursive_DP_Memoization ---
    s = Solution_3_DFS_Recursive_DP_Memoization()
    result = s.allPathsSourceTarget(graph_3)
    print(result)

    # --- Solution 5: BFS ---
    s = Solution_5_BFS()
    result = s.allPathsSourceTarget(graph_5)
    print(result)
