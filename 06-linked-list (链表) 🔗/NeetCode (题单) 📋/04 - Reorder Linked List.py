"""
📌 信号→模式: L0→Ln→L1→Ln-1 → 快慢找中点 + 反转后半 + 交替合并
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
    def reorderList(self, head: Optional[ListNode]) -> None:
        dq = deque()
        while head:
            dq.append(head)
            head = head.next
        prev = ListNode()
        isLeft = True
        while dq:
            node = dq.popleft() if isLeft else dq.pop()
            node.next = None
            prev.next = node
            prev = prev.next
            isLeft = not isLeft
