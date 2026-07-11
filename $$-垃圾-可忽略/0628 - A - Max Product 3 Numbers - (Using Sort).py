from typing import List

"""
Time complexity: O(nlogn)
Space complexity: O(logn)
"""


class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        nums = sorted(nums)
        p1 = nums[0] * nums[1] * nums[-1]
        p2 = nums[-1] * nums[-2] * nums[-3]
        return max(p1, p2)


s = Solution()
input_ = [-100, -98, -1, 2, 3, 4]
result = s.maximumProduct(input_)
print(result)

"""
Runtime
- 240ms
- Beats 78.79%

Memory
17.59mb
- Beats 85.29%
"""
