from typing import List
from bisect import bisect_left, bisect_right


class Solution:
    def searchRange(self, nums: List[int], target_1: int) -> List[int]:
        i1 = bisect_left(nums, target_1)
        i2 = bisect_right(nums, target_1)
        return [i1, i2 - 1] if i1 != i2 else [-1, -1]
