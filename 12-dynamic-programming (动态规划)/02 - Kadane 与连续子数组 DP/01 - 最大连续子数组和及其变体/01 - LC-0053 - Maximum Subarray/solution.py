from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        curr = best = nums[0]
        for x in nums[1:]:
            curr = max(x, curr+x) # Keep growing or restart?
            best = max(best, curr) # Update global best
        return best
