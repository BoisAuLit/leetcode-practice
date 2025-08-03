from functools import lru_cache


"""
Important thing:
It's like fibonacci:
F(i) depends on F(i+1) & F(i+2)
"""


class Solution_Top_Down_Memoization:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        @lru_cache(None)
        def dp(i: int) -> int:
            if i == n - 1:
                return int(s[i] != "0")
            if i >= n:
                return 1
            # Case 1: Current digit alone
            x = dp(i + 1) if s[i] != "0" else 0
            # Case 2: Current digit combined with following
            y = dp(i + 2) if 10 <= int(s[i] + s[i + 1]) <= 26 else 0
            return x + y

        return dp(0)


class Solution_Bottom_Up_Iteration_Efficient:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        dp = [[0] * 2 for _ in range(n)]
        # dp[i][0]: not combine with next
        # dp[i][1]: combine with next
        dp[-1] = [int(s[-1] != "0"), 0]
        for i in range(n - 2, -1, -1):
            dp[i][0] = sum(dp[i + 1]) if s[i] != "0" else 0

            combination_valid = int(10 <= int(s[i] + s[i + 1]) <= 26)
            if i == n - 2:
                dp[i][1] = combination_valid
            else:
                dp[i][1] = sum(dp[i + 2]) if combination_valid else 0

        return sum(dp[0])


class Solution_Space_Optimized_Most_Efficient:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        # x: not combine with next
        # y: combine with next
        x = [int(s[-1] != "0"), 0]
        y = [0, 0]
        for i in range(n - 2, -1, -1):
            curr = [0, 0]

            # Case 1: Current digit alone (curr[0])
            curr[0] = sum(x) if s[i] != "0" else 0

            # Case 2: Current digit combine with next (curr[1])
            combination_valid = int(10 <= int(s[i] + s[i + 1]) <= 26)
            if i == n - 2:
                curr[1] = combination_valid
            else:
                curr[1] = sum(y) if combination_valid else 0
            x, y = curr, x

        return sum(x)


# solution = Solution()
# s = "2101"
# result = solution.numDecodings(s)
# print(result)
