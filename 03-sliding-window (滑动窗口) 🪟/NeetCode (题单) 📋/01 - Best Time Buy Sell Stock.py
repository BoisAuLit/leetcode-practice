from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_ = prices[0]
        res = 0
        for p in prices:
            res = max(res, p - min_)
            min_ = min(min_, p)
        return res
