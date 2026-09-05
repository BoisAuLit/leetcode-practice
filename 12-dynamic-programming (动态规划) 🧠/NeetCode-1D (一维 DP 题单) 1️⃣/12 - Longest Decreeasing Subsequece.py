from typing import List

from bisect import bisect_left

class Solution_1:
    def lengthOfLDS(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [1] * n

        for i in range(n):
            for j in range(i):
                if nums[j] > nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)


class Solution_2:
    def lengthOfLDS(self, nums: List[int]) -> int:
        tails = []

        for num in nums:
            num = -num

            i = bisect_left(tails, num)

            if i == len(tails):
                tails.append(num)
            else:
                tails[i] = num

        return len(tails)
