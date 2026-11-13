# Sliding Window 滑动窗口学习体系（28 题 + 1 道跨专题索引）

面向 Silicon Valley FAANG / Big Tech SWE、AI Engineer 的算法面试与 OA。**所有文件夹编号表示推荐学习顺序，不是 LC 题号。**

| 标签 | 含义 | 数量 |
|---|---|---|
| **P0** | 核心必练，要能闭卷默写 | 10 + 1 道索引（LC-0239）|
| **P1** | 重要变体与进阶应用 | 12 |
| **P2** | 低优先级、重复训练或特殊技巧 | 6 |

## 一、整张知识地图

滑动窗口只有**五种**，区别不在「怎么移动指针」，而在**答案怎么更新**和**什么时候收缩**：

| 家族 | 窗口长度 | 什么时候收缩 | 答案怎么更新 | 代表题 |
|---|---|---|---|---|
| **01 定长** | 恒为 k | 不判断，`right >= k` 就无条件吐一个 | 窗口满了取 max/min | 0643 |
| **02 最长合法** | 变 | **不合法**时收缩 | 收缩后 `max(right-left+1)` | 0003 |
| **03 最短满足** | 变 | **合法**时收缩 | 收缩**前** `min(right-left+1)` | 0209 |
| **04 计数** | 变 | 同 02 | `ans += right-left+1`（至多）或 `+= left`（至少）| 0713 |
| **单调队列**（住在 18 专区） | 定长或变长 | 同上 | 额外维护一个**极值候选队列** | 0239 / 1438 |

**02 和 03 的 while 条件正好相反**，这是本专题最容易写反的地方：

```python
# 02 最长合法                           # 03 最短满足
while not valid():                      while valid():
    shrink()                                best = min(best, right - left + 1)
best = max(best, right - left + 1)          shrink()
```

第 05 层不是新模板，是**把题翻译成窗口**（补集转化、offset 分组、gap 数组）；第 06 层是存档。

## 二、核心不变量与模板

**所有变长窗口都依赖同一条前提：约束是单调的** ——窗口变长只会让约束更难满足。有了它，`left` 才能永不回退，总复杂度 O(n)。

这条前提什么时候会塌：

- **数组有负数**：LC-0209 的窗口法失效 → 见 **LC-0862**（前缀和 + 单调队列）。

- **乘积里有 0 或负数**：LC-0713 的窗口法失效。

- **「恰好 K」**：本身就不单调 → 用 **`exactly(K) = atMost(K) - atMost(K-1)`**。


```python
# 变长窗口通用骨架（02 / 04 同形，只差最后一行）
left = 0
for right, x in enumerate(nums):
    add(x)
    while not valid():
        remove(nums[left]); left += 1
    best = max(best, right - left + 1)     # 02
    # ans += right - left + 1              # 04（至多类）
```

## 三、什么时候该用单调队列

判断只有一句：**窗口状态里需要「极值」吗？**

和、计数、频率表都能 O(1) 增量维护；但**极值不能** —— 移除当前最大值之后，新的最大值无法从一个标量里恢复。这时才需要单调队列保存「未来还可能成为极值的候选」。

不需要极值（0003、0904、1004…）就别上单调队列，一张频率表足够。

## 四、全部题目


### [01 - 定长窗口与频率匹配 (Fixed Window)](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/README.md)

