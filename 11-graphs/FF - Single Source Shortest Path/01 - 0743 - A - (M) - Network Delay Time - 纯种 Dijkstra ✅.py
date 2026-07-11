from typing import List
from collections import defaultdict
import heapq

"""

Source 1:
    Solution: https://www.youtube.com/watch?v=pSqmAO-m7Lk
    At 15:01
只有这个人解释的是最好最完整的，网上其他的解释都是屎，都没有以上这个 YouTube 视频讲得仔细，讲得好
如果想要理解 Dijkstra，只看这个视频就够了，如果一遍不够就看十遍，我是在看了第十遍之后才彻底明白的。

Time complexity: O(E + E·log(N))
Space complexity: O(N + E)
"""


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((w, v))

        visited = set()
        dist = [float("inf")] * (n + 1) # ! It's 1-indexed, so it's (n+1)
        dist[k] = 0 # ! k is the starting node, so it should be 0
        heap = [(0, k)]

        while heap:
            # ! The 1st time a node is popped, it's the shortest path.
            cost, node = heapq.heappop(heap)

            """
            ! Optimizatoin 1 ⭐️
            1. Skips heap entries that were pushed earlier with a worse cost and later improved.
            2. Prevents re-processing a node with an out-of-date distance.
            """
            if dist[node] < cost:
                continue

            # ! Stop early
            visited.add(node)
            if len(visited) == n:
                return cost

            for edge_weight, neighbor in graph[node]:
                if neighbor in visited:
                    continue
                new_cost = cost + edge_weight
                if new_cost < dist[neighbor]:  # ! Optimization 2 ⭐️
                    dist[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
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

# def getShortestPath(
#     self, end: int, dist: List[int], prev: List[int]
# ) -> List[int]:
#     path = []
#     if dist[end] == float("inf"):
#         return path
#     previous_node = end
#     while previous_node:
#         path.append(previous_node)
#         previous_node = prev[previous_node]
#     return path[::-1]
