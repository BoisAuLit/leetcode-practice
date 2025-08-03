## Bellman Ford
from typing import List

"""
https://www.youtube.com/watch?v=lyw4FaxrwHg&t=487s
"""


class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        costs = [float("inf")] * n

        costs[src] = 0
        for _ in range(k + 1):
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
                    temp[end] = min(costs[start] + price, temp[end])
            costs = temp
        return costs[dst] if costs[dst] != float("inf") else -1
