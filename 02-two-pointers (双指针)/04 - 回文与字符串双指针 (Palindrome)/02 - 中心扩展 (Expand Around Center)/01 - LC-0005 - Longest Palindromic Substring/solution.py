"""LC-0005 - Longest Palindromic Substring

Level 1 · 04 回文与字符串双指针 / 02 中心扩展 —— Expand Around Center
题目在问：返回 s 里最长的回文子串

决定性观察：**一个回文由它的中心唯一决定**，所以枚举中心而不是枚举子串，
      就把 O(n³) 的「枚举所有子串再验证」降到 O(n²)。

中心有 **2n-1 个**：
  - 奇数长度：中心是一个字符，共 n 个（`(i, i)`）
  - 偶数长度：中心是两个相邻字符之间的缝，共 n-1 个（`(i, i+1)`）
  漏掉偶数中心是这类题最常见的错误 —— `"abba"` 的答案就落在缝上。

循环不变量：进入 while 时 `s[l:r+1]` 已经是回文；两端相等就能再扩一层，
      所以失败时回退一步得到的就是这个中心能取到的最长回文。

为什么**不必**记 DP 版本：`dp[i][j] = s[i]==s[j] and dp[i+1][j-1]` 时间同为 O(n²)，
      空间却要 O(n²)，而且填表顺序（按长度递增）容易写错。中心扩展空间 O(1)，面试写它。
      Manacher 能做到 O(n)，属于竞赛技巧，面试提一句名字即可。

和 Level 04/01（LC-0125 / 0680）的区别：那两题是**给定区间验证**回文（指针从两端向内收），
      这里是**枚举中心向外扩**（指针从内向两端走）。方向相反，不要混。
"""


##################################################################################################
##### ! Solution 1: 中心扩展（枚举 2n-1 个中心）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：本目录的标准答案；和 LC-0647 共用同一个 expand，只改最后怎么收集结果
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)

        # 从 (l, r) 向两边扩散，返回这个中心能构成的最长回文子串
        def expand(l: int, r: int) -> str:
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1 : r]

        res = ""
        for i in range(n):
            # 奇数中心 (i, i) + 偶数中心 (i, i+1)
            for curr in (expand(i, i), expand(i, i + 1)):
                if len(curr) > len(res):
                    res = curr
        return res


##################################################################################################
##### ! Solution 2: 区间 DP（dp[i][j] = s[i..j] 是不是回文）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：string-dp 专题的练法；时间同阶但空间差一个维度，面试不优先写
##################################################################################################


class Solution_2:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
        dp = [[False] * n for _ in range(n)]
        start, best = 0, 1
        for i in range(n):
            dp[i][i] = True
        # ! 必须按长度递增填表：dp[i][j] 依赖 dp[i+1][j-1]（更短的那个）
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] != s[j]:
                    continue
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > best:
                        start, best = i, length
        return s[start:start + best]


##################################################################################################
##### ! Solution 3: 暴力枚举所有子串（基线）
##### ! 时间复杂度: O(n^3)   空间复杂度: O(1)
##### ! 适用：对拍参照；正好说明「枚举中心」把一层循环省在了哪里
##################################################################################################


class Solution_3:
    def longestPalindrome(self, s: str) -> str:
        best = ""
        for i in range(len(s)):
            for j in range(i, len(s)):
                if s[i:j + 1] == s[i:j + 1][::-1] and j - i + 1 > len(best):
                    best = s[i:j + 1]
        return best


s = Solution_1()
input_ = "ababd"
result = s.longestPalindrome(input_)
print(result)

if __name__ == "__main__":
    import random
    cases = [("babad", {"bab", "aba"}), ("cbbd", {"bb"}), ("a", {"a"}),
             ("abba", {"abba"}), ("", {""}), ("ac", {"a", "c"})]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for inp, ok in cases:
            got = sol.longestPalindrome(inp)
            assert got in ok, f"{type(sol).__name__} {inp!r}: got {got!r}, want one of {ok}"
    rng = random.Random(5)
    for _ in range(3000):
        t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        want = len(Solution_3().longestPalindrome(t))   # 只比长度：最长回文可能不唯一
        for sol in sols:
            got = sol.longestPalindrome(t)
            assert len(got) == want and got == got[::-1] and got in t, (type(sol).__name__, t, got)
    print("3 个解法全过（含 3000 组随机对拍）")
