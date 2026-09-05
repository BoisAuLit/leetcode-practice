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
