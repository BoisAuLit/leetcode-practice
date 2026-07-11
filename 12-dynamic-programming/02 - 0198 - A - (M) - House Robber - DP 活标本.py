from typing import List
from functools import lru_cache


# Solution 1: Iteration
class Solution_Bottom_Up_Iteration:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0:2])
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0:2])
        for i in range(2, n):
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
        return dp[-1]


class Solution_Top_Down_Memoization:
    def rob(self, nums: List[int]) -> int:
        @lru_cache(None)
        def dp(i: int) -> int:
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[0:2])

            return max(nums[i] + dp(i - 2), dp(i - 1))

        return dp(len(nums) - 1)
