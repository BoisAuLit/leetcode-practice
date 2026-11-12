"""LC-2296 - Design a Text Editor

Level 1 · 04 Stack 与 Queue 数据结构设计 → Level 2 · 01 带额外状态的 Stack

题目在问：一个带光标的文本编辑器：`addText`、`deleteText(k)`（删光标左边 k 个）、
`cursorLeft(k)` / `cursorRight(k)`（移动光标并返回光标左边最多 10 个字符）。

### 决定性观察：光标把文本切成「左右两个栈」

    左栈 left  = 光标左边的字符，栈顶是紧挨光标的那个
    右栈 right = 光标右边的字符，**倒着存**，栈顶也是紧挨光标的那个

于是四个操作全部变成栈顶操作：
- addText：逐字 push 进 left
- deleteText(k)：left 弹 k 个（不够就全弹，返回实际弹了几个）
- cursorLeft(k)：从 left 弹到 right，k 次
- cursorRight(k)：从 right 弹到 left，k 次
返回值 `''.join(left[-10:])` —— 光标左边最后 10 个字符。

这就是 gap buffer（真实编辑器的经典实现），也和 LC-1472 Browser History、双栈队列同源：
**「有一个会移动的分界点」⟹ 两个栈背靠背**。

### 容易踩的坑

- 所有操作都是 **O(k)**，不是 O(1)；题目 k ≤ 40，所以没问题。
- Python 的 `str` 不可变，每次 `s = s[:i] + t + s[i:]` 是 O(n)；10^4 次操作、文本到 4×10^5 时会超时 —— `Solution_2` 就是这个反面教材。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 双栈 Gap Buffer
##### ! 时间复杂度: 每个操作 O(k)（k ≤ 40），返回值 O(10)   空间复杂度: O(总字符数)
##### ! 适用：面试标准答案。右栈倒着存，保证「紧挨光标」的字符总在栈顶
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self):
        self.left: List[str] = []                 # ! 光标左边，正序
        self.right: List[str] = []                # ! 光标右边，倒序（栈顶 = 紧挨光标的字符）

    def addText(self, text: str) -> None:
        self.left.extend(text)

    def deleteText(self, k: int) -> int:
        k = min(k, len(self.left))
        del self.left[len(self.left) - k:]
        return k

    def cursorLeft(self, k: int) -> str:
        for _ in range(min(k, len(self.left))):
            self.right.append(self.left.pop())    # ! 字符跨过光标：从左栈顶搬到右栈顶
        return "".join(self.left[-10:])

    def cursorRight(self, k: int) -> str:
        for _ in range(min(k, len(self.right))):
            self.left.append(self.right.pop())
        return "".join(self.left[-10:])


##################################################################################################
##### ! Solution 2: 字符串 + 光标下标（反面教材：每次操作 O(n)）
##### ! 时间复杂度: addText / deleteText O(n)（字符串重建），cursor 移动 O(1)   空间复杂度: O(n)
##### ! 适用：只用来说明为什么不能用不可变字符串拼接；它是下面对拍的真值基线（语义最直白）
##################################################################################################


class Solution_2:
    def __init__(self):
        self.s = ""
        self.cur = 0

    def addText(self, text: str) -> None:
        self.s = self.s[:self.cur] + text + self.s[self.cur:]
        self.cur += len(text)

    def deleteText(self, k: int) -> int:
        k = min(k, self.cur)
        self.s = self.s[:self.cur - k] + self.s[self.cur:]
        self.cur -= k
        return k

    def cursorLeft(self, k: int) -> str:
        self.cur = max(0, self.cur - k)
        return self.s[max(0, self.cur - 10):self.cur]

    def cursorRight(self, k: int) -> str:
        self.cur = min(len(self.s), self.cur + k)
        return self.s[max(0, self.cur - 10):self.cur]


##################################################################################################
##### ! Solution 3: 双向链表 + 光标节点（gap buffer 的链表形态）
##### ! 时间复杂度: 每个操作 O(k)   空间复杂度: O(n)，常数比列表大
##### ! 适用：想要「光标两侧插入删除都 O(1)」且不想维护两个栈时；Python 里实际比 Solution_1 慢，
#####         但它是 C++/Java 面试里常见的写法，知道对应关系即可
##################################################################################################


class _Node:
    __slots__ = ("ch", "prev", "next")

    def __init__(self, ch=""):
        self.ch, self.prev, self.next = ch, None, None


class Solution_3:
    def __init__(self):
        self.head = _Node()                       # ! 哨兵；光标 = 「光标左边最后一个字符」的节点
        self.cur = self.head

    def addText(self, text: str) -> None:
        for ch in text:
            node = _Node(ch)
            node.prev, node.next = self.cur, self.cur.next
            if self.cur.next:
                self.cur.next.prev = node
            self.cur.next = node
            self.cur = node

    def deleteText(self, k: int) -> int:
        n = 0
        while k and self.cur is not self.head:
            prev, nxt = self.cur.prev, self.cur.next
            prev.next = nxt
            if nxt:
                nxt.prev = prev
            self.cur = prev
            k -= 1; n += 1
        return n

    def _left10(self) -> str:
        out, node = [], self.cur
        while node is not self.head and len(out) < 10:
            out.append(node.ch); node = node.prev
        return "".join(reversed(out))

    def cursorLeft(self, k: int) -> str:
        while k and self.cur is not self.head:
            self.cur = self.cur.prev; k -= 1
        return self._left10()

    def cursorRight(self, k: int) -> str:
        while k and self.cur.next:
            self.cur = self.cur.next; k -= 1
        return self._left10()


if __name__ == "__main__":
    import random, string
    random.seed(2296)
    for cls in (Solution_1, Solution_2, Solution_3):
        e = cls()
        e.addText("leetcode")
        out = [e.deleteText(4), e.addText("practice") or None, e.cursorRight(3), e.cursorLeft(8), e.deleteText(10), e.cursorLeft(2), e.cursorRight(6)]
        assert out == [4, None, "etpractice", "leet", 4, "", "practi"], (cls.__name__, out)

    for _ in range(20):
        impls = [Solution_1(), Solution_2(), Solution_3()]
        for _ in range(1500):
            op = random.choice(["add", "del", "left", "right"])
            if op == "add":
                t = "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, 5)))
                for im in impls:
                    im.addText(t)
            else:
                k = random.randint(1, 12)
                f = {"del": "deleteText", "left": "cursorLeft", "right": "cursorRight"}[op]
                outs = [getattr(im, f)(k) for im in impls]
                assert outs[0] == outs[1] == outs[2], (op, k, outs)
    print("所有测试通过 ✓（样例 + 20 × 1500 步随机对拍）")
