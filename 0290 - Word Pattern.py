from collections import defaultdict


class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False
        pattern_to_word = {}
        word_to_pattern = {}
        for p, w in zip(pattern, words):
            if p not in pattern_to_word:
                pattern_to_word[p] = w
            elif pattern_to_word[p] != w:
                return False

            if w not in word_to_pattern:
                word_to_pattern[w] = p
            elif word_to_pattern[w] != p:
                return False

        return True


solution = Solution()

# Test case 1: Expecting True
pattern = "abba"
s = "dog cat cat dog"

# Test case 2: Expecting False
pattern = "abba"
s = "dog cat cat fish"

result = solution.wordPattern(pattern, s)
print(result)
