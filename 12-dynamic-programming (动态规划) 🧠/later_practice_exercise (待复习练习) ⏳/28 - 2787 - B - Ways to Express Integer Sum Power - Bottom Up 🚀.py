from pprint import pprint
import math


class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        mod = 10**9 + 7
        dp = [[0] * (n + 1) for _ in range(n + 1)]

        # Here use math.ceil because 64**(1/3) = 3.9xx6 (not 4)
        root = math.ceil(n ** (1/x))
        val = root**x
        if 1 <= val <= n:
            dp[root][val] = 1

        for i in range(root - 1, 0, -1):
            pow = i**x
            for remain in range(1, n + 1):
                if pow < remain:
                    dp[i][remain] = (
                        dp[i + 1][remain - pow] + dp[i + 1][remain]
                    ) % mod
                elif pow == remain:
                    dp[i][remain] = 1
        return dp[1][-1]


s = Solution()
n = 4
x = 1
result = s.numberOfWays(n, x)
print(result)
