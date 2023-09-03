from typing import List
from math import sqrt

# 👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍
class Solution_Fibonacci_Formula:
    """
    Time complexity: O(log(N))
    Space complexity: O(1)
    """

    def climbStairs(self, n: int) -> int:
        sqrt5 = sqrt(5)
        phi = (1 + sqrt5) / 2
        psi = (1 - sqrt5) / 2
        return int((phi ** (n + 1) - (psi ** (n + 1))) / sqrt5)


class Solution_Fibonacci_1:
    """
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        first = 1
        second = 2
        for i in range(3, n + 1):
            third = first + second
            first = second
            second = third
        return second


class Solution_Fibonacci_2:
    """
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]


class Solution_Recursive_With_Memoization:
    """
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def climbStairs(self, n: int) -> int:
        memo = [0] * n
        return self.climStairsRecursive(0, n, memo)

    def climStairsRecursive(self, i: int, n: int, memo: List[int]) -> int:
        if i > n:
            return 0
        if i == n:
            return 1
        if memo[i] > 0:
            return memo[i]
        memo[i] = self.climStairsRecursive(
            i + 1, n, memo
        ) + self.climStairsRecursive(i + 2, n, memo)
        return memo[i]
