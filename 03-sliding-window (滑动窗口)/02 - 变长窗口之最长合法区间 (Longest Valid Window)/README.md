# 02 - 变长窗口之最长合法区间 (Longest Valid Window)

## 核心定义

right 无条件扩张；**一旦窗口不合法，就收缩 left 直到重新合法**。
每一轮结束时窗口都是合法的，答案取所有轮里的最大长度。

## 决定性观察

1. 约束必须是**单调**的：窗口变长只会让约束更难满足，变短只会更容易。
   有了这条，left 就**永不回退**，总复杂度 O(n)。
2. 所有题的差别只在「窗口状态是什么」和「合法的定义是什么」：

| 题 | 窗口状态 | 合法条件 |
|---|---|---|
| 0003 | 哈希集合 / 上次出现位置 | 无重复字符 |
| 0904 / 0159 | 频率表 | `len(freq) <= K` |
| 2401 | **一个整数 bitmask** | `used & x == 0`（位不重叠）|
| 1004 | 零的个数 | `zeros <= k` |
| 0424 | 频率表 + 历史最大频率 | `长度 - maxFreq <= k` |
| 1208 | 代价之和 | `cost <= maxCost` |
| 1838 | 窗口和（**先排序**）| `nums[r] * len - sum <= k` |

3. 状态不必是频率表 —— 2401 用一个整数就够了。

## Loop Invariant

每轮结束时 `[left, right]` 合法，且它是**以 right 结尾的最长合法窗口**。

## Window Expansion / Shrinking Rule

- **Expansion**：`right` 每轮前进一格，更新状态。
- **Shrinking**：`while 不合法: 吐掉 nums[left]; left += 1`。
  注意是 **while 不是 if**，而且判断条件是「**不**合法」。

## Answer Update Timing

**收缩结束之后**更新：`best = max(best, right - left + 1)`。

## 正确性简证

若某个 left 使窗口不合法，那么对更大的 right 它只会更不合法（单调性），
所以 left 永远不需要回退。left 和 right 各自单调右移 ⇒ 每个元素进出各一次 ⇒ O(n)。

## Python 模板

```python
left = 0
best = 0
for right, x in enumerate(nums):
    add(x)                          # 把 x 并入窗口状态
    while not valid():              # ! 不合法才收缩
        remove(nums[left])
        left += 1
    best = max(best, right - left + 1)   # ! 收缩完成后更新
```

## LC-0424 的 maxFreq 为什么可以不减小（本层最常被问的点）

`maxFreq` 记录的是**历史上出现过的最大频率**，不是当前窗口的真实最大频率。
这看起来是个 bug，其实不是：

- 答案只可能由「某个真实达到过 maxFreq 的窗口」产生。
- 当 maxFreq 偏大时，`长度 - maxFreq <= k` 这个判断会偏**宽松**，
  于是窗口不会收缩，长度保持不变 —— **但 best 也不会变大**，因为 best 只在
  窗口真的变长时才更新，而窗口变长需要 right 前进，right 前进才可能刷新真正的 maxFreq。
- 换句话说：偏大的 maxFreq 只会让窗口「平移」而不是「增长」，不会产生更大的错误答案。