**01 - 数值聚合与固定窗口优化**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0643 - Maximum Average Subarray I](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/01%20-%20LC-0643%20-%20Maximum%20Average%20Subarray%20I) | E | （🆕 新增） |
| **P1** | [LC-2461 - Maximum Sum of Distinct Subarrays With Length K](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/02%20-%20LC-2461%20-%20Maximum%20Sum%20of%20Distinct%20Subarrays%20With%20Length%20K) | M | （🆕 新增） |
| **P1** | [LC-1423 - Maximum Points You Can Obtain from Cards](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/03%20-%20LC-1423%20-%20Maximum%20Points%20You%20Can%20Obtain%20from%20Cards) | M | （🆕 新增） |
| **P1** | [LC-1052 - Grumpy Bookstore Owner](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/01%20-%20%E6%95%B0%E5%80%BC%E8%81%9A%E5%90%88%E4%B8%8E%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E4%BC%98%E5%8C%96/04%20-%20LC-1052%20-%20Grumpy%20Bookstore%20Owner) | M | （🆕 我补充） |
**02 - 固定窗口字符频率匹配**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0567 - Permutation in String](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/02%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D/01%20-%20LC-0567%20-%20Permutation%20in%20String) | M |  |
| **P0** | [LC-0438 - Find All Anagrams in a String](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/02%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D/02%20-%20LC-0438%20-%20Find%20All%20Anagrams%20in%20a%20String) | M | （🆕 新增） |
**03 - 固定窗口字符串去重**

| | 题 | 难度 | |
|---|---|---|---|
| **P2** | [LC-0187 - Repeated DNA Sequences](01%20-%20%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B8%8E%E9%A2%91%E7%8E%87%E5%8C%B9%E9%85%8D%20%28Fixed%20Window%29/03%20-%20%E5%9B%BA%E5%AE%9A%E7%AA%97%E5%8F%A3%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%8E%BB%E9%87%8D/01%20-%20LC-0187%20-%20Repeated%20DNA%20Sequences) | M |  |

### [02 - 变长窗口之最长合法区间 (Longest Valid Window)](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/README.md)

**01 - 无重复与 Distinct 限制**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0003 - Longest Substring Without Repeating Characters](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/01%20-%20LC-0003%20-%20Longest%20Substring%20Without%20Repeating%20Characters) 📦 | M |  |
| **P0** | [LC-0904 - Fruit Into Baskets](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/02%20-%20LC-0904%20-%20Fruit%20Into%20Baskets) | M | （🆕 新增） |
| **P2** | [LC-0159 - Longest Substring with At Most Two Distinct Characters](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/03%20-%20LC-0159%20-%20Longest%20Substring%20with%20At%20Most%20Two%20Distinct%20Characters) | M |  |
| **P2** | [LC-2401 - Longest Nice Subarray](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/01%20-%20%E6%97%A0%E9%87%8D%E5%A4%8D%E4%B8%8E%20Distinct%20%E9%99%90%E5%88%B6/04%20-%20LC-2401%20-%20Longest%20Nice%20Subarray) | M | （🆕 我补充） |
**02 - 允许修改 K 个元素**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-1004 - Max Consecutive Ones III](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/02%20-%20%E5%85%81%E8%AE%B8%E4%BF%AE%E6%94%B9%20K%20%E4%B8%AA%E5%85%83%E7%B4%A0/01%20-%20LC-1004%20-%20Max%20Consecutive%20Ones%20III) | M |  |
| **P0** | [LC-0424 - Longest Repeating Character Replacement](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/02%20-%20%E5%85%81%E8%AE%B8%E4%BF%AE%E6%94%B9%20K%20%E4%B8%AA%E5%85%83%E7%B4%A0/02%20-%20LC-0424%20-%20Longest%20Repeating%20Character%20Replacement) | M |  |
**03 - 预算约束与排序后窗口**

| | 题 | 难度 | |
|---|---|---|---|
| **P1** | [LC-1208 - Get Equal Substrings Within Budget](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/03%20-%20%E9%A2%84%E7%AE%97%E7%BA%A6%E6%9D%9F%E4%B8%8E%E6%8E%92%E5%BA%8F%E5%90%8E%E7%AA%97%E5%8F%A3/01%20-%20LC-1208%20-%20Get%20Equal%20Substrings%20Within%20Budget) | M | （🆕 新增） |
| **P1** | [LC-1838 - Frequency of the Most Frequent Element](02%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E9%95%BF%E5%90%88%E6%B3%95%E5%8C%BA%E9%97%B4%20%28Longest%20Valid%20Window%29/03%20-%20%E9%A2%84%E7%AE%97%E7%BA%A6%E6%9D%9F%E4%B8%8E%E6%8E%92%E5%BA%8F%E5%90%8E%E7%AA%97%E5%8F%A3/02%20-%20LC-1838%20-%20Frequency%20of%20the%20Most%20Frequent%20Element) | M |  |

