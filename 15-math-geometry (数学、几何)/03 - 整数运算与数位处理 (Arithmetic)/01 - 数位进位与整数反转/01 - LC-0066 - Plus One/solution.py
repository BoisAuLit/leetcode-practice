from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)
        carry = 1
        for i in range(n-1, -1, -1):
            carry, digits[i] = divmod(digits[i] + carry, 10)
        if carry:
            return [1] + digits
        return digits
