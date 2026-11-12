"""LC-0647 - Palindromic Substrings

Level 1 · 04 回文与字符串双指针 / 02 中心扩展 —— 同一个模板，只把「取最长」换成「计数」
题目在问：s 里有多少个回文子串（起止位置不同就算不同，内容可以重复）

决定性观察：和 LC-0005 **一模一样的 2n-1 个中心**。区别只在收集方式 ——
      一个中心每成功扩展一次，就恰好多出一个回文子串，所以边扩边 `count += 1`。

循环不变量：进入 while 时 `s[l:r+1]` 已经是回文；每成功一次就说明又找到一个，
      计数和扩展是同一步，不需要另外去重（不同中心产生的子串位置必不相同）。

为什么不会重复计数：每个回文子串的中心是唯一确定的（长度奇偶决定是字符还是缝），
      所以每个子串只会在它自己的那个中心被数到一次。

坑：
  - 还是那条：**2n-1 个中心**，偶数中心不能漏
  - 计数要写在 while 内部（扩展成功才算一个），写在外面会少算或多算
  - 单个字符本身就是回文，所以答案至少是 n
"""


##################################################################################################
##### ! Solution 1: 中心扩展计数
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：和 LC-0005 共用 expand；只把「返回子串」换成「返回扩展成功的次数」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countSubstrings(self, s: str) -> int:
        n = len(s)

        # 从 (l, r) 向两边扩散，返回以这个中心能构成的回文个数
        def expand(l: int, r: int) -> int:
            count = 0
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
                count += 1
            return count

        # 奇数中心 (i, i) + 偶数中心 (i, i+1)
        return sum(expand(i, i) + expand(i, i + 1) for i in range(n))


##################################################################################################
##### ! Solution 2: 区间 DP
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：string-dp 专题的练法；顺带能回答「所有回文子串分别是什么」这类追问
##################################################################################################


class Solution_2:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        cnt = 0
        for i in range(n):
            dp[i][i] = True
            cnt += 1
        for length in range(2, n + 1):      # ! 按长度递增，dp[i][j] 依赖更短的 dp[i+1][j-1]
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    cnt += 1
        return cnt


##################################################################################################
##### ! Solution 3: 暴力枚举所有子串（基线）
##### ! 时间复杂度: O(n^3)   空间复杂度: O(1)
##### ! 适用：对拍参照
##################################################################################################


class Solution_3:
    def countSubstrings(self, s: str) -> int:
        return sum(1 for i in range(len(s)) for j in range(i, len(s))
                   if s[i:j + 1] == s[i:j + 1][::-1])


s = Solution_1()
input_ = "aaa"
result = s.countSubstrings(input_)
print(result)

if __name__ == "__main__":
    import random
    cases = [("abc", 3), ("aaa", 6), ("", 0), ("a", 1), ("abba", 6)]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for inp, want in cases:
            got = sol.countSubstrings(inp)
            assert got == want, f"{type(sol).__name__} {inp!r}: got {got}, want {want}"
    rng = random.Random(647)
    for _ in range(3000):
        t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 11)))
        want = Solution_3().countSubstrings(t)
        for sol in sols:
            assert sol.countSubstrings(t) == want, (type(sol).__name__, t, want)
    print("3 个解法全过（含 3000 组随机对拍）")
