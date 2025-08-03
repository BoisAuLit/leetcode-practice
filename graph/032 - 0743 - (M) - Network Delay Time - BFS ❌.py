from typing import List
from collections import defaultdict, deque
import math


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for x, y, cost in times:
            graph[x].append((cost, y))
        costs = [math.inf] * (n + 1)
        costs[0] = costs[k] = 0
        queue = deque([k])
        while queue:
            node = queue.popleft()
            for cost, neighbor in graph[node]:
                new_time = costs[node] + cost
                if new_time < costs[neighbor]:
                    queue.append(neighbor)
                    costs[neighbor] = new_time
        max_time = max(costs)
        if max_time == math.inf:
            return -1
        return max_time


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
