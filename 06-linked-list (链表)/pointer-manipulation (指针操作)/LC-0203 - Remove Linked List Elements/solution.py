class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


from typing import Optional

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
        
