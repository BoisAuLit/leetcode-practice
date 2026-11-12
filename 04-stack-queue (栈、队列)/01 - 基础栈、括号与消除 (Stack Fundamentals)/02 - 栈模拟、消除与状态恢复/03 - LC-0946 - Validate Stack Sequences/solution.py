"""LC-0946 - Validate Stack Sequences

Level 1 · 01 基础栈、括号与消除 —— 用栈**模拟**一段 push/pop 序列是否可能发生
题目在问：给定 pushed 和 popped 两个排列，问「按 pushed 的顺序入栈」能否得到 popped 的出栈顺序。

决定性观察：
  1. 入栈顺序是**被规定死**的（必须按 pushed 从左到右），我们唯一能决定的是**什么时候 pop**。
  2. 贪心：**只要栈顶等于 popped 当前要的那个数，就立刻弹**。
     为什么立刻弹是安全的？因为元素各不相同，这个数只会出现一次；
     如果现在不弹，就得再压别的数到它上面，那它只会被埋得更深，以后更弹不出来。
     所以「能弹就弹」不会错过任何可行解。
  3. 全部 push 完之后，如果栈空了，说明每一步都对上了 → True。
     栈里还有剩余 → 剩下的顺序和 popped 要的对不上 → False。

栈里的元素代表什么：**已经入栈、但还没轮到它出栈**的元素。
      注意它们的出栈顺序被 LIFO 锁死了 —— 这正是「不可能的序列」会被卡住的原因。

Loop Invariant：`popped[:j]` 已经被成功匹配；栈里是「已 push 未 pop」的元素，自底向上。

复杂度：O(n) 时间（每个元素入栈一次出栈一次），O(n) 空间。
      进阶：可以把 pushed 自身当栈用，做到 O(1) 额外空间（见 Solution_2）。

边界：
  - pushed=[1,2,3,4,5], popped=[4,5,3,2,1] → True
  - pushed=[1,2,3,4,5], popped=[4,3,5,1,2] → False（弹完 4,3 之后栈顶是 2，但 popped 要 5 之后的 1）
  - 空序列 → True
  - 单元素 → True
  - popped 和 pushed 完全相同（每 push 一个立刻 pop）→ True
  - popped 是 pushed 的逆序（全部压完再倒出）→ True
"""

from typing import List


##################################################################################################
##### ! Solution 1: 直接用一个辅助栈模拟，「栈顶等于要出的数就立刻弹」
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：所有「给定操作序列，问能否产生某个结果」的模拟验证题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack: List[int] = []
        j = 0                                     # ! popped 里下一个要被匹配的位置
        for x in pushed:
            stack.append(x)
            while stack and j < len(popped) and stack[-1] == popped[j]:
                stack.pop()                       # ! 能弹就弹：不弹只会被埋得更深
                j += 1
        return not stack                          # ! 栈空 ⟺ 全部匹配成功


##################################################################################################
##### ! Solution 2: 原地复用 pushed 当栈，O(1) 额外空间（面试 follow-up）
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外（会原地修改 pushed）
##### ! 适用：被追问「能不能不用额外空间」时；注意它会破坏入参
##################################################################################################


class Solution_2:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        top = 0                                   # ! pushed[:top] 当作栈
        j = 0
        for x in pushed:
            pushed[top] = x                       # ! push
            top += 1
            while top > 0 and j < len(popped) and pushed[top - 1] == popped[j]:
                top -= 1                          # ! pop
                j += 1
        return top == 0


##################################################################################################
##### ! Solution 3: 暴力搜索所有 push/pop 交错方式（基准答案，用来对拍；只适合很短的输入）
##### ! 时间复杂度: 指数级   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 用它验证「能弹就弹」这个贪心确实不会漏解
##################################################################################################


class Solution_3:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        n = len(pushed)
        seen = set()

        def dfs(i: int, j: int, stack: tuple) -> bool:
            if j == n:
                return True
            key = (i, j, stack)
            if key in seen:
                return False
            seen.add(key)
            if stack and stack[-1] == popped[j]:          # ! 选择一：弹
                if dfs(i, j + 1, stack[:-1]):
                    return True
            if i < n:                                      # ! 选择二：压
                if dfs(i + 1, j, stack + (pushed[i],)):
                    return True
            return False

        return dfs(0, 0, ())


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]), ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]),
             ([], []), ([1], [1]), ([1, 2, 3], [1, 2, 3]), ([1, 2, 3], [3, 2, 1]),
             ([1, 2, 3], [2, 1, 3]), ([1, 2, 3], [3, 1, 2])]
    for pu, po in cases:
        r = Solution_1().validateStackSequences(list(pu), list(po))
        assert r == Solution_2().validateStackSequences(list(pu), list(po))
        assert r == Solution_3().validateStackSequences(list(pu), list(po)), (pu, po)
        print(f"pushed={pu}, popped={po} -> {r}")

    for _ in range(400):                 # ! 随机排列对拍：验证贪心和穷举完全一致
        n = random.randint(0, 6)
        pu = list(range(n))
        random.shuffle(pu)
        po = pu[:]
        random.shuffle(po)
        r1 = Solution_1().validateStackSequences(list(pu), list(po))
        r2 = Solution_2().validateStackSequences(list(pu), list(po))
        r3 = Solution_3().validateStackSequences(list(pu), list(po))
        assert r1 == r2 == r3, (pu, po, r1, r2, r3)
    print("随机对拍 400 组通过 ✓（贪心 == 穷举）")
