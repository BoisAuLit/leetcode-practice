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
        visited = set()
        heap = [(0, k)]
        while heap:
            cost, node = heapq.heappop(heap)
            visited.add(node)
            if len(visited) == n:
                return cost
            for new_cost, neighbor in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + new_cost, neighbor))

        return -1


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
