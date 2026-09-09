"""LC-1971 - Find if Path Exists in Graph

合并自 6 个解法文件:
  1. 1971 - A - Find if path exists - ⭐️ DFS Recursive 教科书 - 效率最低 🐢.py
  2. 1971 - B - Find if path exists - ⭐️ DFS Stack 教科书 - 效率一般 😅.py
  3. 1971 - C - Find if path exists - ⭐️ BFS Queue 教科书 - 效率最高 🔥.py
  4. 1971 - D - Find if path exists - ⭐️ Disjoint Set 教科书 - 效率最高 🚀.py
  5. 1971 - E - Find if path exists - BFS (variant 2).py
  6. 1971 - F - Find if path exists - UnionFind (variant 2).py
"""

from typing import List

from collections import defaultdict

from collections import deque, defaultdict


# ============================================================================
# Solution 1: DFS_Recursive    (原文件: 1971 - A - Find if path exists - ⭐️ DFS Recursive 教科书 - 效率最低 🐢.py)
# ============================================================================

# Time: O(V+E)
# Space: O(n_1+m)
#
# ! All nodes are from 0 to N-1

n_1 = 3

edges_1 = [[0, 1], [1, 2], [2, 0]]

source_1 = 0

destination_1 = 2

n_1 = 6

edges_1 = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]

source_1 = 0

destination_1 = 5

n_1 = 6

edges_1 = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]

source_1 = 0

destination_1 = 5

class Solution_1_DFS_Recursive:
    def validPath(
        self, n_1: int, edges_1: List[List[int]], source_1: int, destination_1: int
    ) -> bool:
        # ! Define the seen array 👁️👁️👁️​
        seen = [False] * n_1

        # ! ​‌‌‌The source_1 vertice is always first seen 💰​
        seen[source_1] = True

        # ! Construct the graph 🏗️
        # ! (Use adjacency list to create a dict representing the graph)
        graph = defaultdict(list)
        for a, b in edges_1:
            # ! Since it is an un-directed graph, the connection is mutual ⬅️ ➡️
            graph[a].append(b)
            graph[b].append(a)

        # ! Define the DFS algorithm 🔢
        def dfs(node: int) -> bool:
            if node == destination_1:
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

        return dfs(source_1)

# ============================================================================
# Solution 2: DFS_Stack    (原文件: 1971 - B - Find if path exists - ⭐️ DFS Stack 教科书 - 效率一般 😅.py)
# ============================================================================

# Time: O(V+E)
# Space: O(n_2+m)

n_2 = 3

edges_2 = [[0, 1], [1, 2], [2, 0]]

source_2 = 0

destination_2 = 2

class Solution_2_DFS_Stack:
    def validPath(
        self, n_2: int, edges_2: List[List[int]], source_2: int, destination_2: int
    ) -> bool:
        """
        We initialize a stack with the source_2 element

        Stack operations
        1. To add element to the queue, we use stack.append() ❇️
        2. To remove element from the queue, we use stack.pop() ❌
        """
        stack = deque([source_2])
        
        """
        ! The following three operations are exactly the same as the DFS recursive one
        ! 1. Declare a seen array
        ! 2. Mark the source_2 node as seen
        ! 3. Construct the graph dictionary (two-way)
        """
        seen = [False] * n_2
        seen[source_2] = True
        graph = defaultdict(list)
        for a, b in edges_2:
            graph[a].append(b)
            graph[b].append(a)

        # ! As long as stack is not empty, we keep looping 🔄
        while stack:
            node = stack.pop()

            # ! This part is exactly the same as the DFS recursive one
            if node == destination_2:
                return True
            
            # ! This part is almost the same as the DFS recursive one
            for next_node in graph[node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    # * Only this part is different from the DFS recursive one
                    stack.append(next_node)

        # ! If we arrive at this place, it means that no valid path is found
        return False

# ============================================================================
# Solution 3: BFS_Queue    (原文件: 1971 - C - Find if path exists - ⭐️ BFS Queue 教科书 - 效率最高 🔥.py)
# ============================================================================

# Time: O(n_3+m)
# Space: O(n_3+m)

n_3 = 3

edges_3 = [[0, 1], [1, 2], [2, 0]]

source_3 = 0

destination_3 = 2

n_3 = 6

edges_3 = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]

