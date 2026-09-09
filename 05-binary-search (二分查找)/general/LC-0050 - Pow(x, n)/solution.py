"""LC-0050 - Pow(x, n)

合并自 2 个解法文件:
  1. 01 - 0050 - A - Power(x,n) - Recursive.py
  2. 01 - 0050 - B - Power(x,n) - Iterative.py
"""


# ============================================================================
# Solution 1: Recursive    (原文件: 01 - 0050 - A - Power(x,n) - Recursive.py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(1)

class Solution_1_Recursive:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        if n < 0:
            return 1.0 / self.myPow(x, -n)
        half = self.myPow(x, n // 2)
        if n % 2 == 0:
            return half * half
        else:
            return half * half * x

# ============================================================================
# Solution 2: Iterative    (原文件: 01 - 0050 - B - Power(x,n) - Iterative.py)
# ============================================================================

# Time complexity: O(logn)
# Space complexity: O(1)

class Solution_2_Iterative:
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
