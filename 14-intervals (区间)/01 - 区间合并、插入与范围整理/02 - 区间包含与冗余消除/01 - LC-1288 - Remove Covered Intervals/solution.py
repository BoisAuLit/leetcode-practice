"""LC-1288 - Remove Covered Intervals

Level 1 · 01 区间合并、插入与范围整理 —— **排序 tie-break 决定成败**
题目在问：删掉所有被其他区间**完全覆盖**的区间，返回剩余个数。
         `[a,b)` 被 `[c,d)` 覆盖 ⟺ `c <= a and b <= d`。

决定性观察：
  1. **排序规则必须是：start 升序，start 相同时 end 降序。**
     ```python
     intervals.sort(key=lambda x: (x[0], -x[1]))
     ```
  2. 排完之后一次扫描，维护 `max_end`：
     - `end <= max_end` ⟹ 当前区间被前面某个区间覆盖 ⟹ 删掉
     - 否则 ⟹ 保留，更新 `max_end = end`
  3. **为什么 start 相同时 end 要降序**（这是全题唯一的坑）：
     考虑 `[[1,4],[1,2]]`。
     - end **降序**排 ⟹ `[1,4], [1,2]` ⟹ 扫到 `[1,2]` 时 `max_end = 4` ⟹ 正确删掉它。
     - end **升序**排 ⟹ `[1,2], [1,4]` ⟹ 扫到 `[1,2]` 时 `max_end = 0` ⟹ **保留了它**，答案错。

     **同起点时，长的必须排在前面**，这样短的才会被判定为「被覆盖」。

  4. **为什么只比较 `max_end` 就够**（不用两两比较）：
     排序后 start 单调不减，所以前面任何区间的 start 都 `<= ` 当前的 start。
     覆盖条件 `c <= a` 自动满足 ⟹ **只需要检查 `b <= d`**，
     而 `d` 的最大值就是 `max_end`。∎

### 本章三道题的排序 tie-break 对照（最该记的一张表）

| 题 | 排序键 | 为什么这个 tie-break |
|---|---|---|
| **LC-0056** Merge Intervals | start 升序（end 随意） | 只要能依次合并，end 顺序不影响 |
| **LC-1288** 本题 | start 升序，**end 降序** | 同起点时长的在前，短的才会被判为被覆盖 |
| **LC-0435** Non-overlapping | **end 升序** | 贪心保留结束最早的，给后面留最多空间 |

> **区间题的第一步永远是「按什么排序」，第二步是「相等时怎么办」。**
> tie-break 写错是这类题最常见的错误，而且小样例往往测不出来。

复杂度：**O(n log n)** 时间（排序主导），O(1) 额外空间。

边界：
  - 完全相同的区间 `[[1,2],[1,2]]` → 1
  - 嵌套 `[[1,10],[2,3],[4,5]]` → 1
  - 互不相交 → n
  - 单个区间 → 1
  - 同起点不同终点 `[[1,4],[1,2]]` → 1
"""

from typing import List


##################################################################################################
##### ! Solution 1: 按 (start 升序, end 降序) 排序 + 一次扫描维护 max_end
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1) 额外
##### ! 适用：所有「区间包含/冗余消除」的题；tie-break（end 降序）是关键
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # ! start 升序；start 相同时 end **降序** —— 让长的排在前面
        intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
        kept = 0
        max_end = 0
        for start, end in intervals:
            if end > max_end:        # ! 没被覆盖（start 条件因为排序已自动满足）
                kept += 1
                max_end = end
        return kept


##################################################################################################
##### ! Solution 2: 暴力两两比较（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：正确性参照 —— 直接按「被覆盖」的定义检查每一对
##################################################################################################


class Solution_2:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        n = len(intervals)
        covered = [False] * n
        for i in range(n):
            a, b = intervals[i]
            for j in range(n):
                if i == j or covered[j]:
                    continue
                c, d = intervals[j]
                # ! i 被 j 覆盖；完全相同时只删一个（用下标打破平局）
                if c <= a and b <= d and (c < a or d > b or j < i):
                    covered[i] = True
                    break
        return n - sum(covered)


if __name__ == "__main__":
    import random

    cases = [([[1, 4], [3, 6], [2, 8]], 2), ([[1, 4], [2, 3]], 1),
             ([[1, 2], [1, 2]], 1), ([[1, 10], [2, 3], [4, 5]], 1),
             ([[1, 4], [1, 2]], 1), ([[1, 2]], 1), ([[1, 2], [3, 4]], 2)]
    for iv, want in cases:
        a = Solution_1().removeCoveredIntervals([x[:] for x in iv])
        b = Solution_2().removeCoveredIntervals([x[:] for x in iv])
        assert a == b == want, (iv, a, b, want)
        print(f"{iv} -> {a}")

    for _ in range(1500):                # ! 小值域随机对拍，专压同起点 / 完全相同的区间
        n = random.randint(1, 7)
        iv = []
        for _ in range(n):
            s = random.randint(0, 5)
            iv.append([s, s + random.randint(1, 5)])
        a = Solution_1().removeCoveredIntervals([x[:] for x in iv])
        b = Solution_2().removeCoveredIntervals([x[:] for x in iv])
        assert a == b, (iv, a, b)
    print("随机对拍 1500 组通过 ✓（排序扫描 == 两两比较；含同起点和完全相同的区间）")
