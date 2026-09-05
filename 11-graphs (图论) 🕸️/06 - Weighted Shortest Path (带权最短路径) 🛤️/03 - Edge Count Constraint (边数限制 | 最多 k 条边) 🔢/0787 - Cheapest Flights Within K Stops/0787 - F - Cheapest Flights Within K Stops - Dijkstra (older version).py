import heapq
from collections import defaultdict
from typing import List

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # Build adjacency list
        adj = defaultdict(list)
        for u, v, w in flights:
            adj[u].append((v, w))
        
        # stops[node] keeps track of the minimum stops used to reach node
        stops = [float('inf')] * n  
        
        # Priority queue: (dist_from_src, node, stops_from_src)
        pq = [(0, src, 0)]
        
        while pq:
            dist, node, steps = heapq.heappop(pq)
            
            # Already found a better path with fewer stops OR too many stops
            if steps >= stops[node] or steps > k + 1:
                continue
            stops[node] = steps
            
            # If destination reached, return distance
            if node == dst:
                return dist
            
            # Explore neighbors
            for neighbor, price in adj[node]:
                heapq.heappush(pq, (dist + price, neighbor, steps + 1))
        
        return -1
