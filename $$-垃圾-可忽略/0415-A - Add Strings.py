from itertools import zip_longest

"""
Time complexity: O(max(N₁, N₂))
Space complexity: O(max(N₁, N₂))
"""


class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        a1 = num1[::-1]
        a2 = num2[::-1]
        result = []
        carry = 0
        ascii_0 = ord("0")
        for d1, d2 in zip_longest(a1, a2, fillvalue="0"):
            digit_sum = (ord(d1) - ascii_0) + (ord(d2) - ascii_0) + carry
            carry, digit = divmod(digit_sum, 10)
            result.append(str(digit))
        if carry == 1:
            result.append("1")
        return "".join(result[::-1])


s = Solution()

# Expecting 533
# num1 = "456"
# num2 = "77"

# Expecting 10
num1 = "1"
num2 = "9"

result = s.addStrings(num1, num2)
print(result)

"""
Runtime
- 45ms
- Beats 86.32%

Memory
16.76mb
- Beats 19.74%
"""