### [03 - 变长窗口之最短满足条件 (Minimum Valid Window)](03%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E7%9F%AD%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%20%28Minimum%20Valid%20Window%29/README.md)

**01 - 数值阈值与最短区间**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0209 - Minimum Size Subarray Sum](03%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E7%9F%AD%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%20%28Minimum%20Valid%20Window%29/01%20-%20%E6%95%B0%E5%80%BC%E9%98%88%E5%80%BC%E4%B8%8E%E6%9C%80%E7%9F%AD%E5%8C%BA%E9%97%B4/01%20-%20LC-0209%20-%20Minimum%20Size%20Subarray%20Sum) | M | （🆕 新增） |
| **P1** | [LC-0862 - Shortest Subarray with Sum at Least K](../18-monotonic-fuck-you%20%28%E5%8D%95%E8%B0%83%E6%A0%88%E3%80%81%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97%29/general/02%20-%20LC-0862%20-%20Shortest%20Subarray%20with%20Sum%20at%20Least%20K) | H | （🆕 我补充） |
**02 - 字符频率覆盖与最小窗口**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0076 - Minimum Window Substring](03%20-%20%E5%8F%98%E9%95%BF%E7%AA%97%E5%8F%A3%E4%B9%8B%E6%9C%80%E7%9F%AD%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%20%28Minimum%20Valid%20Window%29/02%20-%20%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E8%A6%86%E7%9B%96%E4%B8%8E%E6%9C%80%E5%B0%8F%E7%AA%97%E5%8F%A3/01%20-%20LC-0076%20-%20Minimum%20Window%20Substring) 📦 | H |  |

### [04 - 子数组与子串计数 (Counting Windows)](04%20-%20%E5%AD%90%E6%95%B0%E7%BB%84%E4%B8%8E%E5%AD%90%E4%B8%B2%E8%AE%A1%E6%95%B0%20%28Counting%20Windows%29/README.md)

**01 - 正数乘积与批量计数**

| | 题 | 难度 | |
|---|---|---|---|
| **P0** | [LC-0713 - Subarray Product Less Than K](04%20-%20%E5%AD%90%E6%95%B0%E7%BB%84%E4%B8%8E%E5%AD%90%E4%B8%B2%E8%AE%A1%E6%95%B0%20%28Counting%20Windows%29/01%20-%20%E6%AD%A3%E6%95%B0%E4%B9%98%E7%A7%AF%E4%B8%8E%E6%89%B9%E9%87%8F%E8%AE%A1%E6%95%B0/01%20-%20LC-0713%20-%20Subarray%20Product%20Less%20Than%20K) | M | （🆕 新增） |
**02 - Exactly K 与 At Most K**

| | 题 | 难度 | |
|---|---|---|---|
| **P1** | [LC-0930 - Binary Subarrays With Sum](04%20-%20%E5%AD%90%E6%95%B0%E7%BB%84%E4%B8%8E%E5%AD%90%E4%B8%B2%E8%AE%A1%E6%95%B0%20%28Counting%20Windows%29/02%20-%20Exactly%20K%20%E4%B8%8E%20At%20Most%20K/01%20-%20LC-0930%20-%20Binary%20Subarrays%20With%20Sum) | M | （🆕 新增） |
| **P1** | [LC-0992 - Subarrays with K Different Integers](04%20-%20%E5%AD%90%E6%95%B0%E7%BB%84%E4%B8%8E%E5%AD%90%E4%B8%B2%E8%AE%A1%E6%95%B0%20%28Counting%20Windows%29/02%20-%20Exactly%20K%20%E4%B8%8E%20At%20Most%20K/02%20-%20LC-0992%20-%20Subarrays%20with%20K%20Different%20Integers) | H | （🆕 新增） |
**03 - 满足全部字符约束的计数**

