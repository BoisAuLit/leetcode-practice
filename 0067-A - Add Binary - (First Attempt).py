from itertools import zip_longest

"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result = []
        carry = 0
        for i, j in zip_longest(reversed(a), reversed(b), fillvalue="0"):
            carry, digit = divmod(int(i) + int(j) + carry, 2)
            result.append(str(digit))
        if carry == 1:
            result.append("1")
        return "".join(reversed(result))


s = Solution()
str1 = "1001"
str2 = "111"
result = s.addBinary(str1, str2)
print(result)

"""
Runtime
- 55 ms
- Beats 26.49%

Memory
- 16.5 MB
- Beats 10.46%
"""
