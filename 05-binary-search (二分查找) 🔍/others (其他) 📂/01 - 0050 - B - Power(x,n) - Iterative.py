"""
Time complexity: O(logn)
Space complexity: O(1)
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1

        # Handle negative exponent
        if n < 0:
            n = -n
            x = 1 / x

        result = 1
        # Binary exponentiation loop
        while n > 0:
            if n % 2 == 1:
                result *= x
            x *= x
            n //= 2
        return result
