from functools import cache


class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        mod = 10**9 + 7

        @cache
        def dp(i: int, remain: int) -> int:
            val = i**x
            if val == remain:
                return 1
            elif val > remain:
                return 0
            return (
                dp(i + 1, remain - val) % mod + dp(i + 1, remain) % mod
            ) % mod

        return dp(1, n)


s = Solution()
n = 4
x = 1
result = s.numberOfWays(n, x)
print(result)
