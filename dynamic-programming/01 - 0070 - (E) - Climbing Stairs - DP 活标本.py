"""
Problem description:

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps.
In how many distinct ways can you climb to the top?
"""


class Solution_Top_Down_Memoization:
    def climbStairs(self, n: int) -> int:
        def dp(n:int) -> int:
            if n <= 2:
                return n
            if n not in memo:
                memo[n] = dp(n-1) + dp(n-2)
            return memo[n]

        memo = {}
        return dp(n)


class Solution_Bottom_Up_Iteration:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        dp = [0] * (n+1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]
