class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        maxLength = 0
        charSet = set()
        left = 0
        
        for right in range(n):
            if s[right] not in charSet:
                charSet.add(s[right])
                maxLength = max(maxLength, right - left + 1)
            else:
                while s[right] in charSet:
                    charSet.remove(s[left])
                    left += 1
                charSet.add(s[right])
        
        return maxLength


s = Solution()

input_ = "abcabcbb"  # Expecting 3
input_ = "abba"  # Expecting 2

result = s.lengthOfLongestSubstring(input_)

print(result)

"""

"""
