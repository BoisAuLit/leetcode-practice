"""LC-1544 - Make The String Great（第二轮自主新增）

Level 1 · 01 基础栈、括号与消除 —— Adjacent Cancellation（相邻抵消）的第二个代表题
题目在问：反复删除「相邻的同一字母大小写配对」（如 "aA" 或 "Aa"），直到删不动为止。

为什么新增它（和 LC-1047 的关系）：
  LC-1047 删的是「两个完全相同的相邻字符」，LC-1544 删的是「同字母但大小写相反」。
  骨架完全一样，**只有「什么叫可抵消」这个谓词变了**。
  把两题放在一起，就能把「相邻抵消 = 栈 + 一个 cancel(a, b) 谓词」抽象出来，
  而不是把它们记成两道不同的题。成本极低，收益是一个可迁移的模板。

决定性观察：
  1. 删除是**会连锁**的："abBA" 删掉 "bB" 之后，"aA" 又变成相邻的了。
     用栈天然处理连锁：删掉栈顶后，新的栈顶和当前字符又相邻了。
  2. 抵消谓词：`a != b and a.lower() == b.lower()`。
     等价写法 `abs(ord(a) - ord(b)) == 32`（ASCII 里大小写差 32），但前者更不容易出错。
  3. 结果与删除顺序无关（可以证明是 confluent 的），所以一次从左到右的栈扫描就够，
     不需要反复扫描。

Loop Invariant：栈里是「已经处理完、内部再也没有可抵消相邻对」的前缀。

复杂度：O(n) 时间（每个字符最多入栈出栈各一次），O(n) 空间。

坑：
  - 判断里**必须**带 `a != b`：否则 "aa" 会被误删（"aa" 是合法的，不该删）。
  - 只用 `a.lower() == b.lower()` 不够；只用 `abs(ord)==32` 时要小心非字母字符
    （本题保证只有英文字母，所以安全）。

边界：
  - "leEeetcode" → "leetcode"
  - "abBAcC"     → ""（连锁删空：bB → aA → cC）
  - "s"          → "s"
  - "aa"         → "aa"（相同不删）
  - "Pp"         → ""
"""


##################################################################################################
##### ! Solution 1: 栈 + 抵消谓词（和 LC-1047 同一个骨架）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：一切「相邻满足某条件就成对消掉、且会连锁」的字符串题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def makeGood(self, s: str) -> str:
        stack: list[str] = []
        for c in s:
            # ! 抵消谓词：同一个字母、但大小写不同。a != b 不能漏，否则 "aa" 会被误删
            if stack and stack[-1] != c and stack[-1].lower() == c.lower():
                stack.pop()
            else:
                stack.append(c)
        return "".join(stack)


##################################################################################################
##### ! Solution 2: 用 ASCII 差值 32 判断大小写配对（同一算法的另一种谓词写法）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想少写一次 lower() 时；只在「保证全是英文字母」的前提下成立
##################################################################################################


class Solution_2:
    def makeGood(self, s: str) -> str:
        stack: list[str] = []
        for c in s:
            if stack and abs(ord(stack[-1]) - ord(c)) == 32:   # ! 'a'-'A' == 32
                stack.pop()
            else:
                stack.append(c)
        return "".join(stack)


##################################################################################################
##### ! Solution 3: 反复扫描字符串直到不再变化（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照；也最贴近题目字面描述，顺便验证「结果与删除顺序无关」
##################################################################################################


class Solution_3:
    def makeGood(self, s: str) -> str:
        cur = s
        changed = True
        while changed:
            changed = False
            for i in range(len(cur) - 1):
                a, b = cur[i], cur[i + 1]
                if a != b and a.lower() == b.lower():
                    cur = cur[:i] + cur[i + 2:]
                    changed = True
                    break
        return cur


if __name__ == "__main__":
    import random
    import string

    cases = ["leEeetcode", "abBAcC", "s", "aa", "Pp", "", "AaBbCc", "aAa"]
    for s in cases:
        r = Solution_1().makeGood(s)
        assert r == Solution_2().makeGood(s) == Solution_3().makeGood(s), s
        print(f"{s!r} -> {r!r}")

    for _ in range(500):                 # ! 随机对拍，只用 a/A/b/B 以提高连锁抵消的概率
        s = "".join(random.choice("aAbB") for _ in range(random.randint(0, 12)))
        assert Solution_1().makeGood(s) == Solution_2().makeGood(s) == Solution_3().makeGood(s), s
    print("随机对拍 500 组通过 ✓")
