"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def checkAlmostEquivalent(self, word1: str, word2: str) -> bool:
        mapping = {}
        for character in word1:
            if character in mapping:
                mapping[character] += 1
            else:
                mapping[character] = 1
        for character in word2:
            if character in mapping:
                mapping[character] -= 1
            else:
                mapping[character] = -1
        return all(abs(i) <= 3 for i in mapping.values())


s = Solution()

# Expecting False
# word1 = "aaaa"
# word2 = "bccb"

# Expecting True
# word1 = "abcdeef"
# word2 = "abaaacc"

# Expecting True
word1 = "cccddabba"
word2 = "babababab"

result = s.checkAlmostEquivalent(word1, word2)
print(result)

"""
Runtime
- 49 ms
- Beats 55.93%

Memory
- 16.4 MB
- Beats 36.81%
"""
