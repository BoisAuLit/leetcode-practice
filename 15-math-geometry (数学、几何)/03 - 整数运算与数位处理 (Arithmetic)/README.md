# Level 1 · 03 — 整数运算与数位处理（Arithmetic / Digit Processing）

> **本层的统一目标：把一个整数（或表示整数的字符串）按「位」拆开处理。**
> 四道题共享同一个骨架 —— **逐位取出 → 做点事 → 合并回去** ——
> 区别只在「做点事」那一步。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Digit Extraction（数位提取）** | `digit = x % 10`，`x //= 10` |
| **Carry Propagation（进位传播）** | `carry` 从低位一路带到高位；可能产生**新的最高位** |
| **Integer Parsing（整数解析）** | 字符串 → 整数，要处理空白、符号、非法字符、溢出 |
| **Grade-school Multiplication** | `result[i+j+1] += a[i] * b[j]`，位置是乘法的关键 |
| **Fast Exponentiation（平方快速幂）** | 按**指数的二进制位**选平方项，O(log n) |
| **Sieve（筛法）** | 一次预处理出表，之后 O(1) 查询 |

---

## 三个决定性观察

### ① 四道数位题是**同一个骨架**，只有「做点事」不同

| 题 | 载体 | 「做点事」 | 关注点 |
|---|---|---|---|
| [LC-0066 Plus One](<./01 - 数位进位与整数反转/01 - LC-0066 - Plus One>) | 数组（高位在前） | `+1` 并传播 carry | **Carry** |
| [LC-0007 Reverse Integer](<./01 - 数位进位与整数反转/02 - LC-0007 - Reverse Integer>) | 整数本身（低位先出） | 倒着拼回去 | **位序 + 溢出** |
| [LC-0008 atoi](<./02 - 字符串解析与大整数乘法/01 - LC-0008 - String to Integer (atoi)>) | 字符串（高位在前） | 逐字符累加 | **解析规则 + 溢出** |
| [LC-0043 Multiply Strings](<./02 - 字符串解析与大整数乘法/02 - LC-0043 - Multiply Strings>) | 字符串（高位在前） | 两两相乘 + 定位 | **位置 + Carry** |

> **不要把它们当四套算法。** 把骨架记住，然后记四个「做点事」。

### ② Python 的 `//` 和 `%` 对负数是**向下取整**（本层最大的语言陷阱）

| 表达式 | Python | C / C++ / Java |
|---|---|---|
| `-123 // 10` | **`-13`**（向 -∞） | `-12`（向 0 截断） |
| `-123 % 10` | **`7`**（符号跟除数） | `-3`（符号跟被除数） |

**后果**：正数的拆位逻辑**不能**直接套到负数上 ——
`-123 % 10` 给 `7` 而不是 `3`，拆出来的位全错。

**统一解法**：先剥符号，只对绝对值处理。
```python
sign = -1 if x < 0 else 1
x = abs(x)
```
**不要用 `int(x / 10)`** —— 那是浮点，大整数会丢精度。

### ③ Python 不会溢出，但**题目的范围限制必须人工判断**

Python 的 `int` 是**任意精度**的 —— `9646324351` 是个合法整数，
**不会**像 C++ 的 `int` 那样回绕成负数。

**但题目要求「超出 `[-2^31, 2^31-1]` 返回 0」，所以必须自己写：**
```python
if res < -2**31 or res > 2**31 - 1:
    return 0
```

> **C++ 里是「溢出会悄悄发生，所以要提前预判」；
> Python 里是「溢出不会发生，所以要事后判断」。
> 两种语言都要写检查，但原因正好相反。**

---

## 核心不变量

**Carry（LC-0066 / 0043）**：
> 处理到第 `i` 位时，`carry` 恰好等于「低 `i` 位运算产生的、尚未计入的进位」。
> 循环结束后若 `carry > 0`，必须**新增一个最高位**。

**Reverse（LC-0007）**：
> `res` 永远是「已处理的那些数位**倒序**拼成的整数」。

**atoi（LC-0008）**：
> 任意时刻 `res` 是已读入数字前缀的值；遇到第一个非数字字符立即停止。

**Multiply（LC-0043）**：
> `num1[i] * num2[j]` 的结果一定落在 `result[i+j]` 和 `result[i+j+1]` 这两格
> （见下面的证明）。

**Fast Power（LC-0050）**：
> 每轮 `base == x^(2^k)`（`k` = 已处理的位数），
> `result` == 「已处理的那些为 1 的位对应的平方项之积」。

**Sieve（LC-0204）**：
> 外层处理到 `i` 时，所有**最小质因子 < i** 的合数都已被划掉。

