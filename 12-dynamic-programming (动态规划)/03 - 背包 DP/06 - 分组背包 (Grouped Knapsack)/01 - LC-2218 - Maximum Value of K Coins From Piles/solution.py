"""LC-2218 - Maximum Value of K Coins From Piles

Level 1 · 03 背包 DP → Level 2 · 06 分组背包 (Grouped Knapsack)

题目在问：n 堆硬币，每堆只能**从顶往下**依次拿；总共拿恰好 k 枚，最大价值。Σ堆大小 ≤ 2000，k ≤ 2000。

### 这是分组背包：每一堆是一个「组」，组内的选项是「拿前 j 枚」（互斥）

    dp[i][c] = 前 i 堆、总共拿 c 枚 的最大价值
    dp[i][c] = max over 0 <= j <= min(c, len(pile_i)):  dp[i-1][c - j] + prefix_i[j]
    prefix_i[j] = 第 i 堆前 j 枚的和

组内「拿 0 枚 / 1 枚 / … / m 枚」是互斥的选项，这就是**分组背包**和 0-1 背包的区别：
0-1 背包每个物品只有「选 / 不选」两个选项；分组背包每组有多个互斥选项，但每组最多选一个。

### 复杂度：别算成 O(n·k·m)

内层 j 最多走 `len(pile_i)` 步，所有堆加起来 Σm = 2000。所以总复杂度是 **O(k · Σm) = 4×10⁶**，不是 n·k·m。
面试里能把这一点说清楚是加分项。

### 一维滚动：c 必须倒序

和 0-1 背包一样，`dp[c]` 只能用「上一堆」的值，所以 c 从大到小枚举，保证 `dp[c − j]` 还没被本堆更新过。
"""
from functools import lru_cache
from itertools import accumulate
from typing import List


##################################################################################################
##### ! Solution 1: 分组背包，一维滚动数组，c 倒序
##### ! 时间复杂度: O(k · Σ|pile|)   空间复杂度: O(k)
##### ! 适用：面试标准答案；每堆先算前缀和，再对 c 倒序、j 正序更新
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        dp = [0] * (k + 1)                              # ! dp[c] = 恰好拿 c 枚的最大价值（拿不满就是 0，后面会被覆盖）
        for pile in piles:
            prefix = [0] + list(accumulate(pile))       # ! prefix[j] = 前 j 枚的和
            m = len(pile)
            for c in range(k, 0, -1):                   # ! 倒序：dp[c - j] 还是上一堆的值
                for j in range(1, min(c, m) + 1):
                    dp[c] = max(dp[c], dp[c - j] + prefix[j])   # ! 这堆拿 j 枚
        return dp[k]


##################################################################################################
##### ! Solution 2: 二维 dp[i][c]（不滚动，便于理解和回溯）
##### ! 时间复杂度: O(k · Σ|pile|)   空间复杂度: O(n · k)
##### ! 适用：先写这个把转移说清楚，再压成 Solution_1
##################################################################################################


class Solution_2:
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        n = len(piles)
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        for i, pile in enumerate(piles, 1):
            prefix = [0] + list(accumulate(pile))
            for c in range(k + 1):
                dp[i][c] = dp[i - 1][c]                 # ! 这堆拿 0 枚
                for j in range(1, min(c, len(pile)) + 1):
                    dp[i][c] = max(dp[i][c], dp[i - 1][c - j] + prefix[j])
        return dp[n][k]


##################################################################################################
##### ! Solution 3: 记忆化递归 f(i, c)（自顶向下）
##### ! 时间复杂度: O(k · Σ|pile|)   空间复杂度: O(n · k)
##### ! 适用：最接近「对每一堆决定拿几枚」的直觉；它也是对拍的真值基线
##################################################################################################


class Solution_3:
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        n = len(piles)

        @lru_cache(maxsize=None)
        def f(i: int, c: int) -> int:
            if i == n or c == 0:
                return 0
            best, s = f(i + 1, c), 0
            for j in range(1, min(c, len(piles[i])) + 1):
                s += piles[i][j - 1]
                best = max(best, s + f(i + 1, c - j))
            return best

        return f(0, k)


if __name__ == "__main__":
    import random
    cases = [([[1, 100, 3], [7, 8, 9]], 2, 101), ([[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]], 7, 706), ([[5]], 1, 5)]
    for piles, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().maxValueOfCoins([p[:] for p in piles], k)
            assert got == want, (cls.__name__, piles, k, got, want)
    rng = random.Random(2218)
    for _ in range(2000):
        piles = [[rng.randint(1, 20) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 5))]
        k = rng.randint(1, sum(len(p) for p in piles))
        outs = [cls().maxValueOfCoins([p[:] for p in piles], k) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (piles, k, outs)
    print("所有测试通过 ✓")
