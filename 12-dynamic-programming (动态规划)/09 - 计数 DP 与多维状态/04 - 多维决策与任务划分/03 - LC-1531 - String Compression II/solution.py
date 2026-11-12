"""LC-1531 - String Compression II

Level 1 · 09 计数 DP 与多维状态 → Level 2 · 04 多维决策与任务划分

题目在问：最多删 k 个字符，使 run-length 编码（"aabccc" → "a2bc3"）后的长度最短。n ≤ 100，k ≤ 100。Hard。

### 编码长度的规则（先把它写成函数，别在 DP 里现算）

    一段连续 c 重复 m 次的编码长度 = 1 (m==1) / 2 (2..9) / 3 (10..99) / 4 (100)

### 状态设计：dp[i][k] = 处理 s[i:]、还能删 k 个 的最短编码长度

转移时在 i 处做决定：
- **删掉 s[i]**：`dp[i+1][k−1] + 0`
- **保留 s[i]，并以它为一段的开头**：往后扫 j = i..n−1，**保留所有等于 s[i] 的字符，删掉不等于的**（删掉的数量 `diff` 不能超过 k），
  段长 `same` 的编码长度 + `dp[j+1][k − diff]`。

为什么「保留 s[i] 之后只保留和它相同的、删掉不同的」是无损的？
因为一段的编码只取决于它的字符和长度；中间夹着别的字符会把这一段切断、只会更长。所以**在决定「s[i] 开一段」后，这一段应该尽量吞掉后面所有相同字符**，中间的异类要么被删、要么成为这一段的终点（终点由 j 的枚举决定）。

状态 O(n·k)，转移 O(n) ⟹ O(n²·k) = 10⁶，够。

### 另一种状态（Solution_2）：dp[i][k][last][cnt] 太大，所以用「前一段信息压进递归参数 + 记忆化」

记忆化递归 `f(i, k, prev_char, prev_cnt)`：状态数 n·k·26·100 看上去是 2.6×10⁷，但实际可达状态少很多，Python 里能过。
它的好处是**转移只有两种**（删 / 不删），不需要「向后吞」的内层循环，更接近直觉；坏处是状态更多。面试里先讲它再优化成 Solution_1。
"""
from functools import lru_cache


def enc_len(m: int) -> int:
    """m 个相同字符的 run-length 编码长度。"""
    return 1 if m == 1 else 2 if m < 10 else 3 if m < 100 else 4


##################################################################################################
##### ! Solution 1: dp[i][k]，转移「删 s[i]」或「s[i] 开一段并向后吞掉相同字符」
##### ! 时间复杂度: O(n² · k)   空间复杂度: O(n · k)
##### ! 适用：面试标准答案（官方题解方向）。向后扫时 same/diff 两个计数增量维护
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        INF = float("inf")

        @lru_cache(maxsize=None)
        def dp(i: int, k: int) -> int:
            if k < 0:
                return INF
            if i + k >= n:                              # ! 剩下的全删得起 → 长度 0
                return 0
            best = dp(i + 1, k - 1)                     # ! 删掉 s[i]
            same = diff = 0
            for j in range(i, n):                       # ! s[i] 开一段，吞到 j
                if s[j] == s[i]:
                    same += 1
                else:
                    diff += 1
                    if diff > k:
                        break
                best = min(best, enc_len(same) + dp(j + 1, k - diff))
            return best

        return dp(0, k)


##################################################################################################
##### ! Solution 2: 记忆化 f(i, k, prev_char, prev_cnt) —— 每个字符只有「删 / 留」两种选择
##### ! 时间复杂度: 状态 O(n · k · 26 · n)，实际可达远少   空间复杂度: 同状态数
##### ! 适用：最直觉的建模：留下 s[i] 时，和上一段同字符就「延长」（长度变化只在 1→2、9→10、99→100 时 +1），否则新开一段 +1
##################################################################################################


class Solution_2:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def f(i: int, k: int, prev: str, cnt: int) -> int:
            if k < 0:
                return float("inf")
            if i == n:
                return 0
            best = f(i + 1, k - 1, prev, cnt)           # ! 删
            if s[i] == prev:                            # ! 留且延长上一段
                extra = 1 if cnt in (1, 9, 99) else 0   # ! 1→2 多一位数字；9→10、99→100 数字位数 +1
                best = min(best, extra + f(i + 1, k, prev, cnt + 1))
            else:                                       # ! 留且新开一段
                best = min(best, 1 + f(i + 1, k, s[i], 1))
            return best

        return f(0, k, "", 0)


##################################################################################################
##### ! Solution 3: 枚举删哪些字符（真值基线，n ≤ 12）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n)
##### ! 适用：只用来对拍；直接按定义算 run-length 编码长度
##################################################################################################


class Solution_3:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        from itertools import groupby
        n, best = len(s), float("inf")
        for mask in range(1 << n):
            if bin(mask).count("1") > k:
                continue
            kept = [s[i] for i in range(n) if not mask >> i & 1]
            best = min(best, sum(enc_len(len(list(g))) for _, g in groupby(kept)))
        return best


if __name__ == "__main__":
    import random
    cases = [("aaabcccd", 2, 4), ("aabbaa", 2, 2), ("aaaaaaaaaaa", 0, 3), ("a", 1, 0), ("abc", 0, 3), ("aaaaaaaaaa", 1, 2)]
    for s, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().getLengthOfOptimalCompression(s, k)
            assert got == want, (cls.__name__, s, k, got, want)
    rng = random.Random(1531)
    for _ in range(600):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 11)))
        k = rng.randint(0, len(s))
        want = Solution_3().getLengthOfOptimalCompression(s, k)
        for cls in (Solution_1, Solution_2):
            assert cls().getLengthOfOptimalCompression(s, k) == want, (cls.__name__, s, k)
    # ! 规模测试：n=100, k=100 必须秒出
    import time
    t = time.perf_counter()
    big = "".join(rng.choice("abc") for _ in range(100))
    Solution_1().getLengthOfOptimalCompression(big, 50)
    assert time.perf_counter() - t < 5
    print("所有测试通过 ✓")
