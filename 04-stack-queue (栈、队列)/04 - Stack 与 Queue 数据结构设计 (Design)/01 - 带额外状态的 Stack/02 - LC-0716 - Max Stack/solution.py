"""LC-0716 - Max Stack

Level 1 · 04 Stack 与 Queue 数据结构设计 → Level 2 · 01 带额外状态的 Stack

题目在问：一个栈，除了 `push / pop / top`，还要 `peekMax()` 和 **`popMax()`** —— 弹出最大值（有多个取最靠栈顶的）。
它和 LC-0155 Min Stack 的区别只有一个操作，但正是 `popMax` 把难度从 Easy 推到 Hard：
Min Stack 的「同步辅助栈」只能在栈顶做删除，而 `popMax` 要**从栈中间删一个元素**。

### 决定性观察：需要「两种顺序」同时可删

- 按**入栈顺序**删（pop）→ 栈 / 双向链表
- 按**值的顺序**删（popMax）→ 有序结构（堆 / 平衡树）
两边都要能找到并删除**同一个节点** ⟹ 要么用双向链表让「中间删除 O(1)」，要么用懒删除让「中间删除」变成「晚点再删」。

### 三条路线

| 解法 | push | pop | popMax | 思路 |
|---|---|---|---|---|
| 两个栈 + 临时缓冲 | O(1) | O(1) | **O(n)** | popMax 时把上面的元素挪走再放回；最简单，先写它 |
| 堆 + 懒删除 | O(log n) | O(log n) 摊还 | O(log n) 摊还 | 栈和堆各存一份 `(val, id)`，删过的 id 记在集合里，碰到再跳过 |
| 双向链表 + 有序表 | O(log n) | O(log n) | O(log n) | 教科书解；Python 没有内置平衡树，用 `SortedList` 或者用堆 + 懒删除代替 |

面试里：先写两栈版（5 分钟），再被追问时升级到堆 + 懒删除。懒删除是本题真正要考的技巧。
"""
import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 两个栈（主栈 + 同步的「当前最大值」栈），popMax 用临时缓冲挖出来
##### ! 时间复杂度: push/pop/top/peekMax O(1)，popMax O(n)   空间复杂度: O(n)
##### ! 适用：面试「第一版」。思路完全沿用 LC-0155：max_stack[i] = stack[:i+1] 的最大值；
#####         popMax 时把顶上的元素先弹进 buffer，弹到最大值后把 buffer 原样 push 回去（顺带重算 max_stack）
##################################################################################################


class Solution_1:
    def __init__(self):
        self.stack: List[int] = []
        self.max_stack: List[int] = []            # ! max_stack[i] = max(stack[:i+1])

    def push(self, x: int) -> None:
        self.stack.append(x)
        self.max_stack.append(max(x, self.max_stack[-1]) if self.max_stack else x)

    def pop(self) -> int:
        self.max_stack.pop()
        return self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def peekMax(self) -> int:
        return self.max_stack[-1]

    def popMax(self) -> int:
        m = self.peekMax()
        buffer = []
        while self.top() != m:                    # ! 把压在最大值上面的元素临时挖走
            buffer.append(self.pop())
        self.pop()                                # ! 这一个就是最靠栈顶的最大值
        while buffer:
            self.push(buffer.pop())               # ! 原顺序放回，max_stack 顺带重算
        return m


##################################################################################################
##### ! Solution 2: 栈 + 最大堆 + 懒删除（Lazy Deletion）
##### ! 时间复杂度: push O(log n)，其余 O(log n) 摊还   空间复杂度: O(n)
##### ! 适用：面试标准答案。每个元素带一个自增 id：栈存 (val, id)，堆存 (-val, -id)。
#####         pop 删掉的 id 和 popMax 删掉的 id 都丢进 removed 集合；另一边的结构碰到已删 id 时再弹掉。
#####         堆按 (-val, -id) 排 ⟹ 同值时 id 大（更靠栈顶）的先出，正好满足题目的 tie-break
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def __init__(self):
        self.stack: List[tuple] = []              # ! (val, id)
        self.heap: List[tuple] = []               # ! (-val, -id) —— 值大优先，同值 id 大优先
        self.removed = set()                      # ! 已经被另一边删掉的 id
        self.next_id = 0

    def push(self, x: int) -> None:
        self.stack.append((x, self.next_id))
        heapq.heappush(self.heap, (-x, -self.next_id))
        self.next_id += 1

    def _clean_stack(self) -> None:
        while self.stack and self.stack[-1][1] in self.removed:
            self.removed.discard(self.stack.pop()[1])   # ! 真正删掉时把 id 从集合里清掉，集合不会无限长

    def _clean_heap(self) -> None:
        while self.heap and -self.heap[0][1] in self.removed:
            self.removed.discard(-heapq.heappop(self.heap)[1])

    def pop(self) -> int:
        self._clean_stack()
        val, idx = self.stack.pop()
        self.removed.add(idx)                     # ! 告诉堆：这个 id 已经没了
        return val

    def top(self) -> int:
        self._clean_stack()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        self._clean_heap()
        return -self.heap[0][0]

    def popMax(self) -> int:
        self._clean_heap()
        neg_val, neg_idx = heapq.heappop(self.heap)
        self.removed.add(-neg_idx)                # ! 告诉栈：这个 id 已经没了
        return -neg_val


##################################################################################################
##### ! Solution 3: 朴素列表（真值基线）
##### ! 时间复杂度: push/pop/top O(1)，peekMax/popMax O(n)   空间复杂度: O(n)
##### ! 适用：只用来对拍。popMax 从右往左找第一个最大值再 del，语义最直白
##################################################################################################


class Solution_3:
    def __init__(self):
        self.a: List[int] = []

    def push(self, x: int) -> None:
        self.a.append(x)

    def pop(self) -> int:
        return self.a.pop()

    def top(self) -> int:
        return self.a[-1]

    def peekMax(self) -> int:
        return max(self.a)

    def popMax(self) -> int:
        m = max(self.a)
        i = len(self.a) - 1 - self.a[::-1].index(m)   # ! 最靠右（栈顶）的那个最大值
        del self.a[i]
        return m


if __name__ == "__main__":
    import random
    random.seed(716)
    # ! 题目样例
    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        s.push(5); s.push(1); s.push(5)
        out = [s.top(), s.popMax(), s.top(), s.peekMax(), s.pop(), s.top()]
        assert out == [5, 5, 1, 5, 1, 5], (cls.__name__, out)

    # ! 随机对拍：三种实现在 3000 步随机操作序列上必须完全一致
    for _ in range(30):
        impls = [Solution_1(), Solution_2(), Solution_3()]
        size = 0
        for _ in range(3000):
            ops = ["push"] if size == 0 else ["push", "pop", "top", "peekMax", "popMax"]
            op = random.choice(ops)
            if op == "push":
                x = random.randint(-5, 5)              # ! 值域小，制造大量相同值，考验 tie-break
                for im in impls:
                    im.push(x)
                size += 1
            else:
                outs = [getattr(im, op)() for im in impls]
                assert outs[0] == outs[1] == outs[2], (op, outs)
                if op in ("pop", "popMax"):
                    size -= 1
    print("所有测试通过 ✓（样例 + 30 × 3000 步随机对拍）")
