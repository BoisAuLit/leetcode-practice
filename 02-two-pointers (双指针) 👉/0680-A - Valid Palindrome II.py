"""
Time complexity: O(N)
Space complexity: O(1)
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def validPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return self.isPalindrome(
                    s[left + 1 : right + 1]
                ) or self.isPalindrome(s[left:right])
            left += 1
            right -= 1

        return True


s = Solution()

# Expecting True
# input_ = "aguokepatgbnvfqmgmlcupuufxoohdfpgjdmysgvhmvffcnqxjjxqncffvmhvgsymdjgpfdhooxfuupuculmgmqfvnbgtapekouga"

# Expecting True
# input_ = "akbcdeffedcba"

# Expecting False
input_ = "abc"

result = s.validPalindrome(input_)
print(result)

"""
Runtime
- 129ms
- Beats 61.01%

Memory
16.83mb
- Beats 76.96%
"""
