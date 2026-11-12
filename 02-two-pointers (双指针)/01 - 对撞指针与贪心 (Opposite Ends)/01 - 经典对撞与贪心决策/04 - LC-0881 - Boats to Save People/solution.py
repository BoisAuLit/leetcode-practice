"""LC-0881 - Boats to Save People（第二轮自主新增）

Level 1 · 03 排序贪心 —— **排序 + 对撞双指针配对**
题目在问：每条船最多载 **2** 人且总重不超过 limit，求最少需要几条船。

为什么新增它（它补的是哪个缺口）：
  本章其他排序贪心题排完序都是**单向扫描**。
  这道题排完序要用**对撞双指针**配对（最重的配最轻的），
  是「排序 + 两端配对」这个独立模式的最佳代表。成本极低、模式很常用。

决定性观察（贪心策略 + 证明）：
  1. **排序后，让最重的和最轻的配对**：
     ```
     if people[light] + people[heavy] <= limit: light += 1    # 配上
     heavy -= 1                                               # 最重的无论如何都要走
     boats += 1
     ```
  2. **为什么最重的人必须单独考虑**：他要么和某个人配对，要么单独一条船。
     而**如果他能和任何人配对，和最轻的人配对一定可行**（最轻的最容易塞进去）。
     ⟹ 试最轻的那个就够了，不用枚举。
  3. **为什么「最重的配最轻的」是最优的（交换论证）**：
     设最优解里最重的人 H 和某个人 X 同船，而最轻的人 L 和 Y 同船。
     把它们换成 (H, L) 和 (X, Y)：
     - `H + L <= H + X <= limit` ✓（L 最轻）
     - `X + Y <= H + Y <= limit` ✓（H 最重）
     ⟹ 互换后仍然合法，船数不变。所以存在一个「最重配最轻」的最优解。∎
  4. **每条船最多 2 人**这个限制很关键 —— 如果是 3 人或更多，贪心就不成立了
     （变成装箱问题，NP-hard）。

**题目保证 `people[i] <= limit`**，所以每个人至少能单独坐一条船，不会无解。

复杂度：**O(n log n)** 时间（排序主导），O(1) 额外空间。

> 本章的「排序 + 两端配对」还能用在：
> LC-2616 Minimize Max Diff of Pairs（但那题是**相邻**配对，见 05-binary-search）、
> LC-1877 Minimize Maximum Pair Sum in Array（最重配最轻，几乎同一道）。

边界：
  - 每个人都超过 limit/2 ⟹ 每人一条船
  - 所有人都很轻 ⟹ 两两配对，`ceil(n/2)` 条船
  - 单个人 → 1
  - `[3,2,2,1]`, limit=3 → 3
  - `[3,5,3,4]`, limit=5 → 4
"""

# ! ============================================================================================
# ! 下面这段是**用户原有的实现**，一字未改。
# ! 后面追加的 Solution_1 / Solution_2 是本次补充的实现与穷举对拍基准。
# ! ============================================================================================

"""LC-0881 - Boats to Save People

Level 1 · 01 对撞指针与贪心 —— Sorting + Greedy Elimination
题目在问：每条船最多载 2 人、总重不超过 limit，最少要几条船

决定性观察：
  1. 每条船最多 2 人，所以答案 >= ⌈n/2⌉，问题变成「尽量多地凑成两人一船」。
  2. **最重的那个人无论如何都要上船**。既然他必须占一条船，那就让他捎上
     「所有还能和他同船的人里最轻的那个」—— 最轻的人和他配不上，和任何人都配不上。

循环不变量（loop invariant）：排序后用 l / r 两端。
  区间 `[l, r]` 始终是「还没上船的人」，且它一直保持有序。
  每轮结束时 r 一定减 1（最重的人上了船），所以循环必然终止，复杂度 O(n)。

正确性简证（贪心交换论证 exchange argument）：
  设最优解里最重的人 r 和某个 x 同船（或独自）。若 l 能和 r 同船而最优解没这么配，
  把 x 换成 l 不会让任何约束变坏（l <= x，所以 l + r <= x + r <= limit），
  而 x 比 l 重、以后更难配对，留给后面反而更好。所以总是配 l 不会变差。

坑：
  - 循环条件是 `l <= r` 不是 `l < r`：只剩一个人时他也要一条船
  - 题目保证每个人的体重 <= limit，所以不存在「谁都载不了」的情况
  - 不要试图「让两个中等的人配对来省船」—— 最重的人迟早要单独占一条，省不下来
"""

