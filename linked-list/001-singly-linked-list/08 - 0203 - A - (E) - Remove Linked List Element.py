from typing import Optional
from ListNode import ListNode

class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        

        # Removing nodes in the beginning having the same val
        while head and head.val == val:
            head = head.next
        prev = None
        curr = head
        
        while curr:
            if curr.val == val:
                prev.next = curr.next
            else:
                prev = curr
            curr = curr.next
        return head
        

