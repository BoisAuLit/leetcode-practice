"""LC-0787 - Cheapest Flights Within K Stops

合并自 7 个解法文件:
  1. 0787 - A - Cheapest Flights - BFS 🚀🚀🚀⭐️⭐️⭐️.py
  2. 0787 - B - Cheapest Flights - Bellman Ford Naïve 🐢.py
  3. 0787 - C - Cheapest Flights - Bellman Ford with Queue 🚀🚀🚀.py
  4. 0787 - D - Cheapest Flights - Dijkstra 🚀.py
  5. 0787 - E - Cheapest Flights Within K Stops - Bellman Ford (older version).py
  6. 0787 - F - Cheapest Flights Within K Stops - Dijkstra (older version).py
  7. 0787 - G - Cheapest Flights Within K Stops - BFS (older version).py
"""

from typing import List

from collections import defaultdict, deque

from collections import deque, defaultdict

import heapq

from collections import defaultdict


# ============================================================================
# Solution 1: BFS    (原文件: 0787 - A - Cheapest Flights - BFS 🚀🚀🚀⭐️⭐️⭐️.py)
# ============================================================================

# Time complexity: O(N + E·k)
# Space complexity: O(N + E·k)

class Solution_1_BFS:
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

# ============================================================================
# Solution 2: Bellman_Ford_Na_ve    (原文件: 0787 - B - Cheapest Flights - Bellman Ford Naïve 🐢.py)
# ============================================================================

# 我们不需要像 DP 那样有一个尺寸为 E·V 的 array
# 我们自始至终只需要两个尺寸为 E 的 array 就够了

class Solution_2_Bellman_Ford_Na_ve:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        previous = [float("inf")] * n

        previous[src] = 0
        # ! Attention it's (k+1) here not k
        # ! 因为一开始的第一次 pop（） 不算到 k 里面，所以要 +1
        for _ in range(k + 1):
            """
            Here we have to make a copy, because:

            If we update costs directly,
            then changes made in the current iteration 
            will affect calculations for the same iteration, 
            leading to incorrect results.
            """
            current = previous.copy()
            for start, end, price in flights:
                """
                This if condition ensures that we only update
                temp[end] if the starting node (start) has been reached before.

                If costs[start] == float("inf"),
                it means there is no known path to start yet, so we should not update end.
                """
                if previous[start] != float("inf"):
                    current[end] = min(current[end], previous[start] + price)
            previous = current
        return previous[dst] if previous[dst] != float("inf") else -1

# ============================================================================
# Solution 3: Bellman_Ford_with_Queue    (原文件: 0787 - C - Cheapest Flights - Bellman Ford with Queue 🚀🚀🚀.py)
# ============================================================================

# Time complexity: O(E·k)
# Space complexity: O(N·k + E)

class Solution_3_Bellman_Ford_with_Queue:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))

        dist = [float("inf")] * n
        dist[src] = 0
        queue = deque([(src, 0, 0)])# (node, cost, stops)
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

# ============================================================================
# Solution 4: Dijkstra    (原文件: 0787 - D - Cheapest Flights - Dijkstra 🚀.py)
# ============================================================================

# 最重要的事情：我们要将 k stops 编码到 heap 里面

class Solution_4_Dijkstra:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # Build adjacency list
        adj = defaultdict(list)
        for u, v, w in flights:
            adj[u].append((v, w))
        
        # stops[node] keeps track of the minimum stops used to reach node
        stops = [float('inf')] * n  
        
        # Priority queue: (dist_from_src, node, stops_from_src)
        heap = [(0, src, 0)]
        
        while heap:
            dist, node, steps = heapq.heappop(heap)
            
            # ! Already found a better path with fewer stops OR too many stops
            # ! 这里的这两个测试尤为关键
            if steps >= stops[node] or steps > k + 1:
                continue
            stops[node] = steps
            
            # If destination reached, return distance
            if node == dst:
                return dist
            
            # Explore neighbors
            for neighbor, price in adj[node]:
                heapq.heappush(heap, (dist + price, neighbor, steps + 1))
        
        return -1

# ============================================================================
# Solution 5: Bellman_Ford_older_version    (原文件: 0787 - E - Cheapest Flights Within K Stops - Bellman Ford (older version).py)
# ============================================================================

# https://www.youtube.com/watch?v=lyw4FaxrwHg&t=487s

class Solution_5_Bellman_Ford_older_version:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        costs = [float("inf")] * n

        costs[src] = 0
        for _ in range(k + 1): # ! Attention it's (k+1) here not k!
            """
            Here we have to make a copy, because:

            If we update costs directly,
            then changes made in the current iteration 
            will affect calculations for the same iteration, 
            leading to incorrect results.
            """
            temp = costs.copy()
            for start, end, price in flights:
                """
                This if condition ensures that we only update
                temp[end] if the starting node (start) has been reached before.

                If costs[start] == float("inf"),
                it means there is no known path to start yet, so we should not update end.
                """
                if costs[start] != float("inf"):
                    temp[end] = min(temp[end], costs[start] + price)
            costs = temp
        return costs[dst] if costs[dst] != float("inf") else -1

# ============================================================================
# Solution 6: Dijkstra_older_version    (原文件: 0787 - F - Cheapest Flights Within K Stops - Dijkstra (older version).py)
# ============================================================================

class Solution_6_Dijkstra_older_version:
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

# ============================================================================
# Solution 7: BFS_older_version    (原文件: 0787 - G - Cheapest Flights Within K Stops - BFS (older version).py)
# ============================================================================

class Solution_7_BFS_older_version:
    def findCheapestPrice(self, n, flights, src, dst, k):
        graph = defaultdict(list)
        for x, y, w in flights:
            graph[x].append((y, w))
        queue = deque([(src, 0)])
        costs = [float("inf")] * n
        while queue and k >= 0:
            for _ in range(len(queue)):
                node, cost = queue.popleft()
                for next_node, edge_weight in graph[node]:
                    new_cost = cost + edge_weight
                    if new_cost < costs[next_node]:
                        costs[next_node] = new_cost
                        queue.append((next_node, costs[next_node]))
            k -= 1
        return costs[dst] if costs[dst] != float("inf") else -1
