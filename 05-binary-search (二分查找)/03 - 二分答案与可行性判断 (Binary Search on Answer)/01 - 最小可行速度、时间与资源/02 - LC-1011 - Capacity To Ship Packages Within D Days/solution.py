"""LC-1011 - Capacity To Ship Packages Within D Days

Level 1 · 03 二分答案与可行性判断 —— Minimum Feasible Answer（最小可行答案）
题目在问：包裹**必须按给定顺序**装船，求能在 days 天内运完的最小船载重量。

二分答案的三件套（每道这类题都先把这三件事写下来）：
  1. **答案空间**：`lo = max(weights)`（一件都装不下就永远运不完），
                  `hi = sum(weights)`（一天全运完）。
  2. **feasible(cap)**：用容量 cap 贪心装船，算出需要几天，判断 `<= days`。
  3. **单调性**：cap 越大越容易成功 ⟹ `F F F T T T` ⟹ 找 **First True**。

为什么贪心计算天数是对的：
      包裹顺序固定，所以「当前这天能装就装」不会比「提前换一天」更差 ——
      提前开新的一天只会浪费本天剩余容量，天数只可能变多，不会变少。
      （顺序固定是关键前提；如果允许重排，这就变成装箱问题，NP-hard。）

为什么下界必须是 `max(weights)` 而不是 1：
      若 `cap < max(weights)`，那件最重的包裹永远装不上，feasible 恒为 False，
      二分虽然也能收敛，但 `max(weights)` 让下界本来就落在可行域边界附近，更清楚也更安全。

Loop Invariant（左闭右开 `[lo, hi)`）：答案一定在 `[lo, hi]` 内；
      循环结束时 `lo == hi` 就是第一个可行的 cap。

复杂度：**O(n · log(sum - max))**。
      注意不是 O(log n) —— 每次 feasible 检查都要扫一遍数组。
      这就是 `O(log R)` 和 `O(n log R)` 的区别。

和 LC-0875 Koko 的关系：**完全同一个模板**，只是 feasible 的内容换了
（Koko 是 `ceil(pile / speed)` 求和，这里是顺序打包计数）。
不要把它们记成两道题。

边界：
  - weights=[1..10], days=5 → 15
  - days == n → 答案就是 max(weights)（每天一件）
  - days == 1 → 答案就是 sum(weights)
  - 单个包裹
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二分答案 + 贪心可行性检查（First True）
##### ! 时间复杂度: O(n · log(sum - max))   空间复杂度: O(1)
##### ! 适用：所有「最小化某个容量 / 速度 / 阈值，使某个贪心过程能在限额内完成」的题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def feasible(cap: int) -> bool:
            need, cur = 1, 0             # ! 至少要 1 天
            for w in weights:
                if cur + w > cap:        # ! 这天装不下了，开新的一天
                    need += 1
                    cur = 0
                cur += w
            return need <= days

        lo, hi = max(weights), sum(weights)     # ! 下界：最重的那件；上界：一天全运完
        while lo < hi:                          # ! 左闭右开，收敛到 First True
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid                        # ! 可行 → 答案在左边（含 mid）
            else:
                lo = mid + 1
        return lo


##################################################################################################
##### ! Solution 2: 同样的二分，但用「闭区间 + 记录候选答案」的写法
##### ! 时间复杂度: O(n · log(sum - max))   空间复杂度: O(1)
##### ! 适用：不习惯左闭右开时的等价写法；显式记录 ans 更不容易把边界写错
##################################################################################################


class Solution_2:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def days_needed(cap: int) -> int:
            need, cur = 1, 0
            for w in weights:
                if cur + w > cap:
                    need += 1
                    cur = 0
                cur += w
            return need

        lo, hi = max(weights), sum(weights)
        ans = hi
        while lo <= hi:                   # ! 闭区间
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                ans = mid                 # ! 记下候选，继续往小了试
                hi = mid - 1
            else:
                lo = mid + 1
        return ans


##################################################################################################
##### ! Solution 3: 从 max(weights) 开始逐个试（基准答案，用来对拍）
##### ! 时间复杂度: O(n · (sum - max))   空间复杂度: O(1)
##### ! 适用：正确性参照，同时验证 feasible 确实是单调的
##################################################################################################


class Solution_3:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def days_needed(cap: int) -> int:
            need, cur = 1, 0
            for w in weights:
                if cur + w > cap:
                    need += 1
                    cur = 0
                cur += w
            return need

        for cap in range(max(weights), sum(weights) + 1):
            if days_needed(cap) <= days:
                return cap
        return sum(weights)


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), ([3, 2, 2, 4, 1, 4], 3),
             ([1, 2, 3, 1, 1], 4), ([5], 1), ([1, 1, 1], 3), ([1, 1, 1], 1)]
    for w, d in cases:
        a = Solution_1().shipWithinDays(w, d)
        assert a == Solution_2().shipWithinDays(w, d) == Solution_3().shipWithinDays(w, d), (w, d)
        print(f"weights={w}, days={d} -> {a}")

    for _ in range(500):                 # ! 随机对拍，顺带验证 feasible 的单调性
        n = random.randint(1, 8)
        w = [random.randint(1, 9) for _ in range(n)]
        d = random.randint(1, n)
        assert (Solution_1().shipWithinDays(w, d)
                == Solution_2().shipWithinDays(w, d)
                == Solution_3().shipWithinDays(w, d)), (w, d)
    print("随机对拍 500 组通过 ✓")
