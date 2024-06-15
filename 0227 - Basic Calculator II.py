import math

class Solution:
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


s = Solution()
input_ = "22-3*5"
input_ = "3+2*2"
input_ = "14-3/2"
# input_ = " 3/2 "
# input_ = " 3+5 / 2 "
# input_ = "0"
# input_ = "1 + 1"
# input_ = "2*3+4"
result = s.calculate(input_)
print(result)
