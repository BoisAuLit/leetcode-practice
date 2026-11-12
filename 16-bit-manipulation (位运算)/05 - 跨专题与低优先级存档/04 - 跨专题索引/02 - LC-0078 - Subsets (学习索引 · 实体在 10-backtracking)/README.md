# LC-0078 - Subsets（学习索引）

> ⚠️ **这里没有 `solution.py` / `metadata.json` / PDF，只有这份索引。**
> 本仓库铁律：**一道题只能有一个实体文件夹**，否则复习队列会重复叫号。

**👉 实体位置：**
[10-backtracking (回溯)/01 - 子集、组合与目标和 (Subsets and Combinations)/01 - 子集枚举与重复元素去重/01 - LC-0078 - Subsets](<../../../../10-backtracking (回溯)/01 - 子集、组合与目标和 (Subsets and Combinations)/01 - 子集枚举与重复元素去重/01 - LC-0078 - Subsets>)

| 字段 | 值 |
|---|---|
| **Primary Pattern** | **Backtracking（回溯）** —— 这是它归在 `10-backtracking` 的理由 |
| **Secondary Patterns** | **Bitmask Enumeration（位掩码枚举）**、Iterative Doubling |
| **Recommended Algorithm** | 回溯（选 / 不选），可扩展到有重复元素、有剪枝的变体 |
| **Alternative Algorithm** | **Bitmask 枚举 `0 .. 2^n - 1`** —— 本专题关心的就是这个 |
| **Cross-topic Reference** | 本专题 Level 1 · 05 / Level 2 · 04 |

---

## 为什么它在本专题里占一个位置

指令明确说：
> 「LC-78 已经在 Backtracking 专题中存在。
>  可以介绍 Bitmask Enumeration，但不必重复生成题目。」

所以这里**只讲位运算的那一面**：**如何用整数枚举一个集合的所有子集**。

---

## Bitmask 枚举：`2^n` 个整数 ↔ `2^n` 个子集

```python
def subsets(nums):
    n = len(nums)
    res = []
    for mask in range(1 << n):                 # ! 0 .. 2^n - 1，一共 2^n 个
        subset = [nums[i] for i in range(n) if mask >> i & 1]
        res.append(subset)
    return res
```

**为什么这是一个双射？**
长度 `n` 的子集可以唯一表示为一个 `n` 位的「选 / 不选」向量，
而 `n` 位二进制整数恰好有 `2^n` 个，两者一一对应。
`mask >> i & 1 == 1` 读作「第 `i` 个元素被选中」。∎

**优点**：
- **没有递归**，没有栈深度问题
- 枚举顺序天然有序（按 mask 从小到大）
- 配合 `bin(mask).count('1')` 可以**按子集大小分组**

**缺点**：
- `n` 必须 `<= 20` 左右（`2^20 ≈ 100 万`）
- **无法剪枝** —— 回溯能在中途放弃整棵子树，位枚举必须跑完所有 `2^n`
- 处理「有重复元素要去重」（LC-0090）时不如回溯自然

> **这就是为什么它的 Primary Pattern 是 Backtracking 而不是 Bitmask**：
> 位枚举只适用于「无剪枝、`n` 很小」的情况；
> 回溯才是能推广到整个子集 / 组合家族的那套方法。

---

## 三个常用的子集位技巧

### ① 枚举某个 mask 的**所有子集**（子集的子集）

```python
sub = mask
while True:
    ...                      # ! 处理 sub
    if sub == 0: break
    sub = (sub - 1) & mask   # ! 下一个子集
```
**为什么 `(sub - 1) & mask` 能枚举所有子集？**
`sub - 1` 把 `sub` 最低位的 1 变 0、其右边全变 1；
再 `& mask` 把不属于 `mask` 的位清掉
⟹ 恰好得到「字典序上一个」子集。
总复杂度是 **O(3^n)**（枚举所有 (mask, submask) 对），这是状压 DP 的常用骨架。

### ② 枚举所有**大小为 k** 的子集

```python
for mask in range(1 << n):
    if bin(mask).count('1') == k:
        ...
```

### ③ 一些恒等式

| 表达式 | 作用 |
|---|---|
| `mask & (mask - 1)` | 清掉最低位的 1 |
| `mask & (-mask)` | 只保留最低位的 1 |
| `mask \| (1 << i)` | 加入元素 `i` |
| `mask & ~(1 << i)` | 移除元素 `i` |
| `mask ^ (1 << i)` | 翻转元素 `i` |
| `mask >> i & 1` | 元素 `i` 在不在 |
| `(1 << n) - 1` | 全集 |
| `full ^ mask` | 补集 |

---

## 和本专题的血缘

[LC-0318 Maximum Product of Word Lengths](<../../../04 - 二进制分解与原地编码/03 - Bitmask 表示集合/01 - LC-0318 - Maximum Product of Word Lengths>)
用的是同一个思想 —— **一个 int 就是一个集合**。
区别是：
- LC-0078：枚举**全部** `2^n` 个子集
- LC-0318：只用 mask 做**集合相交判定**（`m1 & m2 == 0`），不枚举

> 按指令要求，本专题**不扩充** Advanced Bitmask DP 和 SOS DP。
> 这两道题把「Bitmask 当集合」的概念打通就够了。
