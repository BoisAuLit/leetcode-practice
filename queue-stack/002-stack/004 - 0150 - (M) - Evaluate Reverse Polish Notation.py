from typing import List
from collections import deque


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        operators = set("+-*/")
        stack = deque()
        for token in tokens:
            if token not in operators:
                stack.append(token)
                continue
            a = int(stack.pop())
            b = int(stack.pop())
            if token == "+":
                stack.append(b + a)
            elif token == "-":
                stack.append(b - a)
            elif token == "*":
                stack.append(b * a)
            else:
                if a * b < 0:
                    stack.append(-(abs(b) // abs(a)))
                else:
                    stack.append(b // a)
        return int(stack[0])


s = Solution()

# Test case 1: Expecting 9
# input_ = ["2", "1", "+", "3", "*"]

# Test case 2: Expecting 6
# input_ = ["4", "13", "5", "/", "+"]

# Test case 3: Expecting 22
input_ = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]

result = s.evalRPN(input_)
print(result)