source_3 = 0

destination_3 = 5

n_3 = 6

edges_3 = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]

source_3 = 0

destination_3 = 5

class Solution_3_BFS_Queue:
    def validPath(
        self, n_3: int, edges_3: List[List[int]], source_3: int, destination_3: int
    ) -> bool:
        # Store all the nodes to be visited in 'queue'.
        seen = [False] * n_3
        seen[source_3] = True
        queue = deque([source_3])

        # Store all edges_3 in 'graph'.
        graph = defaultdict(list)
        for a, b in edges_3:
            graph[a].append(b)
            graph[b].append(a)

        while queue:
            curr_node = queue.popleft()
            if curr_node == destination_3:
                return True

            # For all the neighbors of the current node, if we haven't visit it before,
            # add it to 'queue' and mark it as visited.
            for next_node in graph[curr_node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    queue.append(next_node)

        return False

# ============================================================================
# Solution 4: Disjoint_Set    (原文件: 1971 - D - Find if path exists - ⭐️ Disjoint Set 教科书 - 效率最高 🚀.py)
# ============================================================================

# Time complexity: O(m⋅α(n))
#
# The amortized complexity for performing m union find operations is O(m⋅α(n)) 
# time where α is the Inverse Ackermann Function.
# To sum up, the overall time complexity is O(m⋅α(n)).
#
# ========================================================================
#
# Space complexity: O(n)
#
# We used two arrays root and rank to save the root and rank 
# of each node in the DSU data structure, each of them takes O(n) space.
# To sum up, the overall time complexity is O(n).

class UnionFind_4:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n

    def find(self, x: int) -> int:
        if self.root[x] == x:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> None:
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[x] > self.rank[y]:
                self.root[rootY] = rootX
            elif self.rank[x] < self.rank[y]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1

class Solution_4_Disjoint_Set:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        unionFind = UnionFind_4(n)
        for x, y in edges:
            unionFind.union(x, y)
        return unionFind.find(source) == unionFind.find(destination)

# ============================================================================
# Solution 5: BFS_variant_2    (原文件: 1971 - E - Find if path exists - BFS (variant 2).py)
# ============================================================================

# Time complexity: O(V+E)
# Space complexity: O(V+E)

class Solution_5_BFS_variant_2:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        # ! Phase 1: Initialization
        graph = defaultdict(list)
        for x, y in edges:
            graph[x] += (y,)
            graph[y] += (x,)
        queue = deque([source])
        seen = [False] * n
        seen[source] = True

        # ! Phase 2: Iteration
        while queue:
            node = queue.popleft()
            if node == destination:
                return True
            for next_node in graph[node]:
                if not seen[next_node]:
                    seen[next_node] = True
                    queue.append(next_node)

        return False

# ============================================================================
# Solution 6: UnionFind_variant_2    (原文件: 1971 - F - Find if path exists - UnionFind (variant 2).py)
# ============================================================================

class UnionFind_6:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1

class Solution_6_UnionFind_variant_2:
    def validPath(
        self, n: int, edges: List[List[int]], source: int, destination: int
    ) -> bool:
        uf = UnionFind_6(n)
        for x, y in edges:
            uf.union(x, y)
        return uf.find(source) == uf.find(destination)


if __name__ == "__main__":

    # --- Solution 1: DFS_Recursive ---
    s = Solution_1_DFS_Recursive()
    result = s.validPath(n_1, edges_1, source_1, destination_1)
    print(result)

    # --- Solution 2: DFS_Stack ---
    s = Solution_2_DFS_Stack()
    result = s.validPath(n_2, edges_2, source_2, destination_2)
    print(result)

    # --- Solution 3: BFS_Queue ---
    s = Solution_3_BFS_Queue()
    result = s.validPath(n_3, edges_3, source_3, destination_3)
    print(result)
