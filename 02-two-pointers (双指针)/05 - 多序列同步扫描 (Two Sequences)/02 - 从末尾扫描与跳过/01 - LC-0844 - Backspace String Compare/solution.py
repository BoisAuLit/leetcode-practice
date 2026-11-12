"""LC-0844 - Backspace String Compare

Level 1 · 05 多序列同步扫描 —— Backward Traversal（从末尾倒着扫 + 记账跳过）
题目在问：'#' 代表退格，判断两个字符串按退格处理后是否相等。要求 O(1) 额外空间

决定性观察：**退格只影响左边的字符，所以必须倒着扫。**
      正着扫时你不知道后面还有几个 '#' 会把当前字符删掉；倒着扫时，
      遇到 '#' 就"欠一个删除"，遇到普通字符先还债，债还完了它才是真正保留下来的字符。

循环不变量：两个指针各自停在「自己串里下一个真正保留的字符」上，
      或者越界（表示这一侧已经扫完）。每轮比较这两个字符，不等就立刻返回 False。

为什么空间是 O(1)：全程没有构造处理后的字符串，只有两个下标和两个计数器。
      用栈重建虽然更好写，但空间是 O(n)，这题的考点恰恰是那个 O(1)。

坑：
  - 内层必须是 while 不是 if：`"a##"` 这种会连续欠两次债
  - 两侧都扫完才算相等；只有一侧越界 → 长度不同 → False
  - 比较前要确认两个指针都 >= 0，顺序写错会拿负下标去取字符（Python 不报错，静默出错）
"""


##################################################################################################
##### ! Solution 1: 倒序双指针 + 退格计数（O(1) 空间）
##### ! 时间复杂度: O(n + m)   空间复杂度: O(1)
##### ! 适用：所有「后面的操作会抹掉前面内容」的题；倒着扫 + 记账是这类题的统一解法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def backspaceCompare(self, s: str, t: str) -> bool:
        i, j = len(s) - 1, len(t) - 1
        skip_s = skip_t = 0
        while i >= 0 or j >= 0:
            while i >= 0:                      # ! 把 s 的指针推到下一个真正保留的字符
                if s[i] == "#":
                    skip_s += 1; i -= 1
                elif skip_s:
                    skip_s -= 1; i -= 1        # ! 还债：这个字符被退格吃掉了
                else:
                    break
            while j >= 0:                      # ! t 同理
                if t[j] == "#":
                    skip_t += 1; j -= 1
                elif skip_t:
                    skip_t -= 1; j -= 1
                else:
                    break
            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:             # ! 一侧还有字符、另一侧没了 → 长度不同
                return False
            i -= 1
            j -= 1
        return True


##################################################################################################
##### ! Solution 2: 用栈重建两个字符串再比较
##### ! 时间复杂度: O(n + m)   空间复杂度: O(n + m)
##### ! 适用：面试先写这个建立共识（三行、不会错），再说「要 O(1) 空间就得倒着扫」
##################################################################################################


class Solution_2:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def build(x: str) -> list[str]:
            st: list[str] = []
            for ch in x:
                if ch == "#":
                    if st:
                        st.pop()
                else:
                    st.append(ch)
            return st
        return build(s) == build(t)


if __name__ == "__main__":
    import random
    cases = [("ab#c", "ad#c", True), ("ab##", "c#d#", True), ("a#c", "b", False),
             ("", "", True), ("#", "", True), ("a##c", "#a#c", True), ("bxj##tw", "bxo#j##tw", True)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for s, t, want in cases:
            got = sol.backspaceCompare(s, t)
            assert got == want, f"{type(sol).__name__} {s!r} {t!r}: got {got}, want {want}"
    rng = random.Random(844)
    for _ in range(5000):
        gen = lambda: "".join(rng.choice("ab##") for _ in range(rng.randint(0, 8)))
        s, t = gen(), gen()
        want = Solution_2().backspaceCompare(s, t)
        assert Solution_1().backspaceCompare(s, t) == want, (s, t, want)
    print("2 个解法全过（含 5000 组随机对拍）")