所以这个写法是**安全的**，但解释时必须说清「它不等于当前窗口的真实最大频率」。

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0003 - Longest Substring Without Repeating Characters](01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/01%20-%20LC-0003%20-%20Longest%20Substring%20Without%20Repeating%20Characters) 📦 | M | 本层的签名题 |
| **P0** | [LC-0904 - Fruit Into Baskets](01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/02%20-%20LC-0904%20-%20Fruit%20Into%20Baskets) | M | At Most K Distinct（K = 2） |
| **P2** | [LC-0159 - Longest Substring with At Most Two Distinct Characters](01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/03%20-%20LC-0159%20-%20Longest%20Substring%20with%20At%20Most%20Two%20Distinct%20Characters) | M | **和 0904 同一个算法**，换成字符串（Premium） |
| **P2** | [LC-2401 - Longest Nice Subarray](01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/04%20-%20LC-2401%20-%20Longest%20Nice%20Subarray) | M | 窗口状态是 bitmask，不是频率表 |
| **P0** | [LC-1004 - Max Consecutive Ones III](02%20-%20%E5%85%81%E8%AE%B8%E4%BF%AE%E6%94%B9%20K%20%E4%B8%AA%E5%85%83%E7%B4%A0/01%20-%20LC-1004%20-%20Max%20Consecutive%20Ones%20III) | M | `zeros <= k`，最干净的「允许 k 次违规」 |
| **P0** | [LC-0424 - Longest Repeating Character Replacement](02%20-%20%E5%85%81%E8%AE%B8%E4%BF%AE%E6%94%B9%20K%20%E4%B8%AA%E5%85%83%E7%B4%A0/02%20-%20LC-0424%20-%20Longest%20Repeating%20Character%20Replacement) | M | `长度 - maxFreq <= k`；maxFreq 不减小的正确性 |
| **P1** | [LC-1208 - Get Equal Substrings Within Budget](03%20-%20%E9%A2%84%E7%AE%97%E7%BA%A6%E6%9D%9F%E4%B8%8E%E6%8E%92%E5%BA%8F%E5%90%8E%E7%AA%97%E5%8F%A3/01%20-%20LC-1208%20-%20Get%20Equal%20Substrings%20Within%20Budget) | M | 先把题压成代价数组，再做「和 <= 预算的最长区间」 |
| **P1** | [LC-1838 - Frequency of the Most Frequent Element](03%20-%20%E9%A2%84%E7%AE%97%E7%BA%A6%E6%9D%9F%E4%B8%8E%E6%8E%92%E5%BA%8F%E5%90%8E%E7%AA%97%E5%8F%A3/02%20-%20LC-1838%20-%20Frequency%20of%20the%20Most%20Frequent%20Element) | M | **必须先排序**；预算公式 `nums[r]*len - sum <= k` |

## LC-1838 为什么必须先排序

要把窗口里的数全部抬到同一个值，显然抬到**窗口最大值**最省。排序后窗口最大值就是
`nums[right]`，于是所需操作数 = `nums[right] * 窗口长度 - 窗口和`，可以 O(1) 算出来，
并且随窗口变长单调不减 —— 单调性成立，窗口法才合法。
不排序的话「最大值」在窗口里的位置不确定，这个公式和单调性都没了。

## 常见错误与边界

- 收缩条件写成「合法时收缩」—— 那是 Level 03 的最短窗口，答案会完全错。
- 频率归零不 `del`，`len(freq)` 失真。
- 0424 以为 maxFreq 要在收缩时同步减小（不需要，但要能解释为什么）。
- 1838 忘记排序，或者用 `max(window)` 现算（退化成 O(n²)）。
- 2401 吐元素时该用 `^=`（位不重叠，XOR 精确撤销）。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-2958 Length of Longest Subarray With at Most K Frequency](<./01 - 无重复与 Distinct 限制/05 - LC-2958 - Length of Longest Subarray With at Most K Frequency>) | `02 - 变长窗口之最长合法区间 (Longest Valid Window)/01 - 无重复与 Distinct 限制` | LC-0003 的「> 1」改成「> k」；只有刚进来的元素可能超标 | 最长合法窗口模板 |
| [LC-1493 Longest Subarray of 1's After Deleting One Element](<./02 - 允许修改 K 个元素/03 - LC-1493 - Longest Subarray of 1's After Deleting One Element>) | `02 - 变长窗口之最长合法区间 (Longest Valid Window)/02 - 允许修改 K 个元素` | LC-1004 模板 K=1，答案 = 最大窗口长 − 1（自动覆盖「必须删一个」） | prev/cur 两段计数是 O(1) 简化 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
