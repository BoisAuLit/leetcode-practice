"""
Time complexity: O()
Space complexity: O()
"""

from typing import List




class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # Initialize our variables using the first element.
        current_subarray = max_subarray = nums[0]

        # Start with the 2nd element since we already used the first one.
        for num in nums[1:]:
            # If current_subarray is negative, throw it away. Otherwise, keep adding to it.
            current_subarray = max(num, current_subarray + num)
            max_subarray = max(max_subarray, current_subarray)

        return max_subarray

s = Solution()

# Expecting 6
# nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

# Expecting 1
# nums = [1]

# Expecting -1
# nums = [-2, -1]

# Expecting 21
# nums = [8, -19, 5, -4, 20]

# Expecting 23
# nums = [5, 4, -1, 7, 8]

# Expecting 1
# nums = [-2, 1]

# Expecting 3
# nums = [1, 2, -1]

# Expecting 1
nums = [1, -1, -2]


result = s.maxSubArray(nums)
print(result)

"""

"""
