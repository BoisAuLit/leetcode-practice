from typing import List
import math


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = math.inf
        max_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)

        return max_profit


s = Solution()

# Test case 1: Expecting 5
input_ = [7, 1, 5, 3, 6, 4]

result = s.maxProfit(input_)
print(result)
