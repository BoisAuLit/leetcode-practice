"""LC-1312 - Minimum Insertion Steps to Make a String Palindrome（第二轮自主新增）

Level 1 · 08 区间 DP 与博弈 —— **把「最少插入」翻译成「最长回文子序列」**
题目在问：每次可以在任意位置插入一个字符，最少插几次能让 s 变成回文。

为什么新增它（它补的是哪个缺口 —— 一行结论就是全部）：

> ## **答案 = `n − LPS(s)`**

**为什么**：最长回文子序列（LPS）里的字符**已经两两配好对了，不用动**；
剩下的 `n − LPS` 个字符，每个**各配一个镜像字符插进去**就行，一次插一个，刚好 `n − LPS` 次。
- **下界**：至少要插这么多 —— 不在 LPS 里的字符都没有配对，每个都得补一个。
- **可达**：按 LPS 的结构从外往里补，确实能用这么多次做到。

**这个「最少操作数 = n − 某个最优子结构」的转化模式极其常见**：
| 题 | 结论 |
|---|---|
| **LC-1312** 本题 | 最少插入 = `n − LPS(s)` |
| LC-0583 两字符串删除 | 最少删除 = `m + n − 2·LCS` |
| LC-0712 最小 ASCII 删除和 | 类似，但权重是 ASCII 值 |
| LC-0300 的变体「最少删几个变成递增」 | `n − LIS(s)` |

**本专题原本没有一道题点明这个模式**，而它的性价比极高 ——
看懂一次，上面四道题就都会了。所以单独收一道。

### 也可以直接区间 DP（Solution_2）
```
dp[i][j] = 让 s[i..j] 变成回文所需的最少插入
s[i] == s[j] → dp[i][j] = dp[i+1][j-1]
s[i] != s[j] → dp[i][j] = min(dp[i+1][j], dp[i][j-1]) + 1
```
和 LC-0516 的区间 DP 是**完全对偶**的转移（一个取 max 加 2，一个取 min 加 1）。
两种写法都对，**但知道 `n − LPS` 这个结论能让你三行写完**。

复杂度：O(n²) 时间；LPS 用滚动数组可以 O(n) 空间。

边界：
  - 已经是回文 → 0
  - 无重复字符 → `n - 1`
  - 单字符 → 0
  - `"zzazz"` → 0；`"mbadm"` → 2；`"leetcode"` → 5
"""


##################################################################################################
##### ! Solution 1: 答案 = n − LPS(s)，LPS 用 LCS(s, reversed(s)) 求（滚动数组）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：一切「最少插入/删除使其满足某对称性质」的题；记住 n − 最优子结构这个模式
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minInsertions(self, s: str) -> int:
        n = len(s)
        t = s[::-1]
        prev = [0] * (n + 1)
        for i in range(1, n + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        lps = prev[n]
        return n - lps            # ! 不在 LPS 里的字符，每个补一个镜像


##################################################################################################
##### ! Solution 2: 直接区间 DP（和 LC-0516 的转移完全对偶）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：想直接表达「让 s[i..j] 变回文要插几次」这个状态时
##################################################################################################


class Solution_2:
    def minInsertions(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        dp = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1]          # ! 两端已配对，不用插
                else:
                    dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1   # ! 补一个镜像
        return dp[0][n - 1]


##################################################################################################
##### ! Solution 3: BFS 暴力 —— 真的一个一个插字符试（基准答案，用来对拍；只适合极短串）
##### ! 时间复杂度: 指数级   空间复杂度: 指数级
##### ! 适用：正确性参照 —— 直接验证「n − LPS」这个结论
##################################################################################################


class Solution_3:
    def minInsertions(self, s: str) -> int:
        from collections import deque
        if s == s[::-1]:
            return 0
        alphabet = sorted(set(s))
        seen = {s}
        q = deque([(s, 0)])
        while q:
            cur, d = q.popleft()
            for i in range(len(cur) + 1):
                for ch in alphabet:
                    nxt = cur[:i] + ch + cur[i:]
                    if nxt == nxt[::-1]:
                        return d + 1
                    if nxt not in seen and len(nxt) <= len(s) + 4:
                        seen.add(nxt)
                        q.append((nxt, d + 1))
        return -1


if __name__ == "__main__":
    import random

    cases = [("zzazz", 0), ("mbadm", 2), ("leetcode", 5), ("a", 0), ("", 0), ("abc", 2)]
    for s, want in cases:
        a = Solution_1().minInsertions(s)
        b = Solution_2().minInsertions(s)
        assert a == b == want, (s, a, b, want)
        print(f"{s!r} -> {a}")

    for _ in range(300):                 # ! 短串用 BFS 暴力验证「n − LPS」这个结论
        s = "".join(random.choice("ab") for _ in range(random.randint(1, 6)))
        a = Solution_1().minInsertions(s)
        b = Solution_2().minInsertions(s)
        c = Solution_3().minInsertions(s)
        assert a == b == c, (s, a, b, c)
    for _ in range(800):                 # ! 长一点的串只对拍两种 DP
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 12)))
        assert Solution_1().minInsertions(s) == Solution_2().minInsertions(s), s
    print("随机对拍通过 ✓（n − LPS == 区间 DP == 真插字符的 BFS）")
