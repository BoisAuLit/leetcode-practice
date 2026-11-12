# Level 1 · 05 — 跨专题与低优先级存档（Cross-topic & Low-priority Archive）

> **本层的目的：保留全部原有学习成果，同时明确区分
> 「真正的位运算核心算法」和「非典型 / 低迁移性题目」。**
>
> 放在这里**不代表题目没价值** —— 只代表它**不该占用核心复习预算**。
> 分成四类：Popcount 的应用、特殊贪心、**根本不是位运算的题**、跨专题索引。

---

## 为什么要有这一层

Bit Manipulation 的题目质量差异极大：

| 类型 | 该花多少精力 | 例子 |
|---|---|---|
| **核心恒等式 + 不变量** | 反复练到肌肉记忆 | LC-0136、LC-0191、LC-0371 |
| **某个恒等式的轻度应用** | 看懂一次就够 | LC-1356（Popcount 当排序 key） |
| **需要特殊构造 / 冷门贪心** | 知道存在即可 | LC-2571 |
| **压根不是位运算题** | 归档，别当位运算练 | LC-0194（Shell 文本处理） |
| **主归属在别的专题** | 只建索引，不重复生成 | LC-0421（Trie）、LC-0078（回溯） |

**把它们混在核心题里练，会稀释真正重要的那十来道题。**

---

## Level 2 · 01 — Popcount + Sorting

### [LC-1356 Sort Integers by The Number of 1 Bits](<./01 - Popcount + Sorting/01 - LC-1356 - Sort Integers by The Number of 1 Bits>)

**决定性观察**：这是一道**排序题**，位运算只负责提供排序 key。

```python
return sorted(arr, key=lambda x: (x.bit_count(), x))      # ! Python 3.10+
return sorted(arr, key=lambda x: (bin(x).count('1'), x))  # ! 通用写法
```

**核心不变量**：排序是**稳定**的，但题目要求「popcount 相同时按数值升序」
⟹ 必须把 `x` 本身写进 key 的第二项（**不能依赖稳定性**，因为输入未必已排序）。

**为什么用 Popcount**：唯一的位运算成分就是 `bin(x).count('1')`
—— 技巧全部来自 [Level 1 · 01](<../01 - 二进制基础、位计数与位反转>)。

**复杂度**：**O(n log n · 32)** 时间（排序时每次比较要算 popcount）
—— 可以预计算 key 降到 **O(32n + n log n)**。O(n) 空间。

**典型反例**：
- 只写 `key=lambda x: bin(x).count('1')` ⟹ popcount 相同的组内顺序不确定 ❌
- 以为 Python 的 `sorted` 稳定就够 ⟹ 输入乱序时错 ❌

**优先级 P2** —— 技巧已被 LC-0191 覆盖，本题只是一次应用。

---

## Level 2 · 02 — 特殊二进制贪心与有符号幂分解

### [LC-2571 Minimum Operations to Reduce an Integer to 0](<./02 - 特殊二进制贪心与有符号幂分解/01 - LC-2571 - Minimum Operations to Reduce an Integer to 0>)

**决定性观察**：每次操作可以**加或减**任意 `2^i` ⟹ 求把 `n` 变成 0 的最少次数
= 把 `n` 表示成 `±2^i` 之和的**最少项数**（Non-Adjacent Form, NAF）。

**核心不变量（贪心版）**：从最低位开始，
- 当前位是 0 ⟹ 右移
- 当前位是 1 ⟹ 看**下一位**：
  - 下一位是 0 ⟹ **减** `2^i`（`n -= lowbit`），一次操作
  - 下一位是 1 ⟹ **加** `2^i`（`n += lowbit`），把连续的 1 串「进位」成一个更高的 1

**为什么「连续的 1 要加不要减」**：`0b0111 = 7`。
逐个减要 3 次（`-1, -2, -4`）；而 `+1` 变成 `0b1000`，再 `-8` ⟹ **2 次**。
**连续 1 的串越长，加法越划算。**

**正确性**：这就是 NAF（非相邻形式）的构造 ——
NAF 表示的非零项数是所有 `±2^i` 表示中**最少**的，且唯一。
（证明需要 NAF 的最优性定理，属于**数论构造**，不建议死记。）

**Python 模板**：
```python
def minOperations(n):
    cnt = 0
    while n:
        if n & 1 == 0:
            n >>= 1                       # ! 偶数直接右移
        elif n & 3 == 3:                  # ! 末两位是 11 ⟹ 加法更划算
            n += 1; cnt += 1
        else:                             # ! 末两位是 01 ⟹ 减法
            n -= 1; cnt += 1
    return cnt
```
**O(log n)** 时间、O(1) 空间。

**典型反例**：
- 直接返回 `popcount(n)` ⟹ `n = 7` 得 3，正确是 2 ❌
- 一律用减法 ⟹ 遇到连续 1 串就不优 ❌

**优先级 P2** —— 需要 NAF 这个**特殊构造**，迁移性有限。
> **这正是不建议长期记忆的那类技巧**：
> 面试里能把「连续 1 用加法」的直觉说出来就够，不必背 NAF 的最优性证明。

---

## Level 2 · 03 — 非位运算题目与 Shell 文本处理

### [LC-0194 Transpose File](<./03 - 非位运算题目与 Shell 文本处理/01 - LC-0194 - Transpose File>)

