from functools import lru_cache


class Solution_Top_Down_Time_Limit_XXXX:
    mod = 10**9 + 7

    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        @lru_cache(None)
        def dp(n: int, remain: int) -> int:
            if n == 1:
                return 1 if k >= remain else 0
            if remain < 0:
                return 0
            return sum(
                self.numRollsToTarget(n - 1, k, remain - x) % self.mod
                for x in range(1, k + 1)
            )

        return dp(n, target)


"""
function(n, target) means if we can roll dice n times, how many ways to compose target
function(n, target) = sum of:
- function(n-1, target-1)
- function(n-2, target-2)
- ...
- function(n-k, target-k)
"""


class Solution_Very_Efficient:
    mod = 10**9 + 7

    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        dp = [[0] * (n + 1) for _ in range(target + 1)]
        dp[0][0] = 1
        for i in range(1, target + 1):
            for j in range(1, n + 1):
                dp[i][j] = (
                    sum(dp[i - x][j - 1] for x in range(1, k + 1) if i - x >= 0)
                    % self.mod
                )
        return dp[-1][-1]


# s = Solution()
# # n = 1
# # k = 6
# # target = 3
# # n = 2
# # k = 6
# # target = 7
# n = 30
# k = 30
# target = 500
# result = s.numRollsToTarget(n, k, target)
# print(result)
