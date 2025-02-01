from typing import List
from functools import lru_cache


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        @lru_cache(maxsize=None)
        def dfs(current: str):
            if current == s:
                return True
            if len(current) > len(s) or not s.startswith(current):
                return False

            for word in wordDict:
                if dfs(current + word):
                    return True
            return False

        return dfs("")


solution = Solution()
s = "applepenapple"
wordDict = ["apple", "pen"]
result = solution.wordBreak(s, wordDict)
print(result)
