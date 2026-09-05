from typing import List


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        max_val = ans = current_streak = 0
        for num in nums:
            if max_val < num:
                max_val = num
                ans = current_streak = 0

            if max_val == num:
                current_streak += 1
            else:
                current_streak = 0

            ans = max(ans, current_streak)
        return ans


# Test case 1: Expecting 2
s = Solution()
nums = [1, 2, 3, 3, 2, 2]
result = s.longestSubarray(nums)
print(result)
