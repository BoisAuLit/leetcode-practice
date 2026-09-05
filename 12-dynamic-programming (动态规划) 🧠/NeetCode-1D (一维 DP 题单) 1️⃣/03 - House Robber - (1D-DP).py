from typing import List
from functools import lru_cache


class Solution_1:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        # from 0th to ith houses, max money we can rob
        @lru_cache
        def dp(i):
            if i == 0:
                return nums[0]
            if i == 1:
                return max(nums[:2])
            return max(nums[i] + dp(i - 2), dp(i - 1))

        return dp(n - 1)


class Solution_2:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[:2])

        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[:2])
        for i in range(2, n):
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])
        return dp[-1]


class Solution_3:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[:2])
        a, b = nums[0], max(nums[:2])
        for i in range(2, n):
            a, b = b, max(nums[i] + a, b)
        return b
