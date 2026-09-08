"""
📌 信号→模式: 逆序链表加法 → 逐位相加带进位，dummy 头，末尾处理剩余进位
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = prev = ListNode()
        carry = 0
        while l1 or l2:
            d1 = l1.val if l1 else 0
            d2 = l2.val if l2 else 0
            carry, digit = divmod(d1 + d2 + carry, 10)
            newNode = ListNode(digit)
            prev.next = newNode
            prev = newNode
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        if carry:
            prev.next = ListNode(1)

        return dummy.next
