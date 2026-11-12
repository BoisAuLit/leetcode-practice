"""LC-0083 - Remove Duplicates from Sorted List

Level 1 · 01 基础指针、Dummy Node 与反转 —— 有序链表去重，**每个值保留一个**
题目在问：已排序链表，重复的值只留一个。1->1->2->3->3 变成 1->2->3。

决定性观察：
  1. **链表已排序** ⟹ 相同的值一定连续出现，只需要比较相邻节点，不用 set。
  2. 保留第一个 ⟹ 只需要一个指针 `cur`：
     `cur.val == cur.next.val` 就跳过 `cur.next`，否则 `cur = cur.next`。
  3. **这题不需要 Dummy Node** —— 头节点永远会被保留（它是它那组的第一个）。
     这正是它和 LC-0082 的分水岭，见下。

LC-0083 vs LC-0082（**删除语义完全不同，必须分清**）：

| | LC-0083 | LC-0082 |
|---|---|---|
| 规则 | 每个值**保留一个** | 出现过重复的值**一个都不留** |
| `1->1->2` | `1->2` | `2` |
| 头节点会被删吗 | **不会** | **会**（`1->1->2` 的头就被删了） |
| 需要 Dummy 吗 | 不需要 | **需要** |
| 指针数量 | 1 个 cur | prev + cur |

删除时**不要**跳两步：`cur.next = cur.next.next` 之后**不能**立刻 `cur = cur.next`，
因为新的 `cur.next` 可能还是重复值（`1->1->1`）。要在 else 分支里才前进。

复杂度：O(n) 时间，O(1) 空间。

边界：
  - [] → []
  - [1,1,1] → [1]
  - [1,2,3] → [1,2,3]（无重复）
  - [1,1,2,3,3] → [1,2,3]
  - 单节点
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
##### ! Solution 1: 单指针扫描，相邻相同就跳过（不需要 Dummy）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：有序链表「每个值留一个」；注意删除后不要立刻前进
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next     # ! 跳过重复的；cur 原地不动，因为后面可能还重复
            else:
                cur = cur.next               # ! 只有确认不重复才前进
        return head


##################################################################################################
##### ! Solution 2: 重建一条新链（不复用原节点），便于和 LC-0082 的写法对照
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（新建节点）
##### ! 适用：想用统一的「dummy + tail 尾插」骨架同时写 0083 和 0082 时
##################################################################################################


class Solution_2:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        cur = head
        while cur:
            nxt = cur
            while nxt and nxt.val == cur.val:    # ! 整组同值一次吃掉
                nxt = nxt.next
            tail.next = ListNode(cur.val)        # ! 每组留一个
            tail = tail.next
            cur = nxt
        return dummy.next


##################################################################################################
##### ! Solution 3: 转数组去重再重建（基准答案，用来对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = ListNode.to_list(head)
        out = [v for i, v in enumerate(vals) if i == 0 or v != vals[i - 1]]
        return ListNode.from_list(out)


if __name__ == "__main__":
    import random

    for vals in [[], [1], [1, 1, 1], [1, 2, 3], [1, 1, 2, 3, 3], [1, 1, 2, 2]]:
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
