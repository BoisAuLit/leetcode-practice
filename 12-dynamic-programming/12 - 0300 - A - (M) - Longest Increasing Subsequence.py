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
        for each element num, if num is greater than the largest element in our subsequence,
        then add it to the subsequence.
        
        Otherwise, perform a linear scan through the subsequence starting from the
        smallest element and replace the first element that is greater than or equal
        to num with num. This opens the door for elements that are greater than num
        but less than the element replaced to be included in the sequence.
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
