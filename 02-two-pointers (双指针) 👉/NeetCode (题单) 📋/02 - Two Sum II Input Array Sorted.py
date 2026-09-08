"""
📌 信号→模式: 有序数组两数之和 → 首尾相向双指针：和大移右、和小移左
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            sum_ = numbers[l] + numbers[r]
            if sum_ < target:
                l += 1
            elif sum_ > target:
                r -= 1
            else:
                return [l+1, r+1]

