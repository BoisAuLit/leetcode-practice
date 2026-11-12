"""LC-0092 - Reverse Linked List II

Level 1 · 01 基础指针、Dummy Node 与反转 —— 局部区间反转
题目在问：反转链表中第 left 到第 right 个节点（1-indexed），其余不动，一趟完成。

决定性观察：
  1. 反转本身就是 LC-0206 的循环，**新东西只有「接口」**：
     反转完那一段之后，要把它的头尾正确接回前后两部分。
  2. 一共要记住 4 个位置（画图之后就不用背了）：
        prev      = 第 left-1 个节点（反转段之前的那个）
        seg_head  = 第 left 个节点   —— 反转后会变成这一段的**尾巴**
        seg_tail  = 第 right 个节点  —— 反转后会变成这一段的**头**
        after     = 第 right+1 个节点
     最后接线：`prev.next = seg_tail`，`seg_head.next = after`。
  3. **Dummy Node 是必需的**：当 `left == 1` 时，prev 就是 dummy，
     否则「反转段之前没有节点」要写一整套特殊分支。

Loop Invariant（反转循环内）：
      `prev` 指向已反转部分的头，`curr` 指向待反转部分的首节点，
      每一步都必须**先保存 `curr.next`**，再改 `curr.next`，否则链就断了。

头插法（Solution_2）的另一种视角：
      不移动 prev，每次把 curr 后面那个节点「摘下来插到 prev 后面」。
      循环 `right - left` 次即可。这种写法不需要先走到 seg_tail，
      很多人觉得更不容易写错，但指针赋值顺序必须严格。

复杂度：O(n) 时间（只走一趟），O(1) 额外空间。

边界：
  - left == right → 原样返回（一个节点不用反转）
  - left == 1（反转包含头节点）→ 靠 dummy 处理
  - right == n（反转到尾）→ after 为 None
  - 整个链表反转（left=1, right=n）→ 退化成 LC-0206
  - 单节点链表
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def from_list(values: List[int]) -> Optional["ListNode"]:
        dummy = ListNode()
        cur = dummy
        for v in values:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    @staticmethod
    def to_list(head: Optional["ListNode"]) -> List[int]:
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out


##################################################################################################
##### ! Solution 1: 定位四个边界 → 反转中间段 → 接回前后（最直观，和 LC-0206 共用反转循环）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：任何「只反转某一段」的题；想清楚 4 个位置就不用背代码
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):        # ! 走到第 left-1 个节点
            prev = prev.next
        seg_head = prev.next             # ! 第 left 个，反转后会变成这一段的尾巴
        curr, prev_in_seg = seg_head, None
        for _ in range(right - left + 1):          # ! 标准 LC-0206 反转循环，跑 right-left+1 次
            nxt = curr.next              # ! 必须先存，再改 curr.next
            curr.next = prev_in_seg
            prev_in_seg = curr
            curr = nxt
        prev.next = prev_in_seg          # ! prev_in_seg 现在是反转段的新头（原第 right 个）
        seg_head.next = curr             # ! curr 现在是第 right+1 个（可能是 None）
        return dummy.next


##################################################################################################
##### ! Solution 2: 头插法 —— 把后面的节点一个个摘下来插到 prev 后面（不用先走到段尾）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：喜欢「原地搬运」视角的写法；循环次数恰好 right - left 次
##################################################################################################


class Solution_2:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        curr = prev.next                 # ! curr 始终是反转段的「当前尾巴」，位置不变
        for _ in range(right - left):
            moved = curr.next            # ! 摘下 curr 后面那个
            curr.next = moved.next       # ! 把它从链上断开
            moved.next = prev.next       # ! 插到 prev 后面（段首）
            prev.next = moved
        return dummy.next


##################################################################################################
##### ! Solution 3: 转成数组反转再重建（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照；面试不会接受，因为没有体现指针操作
##################################################################################################


class Solution_3:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        vals = ListNode.to_list(head)
        vals[left - 1:right] = vals[left - 1:right][::-1]
        return ListNode.from_list(vals)


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 4, 5], 2, 4), ([5], 1, 1), ([1, 2], 1, 2), ([1, 2, 3], 1, 3),
             ([1, 2, 3, 4], 3, 4), ([1, 2, 3, 4], 1, 1)]
    for vals, l, r in cases:
        a = ListNode.to_list(Solution_1().reverseBetween(ListNode.from_list(vals), l, r))
        b = ListNode.to_list(Solution_2().reverseBetween(ListNode.from_list(vals), l, r))
        c = ListNode.to_list(Solution_3().reverseBetween(ListNode.from_list(vals), l, r))
        assert a == b == c, (vals, l, r, a, b, c)
        print(f"{vals}, left={l}, right={r} -> {a}")

    for _ in range(1000):                # ! 随机对拍，覆盖所有 (left, right) 组合
        n = random.randint(1, 8)
        vals = [random.randint(0, 9) for _ in range(n)]
        l = random.randint(1, n)
        r = random.randint(l, n)
        a = ListNode.to_list(Solution_1().reverseBetween(ListNode.from_list(vals), l, r))
        b = ListNode.to_list(Solution_2().reverseBetween(ListNode.from_list(vals), l, r))
        c = ListNode.to_list(Solution_3().reverseBetween(ListNode.from_list(vals), l, r))
        assert a == b == c, (vals, l, r, a, b, c)
    print("随机对拍 1000 组通过 ✓")
