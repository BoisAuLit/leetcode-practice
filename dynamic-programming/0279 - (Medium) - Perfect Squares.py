import math


class Solution:
    def numSquares(self, n: int) -> int:
        dp = [n] * (n + 1)
        dp[0] = 0
        squares = [i**2 for i in range(0, int(math.sqrt(n)) + 1)]

        for i in range(1, n + 1):
            for square in squares:
                if i - square < 0:
                    break
                if 1 + dp[i - square] < dp[i]:
                    dp[i] = 1 + dp[i - square]

        return dp[n]


s = Solution()

# Test case 1: Expecting 3 (12 = 4 + 4 + 4)
# n = 12

# Test case 2: Expecting 2 (13 = 4 + 9)
n = 13

result = s.numSquares(n)
print(result)
