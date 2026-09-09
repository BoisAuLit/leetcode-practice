"""NC - Word Break

合并自 2 个解法文件:
  1. 10 - Word Break - DP.py
  2. 10 - Word Break - Trie.py
"""

from typing import List

from functools import lru_cache


# ============================================================================
# Solution 1: DP    (原文件: 10 - Word Break - DP.py)
# ============================================================================

class Solution_1_DP:
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

# ============================================================================
# Solution 2: Trie    (原文件: 10 - Word Break - Trie.py)
# ============================================================================

str_ = "neetcode"

wordDict = ["neet", "code"]

class Solution_2_Trie:
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


if __name__ == "__main__":

    # --- Solution 2: Trie ---
    s = Solution_2_Trie()
    result = s.wordBreak(str_, wordDict)
    print(result)
