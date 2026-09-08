"""
📌 信号→模式: 最大乘积子数组 → Kadane 变体同时维护 curMax / curMin（负数翻转）
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        currMax = currMin = res = nums[0]

        for num in nums[1:]:
            prevMax = currMax
            prevMin = currMin
            currMax = max(num, prevMax * num, prevMin * num)
            currMin = min(num, prevMax * num, prevMin * num)
            res = max(res, currMax)

        return res
