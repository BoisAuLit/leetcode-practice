"""LC-0082 - Remove Duplicates from Sorted List II

Level 1 · 01 基础指针、Dummy Node 与反转 —— 有序链表去重，**重复的全删**
题目在问：已排序链表，只要某个值出现过一次以上，**它的所有副本都要删掉**。
         1->2->3->3->4->4->5 变成 1->2->5。

决定性观察（和 LC-0083 的分水岭）：
  1. **头节点可能被删掉**（`1->1->2` 的答案是 `2`），所以 **Dummy Node 是必需的**。
  2. 需要**两个**指针：
        `prev` —— 最后一个确定要保留的节点（初始是 dummy）
        `cur`  —— 正在考察的节点
  3. 判断的是 `cur.val == cur.next.val`：
     - 相同 ⟹ 这一整组都要删 ⟹ 用 while 一路跳到这组的**最后一个**，
       然后 `prev.next = cur.next`（**prev 不动**，因为还不知道下一个值重不重复）。
     - 不同 ⟹ cur 是独苗，保留 ⟹ `prev = cur`。
     最后统一 `cur = cur.next`。

最容易写错的两点：
  - 删除整组之后**把 prev 也往前挪**了 —— 错，prev 必须停在最后一个确定保留的节点上，
    否则下一组重复值会漏删。
  - 用 `if` 而不是 `while` 跳过重复 —— `1->1->1` 只会跳掉一个。

Loop Invariant：`dummy..prev` 这一段已经是最终答案的前缀（里面没有任何重复值）。

复杂度：O(n) 时间，O(1) 空间。

边界：
  - [1,1] → []（全删光，返回空链表）
  - [1,1,2] → [2]（头被删）
  - [1,2,2] → [1]（尾被删）
  - [1,2,3] → [1,2,3]（无重复）
  - [1,1,1,2,3] → [2,3]
  - [] / [1]
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
##### ! Solution 1: Dummy + prev/cur 双指针，整组重复一次跳完
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：有序链表「重复的一个都不留」；prev 不动是关键
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy                       # ! 最后一个确定保留的节点
        cur = head
        while cur:
            if cur.next and cur.val == cur.next.val:
                dup = cur.val
                while cur and cur.val == dup:   # ! 必须用 while，一次跳完整组
                    cur = cur.next
                prev.next = cur            # ! 整组都不要；prev 保持不动
            else:
                prev = cur                 # ! 独苗，保留
                cur = cur.next
        return dummy.next


##################################################################################################
##### ! Solution 2: 统一的「分组 + 只有一个才尾插」写法（和 LC-0083 的 Solution_2 同骨架）
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外（复用原节点）
##### ! 适用：想用一套骨架同时记住 0082 / 0083 —— 区别只在「这一组要不要留」
##################################################################################################


class Solution_2:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        cur = head
        while cur:
            nxt, count = cur, 0
            while nxt and nxt.val == cur.val:   # ! 先把这一组数完
                nxt = nxt.next
                count += 1
            if count == 1:                      # ! 0083 在这里是「无条件留一个」
                tail.next = cur
                tail = cur
            cur = nxt
        tail.next = None                        # ! 必须收尾，否则会挂着被删的残余节点
        return dummy.next


##################################################################################################
##### ! Solution 3: 用 Counter 统计后重建（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照；它不依赖「已排序」，可以顺便验证排序假设没被用错
##################################################################################################


class Solution_3:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        from collections import Counter
        vals = ListNode.to_list(head)
        cnt = Counter(vals)
        return ListNode.from_list([v for v in vals if cnt[v] == 1])


if __name__ == "__main__":
    import random

    for vals in [[], [1], [1, 1], [1, 1, 2], [1, 2, 2], [1, 2, 3],
                 [1, 1, 1, 2, 3], [1, 2, 3, 3, 4, 4, 5]]:
        a = ListNode.to_list(Solution_1().deleteDuplicates(ListNode.from_list(vals)))
        b = ListNode.to_list(Solution_2().deleteDuplicates(ListNode.from_list(vals)))
        c = ListNode.to_list(Solution_3().deleteDuplicates(ListNode.from_list(vals)))
        assert a == b == c, (vals, a, b, c)
        print(f"{vals} -> {a}")

    for _ in range(1000):
        vals = sorted(random.randint(0, 4) for _ in range(random.randint(0, 9)))
        a = ListNode.to_list(Solution_1().deleteDuplicates(ListNode.from_list(vals)))
        b = ListNode.to_list(Solution_2().deleteDuplicates(ListNode.from_list(vals)))
        c = ListNode.to_list(Solution_3().deleteDuplicates(ListNode.from_list(vals)))
        assert a == b == c, (vals, a, b, c)
    print("随机对拍 1000 组通过 ✓")
