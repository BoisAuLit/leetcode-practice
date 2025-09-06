## Bellman Ford
from typing import List

"""
我们不需要像 DP 那样有一个尺寸为 E·V 的 array
我们自始至终只需要两个尺寸为 E 的 array 就够了
"""

class Solution:
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
