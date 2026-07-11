from typing import List

"""
Time complexity: O(min(m,n)⋅(m+n))
Space complexity: O(min(m,n))
"""


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        shorter = str1 if len(str1) < len(str2) else str2
        longer = str2 if str1 == shorter else str1
        for i in range(len(shorter), 0, -1):
            q1, r1 = divmod(len(longer), len(shorter[:i]))
            q2, r2 = divmod(len(shorter), len(shorter[:i]))
            if r1 == 0 and r2 == 0 and q1 * shorter[:i] == longer and q2 * shorter[:i] == shorter:
                return shorter[:i]
        return ""


s = Solution()

# Expecting "ABC"
# str1 = "ABCABC"
# str2 = "ABC"

# Expecting "AB"
# str1 = "ABABAB"
# str2 = "ABAB"


# Expecting ""
str1 = "LEET"
str2 = "CODE"


result = s.gcdOfStrings(str1, str2)
print(result)

"""
Runtime
- 48ms
- Beats 61.41%

Memory
- 16.45mb
- Beats 11.93%
"""
