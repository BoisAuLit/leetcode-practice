from typing import List
from functools import cache


"""
The function dp(i, valid_until) means
- Starting from index i of days, what's the min cost of finishing the
  remaining days?
"""


class Solution_Top_Down_Memoization:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        n = len(days)

        @cache
        def dp(i: int, valid_until: int) -> int:
            if i >= n:
                return 0
            # Don't buy ticket today, because previous ticket is still valid today
            if valid_until >= days[i]:
                return dp(i + 1, valid_until)

            return min(
                costs[0] + dp(i + 1, days[i]),  # Buy a ticket only for 1 day
                costs[1] + dp(i + 1, days[i] + 6),  # Buy a ticket for 7 days
                costs[2] + dp(i + 1, days[i] + 29),  # Buy a ticket for 30 days
            )

        return dp(0, 0)


class Solution_Bottom_Up_Iteration:
    """
    ✅
    path = "../assets/0983.pdf"
    """

    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        travel = set(days)
        last = days[-1]
        dp = [0] * (last + 1)

        for d in range(1, last + 1):
            if d not in travel:
                dp[d] = dp[d - 1]  # no travel, no new cost
            else:
                one = dp[d - 1] + costs[0]
                seven = dp[max(0, d - 7)] + costs[1]
                thirty = dp[max(0, d - 30)] + costs[2]
                dp[d] = min(one, seven, thirty)

        return dp[last]
