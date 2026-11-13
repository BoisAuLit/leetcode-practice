# 18 · Monotonic Stack & Monotonic Deque（单调栈、单调队列）

> 一句话定位：**单调结构不是为了「保持有序」，而是为了「扔掉永远不可能成为答案的候选」。**
> 只要能证明某个旧元素在未来任何情形下都赢不了新元素，就可以永久删除它 —— 这就是全部。

本专题共 **16 道不同题目**（13 道实体目录 + 3 道跨专题索引）。
配套文档：[Pattern Recognition Guide](<_docs/pattern-recognition.md>) ·
[Stack vs Deque](<_docs/stack-vs-deque.md>) ·
[严格 / 非严格比较速查](<_docs/strict-vs-nonstrict.md>) ·
[贡献计数速查](<_docs/contribution-counting.md>) ·
[摊还复杂度](<_docs/amortized-analysis.md>) ·
[原始疑问 FAQ](<_docs/faq.md>) · 原始笔记：[questions_about_monotonic.md](<questions_about_monotonic.md>)

---

## 一、目录地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | 最近更大元素与跨度 | 5 | [→](<01 - 最近更大元素与跨度/README.md>) |
| 02 | 单调边界、矩形与贡献计算 | 5 | [→](<02 - 单调边界、矩形与贡献计算/README.md>) |
| 03 | 单调栈与贪心构造 | 3 | [→](<03 - 单调栈与贪心构造/README.md>) |
| 04 | 单调队列与滑动窗口 | 1 实体 + 2 索引 | [→](<04 - 单调队列与滑动窗口/README.md>) |
| 05 | 单调扫描与跨专题存档 | 3 | [→](<05 - 单调扫描与跨专题存档/README.md>) |

```
01 - 最近更大元素与跨度/
  01 - Next Greater Element 与索引栈/
    01 - LC-0496 - Next Greater Element I            P0
    02 - LC-0739 - Daily Temperatures                P0
    03 - LC-0503 - Next Greater Element II           P1
  02 - Previous Greater 与流式跨度/
    01 - LC-0901 - Online Stock Span                 P0
  03 - 从右扫描与「被弹出的最大值」/
    01 - LC-0456 - 132 Pattern                       P1   ← 第二轮新增
02 - 单调边界、矩形与贡献计算/
  01 - Histogram 与最大矩形/
    01 - LC-0084 - Largest Rectangle in Histogram    P0
    02 - LC-0085 - Maximal Rectangle                 P2
  02 - Subarray 极值贡献计算/
    01 - LC-0907 - Sum of Subarray Minimums          P1
    02 - LC-2104 - Sum of Subarray Ranges            P1
    03 - LC-1856 - Maximum Subarray Min-Product      P2   ← 第二轮新增
03 - 单调栈与贪心构造/
  01 - 字典序优化与安全删除/
    01 - LC-0402 - Remove K Digits                   P0
    02 - LC-0316 - Remove Duplicate Letters          P0
  02 - 固定长度最优子序列/
    01 - LC-1673 - Find the Most Competitive Subseq  P1   ← 第二轮新增
04 - 单调队列与滑动窗口/
  01 - 固定窗口最大值/
    01 - LC-0239 - Sliding Window Maximum            P0
  （LC-1438、LC-0862 的实体目录在 03-sliding-window，本章只建索引）
05 - 单调扫描与跨专题存档/
  01 - Car Fleet 与到达时间单调扫描/
    01 - LC-0853 - Car Fleet                         P1
  02 - Suffix Maximum 与右侧可见性/
    01 - LC-1762 - Buildings With an Ocean View      P2
  03 - Greedy 跨专题来源存档/
    01 - LC-0134 - Gas Station                       P2（Primary Pattern = Greedy）
```

---

## 二、Monotonic Stack vs Monotonic Deque（最重要的一组区别）

|  | Monotonic Stack（单调栈） | Monotonic Deque（单调双端队列） |
|---|---|---|
| 操作 | `append` / `pop`（只动一端） | `append` / `pop` / `popleft`（两端都动） |
| 核心问题 | **当前元素能不能把某个旧元素的答案定下来？** | **谁已经永远不可能成为窗口里的最优解？** |
| 弹出的含义 | 被弹出的元素**此刻拿到了答案** | 被弹出的元素**被淘汰了，没有答案** |
| 为什么不用 popleft | 栈底元素还没拿到答案，不能丢 | 队首可能**过期**（出窗口）或**已结算** |
| 代表题 | 496 / 739 / 84 / 907 / 402 | 239 / 1438 / 862 |

`popleft()` 有两种完全不同的原因，不能一概而论：

- **LC-0239**：队首下标滑出窗口了 → 过期（Expiration）。
- **LC-0862**：队首已经凑出一个合法子数组，答案已记录，留着它只会得到更长的答案 → 已结算。

