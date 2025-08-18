## Dijkstra
from collections import defaultdict
import heapq


class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        visited = {}
        graph = defaultdict(list)
        for src, dist, cost in flights:
            graph[src].append((dist, cost))
        heap = [(0, 0, src)]
        while heap:
            cost, stops, node = heapq.heappop(heap)
            if node == dst and stops - 1 <= k:
                return cost
            if node not in visited or visited[node] > stops:
                visited[node] = stops
                for neighbor, price in graph[node]:
                    heapq.heappush(heap, (cost + price, stops + 1, neighbor))
        return -1
