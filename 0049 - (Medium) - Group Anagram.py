from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ans = defaultdict(list)
        for word in strs:
            count = [0] * 26
            for letter in word:
                count[ord(letter) - ord("a")] += 1
            ans[tuple(count)].append(word)
        return list(ans.values())


s = Solution()

# Test case 1: Expecting [["bat"],["nat","tan"],["ate","eat","tea"]]
input_ = ["eat", "tea", "tan", "ate", "nat", "bat"]

# Test case 2: Expecting [[""]]
input_ = [""]


# Test case 3: Expecting [["bbbbbbbbbbc"],["bdddddddddd"]]
input_ = ["bdddddddddd", "bbbbbbbbbbc"]
result = s.groupAnagrams(input_)
print(result)