**⚠️ 这道题和位运算毫无关系。** 它是一道 **Shell / 文本处理**题
（用 `awk` 把文件按空格转置），被归到这里纯粹是历史原因
（原目录结构把它放在 `bit-basics` 下）。

**保留它的理由**：原有学习成果**必须完整保留**，
但不该让它混进位运算的核心复习序列。

**它真正属于哪里**：Shell / Database 这类「非算法」专题。
若将来建立该专题，应整体迁出。

**优先级 P2（存档）** —— 不要把它当位运算题练。

---

## Level 2 · 04 — 跨专题索引

这两道题的**主归属在其他专题**，按指令要求
「**已在其他专题 ⟹ 仅建立跨专题索引，不重复生成**」：

| 题 | 实体位置 | Primary Pattern | 本专题关心的那一面 |
|---|---|---|---|
| [LC-0421 Maximum XOR of Two Numbers](<./04 - 跨专题索引/01 - LC-0421 - Maximum XOR of Two Numbers in an Array (学习索引 · 实体在 08-tries)>) | `08-tries` | **Binary Trie** | XOR 的**自逆性** + 高位优先贪心 |
| [LC-0078 Subsets](<./04 - 跨专题索引/02 - LC-0078 - Subsets (学习索引 · 实体在 10-backtracking)>) | `10-backtracking` | **Backtracking** | **Bitmask Enumeration** |

**为什么不在本专题建实体？**
一道题在仓库里**只能有一个实体文件夹** —— 否则 `review_due.py` 会重复叫号。
而 Trie 和回溯分别是这两道题更合适的主归属
（LC-0421 的标准解法是二进制 Trie；LC-0078 的位枚举版**无法剪枝**，
推广到整个子集家族要靠回溯）。

两份索引里都写了**完整的位运算视角讲解** —— 点进去看。

---

## 本层的核心不变量（如果一定要概括）

> **这一层没有统一的算法不变量 —— 它的「不变量」是分类标准本身：**
> 一道题属于这里，当且仅当
> **①它的核心技巧已被前四层覆盖**，
> 或**②它需要冷门构造 / 根本不是位运算**，
> 或**③它在别的专题有更合适的主归属**。

---

## 代表题目与优先级

| # | 题 | 优先级 | 为什么在这一层 |
|---|---|---|---|
| 1 | [LC-1356 Sort Integers by The Number of 1 Bits](<./01 - Popcount + Sorting/01 - LC-1356 - Sort Integers by The Number of 1 Bits>) | P2 | Popcount 的轻度应用，技巧已被 LC-0191 覆盖 |
| 2 | [LC-2571 Minimum Operations to Reduce an Integer to 0](<./02 - 特殊二进制贪心与有符号幂分解/01 - LC-2571 - Minimum Operations to Reduce an Integer to 0>) | P2 | 需要 NAF 特殊构造，迁移性有限 |
| 3 | [LC-0194 Transpose File](<./03 - 非位运算题目与 Shell 文本处理/01 - LC-0194 - Transpose File>) | P2（存档） | **根本不是位运算题** |
| 4 | [LC-0421 Maximum XOR of Two Numbers](<./04 - 跨专题索引/01 - LC-0421 - Maximum XOR of Two Numbers in an Array (学习索引 · 实体在 08-tries)>) ↗️ | P1 | 主归属 `08-tries`（Binary Trie） |
| 5 | [LC-0078 Subsets](<./04 - 跨专题索引/02 - LC-0078 - Subsets (学习索引 · 实体在 10-backtracking)>) ↗️ | P1 | 主归属 `10-backtracking` |

↗️ = 只有 README，无 `solution.py` / `metadata.json`
⟹ **不进复习队列**（`review_due.py` 要求同时有 metadata 和匹配的文件夹名）。

---

## 容易混淆的 Pattern

### 「用到了位运算」≠「是位运算题」

| 题 | 用到的位运算 | 真正的考点 |
|---|---|---|
| LC-1356 | `bin(x).count('1')` | **排序的多级 key** |
| LC-2419（Level 03） | AND 的单调性 | **最大值的最长连续段** |
| LC-0078 | `mask >> i & 1` | **子集枚举 / 回溯** |
| LC-0194 | **无** | Shell 文本处理 |

> **判断标准：把位运算换成别的实现，题目还难不难？**
> 不难了 ⟹ 它不是位运算题，位运算只是工具。

### 不建议长期记忆的特殊技巧

按指令要求，本专题**不扩充**下列方向，也不建议花时间背：

| 技巧 | 为什么不建议 |
|---|---|
| **NAF（非相邻形式）的最优性证明** | LC-2571 用得到，但属于数论构造，面试说得出直觉就够 |
| **Gray Code 全套变体** | 构造公式死记硬背，迁移性极低 |
| **Advanced Bitmask DP / 状压 DP** | 属于 DP 专题的高阶内容，不是位运算本身 |
| **SOS DP（Sum over Subsets）** | 竞赛范畴 |
| **LC-0137 的有限状态位运算公式** | 「逐位计数 mod 3」是可理解的；那套 `ones/twos` 位状态公式纯属记忆负担 |
| 各种 bit hack（如用乘法算 popcount） | 现代 CPU 有 `POPCNT` 指令，Python 有 `bit_count()` |

---

## 相关资料

- [位运算恒等式速查表](<../_resources/bit-tricks-cheat-sheet.md>)
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q14 / Q15 + 「本专题刻意不做的」
