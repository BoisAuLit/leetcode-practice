"""
Time complexity: O(log10n)
Space complexity: O(1)
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        if x < 10:
            return True
        hp = 0
        while True:
            x, remainder = divmod(x, 10)
            hp = hp * 10 + remainder
            if hp > x or hp == 0:
                return False
            if hp == x or hp == x // 10:
                return True
            


s = Solution()
input_ = 10
result = s.isPalindrome(input_)
print(result)
