# LC-0421 - Maximum XOR of Two Numbers in an Array（学习索引）

> ⚠️ **这里没有 `solution.py` / `metadata.json` / PDF，只有这份索引。**
> 本仓库铁律：**一道题只能有一个实体文件夹**，否则复习队列会重复叫号。

**👉 实体位置：**
[08-tries (字典树、前缀树)/05 - 进阶变体与跨专题存档/01 - Bitwise Trie 与最大 XOR/01 - LC-0421 - Maximum XOR of Two Numbers in an Array](<../../../../08-tries (字典树、前缀树)/05 - 进阶变体与跨专题存档/01 - Bitwise Trie 与最大 XOR/01 - LC-0421 - Maximum XOR of Two Numbers in an Array>)

| 字段 | 值 |
|---|---|
| **Primary Pattern** | **Binary Trie（二进制字典树）** —— 这是它归在 `08-tries` 的理由 |
| **Secondary Patterns** | XOR 性质、Bit-by-bit Greedy、Prefix Hash Set |
| **Recommended Algorithm** | 二进制 Trie，从最高位往下贪心走「相反的那一边」 |
| **Alternative Algorithm** | 逐位前缀 + Hash Set（代码更短，思想相同） |
| **Cross-topic Reference** | 本专题 Level 1 · 05 / Level 2 · 04 |

---

## 为什么它在本专题里占一个位置

它是**本仓库里唯一一道「XOR + 逐位贪心」的题**，
也是审核清单第 17 项「**Binary Trie Cross-reference**」点名要建索引的题。
按指令要求：**已在 Trie 专题 ⟹ 仅建立跨专题索引，不重复生成。**

---

## 核心：为什么能逐位贪心（从最高位开始）

要最大化 `a ^ b`，就要让**尽可能高的位**变成 1。

**关键性质**：二进制数的大小由**最高的不同位**决定。
所以哪怕低 30 位全是 0，只要第 31 位是 1，就比「第 31 位是 0 但低位全 1」的数大。
⟹ **高位优先，一旦某个高位能取到 1，就绝不为了低位而放弃它。**

```python
mask = 0
best = 0
for i in range(31, -1, -1):           # ! 从最高位往下
    mask |= 1 << i                     # ! 只看前缀的高 (32-i) 位
    prefixes = {x & mask for x in nums}
    candidate = best | (1 << i)        # ! 「这一位也能是 1」的假设
    # ! a ^ b == candidate  ⟺  a == candidate ^ b
    if any(candidate ^ p in prefixes for p in prefixes):
        best = candidate               # ! 假设成立 ⟹ 锁定这一位
return best
```

**为什么 `a ^ b == c` ⟺ `a == c ^ b`？**
XOR 的自逆性：`a ^ b ^ b == a`。两边同时 XOR `b` 即得。∎
这让「存在两个前缀 XOR 出 candidate」变成一次 Hash Set 查询。

**O(32n)** 时间、O(n) 空间。

---

## 二进制 Trie 版本（`08-tries` 的主解法）

把每个数的 32 位当成一个字符串插入 Trie（每层两个分叉：0 和 1）。
查询某个数 `x` 的最大 XOR 伙伴时，**从根开始每层都优先走「和 `x` 当前位相反」的那一边**
（走得通就走，因为那一位能贡献 1；走不通才退回同侧）。

**O(32n)** 时间、**O(32n)** 空间。

> **两种解法的思想完全相同** —— 都是「高位优先贪心」。
> Trie 把「能不能配出这一位」做成了显式的数据结构，
> Hash Set 版把它做成了一次集合查询。
> **面试写 Hash Set 版更快；但 Trie 版能推广到「带限制的最大 XOR」
> （如 LC-1707 Maximum XOR With an Element From Array，需要在 Trie 上附加 min 信息）。**

---

## 和本专题的血缘

| 本专题的题 | 用的 XOR 性质 |
|---|---|
| [LC-0136 Single Number](<../../../02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/01 - LC-0136 - Single Number>) | `x ^ x == 0`（**抵消性**） |
| [LC-0260 Single Number III](<../../../02 - XOR 不变量与二进制算术/01 - XOR 抵消与缺失元素/03 - LC-0260 - Single Number III>) | 抵消性 + **按位分组** |
| [LC-0371 Sum of Two Integers](<../../../02 - XOR 不变量与二进制算术/02 - XOR 与 AND 形成二进制加法/01 - LC-0371 - Sum of Two Integers>) | `a^b` = 无进位和（**算术含义**） |
| **LC-0421** | `a^b==c ⟺ a==c^b`（**自逆性**）+ 高位优先贪心 |

**四道题用的是 XOR 的四个不同性质。** 这是 XOR 值得反复练的原因。
