# 05 - 高阶窗口组合与问题转化 (Advanced Windows)

## 核心定义

题面**不长得像滑动窗口**，需要先做一步转化，才能套上前面几层的模板。
本层练的不是新模板，而是**「怎么把题翻译成窗口」**。

## 三种转化

### 1. Offset 分组（LC-0030）

所有 words 长度相同（设为 L）⇒ 合法起点必然落在 `i % L` 相同的位置上。
于是按 `offset = 0 .. L-1` 分 L 组，**每组内部以「一个单词」为单位做变长窗口**，
每组 O(n/L) 步，总共 O(n)。
不分组的话就只能对每个起点重新扫一遍，退化成 O(n·m·L)。

### 2. Complement（补集）转化 —— 三道题一起记

**「从两端拿走」⟺「中间留下一段连续区间」**。差别只在「固定了什么」：

| 题 | 固定的是 | 中间窗口要求 | 用哪种窗口 |
|---|---|---|---|
| **LC-1423**（在 Level 01）| **长度**（留 n-k 个）| 和最小 | 定长窗口 |
| **LC-1658** | **和**（留下和为 total-x）| 最长 | 变长窗口 |
| **LC-2516** | **每种字符的上限** | 最长 | 变长窗口 |

### 3. Gap Array（LC-3439）

会议之间的空隙组成一个数组；移动最多 k 个会议 ⟺ 合并**连续的 k+1 个 gap**。
于是变成「gap 数组上长度 k+1 的定长窗口最大和」。
本层最值钱的一步是**构造 gap 数组**（别忘了首尾两段空隙）。

## Loop Invariant

转化之后就回到前几层的不变量，没有新的。**转化本身才是考点。**

## Python 模板（LC-0030 的分组骨架）

```python
L, m = len(words[0]), len(words)
need = Counter(words)
for offset in range(L):                      # ! L 个起点分组
    win = Counter()
    count = 0
    left = offset
    for right in range(offset, len(s) - L + 1, L):
        w = s[right:right + L]
        if w not in need:                    # 不合法的单词 → 整个窗口作废
            win.clear(); count = 0; left = right + L
            continue
        win[w] += 1; count += 1
        while win[w] > need[w]:              # ! 某个词超量 → 从左边吐
            win[s[left:left + L]] -= 1
            count -= 1
            left += L
        if count == m:
            res.append(left)
            win[s[left:left + L]] -= 1; count -= 1; left += L
```

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P1** | [LC-0030 - Substring with Concatenation of All Words](01%20-%20%E6%8C%89%E5%8D%95%E8%AF%8D%E9%95%BF%E5%BA%A6%E5%88%86%E7%BB%84%E7%9A%84%E7%AA%97%E5%8F%A3/01%20-%20LC-0030%20-%20Substring%20with%20Concatenation%20of%20All%20Words) | H | Offset 分组 + 以单词为单位的窗口 |
| **P1** | [LC-1658 - Minimum Operations to Reduce X to Zero](02%20-%20Complement%20Window%20%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96/01%20-%20LC-1658%20-%20Minimum%20Operations%20to%20Reduce%20X%20to%20Zero) | M | 固定**和**的补集窗口 |
| **P2** | [LC-2516 - Take K of Each Character From Left and Right](02%20-%20Complement%20Window%20%E9%97%AE%E9%A2%98%E8%BD%AC%E5%8C%96/02%20-%20LC-2516%20-%20Take%20K%20of%20Each%20Character%20From%20Left%20and%20Right) | M | 固定**每类上限**的补集窗口 |
| **P2** | [LC-3439 - Reschedule Meetings for Maximum Free Time I](03%20-%20%E8%BF%9E%E7%BB%AD%E7%A9%BA%E9%9A%99%E7%9A%84%E5%AE%9A%E9%95%BF%E7%AA%97%E5%8F%A3/01%20-%20LC-3439%20-%20Reschedule%20Meetings%20for%20Maximum%20Free%20Time%20I) | M | 构造 gap 数组，再套定长窗口 |

## 常见错误与边界

- 0030：忘了「遇到不在 words 里的单词要整段作废」；或者没按 offset 分组。
- 1658：`target = total - x` 可能为负（直接 -1）或为 0（空窗口合法，答案是 n）。
- 2516：先判「某种字符总数 < k」⇒ -1；上限可能为 0。
- 3439：gap 数组别漏掉第一个会议前和最后一个会议后的空隙。
- 看到「从两端操作」就该条件反射想到补集；真去模拟两端选择是指数级的。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1234 Replace the Substring for Balanced String](<./02 - Complement Window 问题转化/03 - LC-1234 - Replace the Substring for Balanced String>) | `05 - 高阶窗口组合与问题转化 (Advanced Windows)/02 - Complement Window 问题转化` | 看窗口外面：outside[c] <= n/4 全部成立 ⟹ 合法；最短窗口模板「合法就收缩」 | LC-1658 式补集窗口 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
