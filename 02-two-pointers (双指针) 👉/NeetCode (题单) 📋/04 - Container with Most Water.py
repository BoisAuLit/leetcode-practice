"""
📌 信号→模式: 两线围最大面积 → 相向双指针，移动较短的一侧（短板决定高度）
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def maxArea(self, heights: List[int]) -> int:
        res = -1
        l = 0
        r = len(heights) - 1
        while l < r:
            area = min(heights[r], heights[l]) * (r - l)
            res = max(res, area)
            if heights[l] <= heights[r]:
                l += 1
            else:
                r -= 1
        return res
