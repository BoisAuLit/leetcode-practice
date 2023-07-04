from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        last_ten_bits_mask = (1 << 10) - 1
        for i in range(n):
            nums[i] = (nums[i] << 10) + nums[i + n]
        for i in range(n - 1, -1, -1):
            nums[2 * i + 1] = nums[i] & last_ten_bits_mask
            nums[2 * i] = nums[i] >> 10
        return nums


s = Solution()

# nums = [1,1,2,2] # Expecting [1, 2, 1, 2]
# n = 2

nums = [2, 5, 1, 3, 4, 7]
n = 3  # Expecting [2, 3, 5, 4, 1, 7]

result = s.shuffle(nums, n)
print(result)

"""
Runtime
- 72 ms
- Beats 73.39%

Memory
- 16.5 MB
- Beats 31.97%
"""
