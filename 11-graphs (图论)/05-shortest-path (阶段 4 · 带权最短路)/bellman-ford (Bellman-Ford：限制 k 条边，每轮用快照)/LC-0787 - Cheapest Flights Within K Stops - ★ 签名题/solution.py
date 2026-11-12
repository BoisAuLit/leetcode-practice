"""LC-0787 - Cheapest Flights Within K Stops

合并自 7 个解法文件:
  1. 0787 - A - Cheapest Flights - BFS 🚀🚀🚀⭐️⭐️⭐️.py
  2. 0787 - B - Cheapest Flights - Bellman Ford Naïve 🐢.py
  3. 0787 - C - Cheapest Flights - Bellman Ford with Queue 🚀🚀🚀.py
  4. 0787 - D - Cheapest Flights - Dijkstra 🚀.py
  5. 0787 - E - Cheapest Flights Within K Stops - Bellman Ford (older version).py
  6. 0787 - F - Cheapest Flights Within K Stops - Dijkstra (older version).py
  7. 0787 - G - Cheapest Flights Within K Stops - BFS (older version).py

阶段 4 · 带权最短路 · Bellman-Ford(限制 k 条边，每轮用快照) ★ 签名题
题目在问：从 src 飞到 dst，最多中转 k 次(= 最多 k+1 条边)，最便宜多少钱；到不了 -1
点是什么：n 个城市   边是什么：有向航班 u -> v，票价 w
和签名题比改了哪一行：本题就是签名题；"只跑 k+1 轮、每轮只看上一轮的快照"就是边数限制本身
为什么普通 Dijkstra 会错：它一弹出就把点钉死，可最便宜的那条路可能转机太多；
  便宜但超 k 条边的路会把"贵一点但转机少"的路挡掉。要么把 stops 编进状态(Solution 4)，
  要么干脆用 Bellman-Ford 按"第几条边"分层(Solution 1/2/3)
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

##################################################################################################
##### ! Solution 1: 分层 BFS (按"第几条边"一层层推，推 k+1 层)
##### ! 时间复杂度: O(E · k)   空间复杂度: O(N + E)
##### ! 适用：和 Bellman-Ford 同一个意思，只是用队列只碰"上一层真的被更新过的点"；用户原文件给的是 🚀🚀🚀⭐️⭐️⭐️
##################################################################################################

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

##################################################################################################
##### ! Solution 2: Bellman-Ford 快照版 (跑 k+1 轮，每轮只用上一轮的值)
##### ! 时间复杂度: O(E · k)   空间复杂度: O(N)   两个长度 N 的数组轮换
##### ! 适用：边数有上限 / 有负权；第 i 轮结束 = "≤ i 条边"的最便宜价，快照保证一轮只多走一条边
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution   本题是这个模板的签名题：最短、不会错、面试一句话讲清
##################################################################################################

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

##################################################################################################
##### ! Solution 3: Bellman-Ford 队列版 (stops 写进元组，不分层)
##### ! 时间复杂度: O(E · k)   空间复杂度: O(N + E)
##### ! 适用：和 Solution 1 本质相同；不能加 SPFA 的 in_queue 去重，因为同一个点不同 stops 是不同状态
##################################################################################################

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

##################################################################################################
##### ! Solution 4: Dijkstra 改状态 (cost, node, stops)，按"到这点用过的最少边数"剪枝
##### ! 时间复杂度: O(E · k · log(E · k))   空间复杂度: O(E · k)   每个点最多被展开 k+2 次(steps 严格递减)
##### ! 适用：非要用 Dijkstra 就得把 stops 编进状态；普通 Dijkstra 会错：弹出即钉死，可最便宜的路可能超 k 条边
##################################################################################################

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

##################################################################################################
##### ! Solution 5: Bellman-Ford 快照版 (旧版本，和 Solution 2 一样，留着对照)
##### ! 时间复杂度: O(E · k)   空间复杂度: O(N)
##### ! 适用：同 Solution 2
##################################################################################################

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

##################################################################################################
##### ! Solution 6: Dijkstra 改状态 (旧版本，和 Solution 4 一样，留着对照)
##### ! 时间复杂度: O(E · k · log(E · k))   空间复杂度: O(E · k)
##### ! 适用：同 Solution 4
##################################################################################################

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

##################################################################################################
##### ! Solution 7: 分层 BFS (旧版本，和 Solution 1 一样，留着对照)
##### ! 时间复杂度: O(E · k)   空间复杂度: O(N + E)
##### ! 适用：同 Solution 1
##################################################################################################

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


s = Solution_2_Bellman_Ford_Na_ve()
n = 4
flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
src, dst, k = 0, 3, 1
result = s.findCheapestPrice(n, flights, src, dst, k)
print(result)  # 700

n = 3
flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
result = s.findCheapestPrice(n, flights, 0, 2, 1)
print(result)  # 200
result = s.findCheapestPrice(n, flights, 0, 2, 0)
print(result)  # 500


##################################################################################################
##### ! Solution Alt: Dijkstra 状态扩展（把「已用几条边」压进状态）
##### ! 这是同一道题在本专题**另一个算法家族**里的实现 —— 不同算法，不是重复文件。
##### ! 主学习位置：bellman-ford (Bellman-Ford：限制 k 条边，每轮用快照)/LC-0787 - Cheapest Flights Within K Stops - ★ 签名题
##### ! 变体目录　：dijkstra/05 - Dijkstra 状态扩展与时间约束/变体 · 01 - LC-0787 - Cheapest Flights Within K Stops
##### ! 为什么这样定主次：instructions 指定本题优先学 Bellman-Ford + Snapshot；Dijkstra 状态扩展版作为对照实现保留
##### ! 为了让复习队列里一道题只出现一次，变体目录已改名为「变体 · …」（不再匹配题目前缀），
#####   但**文件一个都没删**，PDF / metadata / 笔记都还在原处。
##### ! 下面只搬了它的 import 和 class（类名加 _Alt 后缀避免冲突），
#####   原文件底部的示例驱动代码没有搬，以免干扰本文件的测试。
##################################################################################################


from collections import deque


from heapq import heappop, heappush


from typing import List


class Solution_1_Alt:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in flights:
            adj[u].append((v, w))

        # ! best[u] = 已经弹出过的、到 u 的最少航段数。因为按 cost 升序弹，
        # ! 后来的票一定更贵，只有"用的边更少"才值得再扩展一次
        best = [n + 1] * n
        heap = [(0, src, 0)]  # (总票价, 机场, 已用航段数)
        while heap:
            cost, u, used = heappop(heap)
            if u == dst:
                return cost  # ! 第一次弹到终点就是答案
            if used > k or used >= best[u]:
                continue  # ! 航段用超了，或者这张票被"更便宜且边更少"的记录支配了
            best[u] = used
            for v, w in adj[u]:
                heappush(heap, (cost + w, v, used + 1))
        return -1


class Solution_2_Alt:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):          # ! k 站经停 = 最多 k+1 条边 = 松弛 k+1 轮
            snapshot = dist[:]          # ! 快照是灵魂：本轮只能基于上一轮的结果，否则一轮串起好几条边
            for u, v, w in flights:
                if snapshot[u] + w < dist[v]:
                    dist[v] = snapshot[u] + w
        return -1 if dist[dst] == INF else dist[dst]


class Solution_3_Alt:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in flights:
            adj[u].append((v, w))

        INF = float("inf")
        best = [INF] * n            # ! best[v]：目前为止到 v 的最便宜花费（不限航段）
        best[src] = 0
        q = deque([(src, 0)])
        for _ in range(k + 1):      # ! 恰好扩展 k+1 层
            for _ in range(len(q)):
                u, cost = q.popleft()
                for v, w in adj[u]:
                    # ! 只有变便宜了才往下传，否则同一层会炸开成指数个状态
                    if cost + w < best[v]:
                        best[v] = cost + w
                        q.append((v, cost + w))
        return -1 if best[dst] == INF else best[dst]
