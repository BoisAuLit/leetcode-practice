# Level 1 · 04 链表归并与排序

## 核心定义
链表的归并天然比数组更优雅：**不需要额外数组，只改指针**。
从「两条」到「k 条」再到「自己排序」，是一条清晰的递进链。

## 决定性观察

### ① 两条有序链归并（LC-0021）—— 一切的基础
```python
dummy = tail = ListNode()
while a and b:
    if a.val <= b.val: tail.next, a = a, a.next
    else:              tail.next, b = b, b.next
    tail = tail.next
tail.next = a or b          # 剩下的整条接上，不用循环
return dummy.next
```
`dummy + tail` 的组合让「结果链还是空的吗」这个判断彻底消失。
收尾一行 `tail.next = a or b` 是因为**剩下的那条本来就有序**。
用 `<=` 而不是 `<` 保证**稳定性**（相等时优先取第一条）。

### ② k 条归并（LC-0023）—— 堆 vs 分治
**堆法**：堆里始终放着每条链的当前头，弹出最小的接上，再把它的 next 推进去。
```python
heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
```
**`i` 这个 tie-breaker 必不可少**：Python 的元组比较在第一项相等时会比第二项，
如果只放 `(val, node)`，遇到相同 val 就会去比较 `ListNode` 对象 ⟹ `TypeError`。
用下标 `i`（或 `id(node)`）当第二项即可。

复杂度 **O(N log k)**，N 是所有节点总数，堆大小始终 ≤ k。

**分治法**：两两归并，`log k` 轮，每轮处理 N 个节点 ⟹ 同样 **O(N log k)**，且不需要堆。
面试里提一句两种都能达到同样复杂度即可，**不用背两套代码**。

### ③ 链表归并排序（LC-0148）
```
1. 快慢指针找中点（必须停在「第一个中点」，否则 [1,2] 会无限递归）
2. 切断：mid_prev.next = None
3. 递归排左右两半
4. 用 LC-0021 的归并合并
```
**复杂度要说准**：时间 O(n log n)。
空间**不是 O(1)** —— 递归版有 **O(log n) 的调用栈**。
真要 O(1)，得写自底向上（bottom-up）的迭代归并，
但那是另一套代码，**面试初期不必背两份**，说清楚取舍就够了。

为什么链表排序偏爱归并而不是快排：
链表没有随机访问，快排的分区需要来回跳；而归并只需要顺序遍历 + 改指针，
**且不需要像数组归并那样开辅助数组**。

## 题目

| # | 题 | 优先级 | 复杂度 |
|---|---|---|---|
| 01/01 | LC-0021 Merge Two Sorted Lists | P0 | O(m+n) / O(1) |
| 02/01 | LC-0023 Merge k Sorted Lists | P0 | O(N log k) / O(k) |
| 03/01 | LC-0148 Sort List | P1 | O(n log n) / **O(log n) 栈** |

## 常见错误
- LC-0023 的堆元组没放 tie-breaker ⟹ `TypeError: '<' not supported between ListNode`。
- LC-0148 中点取错（停在第二个中点）⟹ `[1,2]` 切不开，无限递归。
- LC-0148 忘记在中点处 `prev.next = None` 切断 ⟹ 两半还连着，结果错乱。
- 声称 LC-0148 是 O(1) 空间（忽略了递归栈）。

## 跨专题
LC-0023 也是堆的经典应用，[09-heap (堆)](<../../09-heap (堆)/>) 可交叉参考；
实体目录留在本专题，因为核心操作仍是链表指针重连。
