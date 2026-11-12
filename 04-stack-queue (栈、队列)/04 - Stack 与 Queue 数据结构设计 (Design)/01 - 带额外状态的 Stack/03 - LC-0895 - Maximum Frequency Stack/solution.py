"""LC-0895 - Maximum Frequency Stack

Level 1 · 04 Stack 与 Queue 数据结构设计 → Level 2 · 01 带额外状态的 Stack

题目在问：`push(val)`；`pop()` 弹出**出现次数最多**的元素，次数相同时弹**最靠近栈顶**的那个。

### 决定性观察：按「频率」分层，每一层本身是一个栈

把元素按它入栈时的频率归到对应的桶：第 k 次 push 的 x 放进 `group[k]`。

    push 5, 7, 5, 7, 4, 5
    group[1] = [5, 7, 4]      ← 第一次出现的
    group[2] = [5, 7]         ← 第二次出现的
    group[3] = [5]            ← 第三次出现的

pop 永远从**最高的那一层**弹栈顶：`group[maxfreq].pop()`。
为什么这正好满足两条规则？
- 最高层里的元素就是当前频率最大的元素（频率为 k 的元素一定在 1..k 每层都有一份）；
- 同一层内按入栈顺序排列，栈顶就是「最近的」—— 而且**这一层里的顺序 = 这些元素达到频率 k 的先后**，正好是题目的 tie-break。

弹出后 `freq[x] -= 1`，x 自动「降」到下一层（它在下一层的那一份本来就在）。
`maxfreq` 只会在最高层清空时减 1，不会跳 —— 因为频率为 k 的元素在 k−1 层也必然存在。

### 和堆解法的对比

堆解法存 `(freq, timestamp, val)` 也能过，但是 O(log n)；分层桶是 **O(1)**，而且不需要时间戳 —— 这是本题的「aha」。
"""
from collections import defaultdict
from typing import List
import heapq


##################################################################################################
##### ! Solution 1: 频率分层栈（group[freq] 是一个栈）
##### ! 时间复杂度: push / pop 均 O(1)   空间复杂度: O(n)
##### ! 适用：面试标准答案。两张表：freq[val] 当前频率，group[f] 频率为 f 时入栈的元素序列；
#####         pop 永远在 group[maxfreq] 上做
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self):
        self.freq = defaultdict(int)
        self.group = defaultdict(list)           # ! group[f]：第 f 次被 push 的那些值，按 push 顺序
        self.maxfreq = 0

    def push(self, val: int) -> None:
        f = self.freq[val] + 1
        self.freq[val] = f
        self.group[f].append(val)               # ! x 的第 f 份放进第 f 层
        self.maxfreq = max(self.maxfreq, f)

    def pop(self) -> int:
        val = self.group[self.maxfreq].pop()    # ! 最高层的栈顶
        self.freq[val] -= 1
        if not self.group[self.maxfreq]:        # ! 最高层空了才降一层（最多降 1）
            self.maxfreq -= 1
        return val


##################################################################################################
##### ! Solution 2: 最大堆 (−freq, −timestamp, val)
##### ! 时间复杂度: push / pop O(log n)   空间复杂度: O(n)
##### ! 适用：想不到分层时的通解：每次 push 都把 (当前频率, 时间戳) 压进堆；
#####         堆顶就是频率最高、时间最晚的。注意弹出的是「这一份」，频率表要同步减
##################################################################################################


class Solution_2:
    def __init__(self):
        self.freq = defaultdict(int)
        self.heap: List[tuple] = []
        self.t = 0

    def push(self, val: int) -> None:
        self.freq[val] += 1
        self.t += 1
        heapq.heappush(self.heap, (-self.freq[val], -self.t, val))   # ! 频率高优先，再晚入栈优先

    def pop(self) -> int:
        _, _, val = heapq.heappop(self.heap)
        self.freq[val] -= 1
        return val


##################################################################################################
##### ! Solution 3: 朴素列表（真值基线）
##### ! 时间复杂度: push O(1)，pop O(n)   空间复杂度: O(n)
##### ! 适用：只用来对拍。按定义：数频率，从右往左找第一个频率最大的
##################################################################################################


class Solution_3:
    def __init__(self):
        self.a: List[int] = []

    def push(self, val: int) -> None:
        self.a.append(val)

    def pop(self) -> int:
        cnt = defaultdict(int)
        for x in self.a:
            cnt[x] += 1
        best = max(cnt.values())
        for i in range(len(self.a) - 1, -1, -1):
            if cnt[self.a[i]] == best:
                return self.a.pop(i)
        raise RuntimeError


if __name__ == "__main__":
    import random
    random.seed(895)
    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        for v in (5, 7, 5, 7, 4, 5):
            s.push(v)
        out = [s.pop() for _ in range(4)]
        assert out == [5, 7, 5, 4], (cls.__name__, out)

    for _ in range(30):
        impls = [Solution_1(), Solution_2(), Solution_3()]
        size = 0
        for _ in range(2000):
            if size == 0 or random.random() < 0.6:
                x = random.randint(1, 6)
                for im in impls:
                    im.push(x)
                size += 1
            else:
                outs = [im.pop() for im in impls]
                assert outs[0] == outs[1] == outs[2], outs
                size -= 1
    print("所有测试通过 ✓（样例 + 30 × 2000 步随机对拍）")
