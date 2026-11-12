from typing import List
from bisect import bisect_left

"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        i = bisect_left(range(len(arr)), k, key=lambda i: arr[i] - i - 1)
        return k + i


s = Solution()

# Expecting 6
# arr = [2]
# k = 5

# Expecting 6
# arr = [1, 2, 3, 4]
# k = 2

# Expecting 2
# arr = [1, 3]
# k = 1

# Expecting 14
arr = [5,6,7,8,9]
k = 9



result = s.findKthPositive(arr, k)
print(result)

"""
Runtime
- 72ms
- Beats 42.06%

Memory
- 16.37mb
- Beats 91.45%
"""
