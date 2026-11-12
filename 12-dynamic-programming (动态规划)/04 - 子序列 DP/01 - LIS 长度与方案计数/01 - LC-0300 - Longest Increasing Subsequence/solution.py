from bisect import bisect_left
from typing import List

class Solution_N_2_DP:
    """
    Time complexity: O(N²)
    Space complexity: O(N)
    """
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

class Solution_N_Log_N:
    def lengthOfLIS(self, nums: List[int]) -> int:

        """
        sub[i] 保存的是: 长度为 i+1 的 Increasing subsequence 的最小结尾
        之所以存最小结尾, 是因为最小结尾更有潜力被后面的数解题

        这题类似于 Kadane 都是持续更新 Subarray/Subsequence 的最优值
        """
        sub = []
        for num in nums:
            i = bisect_left(sub, num)

            # If num is greater than any element in sub
            if i == len(sub):
                sub.append(num)
            
            # Otherwise, replace the first element in sub greater than or equal to num
            else:
                sub[i] = num
        
        return len(sub)
