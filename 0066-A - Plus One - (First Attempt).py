from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = 0
        for i in range(len(digits) - 1, -1, -1):
            carry, digits[i] = divmod(digits[i] + carry + (i == len(digits) - 1), 10)
        if carry == 1:
            digits.insert(0, 1)
        return digits


s = Solution()
input_ = [9, 9, 9]
result = s.plusOne(input_)
print(result)

"""
Runtime
- 51 ms
- Beats 33.45%

Memory
- 16.4 MB
- Beats 18.67%
"""
