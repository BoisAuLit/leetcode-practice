from math import gcd


"""
Time complexity: O(m + n)
Space complexity: O(m + n)
"""


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""
        max_length = gcd(len(str1), len(str2))
        return str1[:max_length]


"""
Runtime
- 47ms
- Beats 67.65%

Memory
- 16.31mb
- Beats 47.06%
"""
