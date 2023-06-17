import math

"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3:
            return n
        pivot = math.ceil(n / 2)
        a = self.climbStairs(pivot)
        b = self.climbStairs(n - pivot)
        c = self.climbStairs(pivot - 1)
        d = self.climbStairs(n - pivot - 1)
        return a * b + c * d


s = Solution()
input_ = 5
result = s.climbStairs(input_)
print(result)

"""
Runtime
- 44 ms
- Beats 55.74%

Memory
- 16.4 MB
- Beats 19.35%
"""