---

## 简短正确性证明

### LC-0043：为什么结果最多需要 `m + n` 位？

`m` 位数 `< 10^m`，`n` 位数 `< 10^n` ⟹ 乘积 `< 10^(m+n)` ⟹ **最多 `m+n` 位**。
下界：`10^(m-1) × 10^(n-1) = 10^(m+n-2)` ⟹ **至少 `m+n-1` 位**。
所以开 `m+n` 长的数组够用，且最高位可能是 0（要跳过前导零，但**保留 `"0"` 本身**）。∎

### LC-0043：为什么 `num1[i] * num2[j]` 落在 `result[i+j+1]`？

以字符串下标（高位在前）、`m = len(num1)`、`n = len(num2)` 为例：
`num1[i]` 的权重是 `10^(m-1-i)`，`num2[j]` 的权重是 `10^(n-1-j)`
⟹ 乘积权重 `10^(m+n-2-i-j)`。
在长度 `m+n` 的结果数组里（高位在前），权重 `10^k` 对应下标 `m+n-1-k`
⟹ 下标 `= m+n-1-(m+n-2-i-j) = i+j+1` ∎
（进位溢到 `result[i+j]`，所以这两格就够。）

### LC-0050：为什么处理二进制位 = 分解成平方项之积？

把 `n` 写成二进制 `n = Σ bᵢ·2^i`，则
```
x^n = x^(Σ bᵢ·2^i) = Π (x^(2^i))^bᵢ
```
循环里 `base` 每轮自乘，第 `i` 轮恰好是 `x^(2^i)`
⟹ `if n & 1: result *= base` 就是「把 `bᵢ=1` 的项选进乘积」。∎
位数 = `log₂|n|` ⟹ **O(log |n|)** 次循环。

### LC-0204：为什么外层只到 `√n`，内层从 `i*i` 起？

**外层到 `√n`**：若合数 `c` 有因子 `a > √c`，则配对因子 `b = c/a < √c`
⟹ `c` 早已被 `b` 的某个素因子划掉。所以**每个合数都有一个 ≤ √n 的素因子**。∎

**内层从 `i*i`**：`i` 的倍数中小于 `i*i` 的那些（`2i, 3i, …, (i-1)i`）
都含有一个**更小的因子** ⟹ 处理那个更小因子时已被划掉。∎

两者都是**省功**，不是正确性要求 —— 去掉答案仍对，只是更慢。
总操作数 `n·Σ_{p<n} 1/p ≈ n·ln ln n` ⟹ **O(n log log n)**。

---

## Python 模板

### Template 5：Digit Processing + Carry（LC-0066）

```python
def plusOne(digits):
    for i in range(len(digits) - 1, -1, -1):     # ! 从最低位往高位
        if digits[i] < 9:
            digits[i] += 1
            return digits                        # ! 不进位就结束
        digits[i] = 0                            # ! 是 9 ⟹ 置 0 继续进位
    return [1] + digits                          # ! 全是 9 ⟹ 新增最高位
```
**O(n)** 时间、O(1) 额外空间（返回时 `[1]+digits` 是 O(n)）。

### 整数反转（LC-0007）

```python
def reverse(x):
    sign = -1 if x < 0 else 1
    x = abs(x)                                   # ! 剥符号，避开负数的 // % 语义
    res = 0
    while x:
        res = res * 10 + x % 10
        x //= 10
    res *= sign
    return 0 if res < -2**31 or res > 2**31 - 1 else res   # ! 人工范围判断
```
**O(log₁₀ x)** 时间（最多 10 位 ⟹ 实际 O(1)）、O(1) 空间。

### Template 6：Integer Parsing + Bounds（LC-0008）

```python
def myAtoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == ' ': i += 1           # ! ① 跳前导空白
    sign = 1
    if i < n and s[i] in '+-':                    # ! ② 最多一个符号
        sign = -1 if s[i] == '-' else 1
        i += 1
    res = 0
    while i < n and s[i].isdigit():               # ! ③ 遇到非数字立即停
        res = res * 10 + int(s[i]); i += 1
    res *= sign
    return max(-2**31, min(res, 2**31 - 1))       # ! ④ 夹到范围内（不是返回 0！）
```
**O(n)** 时间、O(1) 空间。
⚠️ **LC-0008 是「夹到边界」，LC-0007 是「返回 0」—— 两题的溢出处理不一样。**

### Template 7：Grade-school String Multiplication（LC-0043）

