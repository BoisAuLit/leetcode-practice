"""
Time complexity
- Worst case: O(nm)
- Best case: O(n-m+2m)=O(n+m)
- n-m for rolling hash
- 2m
    - 1m for calculating the hash of the frst m-string in the haystack
    - 1m for calculating the hash of the needle
Space complexity: O(1)
"""


class Solution:
    radix = 26
    mod = 1_000_000_033

    def hash_letter(self, letter: str) -> int:
        return ord(letter) - 97

    def hash_string(self, string: str, m: int) -> int:
        weight = 1
        hash_value = 0
        for index in reversed(range(0, m)):
            hash_value += self.hash_letter(string[index]) * weight % self.mod
            weight *= self.radix
        return hash_value % self.mod

    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)
        if n < m:
            return -1
        hash_needle = self.hash_string(needle, m)
        max_weight = 1
        for _ in range(m):
            max_weight = max_weight * self.radix % self.mod
        for i in range(0, n - m + 1):
            if i == 0:
                hash_prev = self.hash_string(haystack, m)
            else:
                hash_prev = (
                    hash_prev * self.radix % self.mod
                    - self.hash_letter(haystack[i - 1]) * max_weight % self.mod
                    + self.hash_letter(haystack[i + m - 1]) % self.mod
                ) % self.mod
            if hash_prev == hash_needle:
                for j in range(m):
                    if haystack[i + j] != needle[j]:
                        break
                if j == m - 1:
                    return i
        return -1


s = Solution()
haystack = "ababaabbbbababbaabaaabaabbaaaabbabaabbbbbbabbaabbabbbabbbbbaaabaababbbaabbbabbbaabbbbaaabbababbabbbabaaabbaabbabababbbaaaaaaababbabaababaabbbbaaabbbabb"
needle = "abbabbbabaa"  # Expected result --> 92 (✅ passed)
result = s.strStr(haystack, needle)
print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "baabbaaaaaaabbaaaaabbabbababaabbabbbbbabbabbbbbbabababaabbbbbaaabbbbabaababababbbaabbbbaaabbaababbbaabaabbabbaaaabababaaabbabbababbabbaaabbbbabbbbabbabbaabbbaa"
# needle = "bbaaaababa"  # Expected result --> 107 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "ccaccaacdba"
# needle = "dba"  # Expected result --> 8 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)

########################################################################
########################################################################

# s = Solution()
# haystack = "abcabcabc"
# needle = "cab" # Expected result --> 2 (✅ passed)
# result = s.strStr(haystack, needle)
# print(result)
"""
Runtime
- 49 ms
- Beats 31.42%

Memory
- 16.3 MB
- Beats 19.47%
"""
