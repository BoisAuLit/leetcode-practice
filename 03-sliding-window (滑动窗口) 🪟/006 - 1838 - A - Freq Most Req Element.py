from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()

        left = 0
        right = 1
        fuel = 0
        max_freq = 1

        # Moving the right pointer
        for right in range(1, len(nums)):
            fuel += (nums[right] - nums[right - 1]) * (right - left)

            # Moving the left pointer
            while fuel > k:
                fuel -= nums[right] - nums[left]
                left += 1
            max_freq = max(max_freq, right - left + 1)

        return max_freq


# # Test case 1: Expecting 2
# s = Solution()
# nums = [1, 4, 8, 13]
# k = 5
# result = s.maxFrequency(nums, k)
# print(result)

# Test case 2: Expecting 3
s = Solution()
nums = [1, 2, 4]
k = 5
result = s.maxFrequency(nums, k)
print(result)
