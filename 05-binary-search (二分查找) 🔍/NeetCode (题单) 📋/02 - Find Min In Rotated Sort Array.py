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
