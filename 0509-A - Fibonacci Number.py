"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def fib(self, n: int) -> int:
        if n < 2:
            return n
        pp = 0
        p = 1
        for _ in range(n - 1):
            current = pp + p
            pp = p
            p = current
        return current


s = Solution()
input_ = 2  # Expecting 1
result = s.fib(input_)
print(result)

"""
Runtime
- 43 ms
- Beats 83.13%

Memory
- 16.3 MB
- Beats 63.31%
"""
