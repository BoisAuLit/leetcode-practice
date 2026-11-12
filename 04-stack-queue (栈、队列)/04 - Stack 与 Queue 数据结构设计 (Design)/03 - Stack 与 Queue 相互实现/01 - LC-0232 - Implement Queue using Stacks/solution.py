"""LC-0232 - Implement Queue using Stacks

Level 1 · 04 Stack 与 Queue 数据结构设计 —— 两个栈实现 FIFO，摊还 O(1)
题目在问：只用栈的 push/pop/peek/empty，实现一个队列。

决定性观察（两个栈法的核心）：
  1. 一个栈把顺序**倒过来**一次；倒两次就倒回来了。
     所以用 `in_stack` 接收新元素，用 `out_stack` 提供出队顺序 —— 元素从 in 倒进 out 的过程，
     正好把 LIFO 变成 FIFO。
  2. **只有 out_stack 空的时候才整体搬运**。这是全题唯一的关键决策：
     如果每次操作都搬一遍，复杂度退化成 O(n)；只在空的时候搬，每个元素一生只经历
     「进 in → 出 in → 进 out → 出 out」4 次操作。

摊还分析（面试必说）：
      单次 `pop()` 最坏 O(n)（恰好触发一次整体搬运），
      但每个元素总共只被搬运一次，n 次操作总代价 O(n) ⇒ **摊还 O(1)**。
      不能笼统地说「每次操作都是 O(1)」。

和 LC-0225（用队列实现栈）**不是对称的**，这一点必须讲清楚：
      - 232（栈→队列）：靠「倒两次恢复顺序」，可以做到摊还 O(1)，**均摊很便宜**。
      - 225（队列→栈）：队列没法倒序，只能靠 **rotation（把前 n-1 个元素出队再入队）**，
        每次 push（或 pop）都要 O(n)，**没有摊还技巧能降下来**。
      一个是「两次反转抵消」，一个是「每次重排」—— 代码形状和复杂度都不同。

Loop Invariant：队首元素 = out_stack 非空时的 out_stack[-1]，否则是 in_stack[0]。

复杂度：push O(1)；pop / peek 摊还 O(1)、最坏 O(n)；空间 O(n)。
"""

from typing import List


##################################################################################################
##### ! Solution 1: 两个栈（in / out），只在 out 空时整体搬运 —— 摊还 O(1)
##### ! 时间复杂度: push O(1)，pop/peek 摊还 O(1)（单次最坏 O(n)）   空间复杂度: O(n)
##### ! 适用：所有「用 LIFO 结构实现 FIFO 语义」的题；摊还分析的标准例子
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class MyQueue_1:
    def __init__(self) -> None:
        self.in_stack: List[int] = []     # ! 只负责接收
        self.out_stack: List[int] = []    # ! 只负责吐出；它的栈顶就是队首

    def _transfer(self) -> None:
        if not self.out_stack:            # ! 关键：只有空了才搬，否则会打乱顺序也会退化复杂度
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack


##################################################################################################
##### ! Solution 2: 单栈 + 每次 push 都重排（push O(n)，pop O(1)）
##### ! 时间复杂度: push O(n)，pop/peek O(1)   空间复杂度: O(n)
##### ! 适用：读多写少的场景；也用来对照说明「代价可以挪到哪一端」，但不是本题首选
##################################################################################################


class MyQueue_2:
    def __init__(self) -> None:
        self.stack: List[int] = []        # ! 栈顶永远是队首（即逆序存放）

    def push(self, x: int) -> None:
        tmp: List[int] = []
        while self.stack:
            tmp.append(self.stack.pop())
        self.stack.append(x)              # ! 新元素沉到最底
        while tmp:
            self.stack.append(tmp.pop())

    def pop(self) -> int:
        return self.stack.pop()

    def peek(self) -> int:
        return self.stack[-1]

    def empty(self) -> bool:
        return not self.stack


##################################################################################################
##### ! Solution 3: 直接用 list 当队列（基准答案，用来对拍；题目不允许，仅作参照）
##### ! 时间复杂度: pop O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照
##################################################################################################


class MyQueue_3:
    def __init__(self) -> None:
        self.data: List[int] = []

    def push(self, x: int) -> None:
        self.data.append(x)

    def pop(self) -> int:
        return self.data.pop(0)

    def peek(self) -> int:
        return self.data[0]

    def empty(self) -> bool:
        return not self.data


if __name__ == "__main__":
    import random

    q1, q2, q3 = MyQueue_1(), MyQueue_2(), MyQueue_3()
    q1.push(1); q2.push(1); q3.push(1)
    q1.push(2); q2.push(2); q3.push(2)
    print("peek:", q1.peek(), q2.peek(), q3.peek())        # 1
    print("pop :", q1.pop(), q2.pop(), q3.pop())           # 1
    print("empty:", q1.empty(), q2.empty(), q3.empty())    # False

    for _ in range(300):                 # ! 随机操作序列对拍
        a, b, c = MyQueue_1(), MyQueue_2(), MyQueue_3()
        for _ in range(60):
            if c.empty() or random.random() < 0.5:
                v = random.randint(0, 99)
                a.push(v); b.push(v); c.push(v)
            elif random.random() < 0.5:
                assert a.pop() == b.pop() == c.pop()
            else:
                assert a.peek() == b.peek() == c.peek()
            assert a.empty() == b.empty() == c.empty()
    print("随机对拍 300 组 × 60 次操作通过 ✓")
