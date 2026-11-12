from typing import List
from collections import Counter

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        counter = Counter(arr)
        return len(counter) == len(set(counter.values()))


s = Solution()
input_ = [1, 2, 2, 1, 1, 3]  # Expecting True
result = s.uniqueOccurrences(input_)
print(result)

"""
Runtime
- 49 ms
- Beats 79.96%

Memory
- 16.5 MB
- Beats 15.82%
"""
