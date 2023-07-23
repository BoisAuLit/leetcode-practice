from typing import List
from collections import Counter


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return Counter(nums).most_common()[-1][0]



"""
Runtime
- Details
- 144ms
- Beats 64.00%

Memory
- Details
- 19.24mb
- Beats 20.73%
"""
