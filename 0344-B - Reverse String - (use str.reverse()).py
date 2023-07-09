"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def reverseString(self, s):
        s.reverse()


s = Solution()
input_ = ["h","e","l","l","o"] # Expecting ["o","l","l","e","h"]
input_ = ["H","a","n","n","a","h"] # Expecting ["h","a","n","n","a","H"]
result = s.reverseString(input_)
print(result)

"""
Runtime
- 218 ms
- Beats 74.67%

Memory
- 20.8 MB
- Beats 55.12%
"""
