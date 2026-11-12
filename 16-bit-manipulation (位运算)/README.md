# 16 - Bit Manipulation（位运算）

> **一句话**：位运算题几乎不需要「算法」，需要的是**一打恒等式** +
> **知道哪些在 Python 里会出事**。
> 整个专题的重量级知识只有三条：**XOR 的四个性质**、
> **`x & (x-1)` / `x & (-x)` 的区别**、**Python 必须手动模拟固定宽度**。

**21 道题 · 5 个 Level 1 · 14 个 Level 2**

---

## 一、知识地图

```
Level 1 · 01  二进制基础、位计数与位反转          ← 单个数的位分布（地基）
                ├─ 01 Popcount 与最低有效置位      LC-0191  LC-0231  LC-0338
                └─ 02 固定宽度位读取与反转          LC-0190

Level 1 · 02  XOR 不变量与二进制算术              ← 多个数之间的代数关系
                ├─ 01 XOR 抵消与缺失元素           LC-0136  LC-0268  LC-0260★
                ├─ 02 XOR 与 AND 形成二进制加法     LC-0371★
                └─ 03 Range AND 与共同高位前缀      LC-0201★

Level 1 · 03  Bitwise Subarray 与位聚合           ← 一段区间的聚合统计
                ├─ 01 子数组 OR 状态与按位贡献      LC-0898  LC-2411
                └─ 02 最大 Bitwise AND 与连续区间   LC-2419

Level 1 · 04  二进制分解与原地编码                 ← 把一个整数当容器用
                ├─ 01 Powers of Two 与范围乘积      LC-2438
                ├─ 02 In-place 编码与旧状态保护     LC-1470  LC-1920
                └─ 03 Bitmask 表示集合              LC-0318★

Level 1 · 05  跨专题与低优先级存档                 ← 保留成果，但不占核心预算
                ├─ 01 Popcount + Sorting            LC-1356
                ├─ 02 特殊二进制贪心与有符号幂分解   LC-2571
                ├─ 03 非位运算题目与 Shell 文本处理  LC-0194
                └─ 04 跨专题索引                    LC-0421↗ LC-0078↗
```

★ = 本次新增 · ↗️ = 实体在其他专题，只放学习索引

---

## 二、五个 Level 1

| Level 1 | 关心什么 | 主运算 | 核心认识 |
|---|---|---|---|
| [**01** 二进制基础与位计数](<./01 - 二进制基础、位计数与位反转>) | **单个数**的位分布 | AND（清位）、移位 | `x & (x-1)` 清最低位 1 ⟹ Popcount 是 **O(popcount)** |
| [**02** XOR 不变量与二进制算术](<./02 - XOR 不变量与二进制算术>) | **多个数**之间的关系 | **XOR**、AND、进位 | XOR 的**四个性质**，四道题各用一个 |
| [**03** Bitwise Subarray 与位聚合](<./03 - Bitwise Subarray 与位聚合>) | **一段区间**的聚合 | OR、AND | OR 单调 + 32 位 ⟹ **状态数 O(32)** |
| [**04** 二进制分解与原地编码](<./04 - 二进制分解与原地编码>) | 一个整数的**容量** | 移位、`\|` / `&` | **算术编码** vs **Bitmask 集合**是两回事 |
| [**05** 跨专题与低优先级存档](<./05 - 跨专题与低优先级存档>) | 归档 | 混杂 | 「用到位运算」≠「是位运算题」 |

**依赖顺序**：01 是地基 → 02 / 03 / 04 相对独立 → 05 是归档。

---

## 三、全部题目（含真实相对路径）

