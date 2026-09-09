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
