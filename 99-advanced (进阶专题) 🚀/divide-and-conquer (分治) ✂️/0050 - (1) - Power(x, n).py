"""
Time complexity: O(logn)
Space complexity: O(logn)
"""


class Solution:

    cache = {}

    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        elif n == 1:
            return x
        elif n == -1:
            return 1 / x

        if (x, n) in Solution.cache:
            return self.cache[(x, n)]
        result = self.myPow(x, n // 2) * self.myPow(x, n // 2) * self.myPow(x, n % 2)
        self.cache[(x, n)] = result
        return result


s = Solution()
x, n = 2.0, 10  # 1024.0
# x, n = 2.0, -2
# x, n = 2.0, 0
result = s.myPow(x, n)
print(result)
