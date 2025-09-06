## Bellman Ford
from typing import List
from collections import deque, defaultdict

"""
Time complexity: O(E·k)
Space complexity: O(N·k + E)
"""


class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))

        dist = [float("inf")] * n
        dist[src] = 0
        queue = deque()
        queue.append((src, 0, 0))  # (node, cost, stops)
        # 注意，这里不能使用 SPFA 常用的 in_queue 操作，否则会失效

        while queue:
            node, cost, stops = queue.popleft()
            if stops > k:
                continue
            for neighbor, price in graph[node]:
                new_cost = cost + price
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    queue.append((neighbor, new_cost, stops + 1))

        return dist[dst] if dist[dst] != float("inf") else -1