```python
def multiply(num1, num2):
    if num1 == '0' or num2 == '0': return '0'     # ! 提前返回，省掉前导零的麻烦
    m, n = len(num1), len(num2)
    res = [0] * (m + n)                           # ! 最多 m+n 位
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(num1[i]) * int(num2[j])
            total = mul + res[i + j + 1]          # ! 落点是 i+j+1
            res[i + j + 1] = total % 10
            res[i + j] += total // 10             # ! 进位溢到 i+j
    k = 0
    while k < len(res) - 1 and res[k] == 0: k += 1   # ! 跳前导零，但至少留一位
    return ''.join(map(str, res[k:]))
```
**O(m·n)** 时间、O(m+n) 空间。

### Template 8：Exponentiation by Squaring（LC-0050）

```python
def myPow(x, n):
    if n < 0:                                     # ! 负指数 ⟹ 取倒数
        x, n = 1 / x, -n
    result, base = 1.0, x
    while n:
        if n & 1: result *= base                  # ! 这一位是 1 ⟹ 选进乘积
        base *= base                              # ! base 依次是 x^1, x^2, x^4, x^8…
        n >>= 1
    return result
```
**O(log |n|)** 时间、O(1) 空间。
⚠️ C++/Java：`n == INT_MIN` 时 `-n` **溢出**，要先转 `long`。

### Sieve of Eratosthenes（LC-0204）

```python
def countPrimes(n):
    if n < 3: return 0                            # ! n=0,1,2 都是 0（2 不小于 2）
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i < n:                               # ! 外层只到 √n
        if is_prime[i]:
            start = i * i                          # ! 内层从 i*i 起
            is_prime[start::i] = [False] * ((n - start + i - 1) // i)
        i += 1
    return sum(is_prime)
```
**O(n log log n)** 时间、O(n) 空间。

---

## 复杂度对照

| 题 | 时间 | 空间 | 注意 |
|---|---|---|---|
| LC-0066 | **O(n)** | O(1) 额外 | `n` = 位数 |
| LC-0007 | **O(log₁₀ x)** ≈ O(1) | O(1) | 最多 10 位 |
| LC-0008 | **O(n)** | O(1) | `n` = 字符串长度 |
| LC-0043 | **O(m·n)** | O(m+n) | 竖式乘法；Karatsuba 可到 O(n^1.585) 但不要求 |
| LC-0050 | **O(log \|n\|)** | O(1) | ⚠️ **不是 O(n)** |
| LC-0204 | **O(n log log n)** | O(n) | ⚠️ **不是 O(n√n)**，那是试除法 |

---

## 代表题目

| # | 题 | 优先级 | 核心 | 典型陷阱 |
|---|---|---|---|---|
| 1 | [LC-0066 Plus One](<./01 - 数位进位与整数反转/01 - LC-0066 - Plus One>) | **P0** | Carry | 全 9 要新增最高位 |
| 2 | [LC-0007 Reverse Integer](<./01 - 数位进位与整数反转/02 - LC-0007 - Reverse Integer>) | P1 | 位序 + 溢出 | Python 负数 `%`；返回 **0** |
| 3 | [LC-0008 atoi](<./02 - 字符串解析与大整数乘法/01 - LC-0008 - String to Integer (atoi)>) | P1 | 解析规则 | 溢出是**夹边界**，不是返回 0 |
| 4 | [LC-0043 Multiply Strings](<./02 - 字符串解析与大整数乘法/02 - LC-0043 - Multiply Strings>) | P1 | 位置 + Carry | 落点 `i+j+1`；前导零但留 `"0"` |
| 5 | [LC-0050 Pow(x, n)](<./03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)>) ✚ | **P0** | 快速幂 | 负指数；`n = INT_MIN`；**误差是 O(n·ε)，别用 1e-9 卡大指数** |
| 6 | [LC-0204 Count Primes](<./04 - 筛法与素数计数/01 - LC-0204 - Count Primes>) ★ | P2 | 筛法 | `countPrimes(2) == 0` |

✚ 实体已于 2026-11-11 从清空的 `99-advanced/divide-and-conquer` 迁入本层（**5 条复习记录 + `note.md` 随之保留**）· ★ 第二轮审核新增
LC-0066 有用户自己的 `note.md`，已原地保留。

---

## 典型边界情况（数值类必测）

