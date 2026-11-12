# Level 1 · 07 跨专题与低优先级存档

## 用途
保留已有题目，但**不把所有带 Heap 标签的题都列入主线**。本章全部 **P2**。
所有文件在本次重构中**未作任何修改**，只是换了位置。

## 01 - 简单排序或计数可替代的问题

### LC-1337 The K Weakest Rows in a Matrix（P2）

**能用堆，但没必要。**

最直接的解法：对每一行算出士兵数量（行是有序的，可以**二分**找第一个 0 的位置，
O(log n) 而不是 O(n)），然后按 `(soldier_count, row_index)` 排序取前 k 个。

```python
rows = sorted((bisect_right(row, 1, key=...) , i) for i, row in enumerate(mat))
return [i for _, i in rows[:k]]
```

元组 `(count, index)` 天然满足题目的平局规则（数量相同时行号小的在前）。

用堆当然也行（O(m log k)），但**它不引入任何新的 Heap Pattern** ——
只是 Level 1 `01` Top-K 模板的又一次应用。所以标 P2。

**它的真正价值**：提醒你「每行有序 ⟹ 数 1 的个数可以二分」。

## 02 - Ordered Set 与相邻元素查询

### LC-2817 Minimum Absolute Difference Between Elements With Constraint（P2）

> **这道题放在存档区，是因为它根本不是堆题。**

题目要在一个**动态维护的候选集合**里，找「最接近当前元素的数值」。
这需要 **Predecessor / Successor 查询**（前驱 / 后继）。

**为什么堆做不到**：
堆只能 O(1) 告诉你**全局最小或最大**。
要找「最接近 x 的元素」，堆必须**遍历全部元素** O(n) ——
它的内部结构（只保证父子关系，不保证兄弟有序）根本不支持按值定位。

**正确的工具**：
| 工具 | 复杂度 | 说明 |
|---|---|---|
| **Ordered Set / 平衡 BST** | O(log n) 插入 + O(log n) 前驱后继 | C++ 的 `std::set`、Java 的 `TreeSet` |
| **SortedList**（`sortedcontainers`） | 同上 | Python 第三方库，面试要说明依赖 |
| **有序列表 + `bisect`** | 查询 O(log n)，**插入 O(n)** | 标准库能做，但插入是线性 |

本题的做法：随着右端点右移，把 `nums[i - x]`（满足下标距离约束的元素）
插入有序结构，然后二分找最接近 `nums[i]` 的前驱和后继，更新答案。

**这是堆的能力边界的最好例子** —— 值得专门记住这张表：

| 需求 | 堆 | 该用什么 |
|---|---|---|
| 全局最小 / 最大 | ✅ | 堆 |
| 任意元素是否存在 | ❌ | Hash Set |
| **最接近 x 的元素 / 前驱后继** | ❌ | **Ordered Set / SortedList** |
| 区间查询 / 区间更新 | ❌ | 线段树 / 树状数组 |
| 删除任意元素 | ❌（只能惰性） | Lazy Deletion |

已有的 JPEG 图解、代码和全部题目资料**原样保留**。

## 为什么这两道不进主线

| 题 | 原因 |
|---|---|
| LC-1337 | 能用堆，但只是 Top-K 模板的重复；排序 + 二分更简单 |
| LC-2817 | **不是堆能解决的问题**，主工具是 Ordered Set |
