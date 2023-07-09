"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            while left < len(s) and not s[left].isalnum():
                left += 1
            while right > -1 and not s[right].isalnum():
                right -= 1
            if left == len(s) or right == -1:
                return True
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


s = Solution()
# input_ = "A man, a plan, a canal: Panama" # Expecting True
# input_ = "race a car" # Expecting False
# input_ = " "  # Expecting True
input_ = ".,"  # Expecting True
result = s.isPalindrome(input_)
print(result)

"""
Runtime
- 78 ms
- Beats 17.88%

Memory
- 17.2 MB
- Beats 51.59%
"""
