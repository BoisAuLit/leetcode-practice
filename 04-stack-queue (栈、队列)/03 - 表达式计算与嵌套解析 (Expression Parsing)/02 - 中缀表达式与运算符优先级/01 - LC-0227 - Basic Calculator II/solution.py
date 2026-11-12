# https://leetcode.com/problems/basic-calculator-ii/

class Solution:
    def calculate(self, s: str) -> int:
        stack = []          # 存整数;加减转成正负数入栈,乘除直接和栈顶结算
        num = 0             # 正在读的数字
        op = "+"            # 上一个运算符,初始当作 "+"
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)        # 多位数逐位拼
            if ch in "+-*/" or i == len(s) - 1: # 遇到运算符或走到末尾 → 结算上一个运算符
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))  # int() 向零截断,别用 //
                op, num = ch, 0
        return sum(stack)   # 剩下的全是加法,顺序无关


s = Solution()
input_ = "22-3*5"
# input_ = "3+2*2"
# input_ = "14-3/2"
result = s.calculate(input_)
print(result)



