"""LC-0797 - All Paths From Source to Target

合并自 7 个解法文件:
  1. 023 - 0797 - A - All Paths from A to B - DFS Recursive Memoization (empty placeholder, superseded).py
  2. 023 - 0797 - B - All Paths from A to B - DFS Recursive Backtracking (empty placeholder, superseded).py
  3. 0797 - A - All Paths A to B - DFS Recursive DP Memoization.py
  4. 0797 - B - All Paths A to B - DFS Recursive Backtracking 🚀.py
  5. 0797 - C - All Paths from A to B - BFS.py
  6. 0797 - D - All Paths from A to B - DFS Iterative Memoization (TODO, empty).py

阶段 0 · 建图、隐式图、状态图 · 显式建图(边列表 → 邻接表) ○ 核心
题目在问：DAG 上从 0 到 n-1 的所有路径，全部列出来
点是什么：0..n-1   边是什么：graph[i] 里的每个 j 是有向边 i → j(graph 本身就是邻接表)
和签名题(1971)比改了哪一行：不要 seen 数组(DAG 没环，而且同一个点可以出现在不同路径里)；
  dfs 带一个 path，进点 append、回来 pop(回溯)，到 n-1 时把 path 拷一份存进结果
注：Solution 1/2/6/7 是用户留的空占位；这次补的 Solution_8 对应占位 7(DFS 迭代)
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

##################################################################################################
##### ! Solution 3: DFS 递归 + 记忆化(memo[node] = node 到终点的所有路径)
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(2^n · n)   memo 把每个点的路径集都存一份，拼接时还要复制
##### ! 适用：想展示 "DAG 上子问题可复用" 的时候；但本题输出本身就是 2^n 级，记忆化省不了多少，还多吃内存
##################################################################################################

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

##################################################################################################
##### ! Solution 4: DFS 递归 + 回溯(path 进出)
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n)(不算输出)   path 只有一份，走到头拷贝一次
##### ! 适用：本题标准答案，手册点名的 "DFS + 回溯，path 进出"
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

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

##################################################################################################
##### ! Solution 5: BFS，队列里带整条路径副本
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(2^n · n)   每扩展一步就 path + [next]，队列里同时存着一堆半路
##### ! 适用：不想写递归时的写法；DAG 没环所以不用 visited
##################################################################################################

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


##################################################################################################
##### ! Solution 8: DFS 迭代(栈里带路径副本，对应上面的占位 7)
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(2^n · n)   和 Solution 5 一样，只是队列换成栈
##### ! 适用：递归深度受限时；注意栈版出来的路径顺序和递归版不同(LeetCode 不要求顺序)
##################################################################################################


class Solution_8:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        target = len(graph) - 1
        results = []
        stack = [(0, [0])]  # ! (当前点, 到这个点为止的路径)
        while stack:
            node, path = stack.pop()
            if node == target:
                results.append(path)
                continue
            for next_node in graph[node]:
                stack.append((next_node, path + [next_node]))  # ! 每条分支拿自己的一份 path
        return results


if __name__ == "__main__":

    # --- Solution 3: DFS_Recursive_DP_Memoization ---
    s = Solution_3_DFS_Recursive_DP_Memoization()
    result = s.allPathsSourceTarget(graph_3)
    print(result)

    # --- Solution 5: BFS ---
    s = Solution_5_BFS()
    result = s.allPathsSourceTarget(graph_5)
    print(result)
