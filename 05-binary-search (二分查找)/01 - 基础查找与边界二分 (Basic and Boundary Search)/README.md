# Level 1 · 01 基础查找与边界二分 (Basic and Boundary Search)

## 核心定义
在**有序**序列上，用一次 O(1) 的比较丢掉一半搜索空间。
本章把「找到某个值」和「找到某个**边界**」彻底分开 —— 后者才是面试的重点。

## 决定性观察
1. **能丢一半的理由**：`nums[mid] < target` + 数组有序 ⟹ `nums[0..mid]` 全都 < target，
   它们都不可能是答案。有序性是本章的前提；后面几章会放宽它。
2. **边界查找比精确查找更常用**：现实中更多的问题是
   「第一个 >= target 的位置」「第一个 True 的位置」，而不是「存不存在」。
3. **谓词视角统一一切**：把 `nums[i] >= target` 看成一个布尔数组，
   它一定形如 `F F F T T T`。所有边界题都是在找这个分界点。

## Lower Bound vs Upper Bound（必须分清）

| | 定义 | Python | 不变量 |
|---|---|---|---|
| **Lower Bound** | 第一个 `nums[i] >= target` 的下标 | `bisect_left` | `[0, lo)` 全 `< target` |
| **Upper Bound** | 第一个 `nums[i] > target` 的下标 | `bisect_right` | `[0, lo)` 全 `<= target` |

```python
def lower_bound(nums, target):            # bisect_left
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target: hi = mid
        else:                   lo = mid + 1
    return lo

def upper_bound(nums, target):            # bisect_right
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > target: hi = mid
        else:                  lo = mid + 1
    return lo
```

**最常见的误解**：`upper_bound(target)` 返回的**不是**「最后一个等于 target 的下标」，
而是它的**下一个**位置。最后一个等于 target 的下标是 `upper_bound(target) - 1`
（且必须先确认 target 确实存在）。

由此可得：
- `target` 出现次数 = `upper_bound(t) - lower_bound(t)`
- `target` 存在 ⟺ `lower_bound(t) < n and nums[lower_bound(t)] == t`
- LC-0034 的答案 = `[lower_bound(t), upper_bound(t) - 1]`（不存在时返回 `[-1, -1]`）

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0704 Binary Search | P0 | 最纯粹的精确查找，闭区间模板 |
| 02/01 | LC-0035 Search Insert Position | P0 | **就是 Lower Bound**，插入位置 = 第一个 >= target 的下标 |
| 02/02 | LC-0034 Find First and Last Position | P0 | Lower Bound + Upper Bound 各一次 |
| 02/03 | LC-0278 First Bad Version | P1 | 谓词不是比较数值，而是调用 API；**First True 的最纯形态** |
| 03/01 | LC-0074 Search a 2D Matrix | P0 | 二维→一维展开；`row = mid // cols, col = mid % cols` |
| 03/02 | LC-0702 Search in Sorted Array of Unknown Size | P1 | **Exponential Search**：先倍增找上界，再二分（Premium 题） |
| 04/01 | LC-0069 Sqrt(x) | P1 | 找满足 `mid*mid <= x` 的最大整数 ⟹ Last True |
| 04/02 | LC-0367 Valid Perfect Square | P2 | 和 LC-0069 几乎同一个谓词，只是问「是否恰好相等」 |
| 04/03 | LC-0374 Guess Number Higher or Lower | P2 | 和 LC-0704 同构，只是比较换成 API |

**LC-0069 和 LC-0367 不是两个模板** —— 都是在 `[0, x]` 上二分 `mid*mid` 与 x 的关系，
一个要最大的 `mid*mid <= x`，一个问是否存在 `mid*mid == x`。所以 367 只标 P2。

## LC-0074 的适用前提（最常见的误用）
展开成一维**依赖题目给的「上一行末 < 下一行首」条件**。
如果只保证「每行递增、每列递增」（LC-0240 Search a 2D Matrix II），
拼起来**不是**有序数组，必须改用「从右上角走阶梯」的 O(m+n) 解法。
同理，LC-0378（在 Level 1 `03`）也不能用展开法，只能在值域上二分。

## LC-0702 的 Exponential Search
```python
lo, hi = 0, 1
while reader.get(hi) < target:     # 先倍增找到一个足够大的上界
    lo, hi = hi, hi * 2
# 然后在 [lo, hi] 上普通二分
```
O(log P)，P 是 target 的位置。适用于「数组长度未知 / 无限流」的场景。

## 常见错误
- 闭区间和左闭右开**混用**：写了 `while lo <= hi` 却用 `hi = mid` ⟹ 死循环。
- `mid = (lo + hi) // 2` 在 C++/Java 里可能**溢出**，要写 `lo + (hi - lo) // 2`。
  Python 整数无上限，但面试口述时值得提一句。
- 把 Upper Bound 的返回值当成「最后一个等于 target 的下标」。
- LC-0034 找到一个 target 后就向两边线性扩展 ⟹ 全相等数组退化成 O(n)。
- LC-0074 对只满足「行列各自递增」的矩阵套用展开法。

## 复习时的 Pattern Recognition
> 「有序数组里找 X」「插入位置」「第一个 / 最后一个等于 X」
> 「第一个坏版本」「整体有序的矩阵」 → 本章模板，先想清楚要的是**值**还是**边界**。
