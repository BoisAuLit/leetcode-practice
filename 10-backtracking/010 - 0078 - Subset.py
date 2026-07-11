from typing import List, Tuple, Set

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def backtrack(
            start: int, currentSubset: List[int], allSubsets: List[List[int]]
        ):
            allSubsets.append(currentSubset)
            for i in range(start, len(nums)):
                backtrack(i + 1, currentSubset + [nums[i]], allSubsets)

        allSubsets = []
        backtrack(0, [], allSubsets)
        return allSubsets


s = Solution()
nums = [1, 2, 3]
result = s.subsets(nums)
print(result)
