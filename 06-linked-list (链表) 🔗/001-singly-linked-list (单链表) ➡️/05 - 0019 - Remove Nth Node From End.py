# from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# class Solution:
#     def removeNthFromEnd(
#         self, head: Optional[ListNode], n: int
#     ) -> Optional[ListNode]:
#         positions = dict()
#         curr = head
#         length = 0
#         at = 1 # Current index position
#         while curr:
#             positions[at] = curr
#             curr = curr.next
#             at += 1
#             length += 1
#         if n == length:
#             return head.next
#         positions[length - n].next = positions[length - n].next.next
#         return head

class Solution:
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        dummy = ListNode(0)
        dummy.next = head
        first = dummy
        second = dummy
        # Advances first pointer so that the gap between first and second is n nodes apart
        for _ in range(n + 1):
            first = first.next
        # Move first to the end, maintaining the gap
        while first is not None:
            first = first.next
            second = second.next
        second.next = second.next.next
        return dummy.next
