# Level 1 · 01 跳跃、可达性与区间覆盖

## 核心定义 —— 一个骨架，四道题

> ## 维护 **`reach`** = 「目前为止能覆盖到哪里」，一路扫描，**不够就付代价**。

```python
reach = 初始值
for 每个位置 / 元素:
    reach = 扩展(reach, 当前元素)
    if 到了当前层的边界 / 发现缺口:
        付一次代价（跳一次 / 用一个片段 / 补一个数）
```

| 题 | `reach` 的含义 | 扩展方式 | 不够时 |
|---|---|---|---|
| **LC-0055** Jump Game | 能走到的最远**下标** | `max(reach, i + nums[i])` | `i > reach` ⟹ **False** |
| **LC-0045** Jump Game II | 同上，但要**分层** | 同上 | 走到层边界 ⟹ `jumps += 1` |
| **LC-1024** Video Stitching | 片段能覆盖到的**最右端** | `max(curr_far, reach[s])` | 推不动 ⟹ **-1** |
| **LC-0330** Patching Array | 能表示出的**最大整数** | `reach += nums[i]` | **补 `reach+1`，范围翻倍** |

## 01 - 最远可达位置与可行性

### LC-0055 Jump Game
```python
reach = 0
for i, x in enumerate(nums):
    if i > reach: return False      # 走不到 i，后面更走不到
    reach = max(reach, i + x)
return True
```
**`i > reach` 就可以立刻返回 False** —— 因为 `reach` 是单调不减的，之后只会更差。

### LC-0330 Patching Array（本节的高潮）
不变量：**`[1, reach]` 里每个整数都能被表示出来**。

- `nums[i] <= reach + 1` ⟹ **能接上**（没有缺口）⟹ `reach += nums[i]`。
  为什么能接上：`[1, reach]` 都能表示，加上 `nums[i]` 就能表示
  `[nums[i], reach + nums[i]]`，两段**连起来**的前提正是 `nums[i] <= reach + 1`。
- 否则 ⟹ `reach + 1` 表示不出来 ⟹ **必须补一个数**。

**补什么最优？补 `reach + 1`。**
- 必须能表示 `reach + 1` ⟹ 补的数不能超过 `reach + 1`。
- 补 `x` 之后范围变成 `reach + x` ⟹ **x 越大越好** ⟹ 取 `reach + 1`。
- ⟹ 范围**直接翻倍**变成 `2 * reach + 1` ⟹ 所以补的次数是 **O(log n)**。∎

**溢出提醒**：`reach` 可能超 32 位（n 可达 2³¹−1），C++/Java 要用 long。

## 02 - 最少跳跃与最远覆盖

### LC-0045 Jump Game II —— 本质是**不用队列的 BFS 分层**
```python
jumps = curr_end = curr_far = 0
for i in range(len(nums) - 1):        # ★ 只到 n-2
    curr_far = max(curr_far, i + nums[i])
    if i == curr_end:                 # 这一层走完了
        jumps += 1
        curr_end = curr_far
return jumps
```
- `curr_end` = 当前这一层（跳 jumps 次）能覆盖到的最右端
- `curr_far` = 再跳一次最远能到哪
- **循环只到 `n - 2`**：站在终点上不需要再跳了。这是最容易多算一次的地方。

### LC-1024 Video Stitching —— LC-0045 换了层皮
把片段 `[s, e]` 看成「从 s 出发最远能跳到 e」⟹ 完全是 LC-0045。

**两个差别**：
- **可能不可达** ⟹ 要判 `curr_far <= i` 就返回 -1（LC-0045 题目保证可达）。
- 覆盖的是区间 `[0, time]`，循环到 `time` 为止。

> 这个「区间覆盖 ⟹ 跳跃」的转化还能用在 **LC-1326**（水龙头 `[i-r, i+r]`）。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0055 Jump Game | **P0** |
| 01/02 | LC-0330 Patching Array | P2（第二轮新增） |
| 02/01 | LC-0045 Jump Game II | **P0** |
| 02/02 | LC-1024 Video Stitching | P1 |

## 复杂度
全部 **O(n) 时间、O(1) 空间**（LC-1024 的 reach 数组版是 O(time) 空间；
LC-0330 的补数次数是 O(log n)）。

## 常见错误
- **LC-0045 的 `farthest` 少加 `i`** ⟹ `r` 不前进 ⟹ **死循环**。
  （本仓库原有代码就犯了这个错，已修，详见根 README 第六节。）
- LC-0045 循环跑到 `n-1` ⟹ 多算一跳。
- LC-1024 忘了判不可达。
- LC-0330 补的数不是 `reach + 1`（补更大的会留下缺口，补更小的浪费）。
- LC-0055 用 DP 而不是贪心（能过但 O(n²)）。

## 复习时的 Pattern Recognition
> 「能不能到终点」「最少跳几次 / 最少用几个区间覆盖」「最少补几个数」
> → 维护 `reach`，一路扫描。先问：**reach 代表什么？不够时付什么代价？**
