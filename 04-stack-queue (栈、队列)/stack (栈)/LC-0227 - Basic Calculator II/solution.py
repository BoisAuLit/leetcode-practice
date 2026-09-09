"""LC-0227 - Basic Calculator II

合并自 2 个解法文件:
  1. 0227 - Basic Calculator II.py
  2. LC-0227 - Basic Calculator II.py
"""

import math


# ============================================================================
# Solution 1: V1    (原文件: 0227 - Basic Calculator II.py)
# ============================================================================

input__1 = "22-3*5"

input__1 = "3+2*2"

input__1 = "14-3/2"

class Solution_1_V1:
    def calculate(self, s: str) -> int:
        num, PreSign, stack=0, '+', []
        for c in s+'+':
            if c.isdigit():
                num = num * 10 + int(c)
            elif c in "+-*/":
                if PreSign=='+':
                    stack.append(num)
                elif PreSign == '-':
                    stack.append(-num)
                elif PreSign == '*':
                    stack.append(stack.pop()*num)
                elif PreSign == '/':
                    stack.append(math.trunc(stack.pop()/num))
                PreSign=c
                num=0             
        return sum(stack)

# ============================================================================
# Solution 2: V2    (原文件: LC-0227 - Basic Calculator II.py)
# ============================================================================

class Solution_2_V2:
    def calculate(self, s: str) -> int:
        pass


if __name__ == "__main__":

    # --- Solution 1: V1 ---
    s = Solution_1_V1()
    result = s.calculate(input__1)
    print(result)
