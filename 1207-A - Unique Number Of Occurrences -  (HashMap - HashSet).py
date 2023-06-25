from typing import List

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        mapping = {}
        for number in arr:
            if number in mapping:
                mapping[number] += 1
            else:
                mapping[number] = 1
        set_ = set()
        for count in mapping.values():
            set_.add(count)
        return len(set_) == len(mapping)


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
