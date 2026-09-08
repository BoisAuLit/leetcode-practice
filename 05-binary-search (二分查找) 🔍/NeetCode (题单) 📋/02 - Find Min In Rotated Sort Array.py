"""
📌 信号→模式: 旋转有序数组最小值 → 二分，比较 mid 与 right 判断落在哪段
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        if nums[0] <= nums[-1]:
            return nums[0]
        l = 0
        r = len(nums) - 1
        while l <= r:
            m = (l+r)//2
            if nums[m] > nums[m+1]:
                return nums[m+1]
            if nums[m] > nums[l]:
                l = m
            else:
                r = m
        return l
