from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = prices[0]
        max_profit = 0
        for price in prices:
            if price < min_price:
                min_price = price
            profit = price - min_price
            if profit > max_profit:
                max_profit = profit
        return max_profit


s = Solution()
input_ = [7, 1, 5, 3, 6, 4]  # Expecting 6
result = s.maxProfit(input_)
print(result)

"""
Runtime
- 876 ms
- Beats 99.51%

Memory
- 27.4 MB
- Beats 22.52%
"""
