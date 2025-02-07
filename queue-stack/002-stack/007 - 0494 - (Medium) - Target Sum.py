from typing import List

# Approach:Recursion with memoization
"""
Don't set cache direction under Solution, it won't work for different python interpreters


Time complexity: O(N * S)
S is the total sum(nums)

Space complexity: O(N* S)
"""


class Solution:
    def dfs(self, index: int, nums: List[int], target: int, cache) -> int:
        key = (index, target)
        if key in cache:
            return cache[key]
        if index == len(nums) - 1:
            if abs(nums[-1]) != abs(target):
                return 0
            if nums[-1] == 0:
                return 2
            return 1
        result = self.dfs(
            index + 1, nums, target - nums[index], cache
        ) + self.dfs(index + 1, nums, target + nums[index], cache)
        cache[key] = result
        return result

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        return self.dfs(0, nums, target, dict())



s = Solution()

# Test case 1: Expecting 5
nums = [1, 1, 1, 1, 1]
target = 3

# Test case 2: Expecting 2
# nums = [1, 1]
# target = 0

# Test case 3: Expecting 256
# nums = [0, 0, 0, 0, 0, 0, 0, 0, 1]
# target = 1


# Test case 4: Expecting 2
# nums = [1, 0]
# target = 1

result = s.findTargetSumWays(nums, target)
print(result)
