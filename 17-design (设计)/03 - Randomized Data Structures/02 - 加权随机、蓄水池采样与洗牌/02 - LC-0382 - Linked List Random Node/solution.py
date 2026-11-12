"""LC-0382 - Linked List Random Node

Level 1 · 03 Randomized Data Structures → Level 2 · 02 加权随机、蓄水池采样与洗牌

题目在问：给一条单链表，设计 `getRandom()`，每个节点被返回的概率相等。
Follow-up（也是这题存在的唯一理由）：**链表非常长、长度未知、不能全部放进内存** —— 这就是蓄水池采样（Reservoir Sampling）。

### 蓄水池采样 k = 1 的证明（面试一定会被要求口述）

流式扫过第 1, 2, …, n 个元素；看到第 i 个元素时，**以 1/i 的概率用它替换当前答案**。

第 i 个元素最终留下的概率 = 它被选中 × 后面所有人都没把它换掉

    P(i) = (1/i) · (i/(i+1)) · ((i+1)/(i+2)) · … · ((n-1)/n) = 1/n        ✓ 和 i 无关

分子分母交错约掉，这就是「每个元素概率相等」的全部证明。
注意第 1 个元素以 1/1 = 100% 的概率被选中，所以答案永远有初值。

### 两种解法的取舍

| | 存成数组 | 蓄水池采样 |
|---|---|---|
| 空间 | O(n) | **O(1)** |
| 每次 getRandom | O(1) | O(n)（要走完整条链表） |
| 适用 | 链表能放进内存、调用次数多 | 流式数据 / 长度未知 / 内存受限 |

面试里先写数组版，再被追问时写蓄水池 —— 两个都要会。
"""
from collections import Counter
from typing import Optional
import random


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


##################################################################################################
##### ! Solution 1: 蓄水池采样 Reservoir Sampling（k = 1）
##### ! 时间复杂度: 初始化 O(1)，每次 getRandom O(n)   空间复杂度: O(1)
##### ! 适用：Follow-up 的标准答案 —— 链表长度未知、不能存下来；一遍扫描、常数空间
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, head: Optional[ListNode]):
        self.head = head

    def getRandom(self) -> int:
        ans, node, i = 0, self.head, 1
        while node:
            if random.randint(1, i) == 1:       # ! 以 1/i 的概率换成第 i 个节点；i=1 时必中，保证有初值
                ans = node.val
            node, i = node.next, i + 1
        return ans


##################################################################################################
##### ! Solution 2: 预先存进数组，然后均匀抽下标
##### ! 时间复杂度: 初始化 O(n)，每次 getRandom O(1)   空间复杂度: O(n)
##### ! 适用：没有内存限制、getRandom 调用很多次时反而更快；面试里的「第一版」
##################################################################################################


class Solution_2:
    def __init__(self, head: Optional[ListNode]):
        self.vals = []
        while head:
            self.vals.append(head.val)
            head = head.next

    def getRandom(self) -> int:
        return random.choice(self.vals)         # ! random.choice 本身就是均匀抽一个下标


##################################################################################################
##### ! Solution 3: 先数长度，再随机走 k 步（两遍扫描、常数空间）
##### ! 时间复杂度: 初始化 O(n)，每次 getRandom O(n)   空间复杂度: O(1)
##### ! 适用：长度**已知**或允许先扫一遍时的 O(1) 空间做法；和蓄水池的区别在于它不是单遍（single-pass），
#####         真正的流式场景（数据只能看一次）用不了
##################################################################################################


class Solution_3:
    def __init__(self, head: Optional[ListNode]):
        self.head = head
        self.n = 0
        while head:
            self.n += 1
            head = head.next

    def getRandom(self) -> int:
        k = random.randrange(self.n)             # ! [0, n) 均匀
        node = self.head
        for _ in range(k):
            node = node.next
        return node.val


def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


if __name__ == "__main__":
    random.seed(382)
    vals = [1, 2, 3, 4, 5]
    N = 50000
    for cls in (Solution_1, Solution_2, Solution_3):
        obj = cls(build(vals))
        cnt = Counter(obj.getRandom() for _ in range(N))
        freq = {v: cnt[v] / N for v in vals}
        assert all(abs(f - 0.2) < 0.01 for f in freq.values()), (cls.__name__, freq)
        print(f"{cls.__name__:12s} {dict((v, round(f, 3)) for v, f in freq.items())}")
    # ! 单节点链表：永远返回它
    assert all(Solution_1(build([42])).getRandom() == 42 for _ in range(50))
    print("所有测试通过 ✓")
