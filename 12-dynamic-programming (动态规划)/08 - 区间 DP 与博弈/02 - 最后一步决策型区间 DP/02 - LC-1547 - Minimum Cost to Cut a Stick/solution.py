"""LC-1547 - Minimum Cost to Cut a Stick

Level 1 · 08 区间 DP 与博弈 —— **枚举「最后一刀」**（和 LC-0312 Burst Balloons 同族）
题目在问：长度 n 的棍子，必须在 cuts 给定的位置各切一刀（顺序自选）。
         每刀的代价 = 当前那段棍子的长度。求最小总代价。

决定性观察（这类题的灵魂）：
  1. **顺序会影响代价** ⟹ 不能贪心，必须 DP。
  2. 直接想「第一刀切哪里」会失败：切完之后两段的代价**取决于切点**，
     但第一刀之后的子问题边界还和原棍子有关，状态定不下来。
  3. **换成枚举「这一段里的最后一刀」**，子问题就独立了：
     ```
     把 cuts 排序，两端补上 0 和 n
     dp[i][j] = 把 (points[i], points[j]) 这一段上所有内部切点都切完的最小代价
     dp[i][j] = min over k in (i, j) of  dp[i][k] + dp[k][j] + (points[j] - points[i])
     ```
     `points[j] - points[i]` 是**这一段的长度** —— 不管 k 选哪个，
     「切这一段的最后一刀」的代价都是这个长度。
  4. **两端补 0 和 n** 是关键技巧：把「棍子的两端」也变成切点，
     这样所有区间都能统一表达，不需要边界特判。

**为什么是「最后一刀」而不是「第一刀」**：
  枚举最后一刀 k 时，`(i, k)` 和 `(k, j)` 两段**互不影响**（它们已经被 k 分开了），
  子问题完全独立 ⟹ 最优子结构成立。
  枚举第一刀的话，后续两段的代价还会受到彼此的影响，没法拆开。

### 和 LC-0312 Burst Balloons 的对照（同一个 Level 2 的原因）

| | LC-0312 Burst Balloons | LC-1547 本题 |
|---|---|---|
| 枚举什么 | **最后一个被扎破的气球** | **这一段的最后一刀** |
| 代价 | `nums[i] * nums[k] * nums[j]` | `points[j] - points[i]` |
| 补端点 | 两端补 1 | 两端补 0 和 n |
| 遍历顺序 | 区间长度从小到大 | 同 |

**两题是同一个模板，只有「代价函数」不同。** 记住「枚举最后一步」这个思路就够了。

复杂度：**O(m³)**，m = len(cuts) + 2。空间 O(m²)。
      题目 cuts ≤ 100 ⟹ 102³ ≈ 10⁶，可行。

边界：
  - cuts 只有一个切点 → 代价就是 n
  - cuts 已排序 / 乱序（**必须自己排序**）
  - cuts 包含靠近两端的点
  - n = 7, cuts = [1,3,4,5] → 16
  - n = 10, cuts = [1,9] → 19（两种顺序都是 10 + 9，这题的两端切点并不便宜）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 区间 DP，枚举「这一段的最后一刀」（两端补 0 和 n）
##### ! 时间复杂度: O(m^3)   空间复杂度: O(m^2)
##### ! 适用：所有「操作顺序影响代价」的区间题；和 LC-0312 共用「枚举最后一步」模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minCost(self, n: int, cuts: List[int]) -> int:
        points = [0] + sorted(cuts) + [n]       # ! 两端补上，消除边界特判
        m = len(points)
        dp = [[0] * m for _ in range(m)]
        # ! 按区间长度从小到大（length 是下标跨度），保证子区间先算完
        for length in range(2, m):
            for i in range(m - length):
                j = i + length
                # ! 这一段内部至少有一个切点才需要花钱
                dp[i][j] = min(dp[i][k] + dp[k][j] for k in range(i + 1, j)) + points[j] - points[i]
        return dp[0][m - 1]


##################################################################################################
##### ! Solution 2: 记忆化搜索（状态 = 区间两端的下标）
##### ! 时间复杂度: O(m^3)   空间复杂度: O(m^2)
##### ! 适用：最能看清「枚举最后一刀」这个决策；不用操心遍历顺序
##################################################################################################


class Solution_2:
    def minCost(self, n: int, cuts: List[int]) -> int:
        from functools import lru_cache
        points = [0] + sorted(cuts) + [n]

        @lru_cache(maxsize=None)
        def dfs(i: int, j: int) -> int:
            if j - i <= 1:
                return 0                         # ! 段内没有切点，不用花钱
            return min(dfs(i, k) + dfs(k, j) for k in range(i + 1, j)) + points[j] - points[i]

        res = dfs(0, len(points) - 1)
        dfs.cache_clear()
        return res


##################################################################################################
##### ! Solution 3: 暴力枚举所有切割顺序（基准答案，用来对拍；只适合很少的切点）
##### ! 时间复杂度: O(m! · m)   空间复杂度: O(m)
##### ! 适用：正确性参照 —— 直接验证「顺序确实影响代价」且 DP 找到了最优顺序
##################################################################################################


class Solution_3:
    def minCost(self, n: int, cuts: List[int]) -> int:
        from itertools import permutations
        best = float("inf")
        for order in permutations(cuts):
            segments = [(0, n)]
            cost = 0
            for c in order:
                for idx, (lo, hi) in enumerate(segments):
                    if lo < c < hi:
                        cost += hi - lo          # ! 代价 = 当前这段的长度
                        segments.pop(idx)
                        segments.append((lo, c))
                        segments.append((c, hi))
                        break
            best = min(best, cost)
        return int(best)


if __name__ == "__main__":
    import random

    cases = [(7, [1, 3, 4, 5], 16), (9, [5, 6, 1, 4, 2], 22), (5, [3], 5), (10, [1, 9], 19)]   # ! 不管先切哪一刀都是 10 + 9 = 19
    for n, cuts, want in cases:
        a = Solution_1().minCost(n, cuts[:])
        b = Solution_2().minCost(n, cuts[:])
        c = Solution_3().minCost(n, cuts[:])
        assert a == b == c == want, (n, cuts, a, b, c, want)
        print(f"n={n}, cuts={cuts} -> {a}")

    for _ in range(400):
        n = random.randint(2, 12)
        k = random.randint(1, min(5, n - 1))
        cuts = random.sample(range(1, n), k)
        a = Solution_1().minCost(n, cuts[:])
        b = Solution_2().minCost(n, cuts[:])
        c = Solution_3().minCost(n, cuts[:])
        assert a == b == c, (n, cuts, a, b, c)
    print("随机对拍 400 组通过 ✓（区间 DP == 记忆化 == 枚举所有切割顺序）")
