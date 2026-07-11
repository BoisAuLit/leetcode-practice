from pprint import pprint
import math


class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        mod = 10**9 + 7

        dp = [0] * (n + 1)
        root = math.ceil(n ** (1 / x))
        val = root**x
        if 1 <= val <= n:
            dp[val] = 1

        for i in range(root - 1, 0, -1):
            new_dp = [0] * (n + 1)
            pow = i**x
            for remain in range(1, n + 1):
                if pow < remain:
                    new_dp[remain] = (dp[remain - pow] + dp[remain]) % mod
                elif pow == remain:
                    new_dp[remain] = 1
            dp = new_dp
        return dp[-1]

s = Solution()
n = 4
x = 1
result = s.numberOfWays(n, x)
print(result)
