"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        digits = []
        while True:
            x, remainder = divmod(x, 10)
            digits.append(remainder)
            if x == 0:
                break
        i = 0
        while i < len(digits) // 2:
            if digits[i] != digits[-(i+1)]:
                return False
            i += 1
        return True

s = Solution()
input_ = -123
result = s.isPalindrome(input_)
print(result)
