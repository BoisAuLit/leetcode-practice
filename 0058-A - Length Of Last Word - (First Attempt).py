"""
Time complexity: O(m)
Space complexity: O(1)
"""


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        index = len(s) - 1
        while s[index] == " ":
            index -= 1
        length = 0
        while s[index] != " " and index >= 0:
            length += 1
            index -= 1
        return length


s = Solution()
input_ = "   fly me   to   the moon  "
result = s.lengthOfLastWord(input_)
print(result)

"""
Runtime
- 53 ms
- Beats 11.44%

Memory
- 16.3 MB
- Beats 77.96%
"""
