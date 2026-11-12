"""LC-1109 - Corporate Flight Bookings     ★ 第二轮审核新增（差分数组最纯粹的一题）

Level 1 · 04 重叠计数、扫描线与资源分配 —— **差分数组的「裸题」**
题目在问：有 `n` 个航班编号 `1..n`。`bookings[i] = [first, last, seats]` 表示
         **航班 `first` 到 `last`（闭区间，两端都含）各预订了 `seats` 个座位**。
         返回长度 `n` 的数组，第 `i` 位是航班 `i+1` 的总预订座位数。

### 为什么这题值得单独练

[LC-1094 Car Pooling](<../01 - LC-1094 - Car Pooling>) 要的是「峰值是否超限」，
本题要的是**整条前缀和数组本身**。差分数组的两个用法这才算配齐：

| | 要什么 | 做法 |
|---|---|---|
| LC-1094 | 区间加之后的**最大值** | 差分 → 前缀和 → 取 max |
| **LC-1109** 本题 | 区间加之后的**每一项** | 差分 → 前缀和 → **直接返回** |
| LC-2406 | 区间加之后的最大值（**闭区间**） | 差分，`right+1` 处减 |

**核心三行**：
```python
diff = [0] * (n + 1)
for first, last, seats in bookings:
    diff[first - 1] += seats
    diff[last] -= seats          # ! 闭区间 ⟹ 在 last 之后才失效；下标已经 -1 过，所以写 diff[last]
answer = list(itertools.accumulate(diff[:n]))
```

### 下标这件事必须一次说清（本题唯一的坑）

题目的航班编号是 **1-based**（`1 <= first <= last <= n`），数组是 **0-based**。
设 `idx = flight - 1`，则闭区间 `[first, last]` 对应下标区间 `[first-1, last-1]`。
差分的规则是「在**区间后一格**减掉」：
```
diff[first - 1] += seats
diff[(last - 1) + 1] -= seats  ==  diff[last] -= seats
```
所以 `diff` 要开 `n + 1` 长（最大写到 `diff[n]`），返回时只取前 `n` 项。

> **一眼区分**：`+=` 的下标减了 1，`-=` 的下标没减 —— 看起来不对称，
> 恰恰是因为闭区间的 `+1` 和 1-based 的 `-1` 抵消了。
> 对比 LC-1094（半开 + 0-based）是 `diff[start] += v; diff[end] -= v`，两边都不动。
> **先写清「端点语义 + 下标基准」，再落笔。**

**为什么差分数组是对的？**
令 `diff[i] = a[i] - a[i-1]`（`a[-1] = 0`），则 `a[i] = Σ_{j<=i} diff[j]`。
对 `a` 的区间 `[l, r]` 整体加 `v`，只有 `a[l] - a[l-1]` 和 `a[r+1] - a[r]` 两个差值变化
⟹ 只需改 `diff[l] += v`、`diff[r+1] -= v`，**O(1) 完成一次区间加**。
最后一次前缀和把所有修改同时兑现 ⟹ 总 **O(n + m)**，而逐个加是 O(n·m)。∎

**为什么不能排序成事件再扫？** 能，但没必要 ——
下标已经是 `1..n` 的连续整数，`diff` 数组本身就是「排好序的事件表」。
值域离散/巨大时才需要退回事件排序（解法 2）。

复杂度：解法 1 **O(n + m)** 时间、O(n) 空间（`m = len(bookings)`）；
       解法 3 暴力是 O(n · m)，`n, m <= 2e4` 会 TLE。

边界：
  - `n=5, bookings=[[1,2,10],[2,3,20],[2,5,25]]` → `[10,55,45,25,25]`
  - 整个范围 `[[1,n,k]]` → 全是 `k`
  - 单个航班 `[[3,3,7]]`, n=5 → `[0,0,7,0,0]`
  - `last == n`（要写到 `diff[n]`，所以必须开 n+1 长）
  - `bookings` 为空 → 全 0
"""

from itertools import accumulate
from typing import List


##################################################################################################
##### ! Solution 1: 差分数组 + 前缀和（1-based 转 0-based：+= 下标减一，-= 下标不减）
##### ! 时间复杂度: O(n + m)   空间复杂度: O(n)
##### ! 适用：所有「m 次区间加，最后问每一项」的问题；差分数组的标准模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        diff = [0] * (n + 1)                      # ! 多开一格，因为最大会写到 diff[n]
        for first, last, seats in bookings:
            diff[first - 1] += seats              # ! 1-based 编号转 0-based 下标
            diff[last] -= seats                   # ! 闭区间的 (last-1)+1 == last
        return list(accumulate(diff[:n]))         # ! 一次前缀和兑现所有区间加


##################################################################################################
##### ! Solution 2: 事件排序扫描（值域离散/巨大时的通用退路）
##### ! 时间复杂度: O(m log m + n)   空间复杂度: O(m)
##### ! 适用：航班编号不连续、或是时间戳/浮点数时；本题下标连续，用它纯属绕路
##################################################################################################


class Solution_2:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        events: List[tuple] = []
        for first, last, seats in bookings:
            events.append((first, seats))
            events.append((last + 1, -seats))     # ! 闭区间 ⟹ last+1 才失效
        events.sort()
        res = [0] * n
        cur = 0
        k = 0
        for flight in range(1, n + 1):
            while k < len(events) and events[k][0] <= flight:
                cur += events[k][1]
                k += 1
            res[flight - 1] = cur
        return res


##################################################################################################
##### ! Solution 3: 暴力逐航班累加（基准答案，n·m 大时会 TLE）
##### ! 时间复杂度: O(n · m)   空间复杂度: O(n)
##### ! 适用：仅用于对拍，顺便看清差分省掉的就是这个双重循环
##################################################################################################


class Solution_3:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        res = [0] * n
        for first, last, seats in bookings:
            for f in range(first, last + 1):      # ! 闭区间，last 也要加
                res[f - 1] += seats
        return res


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.corpFlightBookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5) == [10, 55, 45, 25, 25]
        assert s.corpFlightBookings([[1, 2, 10], [2, 2, 15]], 2) == [10, 25]
        assert s.corpFlightBookings([[3, 3, 7]], 5) == [0, 0, 7, 0, 0]
        assert s.corpFlightBookings([[1, 5, 4]], 5) == [4, 4, 4, 4, 4]
        assert s.corpFlightBookings([[5, 5, 9]], 5) == [0, 0, 0, 0, 9]   # ! last == n
        assert s.corpFlightBookings([], 3) == [0, 0, 0]

    print("n=5, bookings=[[1,2,10],[2,3,20],[2,5,25]] ->",
          Solution_1().corpFlightBookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5))

    for _ in range(800):                          # ! 随机对拍
        n = random.randint(1, 10)
        bk = []
        for _ in range(random.randint(0, 8)):
            a = random.randint(1, n)
            b = random.randint(a, n)
            bk.append([a, b, random.randint(1, 50)])
        o1 = Solution_1().corpFlightBookings([x[:] for x in bk], n)
        o2 = Solution_2().corpFlightBookings([x[:] for x in bk], n)
        o3 = Solution_3().corpFlightBookings([x[:] for x in bk], n)
        assert o1 == o2 == o3, (n, bk, o1, o2, o3)
    print("随机对拍 800 组通过 ✓（差分数组 == 事件排序扫描 == 逐航班暴力）")
