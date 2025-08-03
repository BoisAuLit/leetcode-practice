from collections import defaultdict, deque


class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        graph = defaultdict(list)
        for x, y, cost in flights:
            graph[x].append((y, cost))
        queue = deque([(src, 0)])
        costs = [float("inf")] * n
        while queue and k >= 0:
            for _ in range(len(queue)):
                node, cost = queue.popleft()
                for neighbor, new_cost in graph[node]:
                    new_total_cost = cost + new_cost
                    if new_total_cost < costs[neighbor]:
                        costs[neighbor] = new_total_cost
                        queue.append((neighbor, costs[neighbor]))
            k -= 1
        return costs[dst] if costs[dst] != float("inf") else -1