from typing import List


##################################################################################################
##### ! Solution 1: 排序 + 对撞指针贪心（最轻的配最重的）
##### ! 时间复杂度: O(n log n)（排序主导）   空间复杂度: O(1) 额外
##### ! 适用：所有「两两配对 + 容量上限」的贪心；和 LC-0011 的区别是这里**两端都会动**
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        l, r = 0, len(people) - 1
        boats = 0
        while l <= r:          # ! <= ：只剩一个人时也要一条船
            if people[l] + people[r] <= limit:
                l += 1         # ! 最轻的搭上这条船
            r -= 1             # ! 最重的无论如何都上船
            boats += 1
        return boats


##################################################################################################
##### ! Solution 2: 计数排序 + 对撞指针（权重值域小的时候）
##### ! 时间复杂度: O(n + limit)   空间复杂度: O(limit)
##### ! 适用：★ 体重上界不大时线性，没有排序的 log；思路一样，只是「排序」换成了桶计数
##################################################################################################


class Solution_2:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        cnt = [0] * (limit + 1)
        for w in people:
            cnt[w] += 1
        l, r = 1, limit
        boats = 0
        while l <= r:
            while l <= r and cnt[l] == 0:   # ! 找最轻的还在的人
                l += 1
            while l <= r and cnt[r] == 0:   # ! 找最重的还在的人
                r -= 1
            if l > r:
                break
            cnt[r] -= 1                     # ! 最重的上船
            if l <= r and l + r <= limit and cnt[l] > 0:
                cnt[l] -= 1                 # ! 捎上最轻的
            boats += 1
        return boats


##################################################################################################
##### ! Solution 1: 排序 + 对撞双指针（最重的配最轻的）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1) 额外
##### ! 适用：「每组最多 2 个 + 有容量上限」⟹ 排序后两端配对
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people = sorted(people)
        light, heavy = 0, len(people) - 1
        boats = 0
        while light <= heavy:
            if people[light] + people[heavy] <= limit:
                light += 1              # ! 最轻的能一起走
            heavy -= 1                  # ! 最重的无论如何这条船都要带走
            boats += 1
        return boats


##################################################################################################
##### ! Solution 2: 暴力搜索最少船数（基准答案，用来对拍；只适合很少的人）
##### ! 时间复杂度: 指数级   空间复杂度: O(2^n)
##### ! 适用：正确性参照 —— 枚举所有「单独走 / 两人配对」的分组方式
##################################################################################################


class Solution_2:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        n = len(people)
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(mask: int) -> int:
            if mask == 0:
                return 0
            # ! 取最低位的那个人，他要么单独走，要么和后面某个人配对
            i = (mask & -mask).bit_length() - 1
            rest = mask & ~(1 << i)
            best = 1 + dfs(rest)                                  # 单独走
            for j in range(i + 1, n):
                if rest >> j & 1 and people[i] + people[j] <= limit:
                    best = min(best, 1 + dfs(rest & ~(1 << j)))   # 和 j 配对
            return best

        r = dfs((1 << n) - 1)
        dfs.cache_clear()
        return r


if __name__ == "__main__":
    import random

    cases = [([1, 2], 3, 1), ([3, 2, 2, 1], 3, 3), ([3, 5, 3, 4], 5, 4),
             ([5], 5, 1), ([2, 2, 2, 2], 4, 2)]
    for people, limit, want in cases:
        a = Solution_1().numRescueBoats(people[:], limit)
        b = Solution_2().numRescueBoats(tuple(sorted(people)), limit)
        assert a == b == want, (people, limit, a, b, want)
        print(f"{people}, limit={limit} -> {a}")

    for _ in range(800):
        limit = random.randint(1, 10)
        n = random.randint(1, 9)
        people = [random.randint(1, limit) for _ in range(n)]   # ! 题目保证每人 <= limit
        a = Solution_1().numRescueBoats(people[:], limit)
        b = Solution_2().numRescueBoats(tuple(sorted(people)), limit)
        assert a == b, (people, limit, a, b)
    print("随机对拍 800 组通过 ✓（两端配对贪心 == 枚举所有分组）")
