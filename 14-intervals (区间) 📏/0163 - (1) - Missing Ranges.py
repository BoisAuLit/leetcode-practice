from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def findMissingRanges(
        self, nums: List[int], lower: int, upper: int
    ) -> List[List[int]]:
        if len(nums) == 0:
            return [[lower, upper]]
        result = []
        if lower < nums[0]:
            result.append([lower, nums[0] - 1])
        for i in range(len(nums) - 1):
            if nums[i + 1] - nums[i] > 1:
                result.append([nums[i] + 1, nums[i + 1] - 1])
        if upper > nums[-1]:
            result.append([nums[-1] + 1, upper])
        return result

s = Solution()

# Expecting [[2,2],[4,49],[51,74],[76,99]]
# nums = [0, 1, 3, 50, 75]
# lower = 0
# upper = 99

# Expecting [[2,2],[4,49],[51,74],[76,99]]
# nums = [-1]
# lower = -1
# upper = -1

# Expecting []
# nums = [-1]
# lower = -1
# upper = -1

# Expecting [[1, 1]]
# nums = []
# lower = 1
# upper = 1

# Expecting [[-2, -1]]
nums = [-1]
lower = -2
upper = -1

result = s.findMissingRanges(nums, lower, upper)
print(result)

"""

"""
