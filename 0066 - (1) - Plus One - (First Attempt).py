from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)
"""


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = 1
        for i in range(len(digits) - 1, -1, -1):
            carry, digits[i] = divmod(digits[i] + carry, 10)
        return [1] + digits if carry == 1 else digits


s = Solution()
input_ = [9, 9, 9]
result = s.plusOne(input_)
print(result)
