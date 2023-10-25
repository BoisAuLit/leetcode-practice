from typing import Optional
from ListNode import ListNode, print_list_node

class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        tmp = head
        while tmp and tmp.next:
            tmp.val, tmp.next.val = tmp.next.val, tmp.val
            tmp = tmp.next.next
        return head
