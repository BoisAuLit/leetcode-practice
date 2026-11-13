# Level 1 · 04 单调队列与滑动窗口

> **Monotonic Deque 不是 Monotonic Stack 换个名字。** 两者的不变量和删除原因都不同，
> 详见 [_docs/stack-vs-deque.md](<../_docs/stack-vs-deque.md>)。

## 核心定义
在一个滑动的窗口里维护极值（或维护「还有价值的候选起点」），
用双端队列把「被支配的候选」从队尾淘汰、把「过期或已结算的候选」从队首移除。

## 决定性观察
1. 窗口的和可以增量维护，但**极值不行** —— 移除最大值之后，新的最大值是谁？
   所以需要一个按值单调排列的候选队列。
2. **支配（Dominance）**：新元素 x 比队尾那些元素更大、而且更年轻（活得更久），
   那些元素在任何未来的窗口里都当不上最大值 → 永久删除。
3. 队首的处理有两种**完全不同**的原因：
   - **过期**（LC-0239）：`dq[0] <= i - k`，下标滑出窗口了。
   - **已结算**（LC-0862）：队首已经凑出一个合法答案并记录，留着只会更长。

## Loop Invariant
队列里存**下标**，下标从队首到队尾递增；对应的值单调（239 是不增，862 是不减）；
队首始终是当前窗口内的最优候选。

## 典型模板
```python
dq = deque(>)                                   # 存下标
for i, x in enumerate(nums):
    while dq and nums[dq[-1]] <= x: dq.pop()   # 队尾：淘汰被支配者
    dq.append(i)
    while dq[0] <= i - k: dq.popleft()         # 队首：过期
    if i >= k - 1: res.append(nums[dq[0]])
```
O(n) 时间：每个下标最多入队一次、出队一次。有嵌套 while **不等于** O(n²)。

## 题目

| # | 题 | 优先级 | 位置 |
|---|---|---|---|
| 01/01 | LC-0239 Sliding Window Maximum | P0 | **本专题实体目录**（含用户原有 note.md） |
| — | LC-1438 Longest Continuous Subarray With Abs Diff ≤ Limit | P1 | 跨专题索引 → [03-sliding-window/05/02/01](<../general/01 - LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit>) |
| — | LC-0862 Shortest Subarray with Sum at Least K | P1 | 跨专题索引 → [03-sliding-window/03/01/02](<../general/02 - LC-0862 - Shortest Subarray with Sum at Least K>) |

**为什么 1438 / 862 只建索引**：这两道题已经在 03-sliding-window 有完整的
solution.py / problem.pdf / metadata.json 和复习记录。
一道题在题库里只能有一个实体文件夹，否则复习队列会出现重复。
它们的 Primary Pattern 是 Sliding Window，Secondary 是 Monotonic Deque。

## 三道题的不变量对照（必须分清）

| | LC-0239 | LC-1438 | LC-0862 |
|---|---|---|---|
| 窗口 | 固定长度 k | 变长，受 max−min ≤ limit 约束 | 变长，求最短 |
| 队列数量 | 1 个（递减） | 2 个（递减 + 递增） | 1 个（前缀和递增） |
| 队列里是什么 | 窗口最大值候选 | 最大值候选 + 最小值候选 | **还有价值的前缀和起点** |
| 队首为什么弹 | 过期 | 过期（收缩时） | **已结算**（找到答案后找更短的） |
| 能不能用普通滑窗 | — | — | **不能**，数组有负数，窗口和不单调 |

## 常见错误
- 队列里存值不存下标 → 没法判断过期。
- LC-1438 收缩时只检查了一个队列的队首。
- LC-0862 直接套正数滑动窗口 → 有负数时窗口和不单调，模板失效。
- 因为代码里有 while 就说复杂度 O(n²)。
