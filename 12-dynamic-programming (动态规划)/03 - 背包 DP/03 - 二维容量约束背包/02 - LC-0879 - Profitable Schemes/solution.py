"""LC-0879 - Profitable Schemes

Level 1 · 03 背包 DP —— 二维约束 + **计数**（而不是求最值）
题目在问：n 个人，每个犯罪 i 需要 `group[i]` 人、产生 `profit[i]` 利润。
         每个人最多参与一个犯罪。求**利润至少为 minProfit** 的方案数（对 1e9+7 取模）。

和 LC-0474 的关系（同一个 Level 2 的原因）：

| | LC-0474 Ones and Zeroes | LC-0879 本题 |
|---|---|---|
| 两个维度 | 0 的个数、1 的个数 | **人数**、**已获利润** |
| dp 的值 | 最多选几个（**max**） | **方案数**（**计数**） |
| 转移 | `dp = max(dp, dp' + 1)` | `dp += dp'` |
| 维度的方向 | 两个都是「不超过」 | 人数「不超过」，利润「**至少**」 |

**本题的两个关键技巧：**

### ① 利润维度要「封顶」
利润是「**至少** minProfit」，上界无穷。
技巧：**把所有超过 minProfit 的利润都当成 minProfit**：
```python
np_ = min(minProfit, p + profit[i])
```
因为「已经达标」之后再多赚也没有区别，所以状态可以合并。
**这一步把无界的维度压成了有界的 minProfit + 1 个取值**，是本题能做的前提。

### ② 初始状态：0 人 0 利润算一种方案
`dp[0][0] = 1`。如果 `minProfit == 0`，那么「什么都不做」也是一个合法方案。
所以答案里包含空方案 —— 这是题目的定义，别漏。

```python
dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
dp[0][0] = 1
for g, pr in zip(group, profit):
    for people in range(n, g - 1, -1):           # ★ 倒序：每个犯罪只做一次
        for p in range(minProfit, -1, -1):
            np_ = min(minProfit, p + pr)
            dp[people][np_] = (dp[people][np_] + dp[people - g][p]) % MOD
return sum(dp[people][minProfit] for people in range(n + 1)) % MOD
```

**答案要把所有人数求和**：`dp[people][minProfit]` 对 `people = 0..n` 全加起来 ——
因为「最多 n 人」，用几个人都算合法方案。

**注意内层的 p 也倒序**：虽然利润维度是「取 min 封顶」的，正序会让同一个犯罪
在同一轮里被重复计入（因为 `np_ >= p`，正序时 `dp[people-g][p]` 可能已经被本轮更新过）。
倒序最安全。

复杂度：**O(len(group) · n · minProfit)** 时间，O(n · minProfit) 空间。
      题目 group ≤ 100、n ≤ 100、minProfit ≤ 100 ⟹ 10⁶，可行。

边界：
  - `minProfit == 0` → 包含空方案
  - 某个 `group[i] > n` → 那个犯罪永远做不了
  - 所有利润都是 0 且 minProfit > 0 → 0
  - 单个犯罪
"""

from typing import List

MOD = 10**9 + 7


##################################################################################################
##### ! Solution 1: 二维约束 0-1 背包计数（利润维度取 min 封顶）
##### ! 时间复杂度: O(len(group) · n · minProfit)   空间复杂度: O(n · minProfit)
##### ! 适用：「至少达到某个值」的计数型背包；核心是把无界维度 min 封顶
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
        dp[0][0] = 1                               # ! 0 人 0 利润算一种方案（空方案）
        for g, pr in zip(group, profit):
            for people in range(n, g - 1, -1):     # ! 倒序：每个犯罪只能做一次
                for p in range(minProfit, -1, -1):
                    np_ = min(minProfit, p + pr)   # ! 关键：超过 minProfit 的都当成 minProfit
                    dp[people][np_] = (dp[people][np_] + dp[people - g][p]) % MOD
        # ! 用 0..n 个人都算合法，全部求和
        return sum(dp[people][minProfit] for people in range(n + 1)) % MOD


##################################################################################################
##### ! Solution 2: 记忆化搜索（状态 = (下标, 剩余人数, 还差多少利润)）
##### ! 时间复杂度: 同上   空间复杂度: 同上
##### ! 适用：最能看清三个状态维度；「还差多少利润」用 max(0, ...) 封底，等价于上面的 min 封顶
##################################################################################################


class Solution_2:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        from functools import lru_cache
        L = len(group)

        @lru_cache(maxsize=None)
        def dfs(i: int, people: int, need: int) -> int:
            if i == L:
                return 1 if need == 0 else 0       # ! need 已经降到 0 ⟹ 达标
            res = dfs(i + 1, people, need)         # ! 不做第 i 个犯罪
            if group[i] <= people:
                # ! max(0, ...) 封底：利润超了就记作「还差 0」
                res += dfs(i + 1, people - group[i], max(0, need - profit[i]))
            return res % MOD

        r = dfs(0, n, minProfit)
        dfs.cache_clear()
        return r


##################################################################################################
##### ! Solution 3: 暴力枚举所有犯罪子集（基准答案，用来对拍）
##### ! 时间复杂度: O(2^L · L)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        L = len(group)
        cnt = 0
        for mask in range(1 << L):
            people = tot = 0
            for i in range(L):
                if mask >> i & 1:
                    people += group[i]
                    tot += profit[i]
            if people <= n and tot >= minProfit:
                cnt += 1
        return cnt % MOD


if __name__ == "__main__":
    import random

    cases = [(5, 3, [2, 2], [2, 3], 2), (10, 5, [2, 3, 5], [6, 7, 8], 7),
             (1, 0, [1], [1], 2), (1, 1, [2], [5], 0), (2, 0, [1, 1], [0, 0], 4)]
    for n, mp, g, p, want in cases:
        a = Solution_1().profitableSchemes(n, mp, g[:], p[:])
        b = Solution_2().profitableSchemes(n, mp, tuple(g), tuple(p))
        c = Solution_3().profitableSchemes(n, mp, g[:], p[:])
        assert a == b == c == want, (n, mp, g, p, a, b, c, want)
        print(f"n={n}, minProfit={mp} -> {a}")

    for _ in range(500):
        L = random.randint(0, 7)
        g = [random.randint(1, 4) for _ in range(L)]
        p = [random.randint(0, 4) for _ in range(L)]
        n = random.randint(0, 6)
        mp = random.randint(0, 6)
        a = Solution_1().profitableSchemes(n, mp, g[:], p[:])
        b = Solution_2().profitableSchemes(n, mp, tuple(g), tuple(p))
        c = Solution_3().profitableSchemes(n, mp, g[:], p[:])
        assert a == b == c, (n, mp, g, p, a, b, c)
    print("随机对拍 500 组通过 ✓（二维计数背包 == 记忆化 == 枚举所有子集）")
