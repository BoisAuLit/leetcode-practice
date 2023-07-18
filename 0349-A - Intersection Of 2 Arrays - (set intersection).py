from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        s1 = set(nums1)
        s2 = set(nums2)
        return list(s1.intersection(s2))


s = Solution()
# Expecting [9, 4]
nums1 = [4, 9, 5]
nums2 = [9, 4, 9, 8, 4]
result = s.intersection(nums1, nums2)
print(result)

"""
Runtime
- 60ms
Beats 74.43%

Memory

- 16.38mb
- Beats 94.26%of
"""
