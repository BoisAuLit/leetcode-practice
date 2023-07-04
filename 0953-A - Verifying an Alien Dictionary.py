from typing import List, Dict
from itertools import zip_longest

"""
Time complexity: O(n²)
Space complexity: O(n)
"""


class Solution:
    def isSorted(self, word1: str, word2: str, mapping: Dict[str, int]) -> bool:
        for x, y in zip_longest(word1, word2, fillvalue="#"):
            if mapping[x] < mapping[y]:
                return True
            if mapping[x] > mapping[y]:
                return False
        return True

    def isAlienSorted(self, words: List[str], order: str) -> bool:
        order = "#" + order
        mapping = {character: index for index, character in enumerate(order)}
        for i in range(len(words) - 1):
            if not self.isSorted(words[i], words[i + 1], mapping):
                return False
        return True


s = Solution()

# Test case 1 --> Expecting True
# words = ["hello", "leetcode"]
# order = "hlabcdefgijkmnopqrstuvwxyz"

# Test case 2 --> Expecting False
# words = ["word", "world", "row"]
# order = "worldabcefghijkmnpqstuvxyz"

# Test case 3 --> Expecting False
words = ["apple", "app"]
order = "abcdefghijklmnopqrstuvwxyz"


result = s.isAlienSorted(words, order)
print(result)

"""
Runtime
- 57 ms
- Beats 36.68%

Memory
- 16.2 MB
- Beats 95.64%
"""
