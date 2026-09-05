from typing import List
from functools import lru_cache


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)

        @lru_cache
        def dfs(i: int) -> bool:
            if i == len(s):
                return True

            for j in range(i + 1, len(s) + 1):
                if s[i:j] in words and dfs(j):
                    return True

            return False

        return dfs(0)
