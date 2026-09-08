"""
📌 信号→模式: 一次买卖最大利润 → 一趟维护历史最低价，当前价 − 最低价取 max
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 下次: 2026-09-05
"""
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_ = prices[0]
        res = 0
        for p in prices:
            res = max(res, p - min_)
            min_ = min(min_, p)
        return res
