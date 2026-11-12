# Level 1 · 02 Kadane 与连续子数组 DP

## 核心定义 —— 本章唯一需要记住的状态定义

> ## `cur` = **以当前元素结尾**的最优值

**不是**「前 i 个里的最优值」。这个区别是整章的关键：
「以 i 结尾」保证了**连续性**，而「前 i 个里的最优」丢掉了「必须连在一起」这个信息。

## Kadane 模板
```python
cur = best = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)        # 要么接上前面，要么从我重新开始
    best = max(best, cur)
return best
```

**`max(x, cur + x)` 的含义**：
前面那段的和如果是负的（`cur < 0`），接上它只会拖累我 ⟹ 不如从我自己重新开始。
等价写法：`cur = max(0, cur) + x`。

**`best` 的初值必须是 `nums[0]` 而不是 0** —— 否则全是负数的数组会返回 0（错）。

## 02 小节：乘积需要**两个**状态

LC-0152 Maximum Product Subarray 的关键：**负数乘负数变正数**。
所以「当前最大乘积」可能来自「上一步的**最小**乘积 × 一个负数」。

```python
cur_max, cur_min = nums[0], nums[0]
for x in nums[1:]:
    cands = (x, cur_max * x, cur_min * x)
    cur_max, cur_min = max(cands), min(cands)      # ★ 必须同时更新
    best = max(best, cur_max)
```

**两个坑**：
1. **必须同时赋值**。先更新 `cur_max` 再算 `cur_min` 时，`cur_min` 会读到新的 `cur_max`。
2. **必须把 `x` 自己放进候选**（相当于「从我重新开始」），否则遇到 0 之后无法重启。

> 这是本专题经验②的典型例子：**一个状态不够，就多开一个。**

LC-1567（最长正积子数组）同理，但维护的是**长度**而不是乘积：
`pos_len` / `neg_len` 两个状态，遇到 0 就全部重置。

## 题目

| # | 题 | 优先级 | 关键点 |
|---|---|---|---|
| 01/01 | LC-0053 Maximum Subarray | **P0** | Kadane 母题；`best` 初值不能是 0 |
| 01/02 | LC-0918 Maximum Sum Circular Subarray | P1 | **环形**，见下 |
| 01/03 | LC-3434 Maximum Frequency After Subarray Operation | P2 | 对每个目标值各跑一次 Kadane |
| 02/01 | LC-0152 Maximum Product Subarray | **P0** | 维护 max 和 min 两个状态 |
| 02/02 | LC-1567 Maximum Length of Subarray With Positive Product | P2 | 维护正积长度和负积长度 |

## LC-0918 环形最大子数组（两种情况）
答案是以下两者的较大值：
1. **不跨越边界**：就是普通 Kadane 的 `max_sum`。
2. **跨越边界**：等价于「**总和 − 中间那段最小子数组和**」⟹ 再跑一次「最小子数组和」的 Kadane。

```python
return max(max_sum, total - min_sum)
```

**关键边界**：如果**全是负数**，`min_sum == total`，上式第二项会是 0
（相当于「什么都不选」），但题目要求子数组**非空** ⟹ 这时答案就是 `max_sum`。
```python
if min_sum == total: return max_sum
```
**漏掉这个判断是本题唯一的坑。**

## 复杂度
全部 **O(n) 时间、O(1) 空间**。

## 和滑动窗口的区别
| | Kadane | 滑动窗口 |
|---|---|---|
| 适用 | 数组**可以有负数** | 通常要求**非负**（和才单调） |
| 维护 | 「以 i 结尾」的最优值 | 一个合法区间 `[left, right]` |
| 例子 | LC-0053、LC-0152 | 见 [03-sliding-window](<../../03-sliding-window (滑动窗口)/>) |

**有负数时滑动窗口的「和太大就收缩」前提崩掉**，必须用 Kadane 或前缀和。
这和 LC-0862 的道理一样。

## 常见错误
- `best` 初值设成 0 ⟹ 全负数数组返回 0。
- LC-0152 没有同时更新 max / min。
- LC-0152 忘记把 `x` 自己放进候选（遇 0 后无法重启）。
- LC-0918 漏掉「全负数」的特判。

## 复习时的 Pattern Recognition
> 「最大/最小**连续**子数组的和/积/长度」
> → Kadane。状态一定是「**以 i 结尾**的最优值」，不是「前 i 个里的最优」。
