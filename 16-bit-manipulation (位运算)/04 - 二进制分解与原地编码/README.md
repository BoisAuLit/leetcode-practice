# Level 1 · 04 — 二进制分解与原地编码（Binary Decomposition / In-place Encoding）

> **本层的统一目标：把「一个整数」当成容器用 —— 装 2 的幂、装两个数值、装一个集合。**
> 三个 Level 2 对应**三种完全不同的「装法」**，不要混。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Binary Decomposition（二进制分解）** | 把 `n` 写成若干 `2^i` 之和，即它的二进制表示 |
| **In-place Encoding（原地编码）** | 把新旧两个值塞进同一个数的高低位，避免额外数组 |
| **Bitmask as Set（位掩码表示集合）** | 第 `k` 位 = 1 表示「第 `k` 个元素在集合里」 |

---

## 三个决定性观察

### ① 二进制分解就是「逐位取出 `1 << i`」

```python
powers = []
while n:
    lowbit = n & (-n)        # ! 只保留最低位的 1 —— 就是一个 2 的幂
    powers.append(lowbit)
    n -= lowbit              # ! 或 n &= n - 1
```
**结果天然升序**，且个数 = popcount(n) ⟹ **O(popcount)**。

📍 [LC-2438 Range Product Queries of Powers](<./01 - Powers of Two 与范围乘积/01 - LC-2438 - Range Product Queries of Powers>)：
先分解成 2 的幂数组，再用**前缀积**（实际是**指数前缀和**）回答区间乘积查询。

**为什么用指数前缀和而不是直接前缀积？**
`powers` 的元素是 `2^e`，区间乘积是 `2^(e_l + ... + e_r)`
⟹ 对**指数**做前缀和，再一次 `pow(2, sum, MOD)` ⟹ 避免大数乘法和取模逆元。

### ② 原地编码：一个数装两个值（**算术编码**）

当题目要求 **O(1) 额外空间**，但新值依赖旧值时：

```python
# ! 第一遍：把新值"叠"在旧值的高位上（K 必须大于所有可能的值）
for i in range(n):
    nums[i] |= (new_value_for_i) << SHIFT       # 或 nums[i] += new * K
# ! 第二遍：把新值"抖"出来
for i in range(n):
    nums[i] >>= SHIFT                            # 或 nums[i] //= K
```

**为什么第一遍不能直接覆盖？**
因为后面的格子还要读**旧值**。这和
[15-math-geometry 的 LC-0289 Game of Life](<../../15-math-geometry (数学、几何)/02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/02 - LC-0289 - Game of Life>)
是**完全相同的模式**：

```
Read Original State  →  Record Updates  →  Apply Updates
```

**`K` / `SHIFT` 怎么选？** 必须**严格大于所有可能的值**：
- LC-1470：`nums[i] <= 1000` ⟹ `SHIFT = 10`（`2^10 = 1024 > 1000`）
- LC-1920：`nums[i] < n <= 1000` ⟹ 同样 `SHIFT = 10`

**选小了会怎样？** 高低位**互相污染** ⟹ 取出来的旧值是错的。
这是本 Level 2 唯一的坑。

📍 [LC-1470 Shuffle the Array](<./02 - In-place 编码与旧状态保护/01 - LC-1470 - Shuffle the Array>)、
[LC-1920 Build Array from Permutation](<./02 - In-place 编码与旧状态保护/02 - LC-1920 - Build Array from Permutation>)

### ③ Bitmask：一个数装一个**集合**（**集合编码**）

```python
mask |= 1 << i          # 加入元素 i
mask & other == 0       # ! 两个集合不相交 —— O(1)！
```

**和②的根本区别**：

| 用法 | 一个 int 代表什么 | 第 `k` 位的含义 | 本层的题 |
|---|---|---|---|
| **算术编码**（②） | 两个**数值** | 某个数值的某一位 | LC-1470、LC-1920 |
| **Bitmask 集合**（③） | 一个**元素集合** | 第 `k` 个元素**在不在** | **LC-0318** |

📍 [LC-0318 Maximum Product of Word Lengths](<./03 - Bitmask 表示集合/01 - LC-0318 - Maximum Product of Word Lengths>)：
26 个小写字母 ⟹ 一个 int 就是一个字母集合
⟹ 「两个单词无公共字母」从 O(L) 的集合比较压到**一次 `&`**。

---

## 核心不变量

**二进制分解（LC-2438）**：
> `powers` 恒为升序排列的 2 的幂，且 `prod(powers) == n`（原数）。
> 指数前缀和 `pre[i]` 恒等于 `powers[0..i-1]` 的指数之和。

