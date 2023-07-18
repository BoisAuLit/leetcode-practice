from typing import List
from statistics import mode

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return mode(nums)
        # return most_common, count = Counter([3, 2, 2, 2, 1, 1]).most_common(1)[0]
        

s = Solution()
nums = [2, 2, 1, 1, 1, 2, 2]
result = s.majorityElement(nums)
print(result)

"""
Runtime
- 178ms
- Beats 49.06%

Memory
- 17.82mb
- Beats 73.71%
"""
