from typing import List
from functools import lru_cache



class Solution_Top_Down_Memoization:
    """
    每次都去掉开头的一小节(一个单词), 然后看剩下的是否成立

    对于当前的 string, 尝试所有的单词 (故用 any)
    """
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        @lru_cache(maxsize=None)
        def dp(s: str) -> bool:
            if len(s) == 0:
                return True

            return any(
                s.startswith(word) and dp(s[len(word) :]) for word in wordDict
            )

        return dp(s)


class Solution_Bottom_Up_Iteration:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        """
        采取的策略为从后往前, 逐渐从最后去除一个一个单词
        """
        dp = [False] * len(s)
        for i in range(len(wordDict)):
            if s.endswith(wordDict[i]):
                dp[-len(wordDict[i])] = True

        for i in range(len(s) - 1, -1, -1):
            if dp[i]:
                continue
            for j in range(len(wordDict)):
                word = wordDict[j]
                if (
                    len(word) <= len(s) - i
                    and s[i:].startswith(word)
                    and dp[i + len(word)]
                ):
                    dp[i] = True
                    break

        return dp[0]


# solution = Solution()
# s = "leetcode"
# wordDict = ["leet", "code"]
# result = solution.wordBreak(s, wordDict)
# print(result)

# solution = Solution()
# s = "applepenapple"
# wordDict = ["apple", "pen"]
# result = solution.wordBreak(s, wordDict)
# print(result)

# solution = Solution()
# s = "catsandog"
# wordDict = ["cats", "dog", "sand", "and", "cat"]
# result = solution.wordBreak(s, wordDict)
# print(result)
