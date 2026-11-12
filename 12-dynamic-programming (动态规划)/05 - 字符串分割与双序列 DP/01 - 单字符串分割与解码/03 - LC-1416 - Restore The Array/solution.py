"""LC-1416 - Restore The Array

Level 1 · 05 字符串分割与双序列 DP → Level 2 · 01 单字符串分割与解码

题目在问：一串数字 `s` 原本是若干个 `[1, k]` 范围内的整数**不带前导零**地拼起来的，问有多少种拆法（mod 1e9+7）。
它是 LC-0091 Decode Ways 的推广：0091 每段是 1..26（最多 2 位），本题每段是 1..k（最多 `len(str(k))` ≤ 10 位）。

### DP：dp[i] = s[i:] 的拆法数

    dp[n] = 1                                        # ! 空串：一种（什么都不拆）
    dp[i] = Σ dp[j]   对所有 j > i 使 s[i:j] 合法：s[i] != '0'，且 int(s[i:j]) <= k
    s[i] == '0' 时 dp[i] = 0（前导零，这里不能开始一段）

内层 j 最多走 `len(str(k))` ≤ 10 步 —— 一旦 `int(s[i:j]) > k` 就 break（数字只会越来越大）。
总复杂度 O(n · log₁₀k)。

### 和 0091 的两处差别

1. 段长上限从 2 变成 `len(str(k))` —— 所以内层要用 while/for 而不是手写两个 if。
2. 要取模。

### 空间优化

dp[i] 只依赖后面 ≤ 10 个位置，可以用长度 11 的滚动数组（`Solution_2`）。面试里说出来即可，一般不必写。
"""


MOD = 10 ** 9 + 7


##################################################################################################
##### ! Solution 1: 后缀 dp，内层最多 len(str(k)) 步，超 k 即 break
##### ! 时间复杂度: O(n · log₁₀k)   空间复杂度: O(n)
##### ! 适用：面试标准答案；逐位累加 num = num*10 + d 避免反复切片转 int
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numberOfArrays(self, s: str, k: int) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        dp[n] = 1
        for i in range(n - 1, -1, -1):
            if s[i] == "0":
                continue                                # ! 前导零：以 i 开头没有合法的段
            num = 0
            for j in range(i, n):
                num = num * 10 + (ord(s[j]) - 48)       # ! s[i..j] 的值
                if num > k:
                    break                               # ! 再长只会更大
                dp[i] = (dp[i] + dp[j + 1]) % MOD
        return dp[0]


##################################################################################################
##### ! Solution 2: 滚动数组（只保留后面 len(str(k)) + 1 个 dp 值）
##### ! 时间复杂度: O(n · log₁₀k)   空间复杂度: O(log₁₀k)
##### ! 适用：n 到 10^5 时省内存；用 deque 从左边推入最新的 dp[i]
##################################################################################################


class Solution_2:
    def numberOfArrays(self, s: str, k: int) -> int:
        from collections import deque
        n, L = len(s), len(str(k))
        window = deque([1])                             # ! window[t] = dp[i + 1 + t]
        for i in range(n - 1, -1, -1):
            cur = 0
            if s[i] != "0":
                num = 0
                for t in range(min(L, n - i)):          # ! 段长最多 L
                    num = num * 10 + (ord(s[i + t]) - 48)
                    if num > k:
                        break
                    cur = (cur + window[t]) % MOD
            window.appendleft(cur)
            if len(window) > L + 1:
                window.pop()
        return window[0]


##################################################################################################
##### ! Solution 3: 记忆化递归（自顶向下，最接近「枚举第一段」的直觉）
##### ! 时间复杂度: O(n · log₁₀k)   空间复杂度: O(n) 递归 + 缓存
##### ! 适用：面试先说这个再翻译成 dp。注意 n 到 10^5 时递归深度会爆，所以生产用 Solution_1
##################################################################################################


class Solution_3:
    def numberOfArrays(self, s: str, k: int) -> int:
        import sys
        from functools import lru_cache
        sys.setrecursionlimit(max(10000, len(s) + 100))
        n = len(s)

        @lru_cache(maxsize=None)
        def ways(i: int) -> int:
            if i == n:
                return 1
            if s[i] == "0":
                return 0
            total, num = 0, 0
            for j in range(i, n):
                num = num * 10 + int(s[j])
                if num > k:
                    break
                total += ways(j + 1)
            return total % MOD

        return ways(0)


def _brute(s, k):
    n = len(s)
    def rec(i):
        if i == n: return 1
        if s[i] == "0": return 0
        return sum(rec(j) for j in range(i + 1, n + 1) if int(s[i:j]) <= k)
    return rec(0) % MOD


if __name__ == "__main__":
    import random
    cases = [("1000", 10000, 1), ("1000", 10, 0), ("1317", 2000, 8), ("2020", 30, 1), ("1234567890", 90, 34)]
    for s, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().numberOfArrays(s, k)
            assert got == want, (cls.__name__, s, k, got, want)
    rng = random.Random(1416)
    for _ in range(3000):
        s = "".join(rng.choice("0123") for _ in range(rng.randint(1, 10)))
        k = rng.choice([1, 2, 9, 10, 23, 99, 100, 312, 1000])
        want = _brute(s, k)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().numberOfArrays(s, k) == want, (cls.__name__, s, k)
    print("所有测试通过 ✓")
