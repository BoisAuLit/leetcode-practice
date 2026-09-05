from typing import List
from collections import defaultdict, deque

"""
Time complexity: O(N + E·k)
Space complexity: O(N + E·k)
"""

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((w, v))
        dist = [float("inf")] * n
        q = deque([(src, 0)])
        while k >= 0:
            for _ in range(len(q)):
                node, cost = q.popleft()
                for weight, neigh in graph[node]:
                    new_cost = weight + cost
                    if new_cost < dist[neigh]:
                        dist[neigh] = new_cost
                        q.append((neigh, new_cost))

            k-=1

        return dist[dst] if dist[dst] != float("inf") else -1
