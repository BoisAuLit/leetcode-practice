"""
Time complexity: O(m+n)
Space complexity: O(m+n)
"""

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        length = min(len(word1), len(word2))         
        array = []
        for i in range(length):
            array.append(word1[i])
            array.append(word2[i])
        return ''.join(array) + word1[length:] + word2[length:]


"""
Runtime
- 35ms
- Beats 98.16%

Memory
16.16mb
- Beats 96.18%
"""