| # | 题 | 优先级 | Pattern | 路径 |
|---|---|---|---|---|
| 1 | LC-0191 Number of 1 Bits | **P0** | Popcount | [→](<./01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/01 - LC-0191 - Number of 1 Bits>) |
| 2 | LC-0231 Power of Two | **P0** | `x & (x-1) == 0` | [→](<./01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/02 - LC-0231 - Power of Two>) |
| 3 | LC-0338 Counting Bits | **P0** | Counting Bits DP | [→](<./01 - 二进制基础、位计数与位反转/01 - Popcount 与最低有效置位/03 - LC-0338 - Counting Bits>) |
| 4 | LC-0190 Reverse Bits | P1 | Fixed-width Reverse | [→](<./01 - 二进制基础、位计数与位反转/02 - 固定宽度位读取与反转/01 - LC-0190 - Reverse Bits>) |
| 5 | LC-0136 Single Number | **P0** | XOR 抵消 | [→](<./02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/01 - LC-0136 - Single Number>) |
| 6 | LC-0268 Missing Number | **P0** | XOR 抵消（下标⊕值） | [→](<./02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/02 - LC-0268 - Missing Number>) |
| 7 | LC-0260 Single Number III ★ | P1 | XOR + **区分位分组** | [→](<./02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/03 - LC-0260 - Single Number III>) |
| 8 | LC-0371 Sum of Two Integers ★ | **P0** | XOR/AND 半加器 | [→](<./02 - XOR 不变量与二进制算术/02 - XOR 与 AND 形成二进制加法/01 - LC-0371 - Sum of Two Integers>) |
| 9 | LC-0201 Bitwise AND of Numbers Range ★ | P1 | **公共高位前缀** | [→](<./02 - XOR 不变量与二进制算术/03 - Range AND 与共同高位前缀/01 - LC-0201 - Bitwise AND of Numbers Range>) |
| 10 | LC-0898 Bitwise ORs of Subarrays | P1 | OR 状态数 O(32) | [→](<./03 - Bitwise Subarray 与位聚合/01 - 子数组 OR 状态与按位贡献/01 - LC-0898 - Bitwise ORs of Subarrays>) |
| 11 | LC-2411 Smallest Subarrays With Max OR | P2 | 每位最近出现位置 | [→](<./03 - Bitwise Subarray 与位聚合/01 - 子数组 OR 状态与按位贡献/02 - LC-2411 - Smallest Subarrays With Maximum Bitwise OR>) |
| 12 | LC-2419 Longest Subarray With Max AND | P2 | **最大 AND = max** | [→](<./03 - Bitwise Subarray 与位聚合/02 - 最大 Bitwise AND 与连续区间/01 - LC-2419 - Longest Subarray With Maximum Bitwise AND>) |
| 13 | LC-2438 Range Product Queries of Powers | P2 | 二进制分解 + 指数前缀和 | [→](<./04 - 二进制分解与原地编码/01 - Powers of Two 与范围乘积/01 - LC-2438 - Range Product Queries of Powers>) |
| 14 | LC-1470 Shuffle the Array | P2 | 算术编码 | [→](<./04 - 二进制分解与原地编码/02 - In-place 编码与旧状态保护/01 - LC-1470 - Shuffle the Array>) |
| 15 | LC-1920 Build Array from Permutation | P2 | 算术编码 | [→](<./04 - 二进制分解与原地编码/02 - In-place 编码与旧状态保护/02 - LC-1920 - Build Array from Permutation>) |
| 16 | LC-0318 Maximum Product of Word Lengths ★ | P1 | **Bitmask 集合** | [→](<./04 - 二进制分解与原地编码/03 - Bitmask 表示集合/01 - LC-0318 - Maximum Product of Word Lengths>) |
| 17 | LC-1356 Sort Integers by Number of 1 Bits | P2 | Popcount 当排序 key | [→](<./05 - 跨专题与低优先级存档/01 - Popcount + Sorting/01 - LC-1356 - Sort Integers by The Number of 1 Bits>) |
| 18 | LC-2571 Min Operations to Reduce Integer to 0 | P2 | NAF 贪心 | [→](<./05 - 跨专题与低优先级存档/02 - 特殊二进制贪心与有符号幂分解/01 - LC-2571 - Minimum Operations to Reduce an Integer to 0>) |
| 19 | LC-0194 Transpose File | P2（存档） | **非位运算** | [→](<./05 - 跨专题与低优先级存档/03 - 非位运算题目与 Shell 文本处理/01 - LC-0194 - Transpose File>) |
| 20 | LC-0421 Maximum XOR of Two Numbers ↗️ | P1 | Binary Trie + XOR 自逆 | [→](<./05 - 跨专题与低优先级存档/04 - 跨专题索引/01 - LC-0421 - Maximum XOR of Two Numbers in an Array (学习索引 · 实体在 08-tries)>) |
| 21 | LC-0078 Subsets ↗️ | P1 | Bitmask Enumeration | [→](<./05 - 跨专题与低优先级存档/04 - 跨专题索引/02 - LC-0078 - Subsets (学习索引 · 实体在 10-backtracking)>) |