| | 题 | 难度 | |
|---|---|---|---|
| **P1** | [LC-1358 - Number of Substrings Containing All Three Characters](04%20-%20%E5%AD%90%E6%95%B0%E7%BB%84%E4%B8%8E%E5%AD%90%E4%B8%B2%E8%AE%A1%E6%95%B0%20%28Counting%20Windows%29/03%20-%20%E6%BB%A1%E8%B6%B3%E5%85%A8%E9%83%A8%E5%AD%97%E7%AC%A6%E7%BA%A6%E6%9D%9F%E7%9A%84%E8%AE%A1%E6%95%B0/01%20-%20LC-1358%20-%20Number%20of%20Substrings%20Containing%20All%20Three%20Characters) | M | （🆕 新增） |

### [05 - 高阶窗口组合与问题转化 (Advanced Windows)](05%20-%20%E9%AB%98%E9%98%B6%E7%AA%97%E5%8F%A3%E7%BB%84%E5%90%88%E4%B8%8E%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96%20%28Advanced%20Windows%29/README.md)

**01 - 按单词长度分组的窗口**

| | 题 | 难度 | |
|---|---|---|---|
| **P1** | [LC-0030 - Substring with Concatenation of All Words](05%20-%20%E9%AB%98%E9%98%B6%E7%AA%97%E5%8F%A3%E7%BB%84%E5%90%88%E4%B8%8E%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96%20%28Advanced%20Windows%29/01%20-%20%E6%8C%89%E5%8D%95%E8%AF%8D%E9%95%BF%E5%BA%A6%E5%88%86%E7%BB%84%E7%9A%84%E7%AA%97%E5%8F%A3/01%20-%20LC-0030%20-%20Substring%20with%20Concatenation%20of%20All%20Words) | H |  |
**02 - Complement Window 问题转化**

| | 题 | 难度 | |
|---|---|---|---|
| **P1** | [LC-1658 - Minimum Operations to Reduce X to Zero](05%20-%20%E9%AB%98%E9%98%B6%E7%AA%97%E5%8F%A3%E7%BB%84%E5%90%88%E4%B8%8E%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96%20%28Advanced%20Windows%29/02%20-%20Complement%20Window%20%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96/01%20-%20LC-1658%20-%20Minimum%20Operations%20to%20Reduce%20X%20to%20Zero) | M | （🆕 新增） |
| **P2** | [LC-2516 - Take K of Each Character From Left and Right](05%20-%20%E9%AB%98%E9%98%B6%E7%AA%97%E5%8F%A3%E7%BB%84%E5%90%88%E4%B8%8E%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96%20%28Advanced%20Windows%29/02%20-%20Complement%20Window%20%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96/02%20-%20LC-2516%20-%20Take%20K%20of%20Each%20Character%20From%20Left%20and%20Right) | M | （🆕 我补充） |
**03 - 连续空隙的定长窗口**

| | 题 | 难度 | |
|---|---|---|---|
| **P2** | [LC-3439 - Reschedule Meetings for Maximum Free Time I](05%20-%20%E9%AB%98%E9%98%B6%E7%AA%97%E5%8F%A3%E7%BB%84%E5%90%88%E4%B8%8E%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96%20%28Advanced%20Windows%29/03%20-%20%E8%BF%9E%E7%BB%AD%E7%A9%BA%E9%9A%99%E7%9A%84%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3/01%20-%20LC-3439%20-%20Reschedule%20Meetings%20for%20Maximum%20Free%20Time%20I) | M |  |

### [06 - 跨专题与低优先级存档 (Archive)](06%20-%20%E8%B7%A8%E4%B8%93%E9%A2%98%E4%B8%8E%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E5%AD%98%E6%A1%A3%20%28Archive%29/README.md)

