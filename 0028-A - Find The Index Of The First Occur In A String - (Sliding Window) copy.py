"""
Time complexity: O(nm)
Space complexity: O(1)
"""


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if len(haystack) < len(needle):
            return -1
        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i : i + len(needle)] == needle:
                return i
        return -1


s = Solution()
haystack = "leetcode"
needle = "de"
result = s.strStr(haystack, needle)
print(result)

"""
Runtime
- 42 ms
- Beats 64.21%

Memory
- 16.2 MB
- Beats 75.20%
"""
