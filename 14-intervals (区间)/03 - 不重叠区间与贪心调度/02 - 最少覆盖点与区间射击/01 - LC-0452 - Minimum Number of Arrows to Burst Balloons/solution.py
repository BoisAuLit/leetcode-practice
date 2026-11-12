"""LC-0452 - Minimum Number of Arrows to Burst Balloons

Level 1 · 03 不重叠区间与贪心调度 —— **最少的点刺穿所有区间**
题目在问：每个气球是一个区间 `[start, end]`，一支箭射在 x 处能扎破所有包含 x 的气球。
         求最少需要几支箭。

决定性观察：
  1. **按 end 升序排序**，每次把箭射在**当前气球的 end** 上。
  2. 然后跳过所有「start <= 这支箭的位置」的气球（它们都被这一箭扎破了）。
  3. **为什么射在 end 上最优（交换论证）**：
     当前 end 最小的气球**必须**被某支箭扎破，那支箭的位置 `x <= 它的 end`。
     把 x 挪到它的 end 上：原来被 x 扎破的气球 `[s, e]` 满足 `s <= x <= e`，
     而 `x <= end`，又因为排序保证 `end <= e`（end 最小），所以 `s <= x <= end <= e`
     ⟹ 挪到 end 之后**仍然扎得破**，而且还可能多扎几个。
     ⟹ 射在 end 上**不会更差**。∎

```python
points.sort(key=lambda p: p[1])          # ★ 按 end 升序
arrows, arrow_x = 1, points[0][1]
for s, e in points[1:]:
    if s > arrow_x:                      # 这一箭扎不到 ⟹ 需要新的一箭
        arrows += 1
        arrow_x = e
return arrows
```

**`s > arrow_x` 用严格大于**：`s == arrow_x` 时气球**是**被扎破的（端点也算）。
题目说区间是闭区间，所以必须用 `>` 而不是 `>=`。

### 和 LC-0435 的关系（本 Level 1 的核心对照）

| | LC-0435 Non-overlapping Intervals | LC-0452 本题 |
|---|---|---|
| 问什么 | 最少**删掉**几个区间使其不重叠 | 最少用几个**点**刺穿所有区间 |
| 排序 | **end 升序** | **end 升序** |
| 贪心 | 保留 end 最小的，冲突就删 | 射在 end 最小的 end 上 |
| 答案 | `n − 保留数` | 箭数 = **保留数** |

> **两题是同一个贪心的两种计数方式！**
> 「最多能选出多少个互不重叠的区间」= 「需要多少支箭」。
> 因为每一支箭对应一组互相重叠的气球，而不同箭对应的组互不重叠。
>
> **记住一个，另一个就是换种数法。**

**为什么都按 end 排序**：保留**结束最早**的区间，给后面留下最多空间。
这是区间调度最经典的贪心（Interval Scheduling），可以用交换论证严格证明。

### 溢出提醒
题目的坐标范围是 `-2^31 ~ 2^31-1`。
**用 `(a[1] - b[1])` 做比较器会溢出**（C++/Java）。Python 没问题，
但面试要提一句：应该用 `a[1] < b[1]` 而不是相减。

复杂度：**O(n log n)** 时间（排序主导），O(1) 额外空间。

边界：
  - 空数组 → 0
  - 单个气球 → 1
  - 全部重叠 → 1
  - 互不重叠 → n
  - 端点相接 `[[1,2],[2,3]]` → **1**（端点也算扎破）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 按 end 升序排序，箭射在当前 end 上
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1) 额外
##### ! 适用：「最少的点刺穿所有区间」；和 LC-0435 是同一个贪心的两种数法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        if not points:
            return 0
        points = sorted(points, key=lambda p: p[1])    # ! 按 end 升序
        arrows = 1
        arrow_x = points[0][1]                         # ! 第一箭射在最早结束的那个 end 上
        for s, e in points[1:]:
            if s > arrow_x:                            # ! 严格大于：s == arrow_x 时是扎得破的
                arrows += 1
                arrow_x = e
        return arrows


##################################################################################################
##### ! Solution 2: 复用 LC-0435 的「最多互不重叠区间数」—— 答案完全相同
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1)
##### ! 适用：用来验证「箭数 == 最多互不重叠区间数」这个等价关系
##################################################################################################


class Solution_2:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        if not points:
            return 0
        points = sorted(points, key=lambda p: p[1])
        count, last_end = 0, float("-inf")
        for s, e in points:
            if s > last_end:          # ! 和前一个选中的区间不重叠（闭区间，端点算重叠）
                count += 1
                last_end = e
        return count


##################################################################################################
##### ! Solution 3: 穷举所有候选点的子集，找最小的覆盖集（基准答案，用来对拍）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n)
##### ! 适用：正确性参照。候选点只需取各区间的 end（见上面的交换论证）。
##### ! 注意：**「每次射能扎破最多气球的那个点」这种最大覆盖贪心是错的** ——
#####   集合覆盖问题的最大覆盖贪心只能给出 O(log n) 近似，不保证最优。
#####   本文件最初就是这么写的，被随机对拍抓了出来（反例见下面测试里的注释）。
##################################################################################################


class Solution_3:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        n = len(points)
        if n == 0:
            return 0
        cands = sorted({e for _, e in points})          # ! 候选点只需取各区间的 end
        m = len(cands)
        # ! 预处理：每个候选点能扎破哪些气球（位掩码）
        hit = []
        for x in cands:
            mask = 0
            for i, (s, e) in enumerate(points):
                if s <= x <= e:
                    mask |= 1 << i
            hit.append(mask)
        full = (1 << n) - 1
        # ! 按子集大小从小到大穷举，第一个能覆盖全部的就是答案
        for k in range(1, m + 1):
            from itertools import combinations
            for comb in combinations(range(m), k):
                cov = 0
                for idx in comb:
                    cov |= hit[idx]
                if cov == full:
                    return k
        return n


if __name__ == "__main__":
    import random

    cases = [([[10, 16], [2, 8], [1, 6], [7, 12]], 2), ([[1, 2], [3, 4], [5, 6], [7, 8]], 4),
             ([[1, 2], [2, 3], [3, 4], [4, 5]], 2), ([], 0), ([[1, 2]], 1),
             ([[1, 2], [2, 3]], 1), ([[1, 10], [2, 3], [4, 5]], 2)]
    for pts, want in cases:
        a = Solution_1().findMinArrowShots([p[:] for p in pts])
        b = Solution_2().findMinArrowShots([p[:] for p in pts])
        assert a == b == want, (pts, a, b, want)
        print(f"{pts} -> {a}")

    # ! 下面这组是当初抓出「最大覆盖贪心」错误的反例：
    #   [[2,4],[2,2],[5,7],[4,7],[3,7]] 正确答案是 2（射 2 和 7），
    #   但「每次挑扎破最多气球的点」会先射 7（扎 3 个），然后还要 2 支 ⟹ 得出 3。
    assert Solution_3().findMinArrowShots([[2, 4], [2, 2], [5, 7], [4, 7], [3, 7]]) == 2

    for _ in range(600):                 # ! 随机对拍（含端点相接、完全重叠）
        n = random.randint(0, 7)
        pts = []
        for _ in range(n):
            s = random.randint(0, 6)
            pts.append([s, s + random.randint(0, 4)])
        a = Solution_1().findMinArrowShots([p[:] for p in pts])
        b = Solution_2().findMinArrowShots([p[:] for p in pts])
        c = Solution_3().findMinArrowShots([p[:] for p in pts])
        assert a == b == c, (pts, a, b, c)
    print("随机对拍 600 组通过 ✓（按 end 贪心 == 最多不重叠区间数 == 贪心覆盖暴力）")
