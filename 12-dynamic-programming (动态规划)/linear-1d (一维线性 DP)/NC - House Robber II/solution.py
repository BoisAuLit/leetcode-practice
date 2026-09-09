from typing import List
from functools import lru_cache

class Solution:
    def robI(self, nums:List[int]) -> int:
        n = len(nums)
        @lru_cache
        def dp(i):
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[:2])
            return max(dp(i-1), dp(i-2) + nums[i])
        return dp(n-1)
            

    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 3:
            return max(nums)
        # If we take first, then we should remove first 2, last 1
        a = nums[0] + self.robI(nums[2:-1])
        # If we don't take first, then we should remove first 1
        b = self.robI(nums[1:])
        return max(a, b)


s = Solution()
nums=[1,2,1,1]
result = s.rob(nums)
print(result)
