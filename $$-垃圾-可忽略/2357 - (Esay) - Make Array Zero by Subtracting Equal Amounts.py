from collections import Counter
from typing import List

"""
File: "./assets/2357.png"
"""

class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        counter = Counter(nums)
        if 0 in counter:
            del counter[0]
        return len(counter)

s = Solution()

# Expecting 3
input_ = [1,5,0,3,5]
result = s.minimumOperations(input_)
print(result)
