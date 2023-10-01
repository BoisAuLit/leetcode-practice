from typing import List
from collections import defaultdict

"""
Time complexity: O(NK)
Space complexity: O(NK)
"""


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mapping = defaultdict(list)
        for str_ in strs:
            counter = [0] * 26
            for letter in str_:
                counter[ord(letter) - ord("a")] += 1
            mapping[tuple(counter)].append(str_)
        return mapping.values()


s = Solution()
input_ = strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
# input_ = strs = ["bdddddddddd", "bbbbbbbbbbc"]
result = s.groupAnagrams(input_)
print(result)

"""

"""
