"""LC-0474 - Ones and Zeroes

Level 1 · 03 背包 DP —— **两个容量维度**的 0-1 背包
题目在问：给一堆二进制字符串，最多用 m 个 `0` 和 n 个 `1`，求最多能选几个字符串。

决定性观察：
  1. 这是标准 0-1 背包，只是**背包有两个容量**（0 的个数、1 的个数）：
     - 「物品」= 每个字符串
     - 「体积」= 该串里 0 的个数 和 1 的个数（**两个维度**）
     - 「价值」= 1（每个串算一个）
  2. `dp[i][j] = 用不超过 i 个 0、j 个 1 时最多能选几个串`。
     转移：`dp[i][j] = max(dp[i][j], dp[i-z][j-o] + 1)`
  3. **两个维度都要倒序遍历**：
     ```python
     for i in range(m, z - 1, -1):
         for j in range(n, o - 1, -1):
             dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)
     ```
     倒序保证每个字符串**只被用一次**（0-1 背包）。
     **任何一个维度写成正序，那个维度就变成完全背包，答案会偏大。**

### 背包维度的通用规律（本 Level 2 的主旨）

| 容量维度 | dp 形状 | 倒序的循环数 |
|---|---|---|
| 1 个（LC-0416、LC-0494、LC-1049） | `dp[capacity]` | 1 层 |
| **2 个**（本题） | `dp[m][n]` | **2 层都要倒序** |
| 2 个 + 计数（LC-0879） | `dp[m][n]` 但值是方案数 | 同上，转移从 max 换成 += |

**记住这条**：容量有几个维度，dp 就有几维，就有几层需要倒序。

复杂度：**O(L · m · n)**，L 是字符串个数。空间 O(m·n)。
      题目 L ≤ 600、m,n ≤ 100 ⟹ 600 × 100 × 100 = 6×10⁶，可行。

**常见误解**：这题看起来像「选最多的物品」的贪心（先选短的），
但**贪心是错的** —— 短的串可能 0 和 1 的分布很差。必须 DP。
反例：`strs = ["10","0001","111001","1","0"]`, m=5, n=3 → 答案 4，
贪心按长度选会选错。

边界：
  - m = n = 0 → 只能选空串（但题目保证串非空，所以是 0）
  - 单个字符串
  - 所有串都放不下 → 0
  - 所有串都能放下 → len(strs)
"""

from typing import List


##################################################################################################
##### ! Solution 1: 二维容量 0-1 背包（两层都倒序）
##### ! 时间复杂度: O(L · m · n)   空间复杂度: O(m · n)
##### ! 适用：背包有多个独立容量约束时；几个维度就几层倒序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for s in strs:
            z = s.count("0")
            o = len(s) - z
            # ! 两个维度都必须倒序，否则同一个字符串会被重复使用
            for i in range(m, z - 1, -1):
                for j in range(n, o - 1, -1):
                    cand = dp[i - z][j - o] + 1
                    if cand > dp[i][j]:
                        dp[i][j] = cand
        return dp[m][n]


##################################################################################################
##### ! Solution 2: 记忆化搜索（状态 = (下标, 剩余 0, 剩余 1)）
##### ! 时间复杂度: O(L · m · n)   空间复杂度: O(L · m · n)
##### ! 适用：先想到这版再压成背包很自然；也最能看清三个状态维度
##################################################################################################


class Solution_2:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        from functools import lru_cache
        counts = [(s.count("0"), len(s) - s.count("0")) for s in strs]
        L = len(counts)

        @lru_cache(maxsize=None)
        def dfs(i: int, z: int, o: int) -> int:
            if i == L:
                return 0
            best = dfs(i + 1, z, o)                      # ! 不选第 i 个
            cz, co = counts[i]
            if cz <= z and co <= o:
                best = max(best, 1 + dfs(i + 1, z - cz, o - co))   # ! 选第 i 个
            return best

        res = dfs(0, m, n)
        dfs.cache_clear()
        return res


##################################################################################################
##### ! Solution 3: 暴力枚举所有子集（基准答案，用来对拍；也用来证明贪心不对）
##### ! 时间复杂度: O(2^L · L)   空间复杂度: O(1)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        L = len(strs)
        counts = [(s.count("0"), len(s) - s.count("0")) for s in strs]
        best = 0
        for mask in range(1 << L):
            z = o = cnt = 0
            for i in range(L):
                if mask >> i & 1:
                    z += counts[i][0]
                    o += counts[i][1]
                    cnt += 1
            if z <= m and o <= n:
                best = max(best, cnt)
        return best


if __name__ == "__main__":
    import random

    cases = [(["10", "0001", "111001", "1", "0"], 5, 3, 4),
             (["10", "0", "1"], 1, 1, 2),
             (["0", "1"], 0, 0, 0),
             (["00", "11"], 2, 2, 2)]
    for strs, m, n, want in cases:
        a = Solution_1().findMaxForm(strs[:], m, n)
        b = Solution_2().findMaxForm(strs[:], m, n)
        c = Solution_3().findMaxForm(strs[:], m, n)
        assert a == b == c == want, (strs, m, n, a, b, c, want)
        print(f"{strs}, m={m}, n={n} -> {a}")

    for _ in range(500):
        L = random.randint(0, 8)
        strs = ["".join(random.choice("01") for _ in range(random.randint(1, 4))) for _ in range(L)]
        m, n = random.randint(0, 5), random.randint(0, 5)
        a = Solution_1().findMaxForm(strs[:], m, n)
        b = Solution_2().findMaxForm(strs[:], m, n)
        c = Solution_3().findMaxForm(strs[:], m, n)
        assert a == b == c, (strs, m, n, a, b, c)
    print("随机对拍 500 组通过 ✓（二维背包 == 记忆化 == 枚举所有子集）")
