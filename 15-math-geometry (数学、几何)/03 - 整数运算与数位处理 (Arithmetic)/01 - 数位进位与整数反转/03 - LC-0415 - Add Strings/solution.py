"""LC-0415 - Add Strings

Level 1 · 03 整数运算与数位处理 → Level 2 · 01 数位进位与整数反转

题目在问：两个用字符串表示的非负大整数相加，**不能用大整数库或直接转 int**。
Meta 电面热身题；LC-0002（链表加法）、LC-0067（二进制加法）、LC-0043（字符串乘法）全是同一套「竖式 + 进位」。

### 竖式模板（背下来，三道题共用）

    i, j = len(a)-1, len(b)-1; carry = 0
    while i >= 0 or j >= 0 or carry:                 # ! 三个条件缺一不可：任一方还有位 or 还有进位
        d = carry + (int(a[i]) if i >= 0 else 0) + (int(b[j]) if j >= 0 else 0)
        carry, digit = divmod(d, 10)
        out.append(digit); i -= 1; j -= 1
    return reversed(out)

### 三个常见错误

1. 循环条件漏了 `or carry`：`"9" + "1"` 会输出 `"0"` 而不是 `"10"`。
2. 结果是**倒着**攒的，最后要 reverse；用列表收集再 `"".join(reversed(...))`，不要在循环里做字符串前插（O(n²)）。
3. `ord(c) - ord('0')` 和 `int(c)` 等价；面试用 Java/C++ 时只能用前者，Python 两者都行。
"""


##################################################################################################
##### ! Solution 1: 双指针从低位到高位的竖式加法
##### ! 时间复杂度: O(max(n, m))   空间复杂度: O(max(n, m))（输出）
##### ! 适用：面试标准答案；循环条件 i >= 0 or j >= 0 or carry 是全部考点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def addStrings(self, num1: str, num2: str) -> str:
        i, j, carry = len(num1) - 1, len(num2) - 1, 0
        out = []
        while i >= 0 or j >= 0 or carry:               # ! 任一方有位 或 还有进位
            d = carry
            if i >= 0:
                d += ord(num1[i]) - 48; i -= 1
            if j >= 0:
                d += ord(num2[j]) - 48; j -= 1
            carry, digit = divmod(d, 10)
            out.append(chr(48 + digit))
        return "".join(reversed(out))


##################################################################################################
##### ! Solution 2: 先把短的补零对齐，再逐位相加
##### ! 时间复杂度: O(max(n, m))   空间复杂度: O(max(n, m))
##### ! 适用：想去掉 i/j 的边界判断时：zfill 把两个数补到同长，循环体里不再有 if；最后单独处理末尾进位
##################################################################################################


class Solution_2:
    def addStrings(self, num1: str, num2: str) -> str:
        n = max(len(num1), len(num2))
        a, b = num1.zfill(n), num2.zfill(n)            # ! 左侧补零
        out, carry = [], 0
        for x, y in zip(reversed(a), reversed(b)):
            carry, digit = divmod(int(x) + int(y) + carry, 10)
            out.append(str(digit))
        if carry:
            out.append("1")                            # ! 最高位进位（和最多是 1）
        return "".join(reversed(out))


##################################################################################################
##### ! Solution 3: 递归（尾部一位 + 递归处理前缀），纯演示
##### ! 时间复杂度: O(max(n, m))   空间复杂度: O(max(n, m)) 递归栈
##### ! 适用：说明「竖式」就是一个尾递归结构；生产代码不用（Python 递归深度上限 1000，字符串可到 10^4）
##################################################################################################


class Solution_3:
    def addStrings(self, num1: str, num2: str) -> str:
        def rec(a: str, b: str, carry: int) -> str:
            if not a and not b:
                return "1" if carry else ""
            x = int(a[-1]) if a else 0
            y = int(b[-1]) if b else 0
            c, d = divmod(x + y + carry, 10)
            return rec(a[:-1], b[:-1], c) + str(d)
        return rec(num1, num2, 0) or "0"


if __name__ == "__main__":
    import random
    for a, b, want in [("11", "123", "134"), ("456", "77", "533"), ("0", "0", "0"), ("9", "1", "10"), ("1", "999", "1000")]:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().addStrings(a, b)
            assert got == want, (cls.__name__, a, b, got, want)
    rng = random.Random(415)
    for _ in range(20000):
        x, y = rng.randint(0, 10 ** rng.randint(0, 40)), rng.randint(0, 10 ** rng.randint(0, 40))
        want = str(x + y)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().addStrings(str(x), str(y)) == want, (cls.__name__, x, y)
    print("所有测试通过 ✓（样例 + 20000 随机对拍）")
