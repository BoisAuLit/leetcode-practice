"""LC-2516 - Take K of Each Character From Left and Right

Level 1 · 06 高阶窗口 / 02 Complement Window —— 补集窗口的进阶版
题目在问：字符串只含 a、b、c。每次只能从最左或最右拿走一个字符，
      要让拿到的 a、b、c 各至少 k 个，最少拿几次（不可能则 -1）

决定性观察（补集转化的第三种形态）：
      **从两端拿走 ⟺ 中间留下一段连续区间。**
      「拿到的每种字符 >= k」⟺ **留下的那段里，每种字符 <= `total[c] - k`**。
      要「拿得最少」⟺ 「留下的那段**最长**」。
      于是变成：**最长的、每种字符出现次数都不超过各自上限的子数组** —— 标准的最长合法窗口。

和同目录两题的对照（三道补集题的区别就在「固定了什么」）：
  - **1423**：固定**长度**（留 n-k 个）⇒ 定长窗口求最小和
  - **1658**：固定**和**（留下和为 total-x）⇒ 变长窗口求最长
  - **2516**：固定**每种字符的上限**（留下 count[c] <= total[c]-k）⇒ 变长窗口求最长

Loop Invariant：窗口内每种字符的出现次数都 <= 它的上限；超了就从左边收缩。

坑：
  - 先判不可能：任何一种字符总数 < k 就直接返回 -1
  - 上限可能是 0（某种字符总共只有 k 个），此时窗口里一个都不能有 —— 代码天然支持
  - 答案是 `n - 最长长度`；最长长度至少是 0（全部拿走总是可行的，只要前面的可行性判断通过）
"""


##################################################################################################
##### ! Solution 1: 补集转化 + 最长合法窗口（每种字符有各自上限）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)（只有 3 种字符）
##### ! 适用：「从两端取、每类都要够量」的题；把它翻译成中间窗口的上限约束
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def takeCharacters(self, s: str, k: int) -> int:
        total = {c: s.count(c) for c in "abc"}
        if any(total[c] < k for c in "abc"):
            return -1                      # ! 总量都不够，不可能
        cap = {c: total[c] - k for c in "abc"}   # ! 留在中间的每种字符的上限
        cnt = {"a": 0, "b": 0, "c": 0}
        left = 0
        longest = 0
        for right, ch in enumerate(s):
            cnt[ch] += 1
            while cnt[ch] > cap[ch]:       # ! 只可能是刚进来的这种超限
                cnt[s[left]] -= 1
                left += 1
            longest = max(longest, right - left + 1)
        return len(s) - longest


##################################################################################################
##### ! Solution 2: 暴力枚举「左边拿 i 个、右边拿 j 个」（基线）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：对拍参照；也最直白地说明了「拿走的部分 = 一个前缀 + 一个后缀」这件事
##################################################################################################


class Solution_2:
    def takeCharacters(self, s: str, k: int) -> int:
        n = len(s)
        pre = [{"a": 0, "b": 0, "c": 0}]
        for ch in s:                       # pre[i] = s[:i] 里各字符的个数
            d = dict(pre[-1]); d[ch] += 1; pre.append(d)
        suf = [{"a": 0, "b": 0, "c": 0}]
        for ch in reversed(s):             # suf[j] = s[n-j:] 里各字符的个数
            d = dict(suf[-1]); d[ch] += 1; suf.append(d)
        best = -1
        for i in range(n + 1):
            for j in range(n - i + 1):     # ! 前缀 i 个 + 后缀 j 个，不重叠
                if all(pre[i][c] + suf[j][c] >= k for c in "abc"):
                    best = i + j if best < 0 else min(best, i + j)
                    break                  # j 再大只会更差
        return best


if __name__ == "__main__":
    import random
    cases = [("aabaaaacaabc", 2, 8), ("a", 1, -1), ("abc", 1, 3),
             ("aabb", 1, -1), ("cacacaca", 1, -1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for s, k, want in cases:
            got = sol.takeCharacters(s, k)
            assert got == want, f"{type(sol).__name__} {s!r} k={k}: got {got}, want {want}"
    def brute(s, k):
        n = len(s); best = -1
        for i in range(n + 1):
            for j in range(n - i + 1):
                t = s[:i] + (s[n - j:] if j else "")
                if all(t.count(c) >= k for c in "abc"):
                    best = i + j if best < 0 else min(best, i + j)
        return best
    rng = random.Random(2516)
    for _ in range(2000):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 10)))
        k = rng.randint(1, 3)
        want = brute(s, k)
        for sol in sols:
            assert sol.takeCharacters(s, k) == want, (type(sol).__name__, s, k, want, sol.takeCharacters(s, k))
    print("2 个解法全过（含 2000 组随机对拍）")
