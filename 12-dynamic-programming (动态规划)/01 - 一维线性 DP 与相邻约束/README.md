# Level 1 · 01 一维线性 DP 与相邻约束

## 核心定义
状态只有一个下标：`dp[i]` = 考虑到第 i 个位置时的最优值。
转移只看**前面常数个**状态 ⟹ 可以滚动成几个变量，O(1) 空间。

## 三个小节的状态定义

| 小节 | 状态 | 转移 |
|---|---|---|
| 01 Fibonacci 型 | `dp[i]` = 到第 i 级的方法数 | `dp[i] = dp[i-1] + dp[i-2]` |
| 02 相邻不能同选 | `dp[i]` = 前 i 个里的最大收益 | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| 03 一维决策 | `dp[i]` = 到位置 i 的最小代价 | 枚举「上一步从哪来」取 min |

**02 的转移是本章的核心**：`max(不选我, 选我)`。
「选我」时必须跳过 `i-1`，所以用 `dp[i-2]`。

## 题目

| # | 题 | 优先级 | 关键点 |
|---|---|---|---|
| 01/01 | LC-0509 Fibonacci Number | P1 | 最简单的线性递推；滚动两个变量 |
| 01/02 | LC-0070 Climbing Stairs | **P0** | **就是 Fibonacci**（`dp[i] = dp[i-1] + dp[i-2]`） |
| 02/01 | LC-0198 House Robber | **P0** | `max(dp[i-1], dp[i-2] + nums[i])`，整章的母题 |
| 02/02 | LC-0213 House Robber II | P1 | **环形**：见下 |
| 02/03 | LC-0740 Delete and Earn | P1 | **先转化**：见下 |
| 03/01 | LC-0746 Min Cost Climbing Stairs | **P0** | 和 0198 同形，只是取 min；注意「可以从 0 或 1 出发」 |
| 03/02 | LC-0983 Minimum Cost For Tickets | P1 | 三种票 ⟹ 三个候选取 min；只在旅行日更新 |
| 03/03 | LC-0343 Integer Break | P2 | `dp[i] = max(j * (i-j), j * dp[i-j])`，两种拆法都要考虑 |

## LC-0213 环形的处理（一个通用技巧）
首尾相邻 ⟹ **第一间和最后一间不能同时选**。
把问题拆成**两个线性子问题**，各跑一次 LC-0198：
```python
return max(rob_linear(nums[:-1]),    # 不要最后一间
           rob_linear(nums[1:]))     # 不要第一间
```
**边界**：`len(nums) == 1` 时上面两个切片都是空的，要特判返回 `nums[0]`。

> 「环形 ⟹ 拆成两个线性」这个技巧还会在 LC-0918（环形最大子数组）里再出现一次。

## LC-0740 的转化（本章最有价值的一步）
题意是「删一个数 x 会连带删掉所有 x-1 和 x+1」。
**先按值聚合**：`points[v] = v * count(v)`。
于是问题变成「在值轴上，相邻的值不能同时选」⟹ **就是 LC-0198**。

```python
points = [0] * (max(nums) + 1)
for v in nums: points[v] += v
# 然后对 points 跑一次 House Robber
```

**这类「先转化再套模板」的题，难点全在转化，不在 DP。**

## 空间优化
所有题都只依赖前两个状态 ⟹ 两个变量即可：
```python
prev2, prev1 = 0, 0
for x in nums:
    prev2, prev1 = prev1, max(prev1, prev2 + x)
return prev1
```
**写成同时赋值**可以避免「先更新了 prev1 导致 prev2 读到新值」的经典 bug。

## 复杂度
全部 O(n) 时间、**O(1) 空间**（LC-0740 是 O(max(nums)) 空间）。

## 常见错误
- LC-0213 忘记 `len == 1` 的特判。
- LC-0746 的终点理解错：可以**跨过**最后一级直接到顶，所以答案是 `min(dp[n-1], dp[n-2])`。
- 空间优化时没用同时赋值，`prev2` 读到了被更新过的 `prev1`。
- LC-0740 直接在原数组上做（必须先按值聚合）。

## 复习时的 Pattern Recognition
> 「有多少种走法」「相邻的不能都选」「到第 i 步的最小花费」
> → 一维线性 DP。先写 `dp[i] = ?`，只看前面一两个状态。
