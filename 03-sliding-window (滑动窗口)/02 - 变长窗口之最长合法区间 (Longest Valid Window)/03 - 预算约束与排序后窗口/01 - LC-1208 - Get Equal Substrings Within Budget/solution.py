"""LC-1208 - Get Equal Substrings Within Budget

Level 1 · 02 最长合法区间 —— Budget-constrained Window（预算约束窗口）
题目在问：把 s 的某个子串逐位改成 t 的对应子串，第 i 位的代价是 `|s[i]-t[i]|`，
      总代价不超过 maxCost，求最长能改的子串长度

决定性观察：先把问题压成一个代价数组 `cost[i] = abs(ord(s[i]) - ord(t[i]))`，
      题目就变成「**和不超过 maxCost 的最长连续子数组**」——
      这是最长合法窗口的标准形态，和 LC-1004（最多 k 个零）结构完全一样，
      只是「约束量」从「零的个数」换成了「代价之和」。

为什么窗口单调性成立：`cost[i] >= 0`。窗口变长时和只增不减，
      所以「不合法就收缩」这条规则能把 left 单调地往右推，O(n)。
      **如果代价可以是负数，这套就不成立了**（对比 LC-0862 的处理方式）。

Loop Invariant：每轮结束时 `cur <= maxCost`，且 `[left, right]` 是以 right 结尾的最长合法窗口。

坑：
  - `maxCost` 可以是 0，此时答案是「最长的 s[i] == t[i] 连续段」，别漏
  - 收缩用 while（一次可能要吐掉好几个）
  - 不要先算前缀和再二分（O(n log n)），这题有更好的 O(n)
"""


##################################################################################################
##### ! Solution 1: 变长窗口，和超预算就收缩
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「某个非负代价之和有上限，求最长区间」的题；1004 是它的 0/1 特例
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        left = 0
        cur = 0
        best = 0
        for right in range(len(s)):
            cur += abs(ord(s[right]) - ord(t[right]))
            while cur > maxCost:               # ! 超预算才收缩
                cur -= abs(ord(s[left]) - ord(t[left]))
                left += 1
            best = max(best, right - left + 1)
        return best


##################################################################################################
##### ! Solution 2: 前缀和 + 二分
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：窗口单调性不明显时的退路；这题用不着，但「前缀和 + 二分」值得会写
##################################################################################################


class Solution_2:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        import bisect
        pre = [0]
        for a, b in zip(s, t):
            pre.append(pre[-1] + abs(ord(a) - ord(b)))
        best = 0
        for right in range(1, len(pre)):
            # ! 找最小的 left 使 pre[right] - pre[left] <= maxCost
            left = bisect.bisect_left(pre, pre[right] - maxCost, 0, right)
            best = max(best, right - left)
        return best


if __name__ == "__main__":
    import random
    cases = [("abcd", "bcdf", 3, 3), ("abcd", "cdef", 3, 1), ("abcd", "acde", 0, 1),
             ("krrgw", "zjxss", 19, 2), ("a", "a", 0, 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for s, t, c, want in cases:
            got = sol.equalSubstring(s, t, c)
            assert got == want, f"{type(sol).__name__} {s!r} {t!r} {c}: got {got}, want {want}"
    rng = random.Random(1208)
    for _ in range(3000):
        n = rng.randint(1, 10)
        s = "".join(rng.choice("abcd") for _ in range(n))
        t = "".join(rng.choice("abcd") for _ in range(n))
        c = rng.randint(0, 6)
        want = max((j - i + 1 for i in range(n) for j in range(i, n)
                    if sum(abs(ord(s[x]) - ord(t[x])) for x in range(i, j + 1)) <= c), default=0)
        for sol in sols:
            assert sol.equalSubstring(s, t, c) == want, (type(sol).__name__, s, t, c, want)
    print("2 个解法全过（含 3000 组随机对拍）")
