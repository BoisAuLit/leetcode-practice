"""LC-0743 - Network Delay Time

合并自 2 个解法文件:
  1. 0743 - A - Network Delay Time - 纯种 Dijkstra ✅.py
  2. 0743 - NeetCode - Network Delay Time (pointer to A).py
"""

from typing import List

from collections import defaultdict

import heapq


# ============================================================================
# Solution 1: Dijkstra    (原文件: 0743 - A - Network Delay Time - 纯种 Dijkstra ✅.py)
# ============================================================================

# Source 1:
#     Solution_1_Dijkstra: https://www.youtube.com/watch?v=pSqmAO-m7Lk
#     At 15:01
# 只有这个人解释的是最好最完整的，网上其他的解释都是屎，都没有以上这个 YouTube 视频讲得仔细，讲得好
# 如果想要理解 Dijkstra，只看这个视频就够了，如果一遍不够就看十遍，我是在看了第十遍之后才彻底明白的。
#
# Time complexity: O(E + E·log(N))
# Space complexity: O(N + E)

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

class Solution_1_Dijkstra:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((w, v))

        visited = set()
        dist = [float("inf")] * (n + 1)  # ! It's 1-indexed
        dist[k] = 0
        heap = [(0, k)]

        while heap:
            # ! The 1st time a node is popped, it's the shortest path.
            # ! The same node can be popped several times. The second time it's popped,
            # ! it'll be skipped
            cost, node = heapq.heappop(heap)

            # ! Optimizatoin 1
            if dist[node] < cost:
                continue

            visited.add(node)
            if len(visited) == n:
                return cost

            for weight, neigh in graph[node]:
                new_cost = cost + weight
                if new_cost < dist[neigh]:  # ! Optimization 2
                    dist[neigh] = new_cost
                    heapq.heappush(heap, (new_cost, neigh))
        return -1

# ============================================================================
# Solution 2: Network_Delay_Time_pointer_to_A    (原文件: 0743 - NeetCode - Network Delay Time (pointer to A).py)
# ============================================================================

# NeetCode "Network Delay Time" = LeetCode 0743. Solution lives next to this file:
# 0743 - A - Network Delay Time - 纯种 Dijkstra ✅.py


if __name__ == "__main__":

    # --- Solution 1: Dijkstra ---
    s = Solution_1_Dijkstra()
    result = s.networkDelayTime(times, n, k)
    print(result)
