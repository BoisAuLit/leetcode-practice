"""LC-0772 - Basic Calculator III

Level 1 · 03 表达式计算与嵌套解析 → Level 2 · 02 中缀表达式与运算符优先级

题目在问：计算含 `+ - * /`、**括号**、非负整数的表达式；除法向零截断。
它是 LC-0227（`+-*/` 无括号）和 LC-0224（`+-` 有括号）的合体 —— Meta 的 calculator 系列最终形态。

### 一套骨架同时处理优先级和括号：「当前符号 + 当前数 + 栈」+ 递归

0227 的核心：遍历时记住**上一个运算符** `op` 和**当前数** `num`；碰到下一个运算符（或结尾）时，
按 `op` 把 `num` 结算进栈：

    '+' → push(num)      '-' → push(-num)
    '*' → push(pop() * num)      '/' → push(int(pop() / num))     # ! 乘除立刻和栈顶结算 = 优先级更高
    最后 sum(stack)

括号怎么办？**把括号里的内容当成一个数**：碰到 `(` 就递归求出子表达式的值，当作 `num` 继续走上面的流程。
递归版最清晰；迭代版把「外层的 stack 和 op」压进另一个栈保存，碰到 `)` 时恢复 —— 两者等价。

### 三个必须说出来的细节

1. **除法向零截断**：Python `//` 是向下取整，`-7 // 2 == -4`，题目要 −3 ⟹ 用 `int(a / b)`（或手写符号处理）。
2. 数字可能多位：`num = num * 10 + int(ch)`，直到遇到非数字。
3. 结尾要**再结算一次**（把最后的 `num` 用最后的 `op` 推进栈）：把「到达字符串末尾」和「遇到运算符」统一成同一个触发条件最不容易漏。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 递归下降 —— 括号内容递归求值，当作一个数；+-*/ 用 0227 的「上一个运算符」栈法
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（栈 + 递归深度 = 括号层数）
##### ! 适用：面试标准答案。一个 helper 用下标 i 顺序扫；碰到 '(' 递归，碰到 ')' 或结尾返回 (值, 新下标)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def calculate(self, s: str) -> int:
        def settle(stack, op, num):
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))   # ! 向零截断（不能用 //）

        def parse(i: int):
            """从 s[i] 开始求值，直到遇到 ')' 或结尾；返回 (值, 停在 ')' 之后的下标)。"""
            stack: List[int] = []
            num, op = 0, "+"
            while True:
                ch = s[i] if i < len(s) else None      # ! None = 结尾，当成一个「结算触发器」
                if ch is not None and ch.isdigit():
                    num = num * 10 + int(ch); i += 1
                    continue
                if ch == "(":
                    num, i = parse(i + 1)              # ! 括号 = 一个数；i 已指向 ')' 后面
                    continue
                settle(stack, op, num)                 # ! 运算符 / ')' / 结尾 → 用上一个 op 结算 num
                if ch == ")":
                    return sum(stack), i + 1
                if ch is None:
                    return sum(stack), i
                op, num = ch, 0
                i += 1

        return parse(0)[0]


##################################################################################################
##### ! Solution 2: 迭代 —— 用「上下文栈」保存外层的 (stack, op)，碰到 ')' 恢复
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：不想递归时；逻辑和 Solution_1 一一对应：'(' 时把当前 stack 和 op 存起来、新开一层；
#####         ')' 时把这一层 sum 出来当作 num 回到外层继续结算
##################################################################################################


class Solution_2:
    def calculate(self, s: str) -> int:
        def apply(stack, op, num):
            if op == "+": stack.append(num)
            elif op == "-": stack.append(-num)
            elif op == "*": stack.append(stack.pop() * num)
            else: stack.append(int(stack.pop() / num))

        ctx = []                                       # ! 外层上下文：(stack, op)
        stack, num, op = [], 0, "+"
        for i, ch in enumerate(s + "+"):               # ! 末尾补一个 '+' 触发最后一次结算
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == "(":
                ctx.append((stack, op))                # ! 保存外层
                stack, num, op = [], 0, "+"            # ! 新开一层
            elif ch in "+-*/)":
                apply(stack, op, num)
                if ch == ")":
                    num = sum(stack)                   # ! 这一层算完，变成外层的一个数
                    stack, op = ctx.pop()
                else:
                    op, num = ch, 0
        return sum(stack)


##################################################################################################
##### ! Solution 3: 经典两栈（数字栈 + 运算符栈，Dijkstra 双栈 / Shunting-yard 思路）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：教科书通解 —— 支持任意多级优先级、任意多种二元运算符；
#####         规则：遇到运算符时，先把运算符栈顶所有「优先级 ≥ 当前」的算掉；'(' 直接入栈，')' 算到 '(' 为止
##################################################################################################


class Solution_3:
    PREC = {"+": 1, "-": 1, "*": 2, "/": 2}

    def calculate(self, s: str) -> int:
        nums: List[int] = []
        ops: List[str] = []

        def compute():
            b, a, op = nums.pop(), nums.pop(), ops.pop()
            nums.append(a + b if op == "+" else a - b if op == "-" else a * b if op == "*" else int(a / b))

        i, n = 0, len(s)
        while i < n:
            ch = s[i]
            if ch.isdigit():
                j = i
                while j < n and s[j].isdigit():
                    j += 1
                nums.append(int(s[i:j])); i = j
                continue
            if ch == "(":
                ops.append(ch)
            elif ch == ")":
                while ops[-1] != "(":
                    compute()
                ops.pop()                              # ! 弹掉 '('
            elif ch in self.PREC:
                while ops and ops[-1] != "(" and self.PREC[ops[-1]] >= self.PREC[ch]:   # ! 左结合：≥
                    compute()
                ops.append(ch)
            i += 1
        while ops:
            compute()
        return nums[0]


def _truth(s: str) -> int:
    """用 Python 自己求值，但把 '/' 换成向零截断的函数（真值基线）。"""
    import re
    expr = re.sub(r"(\d+)", r"_N(\1)", s)
    class _N(int):
        def __truediv__(self, o): return _N(int(int(self) / int(o)))
        def __add__(self, o): return _N(int(self) + int(o))
        def __sub__(self, o): return _N(int(self) - int(o))
        def __mul__(self, o): return _N(int(self) * int(o))
    return int(eval(expr, {"_N": _N}))


def _random_expr(rng, depth=0) -> str:
    """随机生成合法表达式（非负整数、+-*/、括号），避免除零。"""
    if depth > 2 or rng.random() < 0.4:
        return str(rng.randint(0, 20))
    r = rng.random()
    if r < 0.25:
        return "(" + _random_expr(rng, depth + 1) + ")"
    op = rng.choice("+-*/")
    left = _random_expr(rng, depth + 1)
    right = _random_expr(rng, depth + 1)
    if op == "/":
        right = str(rng.randint(1, 9))                 # ! 除数非零
    return left + op + right


if __name__ == "__main__":
    import random
    cases = [("1+1", 2), ("6-4/2", 4), ("2*(5+5*2)/3+(6/2+8)", 21), ("(2+6*3+5-(3*14/7+2)*5)+3", -12),
             ("0", 0), ("(1)", 1), ("7-(2*3)", 1), ("14/(3-5)", -7), ("100", 100)]     # ! 14/(-2) 向零截断 = -7
    for s, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().calculate(s)
            assert got == want, (cls.__name__, s, got, want)
    rng = random.Random(772)
    for _ in range(3000):
        s = _random_expr(rng)
        try:
            want = _truth(s)
        except ZeroDivisionError:
            continue                                   # ! 子表达式算出 0 当除数时跳过
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().calculate(s)
            assert got == want, (cls.__name__, s, got, want)
    print("所有测试通过 ✓（样例 + 3000 条随机表达式对拍）")
