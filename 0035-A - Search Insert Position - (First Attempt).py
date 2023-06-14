from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        for index, number in enumerate(nums):
            if target <= number:
                return index
        return len(nums)


s = Solution()
result = s.searchInsert([1, 3, 5, 6], 5)
print(result)


"""
Runtime
- 69 ms
- Beats 26.1%

Memory
- 17.1 MB
- Beats 71.53%
"""
