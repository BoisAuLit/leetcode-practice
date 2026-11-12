"""LC-0354 - Russian Doll Envelopes

Level 1 · 04 子序列 DP —— **二维 LIS：用排序消掉一个维度**
题目在问：信封 `(w, h)`，能嵌套要求**两个维度都严格更大**。求最多能嵌套几层。

决定性观察（排序规则是全题的灵魂）：
  1. 两个维度都要递增 ⟹ **先排序固定一个维度，另一个维度上做 LIS**。
  2. **排序规则必须是：`w` 升序，`w` 相同时 `h` 降序。**
     ```python
     envelopes.sort(key=lambda e: (e[0], -e[1]))
     ```
  3. **为什么 `h` 要降序**（这是本题最关键、也最容易错的一点）：
     题目要求**严格**大于，所以 `w` 相同的信封**不能互相嵌套**。
     如果 `h` 升序排，`[(1,2), (1,3)]` 在 h 序列里是 `[2, 3]` ——
     LIS 会把它们算成两层，**但它们的 w 相同，根本套不进去**。
     `h` 降序排之后变成 `[3, 2]`，LIS 只会取一个，正好排除了这种非法情形。
  4. 排完序后，直接在 `h` 序列上求 **严格递增**的 LIS 长度。
     用 LC-0300 的 O(n log n) 贪心 + 二分：`bisect_left`（严格递增用 left）。

**`bisect_left` 还是 `bisect_right`**：
  - **严格递增 LIS** ⟹ `bisect_left`（相等的会替换掉，不会增长长度）
  - 非严格（允许相等）⟹ `bisect_right`
  本题要严格 ⟹ `bisect_left`。这个选择和上面的 `h` 降序排是**配套**的。

复杂度：**O(n log n)** 时间（排序 + 二分 LIS），O(n) 空间。
      O(n²) 的朴素 LIS 在 n = 10⁵ 时会 TLE，所以这题**必须**用二分版。

### 和 LC-0300 的关系
LC-0300 是一维 LIS。本题 = **排序消一维 + 一维 LIS**。
这个「排序降维」的套路还能继续推广到三维（LC-1691 Maximum Height by Stacking Cuboids
需要先对每个长方体内部排序，再排序 + LIS）。

边界：
  - 空数组 → 0
  - 全部 w 相同 → 1
  - 全部完全相同 → 1
  - `[[5,4],[6,4],[6,7],[2,3]]` → 3
  - 单个信封 → 1
"""

from bisect import bisect_left
from typing import List


##################################################################################################
##### ! Solution 1: (w 升序, h 降序) 排序 + h 上的 O(n log n) 严格递增 LIS
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：二维（及更高维）的嵌套/包含问题；核心是「排序消一维」+ 正确的 tie-break
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        if not envelopes:
            return 0
        # ! w 升序；w 相同时 h **降序** —— 保证同宽的信封不会被 LIS 算成多层
        envelopes.sort(key=lambda e: (e[0], -e[1]))
        tails: List[int] = []                 # ! tails[k] = 长度为 k+1 的递增序列的最小结尾
        for _, h in envelopes:
            i = bisect_left(tails, h)         # ! 严格递增 ⟹ bisect_left
            if i == len(tails):
                tails.append(h)
            else:
                tails[i] = h
        return len(tails)


##################################################################################################
##### ! Solution 2: 同样排序 + O(n^2) 朴素 LIS（n 大会 TLE，但逻辑最直白）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：理解用；也用来对拍。注意它可以不依赖「h 降序」的技巧，直接双重判断
##################################################################################################


class Solution_2:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        n = len(envelopes)
        if n == 0:
            return 0
        envelopes.sort(key=lambda e: (e[0], e[1]))
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                # ! 两个维度都严格更大才能嵌套（这里显式判断，所以不依赖 h 的排序方向）
                if envelopes[j][0] < envelopes[i][0] and envelopes[j][1] < envelopes[i][1]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


##################################################################################################
##### ! Solution 3: 暴力枚举所有子集（基准答案，用来对拍；只适合很少的信封）
##### ! 时间复杂度: O(2^n · n log n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接验证「严格两维递增」这个定义
##################################################################################################


class Solution_3:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        n = len(envelopes)
        best = 0
        for mask in range(1 << n):
            sub = sorted(envelopes[i] for i in range(n) if mask >> i & 1)
            ok = all(sub[i][0] < sub[i + 1][0] and sub[i][1] < sub[i + 1][1]
                     for i in range(len(sub) - 1))
            if ok:
                best = max(best, len(sub))
        return best


if __name__ == "__main__":
    import random

    cases = [([[5, 4], [6, 4], [6, 7], [2, 3]], 3), ([[1, 1], [1, 1], [1, 1]], 1),
             ([], 0), ([[1, 1]], 1), ([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]], 4)]
    for env, want in cases:
        a = Solution_1().maxEnvelopes([e[:] for e in env])
        b = Solution_2().maxEnvelopes([e[:] for e in env])
        c = Solution_3().maxEnvelopes([e[:] for e in env])
        assert a == b == c == want, (env, a, b, c, want)
        print(f"{env} -> {a}")

    for _ in range(600):                 # ! 小值域随机对拍，专压「同宽不同高」的陷阱
        n = random.randint(0, 8)
        env = [[random.randint(1, 4), random.randint(1, 4)] for _ in range(n)]
        a = Solution_1().maxEnvelopes([e[:] for e in env])
        b = Solution_2().maxEnvelopes([e[:] for e in env])
        c = Solution_3().maxEnvelopes([e[:] for e in env])
        assert a == b == c, (env, a, b, c)
    print("随机对拍 600 组通过 ✓（排序+二分 LIS == O(n²) LIS == 枚举所有子集）")
