# 04 - 子数组与子串计数 (Counting Windows)

## 核心定义

不是找一个最优窗口，而是**数出所有合法的连续区间**。
做法仍然是维护一个合法窗口，但答案从 `max/min(长度)` 换成**一次累加一批**。

## 决定性观察（本层全部的内容）

1. **约束是「至多」时**：合法窗口 `[left, right]` 的**所有后缀**都合法
   （去掉左边的元素只会让约束更宽松），所以以 right 结尾的合法子数组恰好
   **`right - left + 1`** 个，一次加完。
2. **约束是「至少」时**方向相反：窗口越长越容易满足，所以要找**最大的**合法左端 left，
   起点取 `0 .. left` 都合法，一次加 **`left`（或 left+1，看 left 的定义）**。
3. **「恰好 K」不单调**，不能直接数。但
   **`exactly(K) = atMost(K) - atMost(K-1)`** —— 两个单调的东西相减得到不单调的那个。

## 三种答案更新方式的完整对照

| 层 | 答案更新 |
|---|---|
| 02 最长合法 | `best = max(best, right - left + 1)` |
| 03 最短满足 | `best = min(best, right - left + 1)`（收缩前）|
| 04 计数 · 至多 | `ans += right - left + 1` |
| 04 计数 · 至少 | `ans += left` |

## Python 模板

```python
# atMost(k)：统计满足「某个单调的至多约束」的子数组个数
def at_most(k):
    if k < 0:                      # ! exactly 相减时会传进 -1，必须守住
        return 0
    left = 0
    res = 0
    for right, x in enumerate(nums):
        add(x)
        while state > k:           # 不合法就收缩
            remove(nums[left]); left += 1
        res += right - left + 1    # ! 一次加一批
    return res

exactly_k = at_most(k) - at_most(k - 1)
```

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0713 - Subarray Product Less Than K](01%20-%20%E6%AD%A3%E6%95%B0%E4%B9%98%E7%A7%AF%E4%B8%8E%E6%89%B9%E9%87%8F%E8%AE%A1%E6%95%B0/01%20-%20LC-0713%20-%20Subarray%20Product%20Less%20Than%20K) | M | `ans += right-left+1` 的入门；**必须特判 k <= 1** |
| **P1** | [LC-0930 - Binary Subarrays With Sum](02%20-%20Exactly%20K%20%E4%B8%8E%20At%20Most%20K/01%20-%20LC-0930%20-%20Binary%20Subarrays%20With%20Sum) | M | exactly = atMost(K) - atMost(K-1)；也可前缀和 + 哈希表 |
| **P1** | [LC-0992 - Subarrays with K Different Integers](02%20-%20Exactly%20K%20%E4%B8%8E%20At%20Most%20K/02%20-%20LC-0992%20-%20Subarrays%20with%20K%20Different%20Integers) | H | 同一恒等式，atMost 换成「至多 K 种」 |
| **P1** | [LC-1358 - Number of Substrings Containing All Three Characters](03%20-%20%E6%BB%A1%E8%B6%B3%E5%85%A8%E9%83%A8%E5%AD%97%E7%AC%A6%E7%BA%A6%E6%9D%9F%E7%9A%84%E8%AE%A1%E6%95%B0/01%20-%20LC-1358%20-%20Number%20of%20Substrings%20Containing%20All%20Three%20Characters) | M | 约束是「**至少**包含」⇒ 一次加 `left` |

## 常见错误与边界

- `at_most(-1)` 没有返回 0（0930 的 goal 可以是 0）。
- 0713 没特判 `k <= 1`，left 会越过 right，算出负数。
- 把「至少」类题目也写成 `ans += right - left + 1`（方向反了）。
- 正确性都依赖元素非负 / 正数；0930 的前缀和 + 哈希表解法没有这个限制，更通用。

## 与相邻家族的区别

计数窗口的骨架和 Level 02 完全一样（不合法就收缩），
**只有最后一行不同**。看到「有多少个子数组 / 子串」就把 max 换成累加。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1248 Count Number of Nice Subarrays](<./02 - Exactly K 与 At Most K/03 - LC-1248 - Count Number of Nice Subarrays>) | `04 - 子数组与子串计数 (Counting Windows)/02 - Exactly K 与 At Most K` | 奇数→1 偶数→0 后就是 LC-0930；exactly(k) = atMost(k) − atMost(k−1) | 三种标准解法全可用 |
| [LC-2537 Count the Number of Good Subarrays](<./02 - Exactly K 与 At Most K/04 - LC-2537 - Count the Number of Good Subarrays>) | `04 - 子数组与子串计数 (Counting Windows)/02 - Exactly K 与 At Most K` | 「至少 k」模板：while pairs >= k: res += n − r；数对数增量 += cnt[x] | 与 atMost 模板镜像 |
| [LC-2962 Count Subarrays Where Max Element Appears at Least K Times](<./02 - Exactly K 与 At Most K/05 - LC-2962 - Count Subarrays Where Max Element Appears at Least K Times>) | `04 - 子数组与子串计数 (Counting Windows)/02 - Exactly K 与 At Most K` | 先读对题：全局最大值 M ⟹ 0/1 数组「1 的个数 ≥ k」；贡献 = pos[c−k] + 1 | LC-2537 同模板 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
