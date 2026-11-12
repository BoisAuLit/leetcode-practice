LeetCode 里和 **monotonic data structure** 有关的题，主要分成两大类：

* **Monotonic Stack**
* **Monotonic Deque / Queue**

如果你的目标是建立可迁移的 pattern，而不是把所有怪题都刷一遍，我建议优先刷下面这些。

| 题号       | 题目                                                     | 核心模式                           | 推荐度       |
| -------- | ------------------------------------------------------ | ------------------------------ | --------- |
| **496**  | Next Greater Element I                                 | Next Greater 基础模板              | 必刷        |
| **739**  | Daily Temperatures                                     | Next Greater + index           | 必刷        |
| **503**  | Next Greater Element II                                | Next Greater + circular array  | 必刷        |
| **1475** | Final Prices With a Special Discount                   | Next Smaller                   | 推荐        |
| **84**   | Largest Rectangle in Histogram                         | 左右 boundary                    | **必刷**    |
| **42**   | Trapping Rain Water                                    | monotonic stack 应用             | 推荐        |
| **901**  | Online Stock Span                                      | Previous Greater               | **必刷**    |
| **907**  | Sum of Subarray Minimums                               | Previous/Next Smaller boundary | **必刷但偏难** |
| **2104** | Sum of Subarray Ranges                                 | min/max contribution           | 907 延伸    |
| **239**  | Sliding Window Maximum                                 | Monotonic Deque                | **必刷**    |
| **862**  | Shortest Subarray with Sum at Least K                  | Prefix Sum + Monotonic Deque   | 高级        |
| **1438** | Longest Continuous Subarray With Absolute Diff ≤ Limit | 两个 monotonic deque             | 推荐        |

真正最值得你形成肌肉记忆的其实只有下面 **6 道**：

```text
496  Next Greater Element I
739  Daily Temperatures
84   Largest Rectangle in Histogram
901  Online Stock Span
907  Sum of Subarray Minimums
239  Sliding Window Maximum
```

它们基本覆盖了 monotonic 的主要骨架。

你可以这样分类记：

```text
Monotonic Stack
│
├── 1. Next Greater / Smaller
│   ├── 496 Next Greater Element I
│   ├── 503 Next Greater Element II
│   ├── 739 Daily Temperatures
│   └── 1475 Final Prices
│
├── 2. Previous Greater / Smaller
│   └── 901 Online Stock Span
│
└── 3. Boundary / Contribution
    ├── 84 Largest Rectangle in Histogram
    ├── 907 Sum of Subarray Minimums
    └── 2104 Sum of Subarray Ranges


Monotonic Deque
│
├── 239 Sliding Window Maximum
├── 1438 Longest Continuous Subarray
└── 862 Shortest Subarray with Sum at Least K
```

这里面我尤其希望你区分两个完全不同的模型。

**Monotonic Stack：**

```python
while stack and current 可以解决 stack[-1]:
    j = stack.pop()
    resolve(j)

stack.append(i)
```

核心问题永远是：

> 当前元素能不能把以前某个元素的答案确定下来？

而 **Monotonic Deque** 通常是：

```python
while dq and nums[dq[-1]] <= nums[i]:
    dq.pop()

dq.append(i)

while dq[0] 不在窗口内:
    dq.popleft()
```

核心是：

> **删掉以后永远不可能成为最优答案的候选人。**

因此我不建议你一次刷 20 道 monotonic。按这个顺序：

**496 → 739 → 901 → 84 → 239 → 907**

如果这 6 道你真的吃透，LeetCode 绝大多数 monotonic 题你至少能识别出“这是 monotonic”，这比强行记很多题重要得多。
