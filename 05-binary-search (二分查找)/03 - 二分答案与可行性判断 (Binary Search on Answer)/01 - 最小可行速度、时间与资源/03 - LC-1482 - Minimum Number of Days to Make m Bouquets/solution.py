"""LC-1482 - Minimum Number of Days to Make m Bouquets

Level 1 · 03 二分答案与可行性判断 —— Minimum Feasible Answer，可行性是「数连续段」
题目在问：第 i 朵花在 bloomDay[i] 天开放；一束花需要 **k 朵相邻**的已开花；
         求最少等多少天能做出 m 束。做不出返回 -1。

二分答案三件套：
  1. **无解先判**：`m * k > len(bloomDay)` ⟹ 直接返回 -1。
     这一步必须放在最前面，否则二分会在一个空的可行域上给出错误答案。
     注意用 `m * k > n` 而不是先算乘积再比较溢出（Python 无所谓，C++/Java 要留意）。
  2. **答案空间**：`lo = min(bloomDay)`，`hi = max(bloomDay)`。
  3. **feasible(day)**：扫一遍，统计「连续已开花段」能切出多少束
     （一段长 L 能切 `L // k` 束），判断总数 `>= m`。
  4. **单调性**：day 越大，开的花越多，连续段只增不减 ⟹ `F F F T T T` ⟹ First True。

为什么「一段长 L 切 L//k 束」是对的：
      束与束之间不能共享花，且必须相邻，所以一段长 L 的连续花最多切 ⌊L/k⌋ 束，
      而且这个上界总能取到（从左往右贴着切）。

为什么连续段计数可以 O(n) 一遍完成：
      维护一个 `run` 计数器：花开着就 `run += 1`，一旦 `run == k` 就
      `bouquets += 1; run = 0`（立刻结算，等价于贪心贴着切）；遇到没开的花 `run = 0`。

复杂度：**O(n · log(max - min))**，空间 O(1)。

和 LC-0875 / LC-1011 的区别：模板完全相同，差别只在 feasible 的内容 ——
      Koko 数小时、1011 数天数、本题数「连续段能切几束」。
      这三题放在同一个 Level 2，就是为了让你看出「只有 feasible 在变」。

边界：
  - bloomDay=[1,10,3,10,2], m=3, k=1 → 3
  - bloomDay=[1,10,3,10,2], m=3, k=2 → -1（3*2 > 5）
  - bloomDay=[7,7,7,7,12,7,7], m=2, k=3 → 12
  - m*k == n（刚好用完所有花）
  - k == 1（退化成「第 m 小的 bloomDay」）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二分答案 + O(n) 数连续段（First True）
##### ! 时间复杂度: O(n · log(max - min))   空间复杂度: O(1)
##### ! 适用：「最少等多久 / 最小阈值，使某种计数达标」且计数随阈值单调的题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        n = len(bloomDay)
        if m * k > n:                      # ! 花不够，先判无解，不能进二分
            return -1

        def feasible(day: int) -> bool:
            bouquets = run = 0
            for b in bloomDay:
                if b <= day:               # ! 这朵已经开了
                    run += 1
                    if run == k:           # ! 凑满一束，立刻结算（贪心贴着切）
                        bouquets += 1
                        run = 0
                        if bouquets >= m:
                            return True
                else:
                    run = 0                # ! 断了，连续段重新开始
            return bouquets >= m

        lo, hi = min(bloomDay), max(bloomDay)
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 2: 只在「实际出现过的 bloomDay 值」里二分（候选集更小）
##### ! 时间复杂度: O(n log n + n log n)   空间复杂度: O(n)
##### ! 适用：值域非常大但 n 很小时；答案一定是某个 bloomDay，所以可以只在这些值上找
##################################################################################################


class Solution_2:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        n = len(bloomDay)
        if m * k > n:
            return -1

        def feasible(day: int) -> bool:
            bouquets = run = 0
            for b in bloomDay:
                if b <= day:
                    run += 1
                    if run == k:
                        bouquets += 1
                        run = 0
                else:
                    run = 0
            return bouquets >= m

        days = sorted(set(bloomDay))       # ! 答案必然是某一朵花的开放日
        lo, hi = 0, len(days) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(days[mid]):
                hi = mid
            else:
                lo = mid + 1
        return days[lo]


##################################################################################################
##### ! Solution 3: 从小到大逐天枚举（基准答案，用来对拍）
##### ! 时间复杂度: O(n · max)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        n = len(bloomDay)
        if m * k > n:
            return -1
        for day in range(min(bloomDay), max(bloomDay) + 1):
            bouquets = run = 0
            for b in bloomDay:
                if b <= day:
                    run += 1
                    if run == k:
                        bouquets += 1
                        run = 0
                else:
                    run = 0
            if bouquets >= m:
                return day
        return -1


if __name__ == "__main__":
    import random

    cases = [([1, 10, 3, 10, 2], 3, 1), ([1, 10, 3, 10, 2], 3, 2),
             ([7, 7, 7, 7, 12, 7, 7], 2, 3), ([1000000000, 1000000000], 1, 1),
             ([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2)]
    for b, m, k in cases:
        a = Solution_1().minDays(b, m, k)
        assert a == Solution_2().minDays(b, m, k) if a != -1 else True
        assert a == Solution_3().minDays(b, m, k), (b, m, k)
        print(f"bloomDay={b}, m={m}, k={k} -> {a}")

    for _ in range(500):                 # ! 随机对拍（含大量无解与重复 bloomDay）
        n = random.randint(1, 9)
        b = [random.randint(1, 8) for _ in range(n)]
        m, k = random.randint(1, 4), random.randint(1, 3)
        r1, r3 = Solution_1().minDays(b, m, k), Solution_3().minDays(b, m, k)
        assert r1 == r3, (b, m, k, r1, r3)
        if r1 != -1:
            assert Solution_2().minDays(b, m, k) == r1, (b, m, k)
    print("随机对拍 500 组通过 ✓")
