from typing import List

"""
This problem is part of the problem 33 - Search rotated array
"""

class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:    # m 在左边那段高的部分,最小值一定在 m 右边
                l = m + 1            # m 已经排除
            else:                    # m 在右边那段低的部分,m 自己可能就是最小值
                r = m                # 所以不能排除 m
        return nums[l]               # l == r,剩下的那个点就是最小值
