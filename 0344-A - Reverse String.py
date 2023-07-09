from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def reverseString(self, s: List[str]) -> None:
        left = 0
        right = len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1


s = Solution()
input_ = ["h","e","l","l","o"] # Expecting ["o","l","l","e","h"]
input_ = ["H","a","n","n","a","h"] # Expecting ["h","a","n","n","a","H"]
result = s.reverseString(input_)
print(result)

"""
Runtime
- 220 ms
- Beats 66.65%

Memory
- 20.7 MB
- Beats 55.12%
"""
