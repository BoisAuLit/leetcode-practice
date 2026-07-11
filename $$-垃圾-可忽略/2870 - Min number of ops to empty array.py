from typing import List
from collections import Counter
import math

"""
Time complexity: O(N)
Space complexity: O(N)
"""


class Solution:
    def minOperations(self, nums: List[int]) -> int:
        counter = Counter(nums)
        ans = 0
        for c in counter.values():
            if c == 1: 
                return -1
            ans += math.ceil(c / 3)
        return ans


s = Solution()
input_ = [2, 3, 3, 2, 2, 4, 2, 3, 4]  # 4
input_ = [2, 1, 2, 2, 3, 3]  # -1
result = s.minOperations(input_)
print(result)