**01 - 连续字符段与贪心**

| | 题 | 难度 | |
|---|---|---|---|
| **P2** | [LC-3499 - Maximize Active Section with Trade I](06%20-%20%E8%B7%A8%E4%B8%93%E9%A2%98%E4%B8%8E%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E5%AD%98%E6%A1%A3%20%28Archive%29/01%20-%20%E8%BF%9E%E7%BB%AD%E5%AD%97%E7%AC%A6%E6%AE%B5%E4%B8%8E%E8%B4%AA%E5%BF%83/01%20-%20LC-3499%20-%20Maximize%20Active%20Section%20with%20Trade%20I) | M |  |

📦 = 文件夹里有 `_neetcode/`，保存 NeetCode 版本的原始题面和解法（同一道题，不单独占位置）。

## 五、跨专题引用

| 题 | 主归属 | 和本专题的关系 |
|---|---|---|
| **LC-0239** Sliding Window Maximum | [18-monotonic-fuck-you/monotonic-queue](<../18-monotonic-fuck-you (单调栈、单调队列)/04 - 单调队列与滑动窗口/01 - 固定窗口最大值/01 - LC-0239 - Sliding Window Maximum>) | 本专题 Level 05 的签名题，**P0 必练** |
| **LC-0121** Best Time to Buy and Sell Stock | [12-dynamic-programming/stock-series](<../12-dynamic-programming (动态规划)/07 - 股票与状态机 DP/01 - 单次与无限次交易/01 - LC-0121 - Best Time to Buy and Sell Stock>) | 它是 running minimum 不是窗口。本目录原有的 NC 版已按「LC/NC 重复只留 LeetCode」的规则移除 |
| **LC-1695** Maximum Erasure Value | [02-two-pointers/08 存档](../02-two-pointers%20%28%E5%8F%8C%E6%8C%87%E9%92%88%29/08%20-%20%E8%B7%A8%E4%B8%93%E9%A2%98%E4%B8%8E%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E5%AD%98%E6%A1%A3%20%28Archive%29/02%20-%20Sliding%20Window%20%E4%BA%A4%E5%8F%89%E9%A2%98/01%20-%20LC-1695%20-%20Maximum%20Erasure%20Value) | **核心确实是滑动窗口**（窗口内元素互不相同的最大和），等于 LC-0003 的「求和版」。它在双指针专题是历史遗留 |
| **LC-0219** Contains Duplicate II | [01-arrays-hashing/06 低优先级](../01-arrays-hashing%20%28%E6%95%B0%E7%BB%84%E3%80%81%E5%93%88%E5%B8%8C%E8%A1%A8%29/06%20-%20%E4%BD%8E%E4%BC%98%E5%85%88%E7%BA%A7%E4%B8%8E%E8%B7%A8%E4%B8%93%E9%A2%98%E9%A2%98%E7%9B%AE/01%20-%20LC-0219%20-%20Contains%20Duplicate%20II) | 定长窗口 + 哈希集合，可以当 Level 01 的附加练习 |

这四道都**没有**在本专题重复创建文件夹。

## 六、第二轮独立审核结果

第一轮清单的 15 个 Pattern（定长求和、定长频率、最长无重复、至多 K 种、至多 K 次修改、最短合法、频率覆盖、预算约束、子数组计数、Exactly K、补集窗口、窗口最大值、单调队列、排序后窗口、offset 单词窗口）**全部已覆盖**。在此基础上我补了 4 道，每道都填一个真空白：

