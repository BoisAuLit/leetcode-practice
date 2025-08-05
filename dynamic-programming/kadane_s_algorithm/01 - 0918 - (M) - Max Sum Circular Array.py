from typing import List
import math


class Solution:
    """
    There are two cases:
    1. Normal kadane: we scan the array from index 0 to index N-1
    and find the maximum subarray

    2. Circular kadane: we find the minimum subarray, and
    use sum of whole array to substract the minimum subarray
    (only one exception: if all numbers are negative, then this should be zero)

    3. Then we compare the above two results, take the larger one.

    Explanation:
    https://leetcode.com/problems/maximum-sum-circular-subarray/solutions/3066636/weird-kadane-explanation-with-images-by-y4b1m
    """

    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        maxSum = nums[0]
        minSum = nums[0]
        currMaxSum = nums[0]
        currMinSum = nums[0]
        totalSum = nums[0]

        for i in range(1, len(nums)):
            # Kadane's algorithm for maximum sum
            # Either extend previous subarray or start a new one
            currMaxSum = max(currMaxSum + nums[i], nums[i])
            maxSum = max(maxSum, currMaxSum)

            # Kadane's algorithm for minimum sum
            # Either extend previous subarray or start a new one
            currMinSum = min(currMinSum + nums[i], nums[i])
            minSum = min(minSum, currMinSum)

            # Calculate the total sum of all elements
            totalSum += nums[i]

        # The circular sum is the total sum minus the minimum subarray sum
        circularSum = totalSum - minSum

        # Edge case: if all numbers are negative, then maxSum will be negative
        # and circularSum will be 0 (empty subarray), but we need to return the max negative value
        if circularSum == 0:
            return maxSum

        # Return the maximum of the regular subarray sum and the circular subarray sum
        return max(maxSum, circularSum)


s = Solution()
nums = [5, -3, 5]
result = s.maxSubarraySumCircular(nums)
print(result)
