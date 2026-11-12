# 01 - 定长窗口与频率匹配 (Fixed Window)

## 核心定义

窗口长度**恒定为 k**。right 每前进一格，left 就机械地跟进一格（`left = right - k + 1`），
**没有任何收缩判断** —— 这是它和后面所有变长窗口最根本的区别。

## 决定性观察

1. 相邻两个窗口只差两个元素 ⇒ 窗口状态可以 **O(1) 增量更新**（进一个、出一个）。
2. 窗口状态不一定是「和」：可以是频率表（2461、0567）、派生数组的和（1052）、
   哈希集合（0187）。**想清楚「窗口里到底要维护什么」比写循环重要。**
3. 有些题的定长窗口是**转化出来的**：01423「从两端拿 k 个」⟺「中间留 n-k 个」。

## Loop Invariant（循环不变量）

处理完下标 i 时，窗口状态精确对应 `nums[i-k+1 .. i]` 这 k 个元素。
「先加右、再减左」的顺序不能乱。

## Window Expansion / Shrinking Rule

- **Expansion**：每轮无条件把 `nums[right]` 加进状态。
- **Shrinking**：不是「判断后收缩」，而是 `right >= k` 时**无条件**移除 `nums[right-k]`。

## Answer Update Timing

窗口刚好满 k 个元素时（`right >= k - 1`）更新一次答案。写成 `right >= k` 会漏掉第一个窗口。

## 正确性

每个元素恰好进入状态一次、离开一次 ⇒ 总共 O(n) 次状态更新。
因为长度固定，不需要证明任何单调性 —— 这也是定长窗口最容易写对的原因。

## Python 模板

```python
cur = 0                      # 窗口状态：和 / 频率表 / 集合…
best = float("-inf")
for right, x in enumerate(nums):
    cur += x                             # 1. 进
    if right >= k:
        cur -= nums[right - k]           # 2. 出（无条件）
    if right >= k - 1:
        best = max(best, cur)            # 3. 窗口满了才更新答案
```

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0643 - Maximum Average Subarray I](01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/01%20-%20LC-0643%20-%20Maximum%20Average%20Subarray%20I) | E | 最标准的定长窗口骨架 |
| **P1** | [LC-2461 - Maximum Sum of Distinct Subarrays With Length K](01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/02%20-%20LC-2461%20-%20Maximum%20Sum%20of%20Distinct%20Subarrays%20With%20Length%20K) | M | 窗口多带一张频率表；`len(freq) == k` 即无重复 |
| **P1** | [LC-1423 - Maximum Points You Can Obtain from Cards](01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/03%20-%20LC-1423%20-%20Maximum%20Points%20You%20Can%20Obtain%20from%20Cards) | M | **补集转化**：两端取 k 个 ⟺ 中间留 n-k 个 |
| **P1** | [LC-1052 - Grumpy Bookstore Owner](01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/04%20-%20LC-1052%20-%20Grumpy%20Bookstore%20Owner) | M | 基础值 + 窗口内增量；窗口维护的是**派生数组** |
| **P0** | [LC-0567 - Permutation in String](02%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D/01%20-%20LC-0567%20-%20Permutation%20in%20String) | M | 窗口长度 = len(s1)，频率表相等即匹配 |
| **P0** | [LC-0438 - Find All Anagrams in a String](02%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D/02%20-%20LC-0438%20-%20Find%20All%20Anagrams%20in%20a%20String) | M | 和 0567 **同一个算法**，只是要收集所有起点 |
| **P2** | [LC-0187 - Repeated DNA Sequences](03%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%8E%BB%E9%87%8D/01%20-%20LC-0187%20-%20Repeated%20DNA%20Sequences) | M | 定长子串去重；可提 Rolling Hash 但不必深究 |

## 常见错误与边界

- 答案初值设 0（数组可能全负）—— 用第一个窗口的值或 `-inf`。
- `right >= k - 1` 写成 `right >= k`，漏掉第一个窗口。
- 频率表计数归零**不删键**，导致 `len(freq)` 失真（2461 / 0438 都踩）。
- `k > len(nums)` 的边界：要么提前返回，要么让循环自然不触发。
- 0567 / 0438 比较频率表时，用长度 26 的数组比 `Counter` 快得多。

## 与相邻家族的区别

**变长窗口**的 left 由「约束是否满足」驱动，可能一次吐好几个、也可能一个都不吐；
定长窗口的 left 完全由 right 决定。看到「长度恰好为 k」就用本家族，
看到「最长 / 最短 / 有多少个」就去 Level 02 / 03 / 04。
