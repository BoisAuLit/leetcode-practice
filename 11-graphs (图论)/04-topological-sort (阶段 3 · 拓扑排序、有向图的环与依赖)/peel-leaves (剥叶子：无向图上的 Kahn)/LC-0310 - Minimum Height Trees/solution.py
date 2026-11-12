"""LC-0310 - Minimum Height Trees

阶段 3 · 拓扑排序 · 剥叶子（无向图上的 Kahn）○ 核心
题目在问：以哪个点为根整棵树最矮，答案是 1 个或 2 个点（树的中心）
点是什么：树的结点   边是什么：无向树边
和签名题比改了哪一行：207 的"入度为 0 进队"改成"度为 1（叶子）进队"，一层一层剥，剩 <= 2 个点就停
"""
from collections import defaultdict, deque
from typing import List


"""
Time complexity: O(V)
Space Complexity O(V)
"""


##################################################################################################
##### ! Solution 1: 剥叶子（无向图上的 Kahn）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   树有 n - 1 条边，V + E = O(n)
##### ! 适用：求树的中心 / 最矮根；每一轮所有叶子一起掉，最后剩下的 1 或 2 个点就是中心
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Return all roots of Minimum Height Trees (MHTs) in an undirected tree.

        Algorithm:
          - Build adjacency list and initial degrees.
          - Push all current leaves (degree == 1) into a queue.
          - Iteratively trim leaves level by level until ≤ 2 nodes remain.
          - The remaining 1–2 nodes are the centroids (MHT roots).

        Time:  O(n)
        Space: O(n)
        """
        if n == 1:
            return [0]

        # Build graph and degree array
        graph: dict[int, list[int]] = defaultdict(list)
        degree: List[int] = [0] * n

        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
            degree[u] += 1
            degree[v] += 1

        # Initialize leaves
        queue = deque(i for i, d in enumerate(degree) if d == 1)

        # Trim leaves until at most two nodes remain
        remain = n
        while remain > 2:
            leaves_count = len(queue)
            remain -= leaves_count

            for _ in range(leaves_count):
                leaf = queue.popleft()
                for nei in graph[leaf]:
                    degree[nei] -= 1
                    if degree[nei] == 1:
                        queue.append(nei)

        return list(queue)


##################################################################################################
##### ! Solution 2: 两遍 BFS 找直径，取直径的中点
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：记得"最矮根 = 直径中点"这个结论时；第一遍找直径一端 a，第二遍从 a 找另一端 b 并记 parent
##################################################################################################


class Solution_2:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        def bfs(src: int):
            # ! 返回 (离 src 最远的点, parent)，BFS 最后出队的点一定是最远的
            parent = [-1] * n
            parent[src] = src
            q = deque([src])
            far = src
            while q:
                far = q.popleft()
                for v in graph[far]:
                    if parent[v] == -1:
                        parent[v] = far
                        q.append(v)
            return far, parent

        a, _ = bfs(0)  # ! 第一遍：从任意点出发，最远点 a 一定是直径的一个端点
        b, parent = bfs(a)  # ! 第二遍：从 a 出发，最远点 b 是另一端，parent 串起 a -> b 这条路

        path = []
        while b != a:  # ! 沿 parent 从 b 走回 a，得到直径上的所有点
            path.append(b)
            b = parent[b]
        path.append(a)

        k = len(path)  # ! 直径有 k 个点：奇数取正中 1 个，偶数取中间 2 个
        return path[(k - 1) // 2 : k // 2 + 1]


s = Solution()
n = 4
edges = [[1, 0], [1, 2], [1, 3]]
result = s.findMinHeightTrees(n, edges)
print(result)