**实体文件夹 19 个 + 跨专题索引 2 个 = 21 道不同题目。**

---

## 四、P0 / P1 / P2

| 等级 | 数量 | 题 |
|---|---|---|
| **P0**（核心恒等式，必须熟练） | **6** | 0191, 0231, 0338, 0136, 0268, 0371 |
| **P1**（标准面试覆盖面） | **6** | 0190, 0260, 0201, 0898, 0318, 0421↗️ |
| **P1（索引）** | **1** | 0078↗️ |
| **P2**（存档与补充） | **8** | 2411, 2419, 2438, 1470, 1920, 1356, 2571, 0194 |

> P0/P1/P2 是**教学优先级**（恒等式覆盖面 + 学习依赖），
> **不代表任何公司的实际出题频次** —— 本仓库不编造频次数据。

---

## 五、重要位运算操作与公式

### 单位操作：**OR 置一、AND 清零、XOR 翻转**

```python
x >> i & 1            # 读第 i 位
x | (1 << i)          # 置 1
x & ~(1 << i)         # 清 0
x ^ (1 << i)          # 翻转
```

### ⚠️ 最容易记混的一对

| 表达式 | 作用 | `0b1011000` → | 用在哪 |
|---|---|---|---|
| `x & (x - 1)` | **清掉**最低位 1 | `0b1010000` | Popcount、判 2 的幂 |
| `x & (-x)` | **只保留**最低位 1 | `0b0001000` | 区分位分组、lowbit |

### Popcount（三种，复杂度不同）

```python
while x: x &= x - 1; cnt += 1    # ! O(popcount) —— 稀疏数据最快
bin(x).count('1')                 # ! O(32) + 字符串；⚠️ 对负数错
x.bit_count()                     # ! Python 3.10+，最快
```

### 判 2 的幂

```python
x > 0 and x & (x - 1) == 0        # ! x > 0 不能省（x=0 会误判）
```

---

## 六、XOR Cancellation（异或抵消）与 XOR 的四个性质

| 性质 | 表达式 | 哪道题 |
|---|---|---|
| **抵消性** | `x ^ x == 0`、`x ^ 0 == x` | LC-0136、LC-0268 |
| **区分位** | `a != b ⟹ a ^ b != 0` | LC-0260 |
| **算术含义** | `a^b` = 无进位和、`(a&b)<<1` = 进位 | LC-0371 |
| **自逆性** | `a ^ b == c ⟺ a == c ^ b` | LC-0421 |

加上**交换律 + 结合律** ⟹ XOR 一串数时**顺序无关**。

```python
# 1 个异常元素 ⟹ 一次 XOR 就够
acc = 0
for x in nums: acc ^= x

# 2 个异常元素 ⟹ 还要用一个位分组
xor_all = 0
for x in nums: xor_all ^= x
diff = xor_all & (-xor_all)        # ! 区分位
a = 0
for x in nums:
    if x & diff: a ^= x
return [a, xor_all ^ a]
```

---

## 七、Bit DP（Counting Bits）

```python
dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i >> 1] + (i & 1)       # ! 或 dp[i & (i-1)] + 1
```
**O(n)**，而逐个算 popcount 是 O(32n)。📍 LC-0338

---

## 八、Binary Addition（二进制加法）