| 题 | 难度 | 填补的缺口 | 为什么不是重复 | 位置 | |
|---|---|---|---|---|---|
| **LC-0862** Shortest Subarray with Sum at Least K | H | **数组有负数时窗口单调性失效怎么办** | 第一轮只在 0209 的笔记里提了一句「负数不行」，却没有一道题教怎么办。它用前缀和 + 单调队列给出答案 | 03/01 | P1 |
| **LC-1052** Grumpy Bookstore Owner | M | 定长窗口的 **baseline + delta 分解** | 0643/2461/1423 维护的都是原数组的聚合；这题窗口维护的是**派生数组**，且答案要拆成「不变部分 + 窗口内增量」 | 01/01 | P1 |
| **LC-2401** Longest Nice Subarray | M | 窗口状态可以是 **bitmask** 而不是频率表 | 和 0003 同一个骨架，但状态压成一个整数、移除用 XOR。说明「窗口状态」是个开放设计 | 02/01 | P2 |
| **LC-2516** Take K of Each Character | M | 补集窗口的第三种形态（固定**每类上限**）| 1423 固定长度、1658 固定和，这题固定的是「每种字符的上限」，三题凑齐才算讲透补集转化 | 06/02 | P2 |

**评估过但没有加入的候选**（避免无限扩张）：

| 候选 | 为什么不加 |
|---|---|
| LC-1248 Count Number of Nice Subarrays | 把奇数映射成 1 之后就是 LC-0930，技巧完全重复 |
| LC-2024 Maximize the Confusion of an Exam | 等于对 T/F 各跑一次 LC-1004 |
| LC-1456 Maximum Number of Vowels in a Substring | LC-0643 换个计数对象，零增量 |
| LC-2958 Longest Subarray With at Most K Frequency | LC-0904 的频率版，和 02/01 高度重复 |
| LC-1151 Minimum Swaps to Group All 1's Together | 定长窗口数 0 的个数，和 1052 同构 |
| LC-0340 Longest Substring with At Most K Distinct | LC-0159 已经是它 K=2 的特例，README 里说明即可 |

## 七、三层刷题清单

### A. P0 最小核心题库（10 道 + 1 道索引）—— 两周内要面试就只刷这些

```
0643 → 0567 → 0438 → 0003 → 0904 → 1004 → 0424 → 0209 → 0076 → 0713 → 0239(索引)
```

顺序即依赖：定长 → 定长+频率 → 最长合法 → 最短满足 → 计数 → 单调队列。**0076 是其中最难也最值钱的一道。**

### B. P0 + P1 完整标准面试准备（22 道）

在 A 的基础上补：

```
2461 → 1423 → 1052 → 1208 → 1838 → 0862 → 0930 → 0992 → 1358 → 1438 → 1658 → 0030
```

目标不是数量，而是**每种窗口的不变量都能当场讲出来**，被追问「为什么 left 不用回退」答得上。

### C. P2 扩展与存档（6 道）

```
0187 → 0159 → 2401 → 2516 → 3439 → 3499
```

0159 和 0904 是同一个算法（只是字符串版），2401 / 2516 是状态设计的趣味扩展，3439 和 3499 的主算法已经不是滑动窗口了。

## 八、推荐学习顺序（八步）

| 步 | 做什么 | 目标 |
|---|---|---|
| 1 | 0643 → 2461 → 1052 | 定长窗口骨架；理解「窗口状态」可以是任何东西 |
| 2 | 0567 → 0438 | 频率表匹配；两题同一个算法 |
| 3 | 0003 → 0904 → 1004 → 0424 | **最长合法**：不合法才收缩；424 的 maxFreq 要能解释 |
| 4 | 0209 → 0076 | **最短满足**：合法才收缩、收缩前更新；while 条件和第 3 步相反 |
| 5 | 0713 → 0930 → 0992 → 1358 | **计数**：一次加一批；exactly = atMost(K) - atMost(K-1) |
| 6 | 0239(索引) → 1438 → 0862 | **单调队列**：极值无法增量维护；负数场景 |
| 7 | 1423 → 1658 → 2516 | **补集转化**三连，固定长度 / 固定和 / 固定上限 |
| 8 | 1208 → 1838 → 0030 → 3439 | 预算约束、排序后窗口、offset 分组、gap 数组 |
