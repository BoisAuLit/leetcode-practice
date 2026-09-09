from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        insertIndex = 1
        for i in range(1, len(nums)):
            if nums[i - 1] != nums[i]:
                nums[insertIndex] = nums[i]
                insertIndex = insertIndex + 1
        return insertIndex


s = Solution()

# Expecting 2
input_ = [1, 1, 2]

result = s.removeDuplicates(input_)
print(input_)
print(result)
