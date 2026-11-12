"""LC-0007 - Reverse Integer

Level 1 · 03 整数运算与数位处理 —— **Digit Extraction + 32-bit 范围人工判断**
题目在问：把有符号整数 `x` 的十进制数位反转。
         若结果**超出 32-bit signed 范围 `[-2^31, 2^31-1]`** 则返回 **0**。
         且不允许使用 64-bit 整数（原题的 C++/Java 约束）。

### 三步整数运算（不转字符串）

```python
digit = x % 10        # ! Digit Extraction：取最低位
x //= 10              # ! Integer Truncation：砍掉最低位
res = res * 10 + digit   # ! Result Accumulation：倒着拼回去
```

---

## ⚠️ 坑 1：Python 的 `//` 和 `%` 对负数是**向下取整**，不是向零截断

这是本题在 Python 里**唯一**的语言陷阱：

| 表达式 | Python | C / C++ / Java |
|---|---|---|
| `-123 // 10` | **`-13`**（向下取整，往 -∞ 走） | `-12`（向零截断） |
| `-123 % 10` | **`7`**（结果符号跟除数） | `-3`（结果符号跟被除数） |

所以**不能把正数的拆位逻辑直接套到负数上** ——
`-123 % 10` 给的是 `7` 而不是 `3`，拆出来的数位是错的。

**解法**：先存符号，只对**绝对值**做数位处理，最后把符号乘回去。

```python
sign = -1 if x < 0 else 1
x = abs(x)                 # ! 之后的 % 和 // 都作用在非负数上，语义和 C 一致
```

（另一条路：用 `int(x / 10)` 做向零截断 —— 但 `x / 10` 是浮点，
大整数会丢精度，**不要用**。还有 `math.trunc(x / 10)`，同样有浮点问题。）

---

## ⚠️ 坑 2：Python 整数不会溢出，但**题目的输出限制依然要人工判断**

**为什么 Python 不会自动出现 32-bit Overflow？**
Python 的 `int` 是**任意精度（arbitrary precision）**的 ——
底层是一串 30-bit 的「数字」组成的变长数组，需要多少位就分配多少位。
所以 `1534236469` 反转成 `9646324351` 在 Python 里是个完全合法的整数，
**不会**像 C++ 的 `int` 那样回绕成负数。

**但这不代表题目没有这个约束。**
题目模拟的是「32-bit 机器上的环境」，要求：
> 结果超出 `[-2^31, 2^31-1]` 就返回 0。

Python 不会替你报错，所以**必须自己写一行判断**：

```python
if res < -2**31 or res > 2**31 - 1:
    return 0
```

> **一句话**：C++ 里是「溢出会悄悄发生，所以要提前预判」；
> Python 里是「溢出不会发生，所以要事后判断」。
> **两种语言都要写检查，但原因正好相反。**

### 如果是 C++ / Java（不允许 64-bit）怎么写？

必须在**累加之前**预判，因为一旦溢出就来不及了：

```cpp
const int INT_MAX_ = 2147483647;   //  2^31 - 1，末位 7
const int INT_MIN_ = -2147483648;  // -2^31,    末位 8
if (res > INT_MAX_ / 10 || (res == INT_MAX_ / 10 && digit > 7))  return 0;
if (res < INT_MIN_ / 10 || (res == INT_MIN_ / 10 && digit < -8)) return 0;
res = res * 10 + digit;
```
`INT_MAX / 10 == 214748364`；只有当 `res` 恰好等于它时才需要比较末位数字
（`2147483647` 的末位是 **7**，`-2147483648` 的末位是 **8**）。
**本文件的 `Solution_3` 把这个预判逻辑在 Python 里完整复刻了一遍**，
用来练面试里真正要写的那个版本。

---

## LC-0007 和 LC-0066 的关系（不要当成两套不同的算法）

| | [LC-0066 Plus One](<../01 - LC-0066 - Plus One>) | **LC-0007** 本题 |
|---|---|---|
| 共享 | **Digit Processing（数位处理）** | 同 |
| 关注点 | **Carry Propagation（进位传播）** | **位序反转 + Overflow 判断** |
| 数位载体 | 数组（高位在前） | 整数本身（低位先出） |
| 典型坑 | 全 9 要进位到新的最高位 | 负数的 `//` / `%` + 32-bit 范围 |

两题的骨架都是「逐位取出 → 处理 → 逐位放回」，
**只是「处理」那一步做的事不同**。

---

复杂度：**O(log₁₀ x)** 时间（数位个数，最多 10 位 ⟹ 实际 O(1)）、**O(1)** 空间。

边界：
  - `x = 123` → `321`
  - `x = -123` → `-321`（**负数的 `%` 陷阱**）
  - `x = 120` → `21`（**尾部 0 消失**，不是 `021`）
  - `x = 0` → `0`
  - `x = 1534236469` → **`0`**（反转后 `9646324351` 超上界）
  - `x = -2147483648` → **`0`**（反转后 `-8463847412` 超下界）
  - `x = 2147483647` → **`0`**（反转后 `7463847412` 超上界）
  - `x = 1` / `x = -1` → 原样
  - `x = 1000000003` → **`0`**（反转后 `3000000001` 超上界）
"""

