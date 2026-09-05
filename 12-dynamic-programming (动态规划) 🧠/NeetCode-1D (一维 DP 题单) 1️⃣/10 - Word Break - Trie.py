from typing import List
from functools import lru_cache


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        trie = {}

        for word in wordDict:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            node["#"] = True

        @lru_cache
        def dfs(i: int) -> bool:
            if i == len(s):
                return True
            node = trie
            for j in range(i, len(s)):
                # No dictionary word has this prefix
                if s[j] not in node:
                    break

                node = node[s[j]]
                if "#" in node and dfs(j + 1):
                    return True

            return False

        return dfs(0)


s = Solution()
str_ = "neetcode"
wordDict = ["neet", "code"]
result = s.wordBreak(str_, wordDict)
print(result)
