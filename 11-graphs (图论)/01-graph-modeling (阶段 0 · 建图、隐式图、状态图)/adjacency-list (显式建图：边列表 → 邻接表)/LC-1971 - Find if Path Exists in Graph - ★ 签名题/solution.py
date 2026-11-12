"""LC-1971 - Find if Path Exists in Graph

合并自 6 个解法文件:
  1. 1971 - A - Find if path exists - ⭐️ DFS Recursive 教科书 - 效率最低 🐢.py
  2. 1971 - B - Find if path exists - ⭐️ DFS Stack 教科书 - 效率一般 😅.py
  3. 1971 - C - Find if path exists - ⭐️ BFS Queue 教科书 - 效率最高 🔥.py
  4. 1971 - D - Find if path exists - ⭐️ Disjoint Set 教科书 - 效率最高 🚀.py
  5. 1971 - E - Find if path exists - BFS (variant 2).py

阶段 0 · 建图、隐式图、状态图 · 显式建图(边列表 → 邻接表) ★ 签名题
题目在问：n 个点、无向边表 edges，source 能不能走到 destination
点是什么：0..n-1   边是什么：edges 里每一对 [u, v]，无向所以两边都存
和签名题比改了哪一行：本题就是签名题。模板 = 建邻接表 + seen 数组 + (递归 DFS / 栈 DFS / 队列 BFS) 任选一个；
  并查集是另一条路：把边全 union 完，看两点是否同根(适合离线、多次查询)
注：下面 6 个 class 已经覆盖 DFS 递归 / DFS 栈 / BFS / 并查集，没有缺的解法，这次只补 banner 和复杂度
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

##################################################################################################
##### ! Solution 1: DFS 递归
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   邻接表 + seen + 递归栈(最深 V 层)
##### ! 适用：最直观的写法；但 n 到 2e5 的链状图会爆 Python 递归深度，LeetCode 上要 sys.setrecursionlimit 或改用下面的栈版
##### ! 注意：参数名 n_1/edges_1/... 不是 LeetCode 签名(n/edges/source/destination)，贴回去要改名
##################################################################################################


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

##################################################################################################
##### ! Solution 2: DFS 迭代(栈)
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   把递归栈换成自己管的 deque，不怕深度
##### ! 适用：和递归版逻辑一样，只是 "dfs(next_node)" 换成 "stack.append(next_node)"
##################################################################################################


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

##################################################################################################
##### ! Solution 3: BFS 队列
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   和栈版只差 pop() 换 popleft()
##### ! 适用：签名题的最裸模板；要 "能不能到" 用它，以后要 "最少几步" 也是它(加一层 step 计数)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution   (三种遍历并列正确，选 BFS 是因为它直接长成阶段 1 的最短路模板)
##################################################################################################


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

##################################################################################################
##### ! Solution 4: 并查集(按秩合并 + 路径压缩)
##### ! 时间复杂度: O((V + E) · α(V))   空间复杂度: O(V)   不建邻接表，边全 union 完比一次 find
##### ! 适用：离线 / 多次查询连通性时比遍历划算；单次查询其实和 BFS 一样快
##################################################################################################


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
            # ! ⚠️ 这里有问题：比较的是 rank[x] / rank[y](原始点)，应该比 rank[rootX] / rank[rootY](根)，
            # ! ⚠️ 结果仍然正确(只影响树高，不影响连通性判断)，但 "按秩合并" 实际上没生效；正确写法见下面的 UnionFind_6
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

##################################################################################################
##### ! Solution 5: BFS 变体 2(和 Solution 3 完全同构)
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   区别只是参数名改成了 LeetCode 签名、建图用 += (y,)
##### ! 适用：可直接粘贴到 LeetCode 的 BFS 版本
##################################################################################################


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

##################################################################################################
##### ! Solution 6: 并查集变体 2(UnionFind_6 的 rank 比较写对了，用 rootX/rootY)
##### ! 时间复杂度: O((V + E) · α(V))   空间复杂度: O(V)
##### ! 适用：可直接粘贴到 LeetCode 的并查集版本
##################################################################################################


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
