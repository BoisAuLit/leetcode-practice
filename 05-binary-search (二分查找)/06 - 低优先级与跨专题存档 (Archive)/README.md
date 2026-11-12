# Level 1 · 06 低优先级与跨专题存档 (Archive)

## 用途
保留已有学习成果，但不让**低迁移性**或**主归属在别处**的题占据核心路线。
本章全部标 **P2**。

## 题目

### 01 - BST 性质与最近值 → LC-0270 Closest Binary Search Tree Value（P2）

它利用的是 **Binary Search Tree 的有序性**（左小右大，沿途更新最近值），
**不是有序数组上的二分模板**：没有 `lo`/`hi`/`mid`，也没有「丢掉一半数组」这回事
（虽然思想上确实是每步排除一棵子树）。

```python
cur, best = root, root.val
while cur:
    if abs(cur.val - target) < abs(best - target): best = cur.val
    cur = cur.left if target < cur.val else cur.right
```
平衡时 O(log n)，退化成链时 O(n) —— 这一点和数组二分的**保证** O(log n) 不同。

**更适合在 BST 专题复习**：[07-trees (树)](<../../07-trees (树)/>)。
本目录保留原有解法、PDF 和全部资料，只做跨专题引用说明，不删不改。

---

### 02 - 非典型二分标签题 → LC-3346 Maximum Frequency of an Element After Performing Operations I（P2）

LeetCode 给它打了 Binary Search 标签，**但这不是选择解法的理由**。
它的主流解法是 **排序 + 滑动窗口 + 前缀和 / 差分数组**：
把每个数能被调整到的区间 `[x-k, x+k]` 看成一个覆盖区间，统计哪个点被覆盖次数最多。

**不要把它强行讲成典型的 Binary Search on Answer** —— 那会污染你对
Level 1 `03` 那套三件套的直觉。
它更接近 [03-sliding-window (滑动窗口)](<../../03-sliding-window (滑动窗口)/>) 的内容。

现有代码、PDF 和附件**完整保留**。

---

### 03 - 特殊数学约束与二分答案 → LC-3733 Minimum Time to Complete All Deliveries（P2）

这**确实是**一道 Binary Search on Answer，但它的 feasible 比 Koko / Shipping 复杂得多：
- 周期性的不可用时间
- 两个配送主体各自独立的限制
- 两者不能同时执行配送
- 计数需要容斥（Inclusion-Exclusion）或 LCM 相关推导

所以它**不适合当作基础二分答案的模板题**来记。
价值在于说明：二分答案的难点往往不在二分，**而在 feasible 怎么写对**。

保留全部进阶学习资料，标 P2。

---

## 为什么这三道不进核心路线

| 题 | 原因 |
|---|---|
| LC-0270 | 用的是 BST 结构而非数组二分模板；主归属应在 07-trees |
| LC-3346 | 标签误导；实际主解法是排序 + 滑窗 + 差分 |
| LC-3733 | 是真二分答案，但 feasible 过于特殊，迁移性低 |

## 保留承诺
本目录下所有 `solution.py`、`metadata.json`、PDF、附件
在本次重构中**一个字节都没有改动**，只是换了位置。
