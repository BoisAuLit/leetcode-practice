from typing import List
from collections import defaultdict
import heapq

"""
Best tutorial:
https://www.youtube.com/watch?v=pSqmAO-m7Lk
“"""


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for x, y, w in times:
            graph[x].append((w, y))
        dist = [float("inf")] * (n + 1)
        dist[k] = 0
        heap = [(0, k)]
        while heap:
            cost, node = heapq.heappop(heap)
            if cost > dist[node]:
                continue
            for new_cost, neighbor in graph[node]:
                new_total_cost = cost + new_cost
                if new_total_cost < dist[neighbor]:
                    dist[neighbor] = new_total_cost
                    heapq.heappush(heap, (new_total_cost, neighbor))
        answer = max(dist[1:])
        return -1 if answer == float("inf") else answer


s = Solution()
times = [
    [1, 2, 1],
    [1, 4, 3],
    [1, 3, 1],
    [2, 1, 5],
    [2, 4, 2],
    [3, 4, 1],
    [4, 5, 2],
]
n = 5
k = 1

result = s.networkDelayTime(times, n, k)
print(result)
