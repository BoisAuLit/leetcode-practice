"""
📌 信号→模式: 删倒数第 n 个 → 双指针先走 n 步再同步，dummy 处理删头
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from collections import deque
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(
        self, head: Optional[ListNode], n: int
    ) -> Optional[ListNode]:
        dq = deque()
        while head:
            dq.append(head)
            head = head.next
        if len(dq) - n - 1 < 0:
            return dq[-n].next
        prev = dq[-n - 1]
        prev.next = dq[-n].next
        return dq[0]
