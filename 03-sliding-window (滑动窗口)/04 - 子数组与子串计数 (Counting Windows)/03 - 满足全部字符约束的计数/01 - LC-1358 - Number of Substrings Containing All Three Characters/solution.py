"""LC-1358 - Number of Substrings Containing All Three Characters

Level 1 · 04 计数窗口 / 03 满足全部字符约束的计数
题目在问：s 只含 a、b、c，统计**同时包含三种字符**的子串个数

决定性观察：和 LC-0713 的公式方向相反 ——
      713 数的是「以 right 结尾、仍然**合法**的子数组」，所以加 `right - left + 1`；
      本题的约束是「至少要包含…」，**窗口越长越容易满足**，所以要反过来数：
      固定 right，设 `left` 是使 `[left, right]` 仍含全三种字符的**最大**左端，
      那么起点取 `0 .. left` 的子串都合法 ⇒ 一次加 **`left + 1`** 个。

这就是三类窗口答案更新方式的完整对照：
  - 最长合法：`best = max(best, right - left + 1)`
  - 最短满足：`best = min(best, right - left + 1)`（在合法时收缩前更新）
  - 计数（约束是「至多」）：`ans += right - left + 1`
  - 计数（约束是「至少」）：`ans += left`（或 `left + 1`，取决于 left 的定义）

Loop Invariant（解法 1）：while 结束后，`[left, right]` 已经**不再**包含全三种，
      所以合法起点是 `0 .. left-1`，一次加 `left`。

坑：
  - 搞清楚 left 的语义：是「最后一个合法起点」还是「第一个不合法起点」，差一就错
  - 另一种写法（解法 2）是记录 a/b/c 最后出现的位置，
    合法起点数 = `min(last_a, last_b, last_c) + 1`，更短且不用收缩循环
"""


##################################################################################################
##### ! Solution 1: 变长窗口，缩到不合法为止，一次加 left
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：约束是「至少包含 X」的计数题通解；注意加的是 left 而不是 right-left+1
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numberOfSubstrings(self, s: str) -> int:
        cnt = {"a": 0, "b": 0, "c": 0}
        left = 0
        ans = 0
        for ch in s:
            cnt[ch] += 1
            while all(cnt[k] > 0 for k in "abc"):   # ! 一直缩到不再包含全三种
                cnt[s[left]] -= 1
                left += 1
            ans += left        # ! 起点 0..left-1 都能和当前 right 组成合法子串
        return ans


##################################################################################################
##### ! Solution 2: 记录三种字符最后出现的位置
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：★ 最短的写法，没有内层循环；合法起点数 = min(三个最后位置) + 1
##################################################################################################


class Solution_2:
    def numberOfSubstrings(self, s: str) -> int:
        last = {"a": -1, "b": -1, "c": -1}
        ans = 0
        for i, ch in enumerate(s):
            last[ch] = i
            ans += min(last.values()) + 1   # ! 三个都出现过时才是正数，否则 -1+1=0
        return ans


if __name__ == "__main__":
    import random
    cases = [("abcabc", 10), ("aaacb", 3), ("abc", 1), ("a", 0), ("", 0), ("ccccc", 0)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for s, want in cases:
            got = sol.numberOfSubstrings(s)
            assert got == want, f"{type(sol).__name__} {s!r}: got {got}, want {want}"
    rng = random.Random(1358)
    for _ in range(3000):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        want = sum(1 for i in range(len(s)) for j in range(i, len(s))
                   if set("abc") <= set(s[i:j + 1]))
        for sol in sols:
            assert sol.numberOfSubstrings(s) == want, (type(sol).__name__, s, want)
    print("2 个解法全过（含 3000 组随机对拍）")
