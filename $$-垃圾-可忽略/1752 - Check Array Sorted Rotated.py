from typing import List


class Solution:
    def check(self, nums: List[int]) -> bool:
        desc_count = 0
        for i in range(1, len(nums)):
            if nums[i] < nums[i - 1]:
                desc_count += 1
                if desc_count == 2:
                    return False
        return True if desc_count == 0 else nums[0] >= nums[-1]


s = Solution()
# nums = [3, 4, 5, 1, 2] # Expecting True
# nums = [5, 5, 6, 6, 6, 9, 1, 2]  # Expecting True
# nums = [2, 1, 3, 4]  # Expecting False
# nums = [1, 2, 3]  # Expecting True
# nums = [2, 4, 1, 3]  # Expecting false
nums = [6, 10, 6]  # Expecting True
result = s.check(nums)
print(result)

"""
Runtime
- 39ms
- Beats 91.09%

Memory
16.20mb
- Beats 92.15%
"""
