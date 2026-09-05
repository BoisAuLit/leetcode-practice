from typing import List

"""
Time complexity: O(nlogn)
Space complexity: O(n) or O(logn)
"""

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return sorted(x * x for x in nums)        

"""
Runtime
- 227ms
- Beats 69.61%

Memory
- 18.34mb
- Beats 87.83%
"""
