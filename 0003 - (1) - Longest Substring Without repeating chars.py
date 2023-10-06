class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        i = 0
        result = 0
        for j in range(len(s)):
            if s[j] in seen:
                i = max(i, seen[s[j]] + 1)
            seen[s[j]] = j
            result = max(result, j - i + 1)
        return result


s = Solution()

input_ = "abcabcbb"  # Expecting 3
input_ = "abba"  # Expecting 2

result = s.lengthOfLongestSubstring(input_)

print(result)

"""

"""
