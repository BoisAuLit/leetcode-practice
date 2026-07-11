from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        result = [None] * (2 * n)
        result[0] = nums[0]
        result[-1] = nums[-1]
        for i in range(n - 1, -1, -1):
            result[2 * i] = nums[i]
        for i in range(n - 1):
            result[2 * i + 1] = nums[n + i]
        return result


s = Solution()

# nums = [1,1,2,2] # Expecting [1, 2, 1, 2]
# n = 2

nums = [2, 5, 1, 3, 4, 7]
n = 3  # Expecting [2, 3, 5, 4, 1, 7]

result = s.shuffle(nums, n)
print(result)

"""
Runtime
- 77 ms
- Beats 44.65%

Memory
- 16.5 MB
- Beats 31.69%
"""