```python
MASK, MAX_INT = 0xFFFFFFFF, 0x7FFFFFFF
while b:
    carry = ((a & b) << 1) & MASK      # ! 进位，每轮截断
    a = (a ^ b) & MASK                 # ! 无进位和
    b = carry
return a if a <= MAX_INT else ~(a ^ MASK)
```
**O(1)**（最多 32 轮）。📍 LC-0371
⚠️ **MASK 是正确性必需品，不是优化** —— 见第十一节。

---

## 九、Common Prefix（Range AND）

```python
shifts = 0
while left < right:
    left >>= 1; right >>= 1; shifts += 1
return left << shifts
```
**O(32)**。📍 LC-0201

### ⚠️ AND / OR / XOR 的区间规律**完全不同**

| 运算 | `[4,7]` | 规律 | 单调性 |
|---|---|---|---|
| **AND** | `4` | **公共高位前缀** | 递减（只清 1） |
| **OR** | `7` | 公共前缀 + 低位全 1 | 递增（只置 1） |
| **XOR** | `0` | 前缀 XOR 周期公式 | 两个方向 |

**不存在通用公式。** LC-0201 学的是 AND，**不要迁移到 OR / XOR**。

---

## 十、Bitwise Subarray（子数组位聚合）

**决定性观察**：以固定右端点结尾的子数组，**不同的 OR 值最多 O(32) 个**
（OR 单调递增 + 每次变大至少新增一位 + 只有 32 位）。

```python
cur = set()
for x in nums:
    cur = {y | x for y in cur} | {x}      # ! |cur| <= 33，不会爆
    ans |= cur
```
**O(32n)** 而非 O(n²)。📍 LC-0898

**同一个论证适用于**：子数组 **AND**、子数组 **GCD**（O(log V) 个状态）。
❌ **不适用于**子数组和（既不幂等也不有界）。

**最大 AND = `max(nums)`**（AND 只会变小，而单元素子数组可达）
⟹ LC-2419 **退化成「最大值的最长连续段」**，连位运算都不需要了。

---

## 十一、⚠️ Python 固定宽度问题（本专题最重要的一节）

### 整数是**任意精度**的，负数是**无限位补码**

```
-1  ==  ...111111111111      （概念上无限多个 1）
```

**后果**：`(a & b) << 1` 这类**左移**操作在负数上让高位无限生长
⟹ **循环永不终止**。

**实测**：LC-0371 的无 MASK 版本在 `getSum(-1, 1)` 上
`a, b` 依次变成 `(-2,2) → (-4,4) → (-8,16) → …` **永不收敛**。
该题的 `solution.py` 保留了 `Solution_4_BROKEN` 并用测试**实际证明**了这一点。

### 解法：手动模拟 32 位

```python
MASK, MAX_INT = 0xFFFFFFFF, 0x7FFFFFFF
value &= MASK                                           # ! 每轮截断
return value if value <= MAX_INT else ~(value ^ MASK)   # ! 还原符号
```

### 哪些操作需要 MASK

| 操作 | 安全吗 | 为什么 |
|---|---|---|
| `x & (x - 1)`、`x & (-x)` | ✅ `x > 0` 时安全 | 只清位，不生长 |
| `a ^ b`（不左移） | ✅ 安全 | 不生长 |
| **`(a & b) << 1` 并迭代** | ❌ **危险** | 左移让高位无限生长 |
| **逐位扫描负数** | ❌ **危险** | 无限多个符号位 |
| `bin(x).count('1')` 对负数 | ❌ **错** | `bin(-5) == '-0b101'`，不是补码 |
| `>>` 对负数 | ⚠️ **算术右移**（符号延伸） | `-8 >> 1 == -4` |

> **判断标准：有没有 `<<`？有没有「扫完所有位」的循环？**
> 有 ⟹ 先 `& MASK`。

### C++ / Java 的对称陷阱

`-2^31` 时 `-n` / `abs(n)` **会溢出**（`2^31` 放不进 int）。
**Python 不受影响**，但面试写 C++ 要主动提。

> **C++：溢出会悄悄发生，所以要提前预判。
> Python：溢出不会发生，所以要事后判断。
> 两种语言都要写检查，但原因正好相反。**

