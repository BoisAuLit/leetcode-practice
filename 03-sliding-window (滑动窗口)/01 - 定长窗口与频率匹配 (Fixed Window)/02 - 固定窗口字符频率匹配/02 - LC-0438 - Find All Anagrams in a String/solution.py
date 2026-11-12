"""LC-0438 - Find All Anagrams in a String

Level 1 · 01 定长窗口 / 02 固定窗口字符频率匹配
题目在问：返回 s 中所有「是 p 的字母异位词」的子串的起始下标

决定性观察：和 **LC-0567 是同一道题**，窗口长度固定为 `len(p)`，
      唯一区别是 567 找到一个就 `return True`，这里要**收集所有起点**。
      不要把它当成两个模板记。

怎么判断「窗口和 p 的频率相同」—— 三种写法，复杂度递减：
  1. 每次比较两张完整的表：O(26) 一次，总共 O(26n)。够用，面试写这个最不容易错。
  2. 维护一个 `matches` 计数：有多少个字母的计数已经对上了，`matches == 26` 即匹配。
     进出各只影响一个字母，所以更新是 O(1)，总共 O(n)。
  3. 维护一个 `diff` 计数（还差几个字母没对上），本质同 2。

Loop Invariant：`win` 永远是 `s[i-len(p)+1 .. i]` 的字母频率表。
      进一个字母、出一个字母，表的两次修改必须成对出现。

Answer Update Timing：窗口刚好满 `len(p)` 个字符时检查一次。

坑：
  - `len(s) < len(p)` 时直接返回空
  - 用长度 26 的**数组**比 `Counter` 快很多，而且 `==` 比较是 O(26) 常数
  - 维护 matches 时，顺序是「先改计数，再判断这个字母是不是刚好对上/刚好错开」，
    一个字母的计数从 `== need` 变成 `!= need` 要让 matches 减一，反之加一
"""

from typing import List


##################################################################################################
##### ! Solution 1: 定长窗口 + 两张长度 26 的计数数组直接比较
##### ! 时间复杂度: O(26n)   空间复杂度: O(26) = O(1)
##### ! 适用：面试首选 —— 短、清楚、几乎不会写错；26 是常数，和 O(n) 同阶
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        m, n = len(p), len(s)
        if n < m:
            return []
        need = [0] * 26
        win = [0] * 26
        for ch in p:
            need[ord(ch) - 97] += 1
        res = []
        for i, ch in enumerate(s):
            win[ord(ch) - 97] += 1
            if i >= m:
                win[ord(s[i - m]) - 97] -= 1   # ! 进一个、出一个，窗口长度恒为 m
            if i >= m - 1 and win == need:
                res.append(i - m + 1)
        return res


##################################################################################################
##### ! Solution 2: 维护 matches 计数（真正的 O(n)）
##### ! 时间复杂度: O(n)   空间复杂度: O(26) = O(1)
##### ! 适用：★ 去掉了每一步的 26 次比较；追问「能不能做到严格 O(n)」时给这个
##################################################################################################


class Solution_2:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        m, n = len(p), len(s)
        if n < m:
            return []
        need = [0] * 26
        win = [0] * 26
        for ch in p:
            need[ord(ch) - 97] += 1
        matches = sum(1 for c in range(26) if need[c] == 0)   # ! 一开始就对上的字母

        def upd(c: int, delta: int) -> int:
            nonlocal matches
            before = win[c] == need[c]
            win[c] += delta
            after = win[c] == need[c]
            return (1 if after else 0) - (1 if before else 0)

        res = []
        for i, ch in enumerate(s):
            matches += upd(ord(ch) - 97, 1)
            if i >= m:
                matches += upd(ord(s[i - m]) - 97, -1)
            if i >= m - 1 and matches == 26:
                res.append(i - m + 1)
        return res


if __name__ == "__main__":
    import random
    from collections import Counter
    cases = [("cbaebabacd", "abc", [0, 6]), ("abab", "ab", [0, 1, 2]),
             ("a", "ab", []), ("aa", "aa", [0]), ("baa", "aa", [1])]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for s, p, want in cases:
            got = sol.findAnagrams(s, p)
            assert got == want, f"{type(sol).__name__} {s!r} {p!r}: got {got}, want {want}"
    rng = random.Random(438)
    for _ in range(3000):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
        want = [i for i in range(len(s) - len(p) + 1) if Counter(s[i:i + len(p)]) == Counter(p)]
        for sol in sols:
            assert sol.findAnagrams(s, p) == want, (type(sol).__name__, s, p, want)
    print("2 个解法全过（含 3000 组随机对拍）")