**原地编码（LC-1470 / 1920）**：
> 第一遍进行中，`nums[i] & ((1 << SHIFT) - 1)` 恒等于**原始值**
> （因为新值只写在高位）⟹ 任何时刻都能读到正确的旧值。

**Bitmask 集合（LC-0318）**：
> `mask` 的第 `k` 位为 1 ⟺ 单词含有第 `k` 个字母。
> **mask 不保留出现次数** —— 它表示集合，不是多重集。

---

## 为什么用这些位操作

### 为什么原地编码值得学？

它是**「O(1) 额外空间」这个约束的通用解法**：
> 需要同时持有新旧两份数据，但不许开新数组
> ⟹ **把两份数据叠进同一个整数的不同位段**。

迁移到：Game of Life（LC-0289，用 bit 0 / bit 1）、
所有「原地重排但依赖原始下标」的题。

### 为什么 Bitmask 能把 O(L) 压到 O(1)？

**因为硬件的一次 `&` 同时处理了 32/64 个「位」的比较。**
用 set 判交集要逐元素比对 O(L)；
用 bitmask 判交集是一条 CPU 指令。
⟹ 当元素种类 `<= 64` 时，**bitmask 永远是更好的集合表示**。

---

## 简短正确性证明

### 原地编码为什么不丢信息

设 `K = 1 << SHIFT` 且 `K > max(所有值)`。编码后 `v = old + new·K`。
- 取旧值：`v % K == old`（因为 `old < K`）✓
- 取新值：`v // K == new` ✓

两者可**唯一还原** ⟹ 一个整数确实装下了两个值。
⚠️ **前提是 `old < K`** —— 若 `K` 选小了，`old` 会溢进高位段，`v // K` 就错了。∎

### `mask1 & mask2 == 0` ⟺ 无公共字母

`mask1 & mask2` 第 `k` 位为 1 ⟺ 两个 mask 第 `k` 位**都**是 1
⟺ **两个单词都含有**第 `k` 个字母。
所以结果为 0 ⟺ 不存在同时出现在两个单词里的字母。∎

### LC-2438 的指数前缀和

`powers[i] = 2^(e_i)` ⟹ `∏_{i=l}^{r} powers[i] = 2^(Σ_{i=l}^{r} e_i)`。
对指数做前缀和 `pre`，则区间指数和 `= pre[r+1] - pre[l]`
⟹ 一次 `pow(2, 该值, MOD)` 即得答案。
**每个查询 O(log(指数和))**，总共 **O(32 + q log)**。∎

---

## Python 核心模板

```python
# ① 二进制分解（LC-2438）
def powers_of(n):
    out = []
    while n:
        lowbit = n & (-n)                # ! 只保留最低位 1
        out.append(lowbit)
        n -= lowbit
    return out                            # ! 天然升序，长度 = popcount(n)

# LC-2438 的查询：对指数做前缀和
MOD = 10**9 + 7
exps = [p.bit_length() - 1 for p in powers_of(n)]
pre = [0]
for e in exps: pre.append(pre[-1] + e)
ans = [pow(2, pre[r + 1] - pre[l], MOD) for l, r in queries]

# ② 原地编码（LC-1470 / LC-1920）—— SHIFT 必须让 2^SHIFT > max(值)
SHIFT = 10                                # ! 2^10 = 1024 > 1000
for i in range(n):
    nums[i] |= (nums[nums[i] & 1023]) << SHIFT    # ! 旧值用低位读，新值写高位
for i in range(n):
    nums[i] >>= SHIFT                     # ! 第二遍统一兑现

# ③ Bitmask 表示集合（LC-0318）
def mask_of(word):
    m = 0
    for ch in word:
        m |= 1 << (ord(ch) - 97)          # ! 第 k 位 = 含第 k 个字母
    return m
# 判不相交：mask_of(w1) & mask_of(w2) == 0      ← O(1)
```

---

## 时间与空间复杂度

| 题 | 时间 | 空间 | 注意 |
|---|---|---|---|
| LC-2438 | **O(32 + q log)** | O(32 + q) | 分解只有 popcount 项 |
| LC-1470 | **O(n)** | **O(1)** 额外 | O(1) 是题目 Follow-up |
| LC-1920 | **O(n)** | **O(1)** 额外 | 同上 |
| LC-0318 | **O(n·L + m²)** | O(n) | ⚠️ **不是 O(n²·L)** —— bitmask 省掉了 L |

---

## 代表题目