| # | 边界 | 例子 | 期望 |
|---|---|---|---|
| 1 | **0** | `reverse(0)` / `countPrimes(0)` | `0` |
| 2 | 正数 | `reverse(123)` | `321` |
| 3 | **负数** | `reverse(-123)` | `-321`（`%` 陷阱） |
| 4 | **Carry 到新最高位** | `plusOne([9,9,9])` | `[1,0,0,0]` |
| 5 | **Leading Zeros** | `reverse(120)` | `21`（不是 `021`） |
| 6 | **32-bit 边界** | `reverse(1534236469)` | **`0`**（超上界） |
| 6' | 同上，但 atoi | `myAtoi("91283472332")` | **`2147483647`**（夹边界） |
| 7 | **负指数** | `myPow(2.0, -2)` | `0.25` |
| 8 | **极大指数** | `myPow(2.0, 2**31-1)` | 要能算（O(log n)） |
| 9 | `n == 0` | `myPow(x, 0)` | `1.0`（任何 `x`） |
| 10 | `x == -1` | `myPow(-1.0, 3)` | `-1.0`（奇偶性） |
| 11 | **严格小于** | `countPrimes(2)` | **`0`**（2 不小于 2） |
| 12 | 完全平方数 | `countPrimes(25)` | `9`（`i*i` 优化的试金石） |
| 13 | `"0" × "0"` | `multiply("0","0")` | `"0"`（不是 `""`） |
| 14 | atoi 全是空白/非法 | `myAtoi("   ")` / `myAtoi("abc")` | `0` |
| 15 | atoi 带前导零 | `myAtoi("  -0042")` | `-42` |

---

## 常见错误与反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| 直接对负数做 `% 10` | `reverse(-123)` | `-123 % 10 == 7` ⟹ 位全错 ❌ |
| 用 `int(x / 10)` 截断 | 大整数 | 浮点丢精度 ❌ |
| 认为 Python 会自动溢出报错 | `reverse(1534236469)` | 返回 `9646324351` 而不是 `0` ❌ |
| 把 LC-0008 的溢出也写成返回 0 | `myAtoi("91283472332")` | 应该夹成 `2147483647` ❌ |
| LC-0066 全 9 时不新增最高位 | `[9,9]` | 返回 `[0,0]` ❌ |
| LC-0043 落点写成 `i+j` | 任意 | 整体错位一格 ❌ |
| LC-0043 把所有前导零都跳掉 | `multiply("0","0")` | 返回 `""` ❌ |
| LC-0050 用 `n` 次连乘 | `n = 2^31-1` | TLE（21 亿次）❌ |
| LC-0050 忘记负指数取倒数 | `myPow(2.0,-2)` | 返回 4.0 ❌ |
| LC-0050 在 C++ 里写 `-n` | `n == INT_MIN` | 溢出 ❌ |
| LC-0204 不处理 `n < 3` | `countPrimes(1)` | `is_prime[1]` 越界 ❌ |
| LC-0204 用逐个试除 | `n = 5×10^6` | O(n√n) TLE ❌ |

---

## 相邻 Pattern 对比

| | [Level 1 · 02](<../02 - 矩阵变换与状态模拟 (Matrix Transformation)>) | **本层（03）** | [Level 1 · 04](<../04 - 坐标几何与空间计数 (Geometry)>) |
|---|---|---|---|
| 操作对象 | 二维矩阵 | **单个整数 / 数字串** | 平面坐标点 |
| 难点 | 写入顺序、坐标公式 | **符号、进位、溢出** | 整数化、`+1` 与否 |
| 常用技巧 | 原地标记、位编码 | `% 10` / `// 10`、位运算 | `gcd`、`Counter` |
| 共同点 | — | 都刻意**避开浮点** | 都刻意**避开浮点** |

**本层和 Level 04 的共同主题**：**能用整数就绝不用浮点**。
本层是为了避开截断语义和溢出；Level 04 是为了避开斜率精度。

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q7 / Q8 / Q9 / Q14
- [整数溢出与数值陷阱](<../_resources/overflow-and-numeric-pitfalls.md>) — **本层的配套文档**，必读
- [矩阵坐标与边界速查表](<../_resources/matrix-index-cheat-sheet.md>)


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-0415 Add Strings](<./01 - 数位进位与整数反转/03 - LC-0415 - Add Strings>) | `03 - 整数运算与数位处理 (Arithmetic)/01 - 数位进位与整数反转` | 竖式模板 while i>=0 or j>=0 or carry；和 LC-0002 / LC-0067 / LC-0043 共用 | 三道题一个模板 |
| [LC-0273 Integer to English Words](<./02 - 字符串解析与大整数乘法/03 - LC-0273 - Integer to English Words>) | `03 - 整数运算与数位处理 (Arithmetic)/02 - 字符串解析与大整数乘法` | 每 3 位一组 + 单位词；组内 0 不输出、组值 0 单位词也不输出、10..19 查表 | Meta 高频，纯边角 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
