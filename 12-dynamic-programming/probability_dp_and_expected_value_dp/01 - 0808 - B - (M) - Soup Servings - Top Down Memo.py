from math import ceil
from functools import cache


class Solution:
    def soupServings(self, n: int) -> float:
        m = ceil(n / 25)

        @cache
        def dp(i: int, j: int) -> float:
            if i <= 0 and j <= 0:
                return 0.5
            if i <= 0:
                return 1.0
            if j <= 0:
                return 0.0

            return (
                dp(i - 4, j)
                + dp(i - 3, j - 1)
                + dp(i - 2, j - 2)
                + dp(i - 1, j - 3)
            ) / 4.0

        # This is very imporant to avoid stack overflow!
        for k in range(1, m + 1):
            if dp(k, k) > 1 - 1e-5:
                return 1.0
        return dp(m, m)


# Test case 1: Expecting 0.71875
s = Solution()
n = 100
result = s.soupServings(n)
print(result)