| # | 题 | 优先级 | 「装法」 |
|---|---|---|---|
| 1 | [LC-2438 Range Product Queries of Powers](<./01 - Powers of Two 与范围乘积/01 - LC-2438 - Range Product Queries of Powers>) | P2 | 二进制分解 + 指数前缀和 |
| 2 | [LC-1470 Shuffle the Array](<./02 - In-place 编码与旧状态保护/01 - LC-1470 - Shuffle the Array>) | P2 | **算术编码**（两个数值） |
| 3 | [LC-1920 Build Array from Permutation](<./02 - In-place 编码与旧状态保护/02 - LC-1920 - Build Array from Permutation>) | P2 | **算术编码**（两个数值） |
| 4 | [LC-0318 Maximum Product of Word Lengths](<./03 - Bitmask 表示集合/01 - LC-0318 - Maximum Product of Word Lengths>) ★ | P1 | **Bitmask 集合** |

★ 第二轮审核新增 —— 本专题原本**一道 Bitmask 集合题都没有**。

---

## 典型反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| 原地编码 `SHIFT` / `K` 选小了 | `nums[i] = 1000`，`SHIFT = 9`（`512 < 1000`） | 高低位**互相污染**，旧值读错 ❌ |
| 原地编码第一遍直接覆盖 | 任意 | 后面的格子读到新值而非旧值 ❌ |
| 原地编码忘了第二遍 `>>= SHIFT` | 任意 | 返回的是编码后的大数 ❌ |
| LC-1920 用 `nums[nums[i]]` 直接读 | `[0,2,1,5,3,4]` | 读到已被改写的值 ❌ |
| LC-2438 直接算前缀**积** | 大 n | 需要模逆元才能做区间除法；指数前缀和更简单 ⚠️ |
| LC-2438 分解时用 `while n: out.append(n % 2)` | 任意 | 得到的是位序列不是 2 的幂；还要再转 ⚠️ |
| LC-0318 用 set 两两判交集 | `n = 1000, L = 1000` | O(n²L) = 10^9 ⟹ 慢 ❌ |
| LC-0318 以为 mask 保留了出现次数 | `"abb"` vs `"ab"` | 两者 **mask 相同**（都是 `0b11`）⚠️ |
| LC-0318 忘了「需要两个不同单词」 | `["a"]` | 返回非 0 ❌（正确是 0） |
| 把 Bitmask 用在元素种类 > 64 的集合上 | — | 一个 int 装不下 ⟹ 要用 set 或多个 int ❌ |

---

## 容易混淆的 Pattern

### 算术编码 vs Bitmask 集合（**本层最重要的区分**）

| | **算术编码**（LC-1470 / 1920） | **Bitmask 集合**（LC-0318） |
|---|---|---|
| 一个 int 代表 | 两个**数值** | 一个**元素集合** |
| 第 `k` 位的含义 | 某个数值的第 `k` 个二进制位 | 第 `k` 个**元素**在不在 |
| 取出方式 | `v % K` / `v // K`（**算术**） | `v >> k & 1`（**按位**） |
| 典型操作 | 加 / 除 / 移位 | `\|`（并）、`&`（交）、`^`（对称差） |
| 容量限制 | `K > max(值)` | 元素种类 `<= 32/64` |

> **两者都是「一个 int 装多份信息」，但信息的组织方式完全不同。**
> 搞混的典型症状：对 bitmask 做除法，或对算术编码做 `& `判交集。

### 二进制分解 vs 位枚举

| | 二进制分解（LC-2438） | 位枚举（LC-0078） |
|---|---|---|
| 做什么 | 把**一个**数拆成 2 的幂 | 枚举**所有** `2^n` 个 mask |
| 次数 | O(popcount) | **O(2^n)** |
| 用途 | 快速幂、稀疏表示 | 子集枚举、状压 DP |

### 和 15-math-geometry 的 LC-0289 同构

| | LC-0289 Game of Life | LC-1470 / LC-1920 |
|---|---|---|
| 模式 | `Read Original → Record → Apply` | **完全相同** |
| 新旧分居 | bit 0（旧）/ bit 1（新） | 低位段（旧）/ 高位段（新） |
| 第二遍 | `>>= 1` | `>>= SHIFT` |

> **「原地修改但依赖旧值」这个问题，矩阵题和数组题的解法一模一样。**

---

## 相邻 Pattern 对比

| | [Level 1 · 03](<../03 - Bitwise Subarray 与位聚合>) | **本层（04）** | [Level 1 · 05](<../05 - 跨专题与低优先级存档>) |
|---|---|---|---|
| 关心 | 一段区间的**聚合统计** | 一个整数的**结构 / 容量** | 低迁移性题目的归档 |
| 主运算 | OR、AND | 移位、按位分解、`\|` / `&` | 混杂 |
| 典型技巧 | 状态数有界 | **二进制分解、原地编码、Bitmask** | — |

---

## 相关资料

- [位运算恒等式速查表](<../_resources/bit-tricks-cheat-sheet.md>) — 第七节「Bitmask 当集合用」
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q11 / Q12 / Q13 / Q14
