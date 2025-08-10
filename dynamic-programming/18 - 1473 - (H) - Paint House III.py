from functools import lru_cache
from typing import List


class Solution_Top_Down_Memoization:
    def minCost(
        self,
        houses: List[int],
        cost: List[List[int]],
        m: int,
        n: int,
        target: int,
    ) -> int:
        @lru_cache(None)
        def min_cost_helper(i, prev_color, groups):
            if i == m:
                return 0 if groups == target else float("inf")

            if houses[i] != 0:
                return min_cost_helper(
                    i + 1, houses[i], groups + int(prev_color != houses[i])
                )

            total = float("inf")
            for color in range(1, n + 1):
                total = min(
                    total,
                    cost[i][color - 1]
                    + min_cost_helper(
                        i + 1, color, groups + int(prev_color != color)
                    ),
                )

            return total

        ans = min_cost_helper(0, -1, 0)
        return ans if ans != float("inf") else -1


class Solution:
    def minCost(
        self,
        houses: List[int],
        cost: List[List[int]],
        m: int,
        n: int,
        target: int,
    ) -> int:
        MAX_COST = 1_000_001

        @lru_cache(None)
        def find_min_cost(idx: int, neighborhoods: int, prev_color: int) -> int:
            if idx == m:
                return 0 if neighborhoods == target else MAX_COST
            if neighborhoods > target:
                return MAX_COST

            # Already painted
            if houses[idx] != 0:
                new_nb = neighborhoods + (1 if houses[idx] != prev_color else 0)
                return find_min_cost(idx + 1, new_nb, houses[idx])

            # Try all colors
            ans = MAX_COST
            for color in range(1, n + 1):
                new_nb = neighborhoods + (1 if color != prev_color else 0)
                curr = cost[idx][color - 1] + find_min_cost(
                    idx + 1, new_nb, color
                )
                if curr < ans:
                    ans = curr
            return ans

        res = find_min_cost(0, 0, 0)
        return -1 if res == MAX_COST else res
