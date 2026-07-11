from collections import Counter
from typing import List


class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        counter = Counter(nums)
        dp = [0] * len(counter)
        items = sorted(counter.items())
        dp[0] = items[0][0] * items[0][1]
        for i in range(1, len(items)):
            num, count = items[i]
            if items[i][0] == items[i - 1][0] + 1:
                dp[i] = max(
                    dp[i - 1], num * count + (dp[i - 2] if i - 2 >= 0 else 0)
                )
            else:
                dp[i] = num * count + dp[i - 1]
        return dp[-1]