```python
# Monotonic Stack 骨架
while stack and 当前元素能解决 stack[-1]:
    j = stack.pop(); resolve(j)
stack.append(i)

# Monotonic Deque 骨架
while dq and 新元素支配 dq[-1]:
    dq.pop()                 # 队尾：淘汰被支配的候选
dq.append(i)
while dq and dq[0] 已过期或已结算:
    dq.popleft()             # 队首：两种不同原因，见上
```

---

## 三、为什么可以安全地 Pop（本专题唯一需要真正理解的事）

**支配关系（Dominance）**：若元素 b 比 a 晚出现，且在目标函数上不比 a 差，
那么任何以后用得上 a 的场合都能换成 b（b 活得更久、还更优），于是 **a 可以被永久删除**。

- Next Greater（496/739/503）：新来的 `x > nums[j]` → j 的答案就是 x，j 再无用处。
- Histogram（84）：遇到更矮的柱子 → 高柱子的右边界已定，可以立刻结算面积。
- Greedy（402/316/1673）：前面更大的数字在高位上，换成当前更小的数字字典序一定变小。
- Deque（239）：更年轻且更大的元素出现 → 老的更小元素永远当不上窗口最大值。

**Stack 里存值还是下标？**
需要算距离、宽度、区间和，或者元素可能重复 → **存下标**（739/84/907/239/503）。
只关心值本身的聚合 → 存值或 `(值, 聚合量)` 也可以（901 存 `(price, span)`，456 存值）。

---

## 四、核心 Python 模板

**Template 1 · Next Greater Element（索引栈）**
```python
res, stack = [-1] * n, []                 # stack 存下标，对应值单调不增
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:  # 严格小于才弹 → 找「严格更大」
        res[stack.pop()] = x              # 弹出时就是它拿到答案的时刻
    stack.append(i)
```
O(n) / O(n)。复用：496、739、503（外层改成 `range(2n)` + `i % n`，第二轮不入栈）。

**Template 2 · Previous / Next Smaller 边界**
```python
left = [-1] * n                           # 左边第一个严格更小
stack = []
for i in range(n):
    while stack and nums[stack[-1]] >= nums[i]:
        stack.pop()
    left[i] = stack[-1] if stack else -1
    stack.append(i)
```
右边界把方向和符号对称翻过来即可。复用：84、907、2104、1856。

**Template 3 · Histogram 最大矩形**
```python
stack, best = [], 0                       # 单调递增索引栈
for i in range(n + 1):
    cur = 0 if i == n else heights[i]     # 末尾哨兵（Sentinel），把栈清空
    while stack and heights[stack[-1]] > cur:
        h = heights[stack.pop()]
        left = stack[-1] if stack else -1 # 弹完后的新栈顶就是左边界
        best = max(best, h * (i - left - 1))   # 宽度减 1：两边都是开区间
    stack.append(i)
```
O(n) / O(n)。复用：84、85（每行一次）、1856（把宽度换成前缀和之差）。

**Template 4 · 贡献计数（Contribution Counting）**
```python
total, stack = 0, []
for i in range(n + 1):
    cur = float('-inf') if i == n else arr[i]
    while stack and arr[stack[-1]] > cur:        # 严格大于才弹 → 相等留栈里
        j = stack.pop()
        left = stack[-1] if stack else -1
        total += arr[j] * (j - left) * (i - j)   # 起点 i-left 种 × 终点 right-i 种
    stack.append(i)
```
O(n) / O(n)。复用：907（取模）、2104（Σmax − Σmin，不取模）、1856（换成取 max）。

**Template 5 · 贪心单调栈**
```python
stack = []
for x in nums:
    while stack and stack[-1] > x and 还允许删除:   # 「还允许删除」就是三道题的唯一区别
        stack.pop()
    stack.append(x)
```
`还允许删除` 的三种写法：402 是 `k > 0`；316 是 `last_occur[stack[-1]] > i`；
1673 是 `len(stack) + (n - i) > k`。

**Template 6 · 固定窗口最大值（Deque）**
```python
dq = deque()                               # 存下标，对应值单调不增
for i, x in enumerate(nums):
    while dq and nums[dq[-1]] <= x: dq.pop()      # 队尾淘汰被支配者
    dq.append(i)
    if dq[0] <= i - k: dq.popleft()               # 队首过期
    if i >= k - 1: res.append(nums[dq[0]])
```

**Template 7 · 两个 Deque 维护变长窗口 max / min** → 见 LC-1438（03-sliding-window）。
**Template 8 · Prefix Sum + Deque** → 见 LC-0862（03-sliding-window）。

---

## 五、P0 / P1 / P2 与学习路线

**P0（6 道，必须形成肌肉记忆）**
LC-0496 → LC-0739 → LC-0901 → LC-0084 → LC-0239 → LC-0402 / LC-0316

**P1（6 道，重要独立变体）**
LC-0503、LC-0907、LC-2104、LC-0853、LC-0456、LC-1673