INT_MIN = -(2**31)          # ! -2147483648
INT_MAX = 2**31 - 1         # !  2147483647


##################################################################################################
##### ! Solution 1: 存符号 + 对绝对值拆位 + 最后一次范围判断
##### ! 时间复杂度: O(log x)   空间复杂度: O(1)
##### ! 适用：Python 下最清晰正确的写法。先剥符号，避开 // 和 % 的负数语义差异
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)                              # ! 之后的 % // 都作用在非负数上
        res = 0
        while x:
            res = res * 10 + x % 10             # ! Digit Extraction + Accumulation
            x //= 10                            # ! Integer Truncation
        res *= sign
        # ! Python 不会溢出，所以这个检查必须手写（题目的输出限制）
        if res < INT_MIN or res > INT_MAX:
            return 0
        return res


##################################################################################################
##### ! Solution 2: 字符串反转（最短，但要小心符号和前导零）
##### ! 时间复杂度: O(log x)   空间复杂度: O(log x)
##### ! 适用：允许字符串操作时的速写版。注意 int("021") == 21 自动吃掉前导零
##################################################################################################


class Solution_2:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        # ! int() 会自动丢掉前导零：int("021") == 21，所以 120 -> 21 天然正确
        res = sign * int(str(abs(x))[::-1])
        return 0 if res < INT_MIN or res > INT_MAX else res


##################################################################################################
##### ! Solution 3: 预判式溢出检查（复刻 C++/Java 不允许 64-bit 时必须写的版本）
##### ! 时间复杂度: O(log x)   空间复杂度: O(1)
##### ! 适用：面试写 C++/Java 时的真正答案 —— 在累加之前就拦下溢出
##################################################################################################


class Solution_3:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)
        limit = INT_MAX if sign == 1 else -INT_MIN   # ! 正数上界 2147483647，负数上界 2147483648
        last_allowed = limit % 10                    # ! 正数末位 7，负数末位 8
        res = 0
        while x:
            digit = x % 10
            x //= 10
            # ! 关键：在 res*10+digit 之前判断，而不是之后
            if res > limit // 10 or (res == limit // 10 and digit > last_allowed):
                return 0
            res = res * 10 + digit
        return sign * res


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.reverse(123) == 321
        assert s.reverse(-123) == -321              # ! 负数的 % 陷阱
        assert s.reverse(120) == 21                 # ! 尾部 0 消失
        assert s.reverse(0) == 0
        assert s.reverse(1) == 1
        assert s.reverse(-1) == -1
        assert s.reverse(1534236469) == 0           # ! 9646324351 超上界
        assert s.reverse(-2147483648) == 0          # ! -8463847412 超下界
        assert s.reverse(2147483647) == 0           # ! 7463847412 超上界
        assert s.reverse(1000000003) == 0           # ! 3000000001 超上界
        assert s.reverse(-1000000003) == 0
        assert s.reverse(1463847412) == 2147483641  # ! 刚好落在界内
        assert s.reverse(-1463847412) == -2147483641

    # ! 展示 Python 负数 // 和 % 的实际行为（本题的语言陷阱）
    print("-123 // 10 =", -123 // 10, "  (C/C++/Java 给 -12)")
    print("-123 %  10 =", -123 % 10, "   (C/C++/Java 给 -3)")
    print("reverse(-123) =", Solution_1().reverse(-123))
    print("reverse(1534236469) =", Solution_1().reverse(1534236469), "(超 32-bit 上界 ⟹ 0)")

    for _ in range(4000):                           # ! 随机对拍，刻意覆盖边界附近
        x = random.choice([
            random.randint(-10, 10),
            random.randint(INT_MIN, INT_MAX),
            random.randint(2147483000, INT_MAX),
            random.randint(INT_MIN, -2147483000),
            random.randint(-1000, 1000) * 10,        # ! 制造尾部 0
        ])
        a = Solution_1().reverse(x)
        b = Solution_2().reverse(x)
        c = Solution_3().reverse(x)
        assert a == b == c, (x, a, b, c)
    print("随机对拍 4000 组通过 ✓（拆位+事后判断 == 字符串反转 == C 风格预判）")
