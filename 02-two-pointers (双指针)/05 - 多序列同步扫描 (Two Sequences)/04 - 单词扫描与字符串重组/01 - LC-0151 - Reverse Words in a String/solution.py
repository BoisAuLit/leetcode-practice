"""LC-0151 - Reverse Words in a String

Level 1 · 05 多序列同步扫描 —— 单词边界扫描与重组
题目在问：把句子里的单词顺序反过来，去掉首尾空格，单词之间只留一个空格

决定性观察：有两条互不相同的路线，面试要能都说出来 ——
  A. **倒着扫一遍，遇到单词就整段抄出来**：天然得到逆序，边界处理集中在一个地方。
  B. **三次反转**：整个串反转 → 每个单词再各自反转 → 顺手压缩空格。
     和 LC-0189 Rotate Array 的「三次反转」是同一个恒等式，只是单位从元素变成了单词。

关于空间复杂度（这题最容易说错的一点）：
  **Python 的 str 不可变**，任何方案都要先 `list(s)` 或者新建列表，所以
  Python 实现的空间是 **O(n)**，不能声称 O(1)。
  只有在 C++ / Java 的 `char[]`（可变字符数组）上，三次反转法才是真正的 O(1) 额外空间。
  解法 3 在 `list(s)` 上演示那套原地操作，用来说明思想；它的 O(1) 指的是
  「除了那份必需的可变副本之外不再额外开空间」。

坑：
  - 中间可能有多个连续空格，首尾也可能有空格；输出必须是单个空格分隔、无首尾空格
  - `s.split()`（不传参数）会自动按任意空白切分并丢掉空串，`s.split(" ")` 不会 —— 别用后者
  - 三次反转法里，压缩空格这一步不能漏，否则 `"  a  b "` 会输出 `" b  a  "`
"""

from typing import List


##################################################################################################
##### ! Solution 1: split + 反转 + join
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：Python 里的标准答案，三行、不会错；面试先给它，再讲下面两种的思想
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def reverseWords(self, s: str) -> str:
        return " ".join(reversed(s.split()))  # ! split() 不传参 → 自动处理连续空格和首尾空格


##################################################################################################
##### ! Solution 2: 倒序双指针扫单词边界，边扫边收集
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（输出本身）
##### ! 适用：不依赖库函数，面试官要求"不要用 split"时就写这个；指针移动规则看得最清楚
##################################################################################################


class Solution_2:
    def reverseWords(self, s: str) -> str:
        res: List[str] = []
        i = len(s) - 1
        while i >= 0:
            while i >= 0 and s[i] == " ":   # ! 跳过单词之间（和末尾）的空格
                i -= 1
            if i < 0:
                break
            j = i                            # ! j 是这个单词的右端
            while i >= 0 and s[i] != " ":    # ! 往左扫到单词的左端
                i -= 1
            res.append(s[i + 1:j + 1])       # ! i 现在停在空格或 -1，所以要 +1
        return " ".join(res)


##################################################################################################
##### ! Solution 3: 三次反转（在可变字符数组上，演示 C++/Java 的 O(1) 空间做法）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（Python 必需的可变副本）/ C++ 里是 O(1)
##### ! 适用：和 LC-0189 共享同一个恒等式；想说清"为什么三次反转等价于整体移位"就用它
##################################################################################################


class Solution_3:
    def reverseWords(self, s: str) -> str:
        a = list(s)

        def rev(lo: int, hi: int) -> None:
            while lo < hi:
                a[lo], a[hi] = a[hi], a[lo]
                lo += 1
                hi -= 1

        # ! 第一步：压缩空格（读写双指针），让单词之间恰好一个空格、首尾无空格
        write = 0
        read = 0
        n = len(a)
        while read < n:
            while read < n and a[read] == " ":
                read += 1
            if read == n:
                break
            if write:                        # ! 不是第一个单词 → 先补一个分隔空格
                a[write] = " "; write += 1
            start = write
            while read < n and a[read] != " ":
                a[write] = a[read]; write += 1; read += 1
            rev(start, write - 1)            # ! 第二步：每个单词各自反转
        del a[write:]
        rev(0, len(a) - 1)                   # ! 第三步：整体反转 → 单词顺序倒过来、字母回正
        return "".join(a)


if __name__ == "__main__":
    import random
    cases = [("the sky is blue", "blue is sky the"), ("  hello world  ", "world hello"),
             ("a good   example", "example good a"), ("   ", ""), ("x", "x"),
             ("  a  ", "a")]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for s, want in cases:
            got = sol.reverseWords(s)
            assert got == want, f"{type(sol).__name__} {s!r}: got {got!r}, want {want!r}"
    rng = random.Random(151)
    for _ in range(3000):
        s = "".join(rng.choice("ab  c ") for _ in range(rng.randint(0, 14)))
        want = " ".join(reversed(s.split()))
        for sol in sols:
            assert sol.reverseWords(s) == want, (type(sol).__name__, repr(s))
    print("3 个解法全过（含 3000 组随机对拍）")
