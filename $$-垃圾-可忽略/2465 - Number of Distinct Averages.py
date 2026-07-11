from typing import List


class Solution:
    def distinctAverages(self, nums: List[int]) -> int:
        nums.sort()
        p1 = 0
        p2 = len(nums) - 1
        sums = set()
        while p1 < p2:
            sums.add(nums[p1] + nums[p2])
            p1 += 1
            p2 -= 1
        return len(sums)
