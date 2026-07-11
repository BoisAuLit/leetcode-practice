from typing import List

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        return max(sum(x) for x in accounts)


s = Solution()
input_ = [[2, 8, 7], [7, 1, 3], [1, 9, 5]]  # Expecting 17
result = s.maximumWealth(input_)
print(result)

"""
Runtime
- 58 ms
- Beats 96.93%

Memory
- 16.3 MB
- Beats 93%
"""
