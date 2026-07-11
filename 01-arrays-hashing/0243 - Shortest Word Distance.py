from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def shortestDistance(self, words: List[str], word1: str, word2: str) -> int:
        shortestDistance = len(words)
        position1, position2 = -1, -1
        for i in range(len(words)):
            if words[i] == word1:
                position1 = i
            elif words[i] == word2:
                position2 = i

            if position1 != -1 and position2 != -1:
                shortestDistance = min(
                    shortestDistance, abs(position1 - position2)
                )
        return shortestDistance


s = Solution()

# Expecting 3
wordsDict = ["practice", "makes", "perfect", "coding", "makes"]
word1 = "coding"
word2 = "practice"

result = s.shortestDistance(wordsDict, word1, word2)
print(result)

"""

"""