---

## 十二、跨专题索引

| 题 | 实体位置 | Primary Pattern | Secondary Pattern | Recommended Algorithm |
|---|---|---|---|---|
| **LC-0421** Maximum XOR of Two Numbers | [`08-tries`](<../08-tries (字典树、前缀树)/05 - 进阶变体与跨专题存档/01 - Bitwise Trie 与最大 XOR/01 - LC-0421 - Maximum XOR of Two Numbers in an Array>) | **Binary Trie** | XOR 自逆性、高位贪心 | 二进制 Trie 走「相反的那一边」/ 逐位 Hash Set |
| **LC-0078** Subsets | [`10-backtracking`](<../10-backtracking (回溯)/01 - 子集、组合与目标和 (Subsets and Combinations)/01 - 子集枚举与重复元素去重/01 - LC-0078 - Subsets>) | **Backtracking** | **Bitmask Enumeration** | 回溯（可剪枝、可扩展到重复元素）/ `for mask in range(1<<n)` |
| **LC-0289** Game of Life | [`15-math-geometry`](<../15-math-geometry (数学、几何)/02 - 矩阵变换与状态模拟 (Matrix Transformation)/02 - 原地标记与同步状态更新/02 - LC-0289 - Game of Life>) | Simultaneous State Update | **位编码（bit 0 旧 / bit 1 新）** | 和本专题 LC-1470/1920 的原地编码**同构** |
| **LC-0050** Pow(x, n) | [`15-math-geometry`](<../15-math-geometry (数学、几何)/03 - 整数运算与数位处理 (Arithmetic)/03 - Fast Exponentiation 平方快速幂/01 - LC-0050 - Pow(x, n)>) | Fast Exponentiation | **按指数的二进制位** | `while n: if n&1: res*=base; base*=base; n>>=1` |

**跨专题规则**（本次执行遵循）：
1. 本专题已有原始资料 ⟹ **完整保留**。
2. 其他专题已有 ⟹ **只建 README 引用**，不重复生成、不复制 PDF。
3. **不修改其他专题的任何文件。**
4. 一道题只能有一个实体文件夹（否则 `review_due.py` 重复叫号）。
5. **不以 LeetCode 标签作为唯一分类依据**（LC-0078 标了 Bitmask，但主归属是回溯）。

---

## 十三、第二轮独立审核结果

**第一轮（指令给定）新增 2 道**：LC-0371、LC-0201 —— 仓库里都没有，**全部新建**。

**第二轮自主新增 2 道**（上限 2，用满）：

| 题 | 填补的缺口（C） | 独立可迁移的 Pattern（B） | 为什么不重复（D） |
|---|---|---|---|
| **LC-0260** Single Number III | 「**2 个**异常元素」—— 原有题只覆盖 1 个 | **用一个位把数组劈成两半**（迁移到按位分治、Trie 分叉） | LC-0136/0268 一次 XOR 就出答案；本题**必须再分组** |
| **LC-0318** Maximum Product of Word Lengths | **Bitmask 当集合用** —— 本专题原本一道都没有 | `a & b == 0` 判集合相交；是**所有状压 DP 的基础** | 原有「编码」题（LC-1470/1920）是**算术编码**，和集合编码完全不同 |

**未新增的候选及原因**：

| 题 | 违反条件 | 原因 |
|---|---|---|
| LC-0461 Hamming Distance / LC-2220 Min Bit Flips | **D** | 都是 `popcount(a ^ b)`，与 LC-0136 + LC-0191 高度重复（指令也这么说） |
| LC-0137 Single Number II | **D, E** | 「单一元素」家族的第三道，重复训练；且有限状态位公式属于**记忆负担**（指令明确提醒不要机械记忆）。「逐位计数 mod 3」的思路已写进 LC-0260 的对照表 |
| LC-1318 Min Flips to Make a OR b Equal to c | **D** | 逐位真值表，技巧已被 LC-0371 的半加器真值表覆盖 |
| LC-0078 Subsets | **F** | **已在 `10-backtracking`** ⟹ 只建索引（指令明确「不必重复生成」） |
| LC-0421 Maximum XOR | **F** | **已在 `08-tries`** ⟹ 只建索引（审核清单第 17 项就是要建这个索引） |
| Gray Code 全套变体 | **F** | 构造公式死记硬背，迁移性极低；指令明确不扩充 |
| Advanced Bitmask DP | **E, F** | 属于 DP 专题高阶内容；指令明确不扩充 |
| SOS DP（Sum over Subsets） | **E, F** | 竞赛范畴；指令明确不扩充 |

