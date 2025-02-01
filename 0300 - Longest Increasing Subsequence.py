from typing import List
from functools import lru_cache
import math

"""
Difficulty: Medium

Files: "./assets/0300_craft.jpeg"

"""


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        length = len(nums)

        @lru_cache(maxsize=None)
        def dfs(p: int) -> int:
            if p == length:
                return 1
            results = [0]
            smallest_bigger_number = math.inf
            for i in range(p + 1, length):
                if nums[i] > nums[p] and nums[i] < smallest_bigger_number:
                    smallest_bigger_number = nums[i]
                    results.append(dfs(i))
            return 1 + max(results)

        return max(dfs(p) for p in range(length))


s = Solution()
input_ = [10, 9, 2, 5, 3, 7, 101, 18]
result = s.lengthOfLIS(input_)
print(result)
