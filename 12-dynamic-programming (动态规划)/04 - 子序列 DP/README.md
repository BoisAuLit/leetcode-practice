# Level 1 · 04 子序列 DP

## 核心定义
子序列**不要求连续**（和 Level 1 `02` 的连续子数组相对）。
状态通常是「**以 i 结尾**的最优值」，转移要**往回看所有 j < i**
⟹ 天然是 O(n²)，除非能用额外结构优化。

## LIS 的两种写法（必须都会）

### ① O(n²) DP
```python
dp = [1] * n                     # dp[i] = 以 i 结尾的 LIS 长度
for i in range(n):
    for j in range(i):
        if nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)
return max(dp)
```

### ② O(n log n) 贪心 + 二分
```python
tails = []                       # tails[k] = 长度为 k+1 的递增序列的最小结尾
for x in nums:
    i = bisect_left(tails, x)    # ★ 严格递增用 bisect_left
    if i == len(tails): tails.append(x)
    else:                tails[i] = x
return len(tails)
```

**`tails` 的含义**：第 k 个位置存「所有长度为 k+1 的递增子序列中，**结尾最小**的那个值」。
结尾越小，后面越容易接上去 —— 这就是贪心的依据。
**`tails` 本身不是一个合法的 LIS**，只有它的**长度**是答案。

**bisect_left vs bisect_right**：
- **严格**递增 ⟹ `bisect_left`（相等的会被替换掉，长度不增长）
- **非严格**（允许相等）⟹ `bisect_right`

## 题目

| # | 题 | 优先级 | 关键点 |
|---|---|---|---|
| 01/01 | LC-0300 Longest Increasing Subsequence | **P0** | 两种写法都要会 |
| 01/02 | LC-0673 Number of LIS | P2 | **再开一个 `cnt[]`**，见下 |
| 01/03 | LC-0354 Russian Doll Envelopes | P2 | **排序降维**，见下 |
| 02/01 | LC-0368 Largest Divisible Subset | P1 | 先排序，然后「能整除」就是偏序关系 ⟹ 就是 LIS |
| 02/02 | LC-1048 Longest String Chain | P1 | 按长度排序 + 哈希表存「删一个字符后的前驱」 |
| 02/03 | LC-3201 Valid Subsequence I | P2 | 奇偶模式；状态是「上一个的奇偶」 |
| 02/04 | LC-3202 Valid Subsequence II | P2 | 推广到 mod k；`dp[余数][上一个余数]` |

## LC-0673：最优值 + 方案数

```python
if dp[j] + 1 >  dp[i]:  dp[i] = dp[j] + 1;  cnt[i] = cnt[j]    # 更优 ⟹ 计数【重置】
elif dp[j] + 1 == dp[i]: cnt[i] += cnt[j]                       # 同优 ⟹ 计数【累加】
```

> **「更优就重置、同优才累加」** —— 这两种情况必须分开写。
> 写成一个 `+=` 就全错了。这是「最优值 + 方案数」类 DP 的通用骨架。

**常见错解**：用「`dp` 的最大值出现了几次」当答案。错 —— 同一个结尾可能对应多条路径。

## LC-0354：排序降维（两维 LIS）

排序规则**必须是**：`w` 升序，`w` 相同时 `h` **降序**。
```python
envelopes.sort(key=lambda e: (e[0], -e[1]))
```

**为什么 `h` 要降序**：题目要求**严格**大于 ⟹ `w` 相同的信封不能互相嵌套。
`h` 升序时 `[(1,2),(1,3)]` 的 h 序列是 `[2,3]`，LIS 会算成两层 —— 但它们 w 相同，套不进去。
`h` 降序后变成 `[3,2]`，LIS 只取一个，正好排除非法情形。

然后在 `h` 上跑**严格递增**的 O(n log n) LIS（`bisect_left`）。
n 可达 10⁵，**O(n²) 会 TLE**，所以这题必须用二分版。

> 「排序消一维 + 一维 LIS」还能推广到三维（LC-1691）。

## 和连续子数组（Level 1 `02`）的对照

| | 子序列（本章） | 连续子数组（Level 1 `02`） |
|---|---|---|
| 连续吗 | 不要求 | 要求 |
| 转移 | 往回看**所有** j < i | 只看 `i-1` |
| 复杂度 | O(n²) 或 O(n log n) | **O(n)** |
| 空间 | O(n) | O(1) |

## 复杂度
| 题 | 时间 |
|---|---|
| LC-0300 | O(n²) 或 **O(n log n)** |
| LC-0673 | O(n²)（O(n log n) 要树状数组，实现重得多） |
| LC-0354 | **必须 O(n log n)** |
| LC-0368 / LC-1048 | O(n²) / O(n · L²) |

## 常见错误
- LIS 二分版用了 `bisect_right`（变成非严格递增）。
- 以为 `tails` 数组本身是一个合法的 LIS（它不是，只有长度对）。
- LC-0673 把「重置」和「累加」合并成一个 `+=`。
- LC-0354 把 `h` 升序排。
- LC-0354 用 O(n²) ⟹ TLE。
- LC-0368 忘了先排序（整除关系需要有序才能单向转移）。

## 复习时的 Pattern Recognition
> 「最长递增/满足某偏序的**子序列**」「这样的子序列有几个」
> → 子序列 DP。状态「以 i 结尾」，往回看所有 j。
> 二维就先**排序降维**。
