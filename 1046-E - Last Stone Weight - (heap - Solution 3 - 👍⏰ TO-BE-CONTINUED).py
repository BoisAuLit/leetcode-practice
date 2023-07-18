from typing import List
import bisect

"""
Time complexity: O(n2)
Space complexity:
- O(1) if we can modify input list in place
- O(n) if we cannot modify input list in place
"""


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        pass


s = Solution()
input_ = [2, 7, 4, 1, 8, 1]  # Expecting 1
# input_ = [1] # Expecting 1
# input_ = [3, 7, 8]  # Expecting 2
# input_ = [4, 3, 4, 3, 2]  # Expecting 2
result = s.lastStoneWeight(input_)
print(result)

"""
Runtime
- 48 ms
- Beats 60.6%

Memory
- 16.3 MB
- Beats 33.76%
"""