**P2（4 道，扩展与存档）**
LC-0085、LC-1856、LC-1762、LC-0134

**阶段式路线**

| 阶段 | 内容 | 题目 |
|---|---|---|
| A | Next Greater 基本功 | 496 → 739 → 503 |
| B | Previous / 跨度 | 901 |
| C | 边界与矩形 | 84 → 85 |
| D | 贡献计数 | 907 → 2104 → 1856 |
| E | 贪心构造 | 402 → 316 → 1673 |
| F | 单调队列 | 239 → 1438 → 862 |
| G | 相关单调扫描 | 853 → 1762 → 456 |

**真正最核心的 7 道**（覆盖全部不同的不变量，不重复刷同类）：
`496`（Next Greater 骨架）、`739`（索引栈 + 距离）、`901`（Previous + 状态压缩）、
`84`（边界 + 宽度）、`907`（贡献计数 + Tie Breaking）、`239`（Deque + 过期）、
`402`（贪心删除）。不含跨专题的 LC-0134。

---

## 六、跨专题索引

| LC | Primary Pattern | Secondary | 实体目录 |
|---|---|---|---|
| LC-0239 | Monotonic Deque | Sliding Window | **本专题** `04/01/01`；滑动窗口专题在 README 里引用它 |
| LC-1438 | Sliding Window | Two Monotonic Deques | [`03-sliding-window/05/02/01`](<general/01 - LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit>) |
| LC-0862 | Prefix Sum + Deque | Sliding Window | [`03-sliding-window/03/01/02`](<general/02 - LC-0862 - Shortest Subarray with Sum at Least K>) |
| LC-0042 | Two Pointers | Monotonic Stack | [`02-two-pointers/01/01/03`](<general/03 - LC-0042 - Trapping Rain Water>) |
| LC-0134 | **Greedy** | Running Balance | **本专题存档** `05/03/01`（13-greedy 当前没有此题） |
| LC-0084 / 0853 | Monotonic Stack / 排序+扫描 | — | 本专题（原 NC 来源已正式化为 LC 编号） |

04-stack-queue 专题的「单调栈」「单调队列」两个 Level 1 **只建索引、不放实体题**，
全部指回本专题 —— 仓库的铁律是：沾单调栈 / 单调队列的题一律归 18。

---

## 七、第二轮独立审核结果

**新增 3 道**（上限 3，已用满）：

| 题 | 新增理由 |
|---|---|
| LC-0456 - 132 Pattern | 不变量和前面所有题都不同：栈里是候选「3」，栈外 `third` 记住**被弹出的最大值**当「2」。从右往左扫，是单调栈的另一个方向。 |
| LC-1673 - Most Competitive Subsequence | 和 402「删 k 个」、316「每种一次」构成贪心栈的**三种预算写法**，把「什么时候允许 Pop」这件事讲透，而不是背三份代码。 |
| LC-1856 - Max Subarray Min-Product | 84 的骨架 + 目标函数换成「前缀和之差」，是边界法最直接的迁移练习；也强调了「元素必须为正」这个前提。 |

**审核过、决定不加的候选（Future Candidates）**

| 题 | 不加的理由 |
|---|---|
| LC-0042 Trapping Rain Water | 02-two-pointers 已有完整资料，只建跨专题索引 |
| LC-1475 Final Prices | 就是 Next Smaller，和 496 模板相同，不引入新东西 |
| LC-1019 Next Greater Node in Linked List | 739 换个容器，先转成数组就一模一样 |
| LC-1944 Number of Visible People in a Queue | 739 的计数变体，收益小于记忆成本 |
| LC-1081 Smallest Subsequence of Distinct Characters | 与 LC-0316 **是同一道题**，不应重复建目录 |
| LC-2289 Steps to Make Array Non-decreasing | 单调栈 + 轮次 DP，学习成本高、迁移性差 |
| LC-2398 Maximum Robots Within Budget | 与 LC-1438 的两 Deque 变长窗口高度重合 |

---

## 八、复杂度：别机械地写 O(n)

| 题 | 真实复杂度 | 为什么不是裸 O(n) |
|---|---|---|
| 496 / 739 / 901 / 84 / 907 / 239 | O(n) | 每个元素最多入栈出栈各一次 → 摊还（Amortized）O(n) |
| 503 | O(n) | 跑 2n 轮，但只有前 n 轮入栈 |
| 901 单次 `next()` | 最坏 O(n)，摊还 O(1) | 一次调用可能弹空整个栈，**不能说单次 O(1)** |
| 853 Car Fleet | **O(n log n)** | 扫描是 O(n)，但前面有一次排序 |
| 85 Maximal Rectangle | O(rows × cols) | 每行跑一次 O(cols) 的栈 |
| 84 空间 | O(n) | 严格递增的输入会让栈装满 |

详见 [_docs/amortized-analysis.md](<_docs/amortized-analysis.md>)。
