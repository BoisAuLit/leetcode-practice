"""LC-0044 - Wildcard Matching

Level 1 · 05 字符串分割与双序列 DP —— 通配符匹配（和 LC-0010 正则匹配对照）
题目在问：`?` 匹配任意**单个**字符，`*` 匹配**任意序列**（包括空），判断 p 能否匹配整个 s。

### 和 LC-0010 Regular Expression Matching 的区别（必须分清）

| | LC-0010 正则 | LC-0044 本题 |
|---|---|---|
| `.` / `?` | `.` 匹配任意**单个**字符 | `?` 匹配任意**单个**字符 |
| `*` 的含义 | **前一个字符**重复 0 次或多次（`a*`、`.*`） | **自己**匹配任意序列，和前一个字符**无关** |
| `*` 能独立出现吗 | **不能**（必须跟在一个字符后面） | **能**（`*` 自己就是一个单元） |
| 转移复杂度 | 要看 `p[j-1]` 和 `p[j]` 两个字符 | 只看 `p[j-1]` 一个字符 |

**本题其实比 LC-0010 简单** —— 因为 `*` 是独立的，不用回头看前一个字符。
很多人把两题搞混，结果在本题里写出 `p[j-2]` 这种只有正则才需要的东西。

### 状态与转移
```
dp[i][j] = s 的前 i 个字符能否匹配 p 的前 j 个字符

p[j-1] == '*'      → dp[i][j] = dp[i][j-1]          (* 匹配空)
                               or dp[i-1][j]        (* 再多吃一个 s 的字符)
p[j-1] == '?' 或相等 → dp[i][j] = dp[i-1][j-1]
否则                 → False
```

**`*` 那一行的两个分支是本题的全部**：
- `dp[i][j-1]`：`*` 匹配**空串**（不吃 s 的字符）
- `dp[i-1][j]`：`*` **再多吃一个** s 的字符（`*` 自己留在 p 里继续用）

**初始化**（最容易漏）：
```
dp[0][0] = True
dp[0][j] = dp[0][j-1] if p[j-1] == '*' else False
```
即：**空的 s 只能被「全是 `*` 的前缀」匹配**。
不写这一行，`s = "", p = "***"` 就会返回 False。

### 另一种解法：贪心双指针（Solution_2）
O(m+n) 时间、**O(1) 空间**。核心是记住「最后一个 `*` 的位置」和「它当时匹配到 s 的哪里」，
一旦后面失配就回到那个 `*`，让它多吃一个字符。
**这题的贪心是对的**（因为 `*` 独立），而 **LC-0010 的正则没有这种贪心解法**。

复杂度：Solution_1 O(m·n) 时间 / O(n) 空间（滚动）；Solution_2 O(m+n) / O(1)。

边界：
  - `s = "", p = ""` → True
  - `s = "", p = "*"` → True；`p = "***"` → True；`p = "?"` → False
  - `s = "abc", p = "*"` → True
  - `s = "aa", p = "a"` → False
  - 连续多个 `*`（`"a**b"`）
"""


##################################################################################################
##### ! Solution 1: 双序列 DP（滚动数组，O(n) 空间）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(n)
##### ! 适用：通配符 / 编辑距离一类的双串匹配；注意初始化「空 s 只能被全 * 匹配」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        prev = [False] * (n + 1)
        prev[0] = True
        for j in range(1, n + 1):
            # ! 空的 s 只能被「全是 * 的前缀」匹配
            prev[j] = prev[j - 1] and p[j - 1] == "*"
        for i in range(1, m + 1):
            cur = [False] * (n + 1)
            cur[0] = False                     # ! 非空的 s 配不上空的 p
            for j in range(1, n + 1):
                if p[j - 1] == "*":
                    # ! 两个分支：* 匹配空（cur[j-1]）/ * 再多吃一个 s 的字符（prev[j]）
                    cur[j] = cur[j - 1] or prev[j]
                elif p[j - 1] == "?" or p[j - 1] == s[i - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = False
            prev = cur
        return prev[n]


##################################################################################################
##### ! Solution 2: 贪心双指针（O(1) 空间）—— 记住最后一个 * 的位置，失配就回溯
##### ! 时间复杂度: O(m + n) 平均   空间复杂度: O(1)
##### ! 适用：本题特有（因为 * 是独立单元）；**LC-0010 的正则没有这种贪心解法**
##################################################################################################


class Solution_2:
    def isMatch(self, s: str, p: str) -> bool:
        i = j = 0
        star = -1          # ! p 中最后一个 * 的下标
        match = 0          # ! 那个 * 当时匹配到 s 的哪个位置
        while i < len(s):
            if j < len(p) and (p[j] == "?" or p[j] == s[i]):
                i += 1
                j += 1
            elif j < len(p) and p[j] == "*":
                star = j
                match = i
                j += 1                     # ! 先假设 * 匹配空串
            elif star != -1:
                j = star + 1               # ! 失配：回到那个 *
                match += 1                 # ! 让它多吃一个字符
                i = match
            else:
                return False
        while j < len(p) and p[j] == "*":   # ! p 剩下的必须全是 *
            j += 1
        return j == len(p)


##################################################################################################
##### ! Solution 3: 记忆化搜索（基准答案，用来对拍）
##### ! 时间复杂度: O(m·n)   空间复杂度: O(m·n)
##### ! 适用：正确性参照；也最直白地表达两个分支
##################################################################################################


class Solution_3:
    def isMatch(self, s: str, p: str) -> bool:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            if p[j] == "*":
                # ! * 匹配空 / * 吃掉 s[i]
                return dfs(i, j + 1) or (i < len(s) and dfs(i + 1, j))
            if i < len(s) and (p[j] == "?" or p[j] == s[i]):
                return dfs(i + 1, j + 1)
            return False

        r = dfs(0, 0)
        dfs.cache_clear()
        return r


if __name__ == "__main__":
    import random

    cases = [("aa", "a", False), ("aa", "*", True), ("cb", "?a", False),
             ("adceb", "*a*b", True), ("acdcb", "a*c?b", False),
             ("", "", True), ("", "*", True), ("", "***", True), ("", "?", False),
             ("abc", "a**b*c", True)]
    for s, p, want in cases:
        a = Solution_1().isMatch(s, p)
        b = Solution_2().isMatch(s, p)
        c = Solution_3().isMatch(s, p)
        assert a == b == c == want, (s, p, a, b, c, want)
        print(f"s={s!r}, p={p!r} -> {a}")

    for _ in range(3000):                # ! 随机对拍，小字母表 + 大量 * 和 ?
        s = "".join(random.choice("ab") for _ in range(random.randint(0, 6)))
        p = "".join(random.choice("ab?*") for _ in range(random.randint(0, 6)))
        a = Solution_1().isMatch(s, p)
        b = Solution_2().isMatch(s, p)
        c = Solution_3().isMatch(s, p)
        assert a == b == c, (s, p, a, b, c)
    print("随机对拍 3000 组通过 ✓（DP == 贪心双指针 == 记忆化）")
