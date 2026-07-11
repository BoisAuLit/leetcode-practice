"""
Time complexity: O()
Space complexity: O()
"""

from typing import List

"""
Kadane's Algorithm
"""


class Solution:
    def maxSubArray(self, numbers: List[int]) -> int:
        max_sum = -float("inf")
        current_sum = 0
        for x in numbers:
            current_sum = max(x, current_sum + x)
            max_sum = max(max_sum, current_sum)
        return max_sum


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
