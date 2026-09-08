"""
📌 信号→模式: 找成环边 → 反复剥度为 1 的叶子，留在环上的最后一条输入边即答案
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from collections import defaultdict, deque
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)

        adj = defaultdict(list)
        degree = [0] * (n + 1)

        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
            degree[a] += 1
            degree[b] += 1

        q = deque()

        # 所有 leaf 都不可能属于 cycle
        for node in range(1, n + 1):
            if degree[node] == 1:
                q.append(node)

        # 一层一层剥掉 leaves
        while q:
            node = q.popleft()

            degree[node] = 0  # 代表这个 node 已经被删除

            for neigh in adj[node]:
                if degree[neigh] == 0:
                    continue

                degree[neigh] -= 1 

                if degree[neigh] == 1:
                    q.append(neigh)

        # degree > 0 的节点现在全部在 cycle 中
        # 从后往前找最后出现的 cycle edge
        for a, b in reversed(edges):
            if degree[a] > 0 and degree[b] > 0:
                return [a, b]

        return []
