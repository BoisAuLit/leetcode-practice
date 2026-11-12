"""LC-0516 - Longest Palindromic Subsequence

Level 1 · 08 区间 DP 与博弈 —— **区间 DP 的入门题**
题目在问：最长回文**子序列**（不要求连续）的长度。

### 区间 DP 的三件套（本 Level 1 共用）
1. **状态**：`dp[i][j] = 区间 [i, j] 上的答案`。
2. **转移**：看区间**两端**（或枚举区间内的分割点 / 最后一步）。
3. **遍历顺序**：**必须保证小区间先算完** ——
   要么按**区间长度**从小到大，要么 `i` 倒序 + `j` 正序。

本题的转移：
```
s[i] == s[j]  →  dp[i][j] = dp[i+1][j-1] + 2        （两端配上）
s[i] != s[j]  →  dp[i][j] = max(dp[i+1][j], dp[i][j-1])   （弃掉一端）
dp[i][i] = 1                                          （单字符是长度 1 的回文）
```

**为什么 `dp[i+1][j-1]` 保证已算完**：它的区间更短。
所以用 `for i in range(n-1, -1, -1): for j in range(i+1, n)` 的顺序 ——
`i+1 > i`（已算过），`j-1 < j`（本轮已算过）。

### 一个漂亮的等价结论
**最长回文子序列 = `LCS(s, reverse(s))`**。
因为回文子序列在正序和逆序里都存在。
所以本题可以直接复用 LC-1143 的 LCS 代码（Solution_2）。
面试里说出这个等价关系是加分项。

### 不要和「最长回文**子串**」混（LC-0005）

| | LC-0516 子序列 | LC-0005 子串 |
|---|---|---|
| 连续吗 | **不要求** | 要求连续 |
| 解法 | 区间 DP / LCS | 中心扩展（O(n²) O(1) 空间）或 Manacher |
| LC-0005 位置 | — | [02-two-pointers](<../../../02-two-pointers (双指针)/04 - 回文与字符串双指针 (Palindrome)/02 - 中心扩展 (Expand Around Center)/01 - LC-0005 - Longest Palindromic Substring>) |

复杂度：**O(n²)** 时间、O(n²) 空间（可以滚动到 O(n)）。

边界：
  - 单字符 → 1
  - 全部相同 → n
  - 无重复字符 → 1
  - `"bbbab"` → 4
"""

from typing import List


##################################################################################################
##### ! Solution 1: 区间 DP（i 倒序、j 正序，保证小区间先算完）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：区间 DP 的标准模板；看两端是否相等决定转移
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        dp = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1                           # ! 单字符本身就是回文
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2    # ! 两端配上（i+1 > i，区间更短，已算完）
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])   # ! 弃掉一端
        return dp[0][n - 1]


##################################################################################################
##### ! Solution 2: LCS(s, reverse(s)) —— 直接复用 LC-1143 的代码
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：说明「最长回文子序列 == s 和它的逆序的 LCS」；面试说出这个等价是加分项
##################################################################################################


class Solution_2:
    def longestPalindromeSubseq(self, s: str) -> int:
        t = s[::-1]
        n = len(s)
        prev = [0] * (n + 1)
        for i in range(1, n + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[n]


##################################################################################################
##### ! Solution 3: 暴力枚举所有子序列（基准答案，用来对拍；只适合很短的串）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        best = 0
        for mask in range(1 << n):
            sub = "".join(s[i] for i in range(n) if mask >> i & 1)
            if sub == sub[::-1]:
                best = max(best, len(sub))
        return best


if __name__ == "__main__":
    import random

    cases = [("bbbab", 4), ("cbbd", 2), ("a", 1), ("", 0), ("abcde", 1), ("aaaa", 4)]
    for s, want in cases:
        a = Solution_1().longestPalindromeSubseq(s)
        b = Solution_2().longestPalindromeSubseq(s)
        c = Solution_3().longestPalindromeSubseq(s)
        assert a == b == c == want, (s, a, b, c, want)
        print(f"{s!r} -> {a}")

    for _ in range(800):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 11)))
        a = Solution_1().longestPalindromeSubseq(s)
        b = Solution_2().longestPalindromeSubseq(s)
        c = Solution_3().longestPalindromeSubseq(s)
        assert a == b == c, (s, a, b, c)
    print("随机对拍 800 组通过 ✓（区间 DP == LCS(s, reversed(s)) == 枚举所有子序列）")
