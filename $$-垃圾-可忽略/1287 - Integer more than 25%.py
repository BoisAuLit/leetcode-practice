
from bisect import bisect_left, bisect_right
from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def findSpecialInteger(self, arr: List[int]) -> int:
        n = len(arr)
        candidates = [arr[n // 4], arr[n // 2], arr[3 * n // 4]]
        target = n / 4
        
        for candidate in candidates:
            left = bisect_left(arr, candidate)
            right = bisect_right(arr, candidate) - 1
            if right - left + 1 > target:
                return candidate
            
        return -1

s = Solution()
input_ = [1,2,2,6,6,6,6,7,10]
result = s.findSpecialInteger(input_)
print(result)

