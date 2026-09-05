from typing import List
from functools import cache


class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        # States:
        # 1. Holding or not (0 means not holding, 1 means holding)
        # 2. i (index currently being processed)
        # 3. transactions already made (decides if we can continue or not)

        # Only when we sell will we decrease remain by 1
        @cache
        def dp(i: int, holding: int, remain: int) -> int:
            if i >= n or remain == 0:
                return 0
            do_nothing = dp(i + 1, holding, remain)
            if holding:
                return max(prices[i] + dp(i + 1, 0, remain - 1), do_nothing)
            else:
                return max(-prices[i] + dp(i + 1, 1, remain), do_nothing)

        return dp(0, 0, k)


# s = Solution()
# k = 2
# prices = [3, 2, 6, 5, 0, 3]
# result = s.maxProfit(k, prices)
# print(result)
