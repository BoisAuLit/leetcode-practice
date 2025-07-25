class Solution:
    def tribonacci(self, n: int) -> int:
        if n == 0:
            return 0
        if n <= 2:
            return 1
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 1
        for i in range(3, n + 1, 1):
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
        return dp[n]


s = Solution()
n = 25
result = s.tribonacci(n)
print(result)
