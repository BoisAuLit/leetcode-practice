from collections import defaultdict, deque

"""
Time complexity: O(N + E·k)
Space complexity: O(N + E·k)
"""

class Solution:
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
