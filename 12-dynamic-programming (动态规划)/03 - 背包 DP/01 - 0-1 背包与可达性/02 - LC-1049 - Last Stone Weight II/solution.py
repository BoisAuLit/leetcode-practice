"""LC-1049 - Last Stone Weight II

Level 1 · 03 背包 DP —— **伪装成模拟题的 0-1 背包**
题目在问：每次挑两块石头对撞，剩下重量差，求最后剩下的最小重量。

决定性观察（整道题就是这一步转化）：
  1. 每次对撞相当于给两块石头**各赋一个 ± 号**。
     反复对撞之后，最终结果等价于：
     **给每块石头赋 `+` 或 `-`，求 `|Σ ± stone|` 的最小值。**
  2. 设赋 `+` 的那组和为 P，赋 `-` 的为 N，则 `P + N = total`，答案 = `|P - N|`。
     要让 `|P - N|` 最小，就要让 **P 尽量接近 total / 2**。
  3. 于是问题变成：**从石头里选一个子集，使它的和尽量接近但不超过 `total // 2`**
     ⟹ **0-1 背包可达性**（和 LC-0416 Partition Equal Subset Sum 是同一个模型，
     只是 416 问「能否恰好等于一半」，本题问「最接近一半是多少」）。
  4. 答案 = `total - 2 * best`，其中 `best` 是不超过 `total//2` 的最大可达和。

**为什么「赋 ± 号」的等价性成立**（值得想清楚）：
  对撞 `a, b → |a-b|` 相当于把 b 的符号取反后合并。
  反过来，任何一种 ± 赋值（只要两组都非空）都能通过某个对撞顺序实现。
  所以两个问题的可达结果集合相同。

```python
total = sum(stones); half = total // 2
dp = [False] * (half + 1); dp[0] = True
for s in stones:
    for j in range(half, s - 1, -1):      # ★ 倒序 = 0-1 背包
        dp[j] |= dp[j - s]
best = max(j for j in range(half, -1, -1) if dp[j])
return total - 2 * best
```

**倒序遍历**是 0-1 背包的标志（每块石头只能用一次）。正序会变成完全背包。

复杂度：**O(n · total)** 时间，O(total) 空间。
      题目限制 `n <= 30`、`stones[i] <= 100` ⟹ total <= 3000，完全可行。

和同 Level 2 另一道题的关系：

| | LC-0416 | LC-1049 本题 |
|---|---|---|
| 问什么 | 能否划分成**两个和相等**的子集 | 两组和的差**最小是多少** |
| DP | `dp[half]` 是否可达 | 不超过 half 的**最大可达和** |
| 答案 | bool | `total - 2 * best` |

**416 是本题的特例**：当 `best == half` 时答案为 0（或 1，取决于 total 的奇偶）。

边界：
  - 单块石头 → 它自己的重量
  - 两块相同 → 0
  - 全部相同且偶数块 → 0
  - `[2,7,4,1,8,1]` → 1
  - 和为奇数 → 答案至少是 1
"""

from typing import List


##################################################################################################
##### ! Solution 1: 转成 0-1 背包可达性，求不超过 total//2 的最大可达和
##### ! 时间复杂度: O(n · total)   空间复杂度: O(total)
##### ! 适用：所有「把元素分成两组使差最小」的题；和 LC-0416 同一个模型
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        total = sum(stones)
        half = total // 2
        dp = [False] * (half + 1)
        dp[0] = True                           # ! 空集的和是 0
        for s in stones:
            for j in range(half, s - 1, -1):   # ! 倒序 ⟹ 每块石头只用一次（0-1 背包）
                if dp[j - s]:
                    dp[j] = True
        best = max(j for j in range(half, -1, -1) if dp[j])
        return total - 2 * best                # ! |P - N| = total - 2P


##################################################################################################
##### ! Solution 2: 用 set 记录所有可达的子集和（写法更短，思路相同）
##### ! 时间复杂度: O(n · total)   空间复杂度: O(total)
##### ! 适用：不想手写背包循环时；Python 的 set 推导很适合表达「可达集合」
##################################################################################################


class Solution_2:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        total = sum(stones)
        reachable = {0}
        for s in stones:
            reachable |= {r + s for r in reachable}       # ! 每块石头选或不选
        return min(abs(total - 2 * r) for r in reachable)  # ! 直接取 |P - N| 的最小值


##################################################################################################
##### ! Solution 3: 暴力枚举所有 ± 赋值（基准答案，用来对拍）
##### ! 时间复杂度: O(2^n)   空间复杂度: O(1)
##### ! 适用：正确性参照 —— 直接验证「对撞 ⟺ 赋 ± 号」这个转化
##################################################################################################


class Solution_3:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        n = len(stones)
        total = sum(stones)
        best = total
        for mask in range(1 << n):
            p = sum(stones[i] for i in range(n) if mask >> i & 1)
            best = min(best, abs(total - 2 * p))
        return best


if __name__ == "__main__":
    import random

    cases = [([2, 7, 4, 1, 8, 1], 1), ([31, 26, 33, 21, 40], 5), ([1], 1),
             ([3, 3], 0), ([1, 2], 1), ([2, 2, 2, 2], 0)]
    for stones, want in cases:
        a = Solution_1().lastStoneWeightII(stones[:])
        b = Solution_2().lastStoneWeightII(stones[:])
        c = Solution_3().lastStoneWeightII(stones[:])
        assert a == b == c == want, (stones, a, b, c, want)
        print(f"{stones} -> {a}")

    for _ in range(600):
        stones = [random.randint(1, 15) for _ in range(random.randint(1, 10))]
        a = Solution_1().lastStoneWeightII(stones[:])
        b = Solution_2().lastStoneWeightII(stones[:])
        c = Solution_3().lastStoneWeightII(stones[:])
        assert a == b == c, (stones, a, b, c)
    print("随机对拍 600 组通过 ✓（0-1 背包 == 可达集合 == 枚举所有 ± 赋值）")
