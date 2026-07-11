from typing import List
from collections import Counter


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        counter1 = Counter(nums1)
        counter2 = Counter(nums2)
        result = []
        for num, count in counter1.items():
            if num in counter2:
                result.extend([num] * min(count, counter2[num]))
        return result


s = Solution()

# Expecting [4, 9] or [9, 4]
# nums1 = [4, 9, 5]
# nums2 = [9, 4, 9, 8, 4]

# Expecting [2, 2]
nums1 = [1, 2, 2, 1]
nums2 = [2, 2]


result = s.intersect(nums1, nums2)
print(result)

"""

"""
