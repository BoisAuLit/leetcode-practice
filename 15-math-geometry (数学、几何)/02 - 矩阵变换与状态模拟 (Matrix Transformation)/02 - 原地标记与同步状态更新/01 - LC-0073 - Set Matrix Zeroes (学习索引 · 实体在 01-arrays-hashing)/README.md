# LC-0073 - Set Matrix Zeroes（学习索引）

> ⚠️ **这里没有 `solution.py` / `metadata.json` / PDF，只有这份索引。**
> 本仓库铁律：**一道题只能有一个实体文件夹**，否则复习队列会重复叫号。
> LC-0073 的实体在 `01-arrays-hashing`（它更早入库，并且带有 `note.md`）：

**👉 实体位置：**
[01-arrays-hashing (数组、哈希表)/04 - Array Index Mapping 与 In-place Marking/05 - LC-0073 - Set Matrix Zeroes](<../../../../01-arrays-hashing (数组、哈希表)/04 - Array Index Mapping 与 In-place Marking/05 - LC-0073 - Set Matrix Zeroes>)

| 字段 | 值 |
|---|---|
| **Primary Pattern** | In-place Marking（原地标记）—— 这是它归在 `01-arrays-hashing` 的理由 |
| **Secondary Patterns** | Simultaneous State Update（同步状态更新）、Matrix Traversal |
| **Recommended Algorithm** | 用第一行 / 第一列当标记位，O(1) 额外空间 |
| **Alternative Algorithm** | Row Set + Column Set，O(m+n) 额外空间 |
| **Cross-topic Reference** | 本专题 Level 1 · 02 / Level 2 · 02（与 LC-0289 配对） |

---

## 为什么它在本专题里占一个位置

LC-0073 和 [LC-0289 Game of Life](<../02 - LC-0289 - Game of Life>) 是
**同一个模式的两道题**：

```
Read Original State  →  Record Updates  →  Apply Updates
```

**两阶段**是本质。不把 LC-0073 列出来，本 Level 2 就只剩一道题，
「同步状态更新」这个 Pattern 的对照就立不起来。

---

## 核心：为什么必须两阶段

题意：若 `matrix[i][j] == 0`，把**整行和整列**都置 0。

**不能在第一次发现 0 时就立刻清零整行整列** ——
新写进去的 0 会被后面的扫描当成「原始的 0」，继续扩散
⟹ **最后整个矩阵全是 0**。

**反例**：
```
1 0        正确答案：0 0        边扫边清：0 0
1 1                  1 0                  0 0   ❌
```
扫到 `(0,1)` 的 0 ⟹ 清第 0 行和第 1 列 ⟹ `(1,1)` 变成 0
⟹ 继续扫到 `(1,1)` 的 0 ⟹ 又清第 1 行 ⟹ `(1,0)` 也没了。

所以必须**先把「哪些行、哪些列需要清零」全部记下来，再统一执行**。
这就是 **Original State vs Final State** 的区分。

---

## 解法 A：Row Set + Column Set（O(m+n) 空间）

```python
rows = {i for i in range(m) for j in range(n) if matrix[i][j] == 0}
cols = {j for i in range(m) for j in range(n) if matrix[i][j] == 0}
for i in range(m):
    for j in range(n):
        if i in rows or j in cols:
            matrix[i][j] = 0
```
最容易理解，面试先写它证明思路正确。

---

## 解法 B：第一行 / 第一列当标记位（O(1) 额外空间）

**核心想法**：既然「第 `i` 行要清零」这个信息本来就要存，
那就存在 `matrix[i][0]`（第一列）里；「第 `j` 列要清零」存在 `matrix[0][j]`（第一行）里。

**为什么第一行和第一列有特殊性？**
它们是**唯一一组「既能当标记位、又恰好能覆盖所有行列」**的格子：
每一行都有一个第一列的格子，每一列都有一个第一行的格子。

**`matrix[0][0]` 的冲突怎么办？**
`matrix[0][0]` 同时是「第 0 行的标记」和「第 0 列的标记」——
**一个格子存不下两个 bit**。所以要**额外一个变量**：

```python
first_col_zero = any(matrix[i][0] == 0 for i in range(m))   # ! 第 0 列单独记
# 之后 matrix[0][0] 专门表示「第 0 行要不要清零」
```

**为什么写入顺序影响正确性？**
必须**从右下往左上**回填（或者：先处理第 1..m-1 行、第 1..n-1 列，
最后才处理第 0 行和第 0 列）。
因为第一行 / 第一列**同时是标记区和数据区** ——
如果先把第 0 行清零了，存在那里的「列标记」就全丢了，
后面的列再也不知道自己该不该清零。

**如何避免污染尚未读取的原始标记？**
三条规矩：
1. **先**整体扫一遍，把标记写进第一行 / 第一列（这一步只写标记，不清数据）。
2. **再**回填内部区域 `i >= 1, j >= 1`（读标记，不改标记）。
3. **最后**才根据 `matrix[0][0]` 和 `first_col_zero` 清第 0 行和第 0 列。

> **顺序是解法 B 的全部难点。** 想通「标记区和数据区重叠」这一点，代码就自然了。

**复杂度**：**O(m·n)** 时间、**O(1)** 额外空间（只有一个 `first_col_zero` 变量）。

---

## 与本 Level 2 另一题的对照

| | **LC-0073** Set Matrix Zeroes | [LC-0289](<../02 - LC-0289 - Game of Life>) Game of Life |
|---|---|---|
| 新状态依赖 | **整行 / 整列**是否有 0 | **周围 8 格**的旧状态 |
| 标记存哪 | 第一行 / 第一列（**和数据区重叠**） | 每个格子的**高位 bit**（和数据区**不**重叠） |
| 难点 | **写入顺序** | **读旧位 `x & 1`** |
| 第二遍做什么 | 根据标记清零 | 统一 `>>= 1` 兑现新状态 |
| O(1) 空间的代价 | 要额外一个 `first_col_zero` 变量 | 无额外变量（位是免费的） |

> **LC-0289 的位编码更干净**，因为标记和数据分住在不同的 bit 上，
> 天然不会互相污染。**LC-0073 的标记挤占了数据位**，所以必须靠顺序来保证正确。
> 两题一起看，就能明白「原地算法」的真正难点是**什么时候能安全覆盖**。

---

## 边界

- 第一行就有 0（标记区本身被污染）
- 第一列就有 0（`first_col_zero` 的用处）
- `matrix[0][0] == 0`（行列标记冲突）
- 全是 0 / 一个 0 都没有
- 单行 `1×n` / 单列 `n×1`
- `1×1` 矩阵
