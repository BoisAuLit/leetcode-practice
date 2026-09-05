from typing import List
from collections import defaultdict


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adj = defaultdict(list)

        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        nodes = set(range(n))  # 所有还没访问过的节点
        res = 0

        while nodes:
            node = nodes.pop()  # 随便选一个未访问节点
            stack = [node]

            while stack:
                node = stack.pop()

                for neigh in adj[node]:
                    if neigh in nodes:
                        nodes.remove(neigh)
                        stack.append(neigh)

            res += 1

        return res



s = Solution()
n = 5
edges = [[0, 1], [1, 2], [3, 4]]
result = s.countComponents(n, edges)
print(result)
