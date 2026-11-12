"""LC-1092 - Shortest Common Supersequence

Level 1 · 05 字符串分割与双序列 DP → Level 2 · 02 LCS 与连续公共片段

题目在问：求一个**最短**的字符串，使 `str1` 和 `str2` 都是它的子序列。输出任一解。

### 决定性观察：SCS = 把 LCS 只写一遍，其余字符按顺序插进去

    |SCS| = |str1| + |str2| − |LCS|

公共子序列里的字符两边共享，所以 LCS 越长，SCS 越短；最优就是取**最长**公共子序列。
构造答案 = **沿着 LCS 的 DP 表回溯**：
- `str1[i] == str2[j]`：这是 LCS 的字符，输出一次，i、j 同时退
- 否则看 dp 表哪边大就退哪边，把被跳过的字符输出（它只属于一边）
- 一边走完后，把另一边剩下的全部输出

### 两种回溯写法

1. 先算 LCS 字符串，再**双指针合并**：对 LCS 的每个字符 c，把 str1 中 c 之前的、str2 中 c 之前的字符都先输出，再输出 c。
   概念最清楚，适合口述。
2. 直接在 dp 表上从 (n, m) 往回走（`Solution_2`），一遍完成；代码短但要小心边界。

### 和 LC-1143 的关系

1143 只要长度；本题要**构造**。构造类 DP 的通用套路：**正着填表，倒着回溯**。
"""
from typing import List


##################################################################################################
##### ! Solution 1: LCS 表 + 回溯得到 LCS 字符串 + 双指针合并
##### ! 时间复杂度: O(n·m)   空间复杂度: O(n·m)
##### ! 适用：面试标准答案，三步分明：① dp 表 ② 回溯出 LCS ③ 按 LCS 合并两串
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]      # ! dp[i][j] = LCS(str1[:i], str2[:j])
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dp[i][j] = dp[i - 1][j - 1] + 1 if str1[i - 1] == str2[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
        # ! ② 回溯出 LCS
        lcs, i, j = [], n, m
        while i and j:
            if str1[i - 1] == str2[j - 1]:
                lcs.append(str1[i - 1]); i -= 1; j -= 1
            elif dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        lcs.reverse()
        # ! ③ 以 LCS 为骨架合并：每个 LCS 字符之前，先把两边「不属于 LCS」的字符按顺序放进去
        out, i, j = [], 0, 0
        for c in lcs:
            while str1[i] != c:
                out.append(str1[i]); i += 1
            while str2[j] != c:
                out.append(str2[j]); j += 1
            out.append(c); i += 1; j += 1
        out.append(str1[i:]); out.append(str2[j:])      # ! 剩余尾巴
        return "".join(out)


##################################################################################################
##### ! Solution 2: 直接在 dp 表上回溯构造（一遍完成）
##### ! 时间复杂度: O(n·m)   空间复杂度: O(n·m)
##### ! 适用：代码更短。从 (n, m) 往回走：相等 → 输出一次并双退；否则往 dp 大的那边退并输出被跳过的字符；最后补另一边
##################################################################################################


class Solution_2:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dp[i][j] = dp[i - 1][j - 1] + 1 if str1[i - 1] == str2[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
        out, i, j = [], n, m
        while i and j:
            if str1[i - 1] == str2[j - 1]:
                out.append(str1[i - 1]); i -= 1; j -= 1
            elif dp[i - 1][j] >= dp[i][j - 1]:
                out.append(str1[i - 1]); i -= 1        # ! 这个字符只属于 str1
            else:
                out.append(str2[j - 1]); j -= 1
        out.append(str1[:i][::-1]); out.append(str2[:j][::-1])   # ! 剩余部分（倒着放，最后整体反转）
        return "".join(out)[::-1]


##################################################################################################
##### ! Solution 3: 直接对 SCS 长度做 DP（不经过 LCS），再回溯
##### ! 时间复杂度: O(n·m)   空间复杂度: O(n·m)
##### ! 适用：展示「SCS 自己也有递推」：f[i][j] = f[i-1][j-1] + 1（相等）/ min(f[i-1][j], f[i][j-1]) + 1；
#####         边界 f[i][0] = i, f[0][j] = j。回溯方式与 Solution_2 对称
##################################################################################################


class Solution_3:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            f[i][0] = i
        for j in range(m + 1):
            f[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                f[i][j] = f[i - 1][j - 1] + 1 if str1[i - 1] == str2[j - 1] else min(f[i - 1][j], f[i][j - 1]) + 1
        out, i, j = [], n, m
        while i and j:
            if str1[i - 1] == str2[j - 1]:
                out.append(str1[i - 1]); i -= 1; j -= 1
            elif f[i - 1][j] <= f[i][j - 1]:
                out.append(str1[i - 1]); i -= 1
            else:
                out.append(str2[j - 1]); j -= 1
        out.append(str1[:i][::-1]); out.append(str2[:j][::-1])
        return "".join(out)[::-1]


def _is_subseq(a: str, b: str) -> bool:
    it = iter(b)
    return all(c in it for c in a)


def _lcs_len(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


if __name__ == "__main__":
    import random
    for a, b in [("abac", "cab"), ("aaaaaaaa", "aaaaaaaa"), ("a", "b"), ("geek", "eke"), ("", "abc") if False else ("abc", "abc")]:
        want_len = len(a) + len(b) - _lcs_len(a, b)
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().shortestCommonSupersequence(a, b)
            assert len(got) == want_len and _is_subseq(a, got) and _is_subseq(b, got), (cls.__name__, a, b, got)
    assert Solution_1().shortestCommonSupersequence("abac", "cab") in ("cabac",)      # ! 题目样例
    rng = random.Random(1092)
    for _ in range(3000):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        want_len = len(a) + len(b) - _lcs_len(a, b)
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().shortestCommonSupersequence(a, b)
            assert len(got) == want_len and _is_subseq(a, got) and _is_subseq(b, got), (cls.__name__, a, b, got)
    print("所有测试通过 ✓（长度最短 + 两串都是子序列）")
