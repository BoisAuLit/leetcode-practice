# Level 1 · 05 单调队列与滑动窗口 (Monotonic Deque) —— 跨专题索引目录

> **本目录刻意不放任何题目文件夹**，原因同 Level 1 `02`：
> 一道题在题库里只能有一个实体文件夹，否则复习队列会重复。

## Monotonic Stack 与 Monotonic Deque 不是同一个模板

|  | Monotonic Stack | Monotonic Deque |
|---|---|---|
| 操作 | `append` / `pop` | `append` / `pop` / **`popleft`** |
| 核心问题 | 当前元素能否**确定某个旧元素的答案** | 谁**永远不可能**成为窗口最优解 |
| 弹出语义 | 被弹者**拿到答案** | 被弹者**被淘汰** |
| 为什么要 popleft | 不需要 | 候选会**过期**或**已结算** |

`popleft()` 的两种原因（不能一概说成「窗口过期」）：
- **过期**（LC-0239）：`dq[0] <= i - k`，下标滑出窗口。
- **已结算**（LC-0862）：队首已凑出合法答案并记录，留着只会得到更长的子数组。

## 模板

```python
# 固定窗口最大值
dq = deque()                                   # 存下标，对应值单调不增
for i, x in enumerate(nums):
    while dq and nums[dq[-1]] <= x: dq.pop()   # 队尾：淘汰被支配的候选
    dq.append(i)
    if dq[0] <= i - k: dq.popleft()            # 队首：过期
    if i >= k - 1: res.append(nums[dq[0]])
```
O(n) 时间 —— 每个下标最多入队一次、出队一次。**有嵌套 while 不等于 O(n²)。**

## 本章的三道核心题（全部在别的专题）

| LC | 题 | Primary Pattern | 实体目录 |
|---|---|---|---|
| 0239 | Sliding Window Maximum | Monotonic Deque | [18 · 04/01/01](<../../18-monotonic-fuck-you (单调栈、单调队列)/04 - 单调队列与滑动窗口/01 - 固定窗口最大值/01 - LC-0239 - Sliding Window Maximum>) |
| 1438 | Longest Continuous Subarray With Abs Diff ≤ Limit | Sliding Window | [03-sliding-window · 05/02/01](<../../03-sliding-window (滑动窗口)/05 - 单调队列与窗口极值 (Monotonic Deque)/02 - 变长窗口最大最小值约束/01 - LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit>) |
| 0862 | Shortest Subarray with Sum at Least K | Prefix Sum + Deque | [03-sliding-window · 03/01/02](<../../03-sliding-window (滑动窗口)/03 - 变长窗口之最短满足条件 (Minimum Valid Window)/01 - 数值阈值与最短区间/02 - LC-0862 - Shortest Subarray with Sum at Least K>) |

## 三者的不变量对照

| | LC-0239 | LC-1438 | LC-0862 |
|---|---|---|---|
| 窗口 | 固定长度 k | 变长，受 `max − min ≤ limit` 控制 | 变长，求最短 |
| 队列数 | 1（递减） | 2（递减 + 递增） | 1（前缀和递增） |
| 队列里是什么 | 最大值候选 | 最大 + 最小候选 | **还有价值的前缀和起点** |
| 队首为什么弹 | 过期 | 过期 | **已结算** |
| 普通滑窗行不行 | — | — | **不行**，有负数，窗口和不单调 |

## LC-0862 为什么必须用 Deque
数组可能有负数 ⇒ 右端点右移时窗口和**不单调**，
「和太大就收缩左端」这个标准滑动窗口的前提直接崩掉。
改成前缀和之后，问题变为「找 `j < i` 使 `prefix[i] - prefix[j] >= k` 且 `i - j` 最小」，
用单调递增的前缀和候选队列解决。它属于 **P1 进阶**，掌握前缀和之后再练。

完整讲解见 [18 专题根 README](<../../18-monotonic-fuck-you (单调栈、单调队列)/README.md>)
和 [Stack vs Deque 对照](<../../18-monotonic-fuck-you (单调栈、单调队列)/_docs/stack-vs-deque.md>)。
