# Level 1 · 02 K-way Merge 与候选扩展

## 核心定义
有 k 个**各自有序**的来源，要按全局顺序取出元素（或取前 k 个）。
堆里**每一路只放一个候选**，弹一个就从同一路补一个。

## 决定性观察
1. **绝不能把所有候选一次性入堆**。
   LC-0373 的数对有 m×n 个（可达 10¹⁰），全入堆直接爆内存。
2. **堆的大小始终 = 路数 k**（或 min(k, 路数)）。
   这是 K-way Merge 和普通 Top-K 最大的区别：
   Top-K 的堆装「答案候选」，K-way Merge 的堆装「每一路的前沿」。
3. **正确性论证**（三道题通用）：
   堆里始终包含「所有已弹出元素的**直接后继**」。
   任何还没入堆的元素，它在自己那一路上的前驱要么还在堆里、要么已弹出且后继已入堆
   ⟹ **全局最小的未弹出元素一定在堆里** ⟹ 弹堆顶就是全局下一个。∎

## 通用骨架
```python
heap = [(每路的第一个值, 路编号 i, 路内下标 j) for 每一路]
heapq.heapify(heap)
while heap:
    val, i, j = heapq.heappop(heap)
    处理 val
    if 该路还有下一个:
        heapq.heappush(heap, (下一个值, i, j + 1))
```

## 三道题的差异（骨架相同，「一路」的定义不同）

| 题 | 「一路」是什么 | 每轮做什么 | 额外技巧 |
|---|---|---|---|
| **LC-0378** Kth Smallest in Sorted Matrix | 矩阵的每一行 | 弹第 t 小 | 也可以**值域二分 + 计数**（见 solution.py） |
| **LC-0373** K Pairs with Smallest Sums | `nums1[i]` 配上整个 nums2 | 弹最小和 | **只初始化 min(k, m) 路** |
| **LC-0632** Smallest Range Covering K Lists | 每个列表 | 记录 `[堆顶, cur_max]` | 堆给**下界**，外部变量给**上界** |

### LC-0373 的剪枝为什么成立
答案最多 k 个数对。第 k+1 条链的第一个数对 `(nums1[k], nums2[0])`
已经不小于前 k 条链的第一个数对 ⟹ 它进不了前 k 名 ⟹ 那条链整个不用初始化。
堆大小从 m 降到 **min(k, m)**。

### LC-0632 为什么「弹最小」
当前区间是 `[堆顶, cur_max]`。要让区间变小，只能**抬高下界** ——
推进最小值所在的那一路。动其他路只会让 `cur_max` 变大、区间更长。
**某一路走到头就立刻结束**：它再也无法贡献元素，不可能有更优区间。

## 题目

| # | 题 | 优先级 | 复杂度 |
|---|---|---|---|
| 01/01 | LC-0378 Kth Smallest Element in a Sorted Matrix | P1 | O(k log n) 堆 / O(n log(max-min)) 值域二分 |
| 02/01 | LC-0373 Find K Pairs with Smallest Sums | P1 | O(min(k,m) + k log min(k,m)) |
| 03/01 | LC-0632 Smallest Range Covering K Lists | P2 | O(N log k) |

## 跨专题
**LC-0023 Merge k Sorted Lists** 是 K-way Merge 的链表版，
实体目录在 [06-linked-list](<../../06-linked-list (链表)/04 - 链表归并与排序/02 - K 条有序链表归并/01 - LC-0023 - Merge k Sorted Lists>)。
它的堆元组必须带 tie-breaker（`id(node)` 或下标），否则值相同时会去比较 ListNode 对象。

**LC-0378 的另一条路**：值域二分 + 阶梯计数，O(n log(max−min))。
注意它**不能**用 LC-0074 的「展开成一维」—— 本题只保证行、列各自有序，
拼起来不是有序数组。详见
[05-binary-search 的索引说明](<../../05-binary-search (二分查找)/03 - 二分答案与可行性判断 (Binary Search on Answer)/04 - 值域二分与计数可行性/README.md>)。

## 常见错误
- 把所有候选一次性入堆。
- 弹出后从**错误的路**补元素（必须是同一路的下一个）。
- LC-0373 不做 `min(k, m)` 剪枝。
- LC-0632 忘了「某一路走到头就结束」，导致越界或死循环。
- 元组缺 tie-breaker。

## 复习时的 Pattern Recognition
> 「k 个有序列表 / 有序矩阵」「第 k 小的和 / 第 k 小的元素」「覆盖所有列表的最小区间」
> → K-way Merge。**堆的大小应该是 k，不是 n。**