判断标准（指令第六节 A–F）：
A 经典面试价值 · B 独立可迁移的 Pattern · C 现有题确实没覆盖 ·
D 不是已有题的简单重复 · E 学习成本合理 · F 不把本专题扩成竞赛题库。

参考：NeetCode 150/250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Bit Manipulation 分区。**未编造任何公司的实际出题频次。**

---

## 十四、不建议长期记忆的特殊技巧

| 技巧 | 为什么不建议 |
|---|---|
| **NAF（非相邻形式）的最优性证明** | LC-2571 用得到，但属数论构造；说得出「连续 1 用加法」的直觉就够 |
| **LC-0137 的 `ones/twos` 位状态公式** | 纯记忆负担；「逐位计数 mod 3」才是可理解的版本 |
| **Gray Code 的构造公式** | `g = i ^ (i >> 1)` 好记，但变体全靠背 |
| **用乘法 / 魔数算 popcount** | 现代 CPU 有 `POPCNT`，Python 有 `bit_count()` |
| **各种 bit hack**（如无分支取 min/max） | 编译器已经做得更好，可读性反而更差 |
| **SOS DP / 高维前缀和** | 竞赛范畴，面试不考 |

> **本专题要的是十来个恒等式和三条 Python 注意事项，不是一本 bit hack 大全。**

---

## 十五、最终推荐刷题路线

```
【第一遍 · 6 道】核心恒等式（P0）
  0191 → 0231 → 0338 → 0136 → 0268 → 0371

【第二遍 · 13 道】标准面试覆盖面（P0 + P1）
  0191 → 0231 → 0338 → 0190
       → 0136 → 0268 → 0260 → 0371 → 0201
       → 0898 → 0318 → 0421 → 0078

【第三遍 · 21 道】按 Level 1 顺序
  L1 → 0191 0231 0338 0190
  L2 → 0136 0268 0260 0371 0201
  L3 → 0898 2411 2419
  L4 → 2438 1470 1920 0318
  L5 → 1356 2571 0194 0421 0078
```

**配对练习**（一次打穿各自的坑）：

| 配对 | 对照的是什么 |
|---|---|
| `0191` → `0231` | 同一个 `x & (x-1)`，两种用法 |
| `0136` → `0260` | 1 个异常（一次 XOR） vs **2 个异常（XOR + 分组）** |
| `0191` → `0260` | `x & (x-1)` **清**最低位 1 vs `x & (-x)` **留**最低位 1 |
| `0371` → `0201` | XOR 的**算术含义** vs AND 的**单调性** |
| `0201` → `2419` | 值域区间的 AND vs **数组子区间**的 AND（**毫无关系**） |
| `0898` → `2419` | OR 要维护 O(32) 状态 vs AND **退化成扫描** |
| `1470` → `0318` | **算术编码**（两个数值） vs **Bitmask 集合**（一个集合） |
| `0190` → `0191` | **固定宽度**（前导零有效） vs 任意宽度 |

---

## 相关资料

| 文档 | 内容 |
|---|---|
| [位运算恒等式速查表](<./_resources/bit-tricks-cheat-sheet.md>) | 全部恒等式 + XOR 四性质 + 区间聚合 + **Python 陷阱** + 必测边界 |
| [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>) | Q1–Q16 决策树 + 三秒速判表 + 读题三问 |
| [_audit/post-migration-report.md](<./_audit/post-migration-report.md>) | 迁移映射、SHA-256 校验、NC 正式化、跨专题去重结果 |
