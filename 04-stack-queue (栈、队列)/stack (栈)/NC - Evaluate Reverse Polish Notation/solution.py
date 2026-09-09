from typing import List


import math

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operators = set(["+", "-", "*", "/"])
        for token in tokens:
            if token in operators:
                b = int(stack.pop())
                a = int(stack.pop())
                if token == "+":
                    stack.append(a+b)
                elif token == "-":
                    stack.append(a-b)
                elif token == "*":
                    stack.append(a*b)
                else:
                    """
                    这里是最容易出错的地方
                    math.trunc() 只取整数部分，与题目完全相符


                    而在 python 里 a/b 如果是 - 0.5， 那么 a//b == -1
                    因为其是向负无穷取整

                    有两个解决方案
                    stack.append(int(a/b))
                    stack.append(math.trunc(a/b))
                    都可以达到只取整数部分的目的
                    """
                    stack.append(int(a/b))
            else:
                stack.append(token)
        return int(stack[0])
