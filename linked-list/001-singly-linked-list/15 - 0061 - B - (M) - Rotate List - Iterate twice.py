from typing import Optional
from ListNode import ListNode

class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length = 0
        curr = head
        old_tail = None
        while curr:
            length += 1
            if not curr.next:
                old_tail = curr
            curr = curr.next
        k %= length
        if k == 0:
            return head
        
        index = 0
        curr = head
        new_tail = None
        while curr:
            if index == length - k - 1:
                new_tail = curr
                break
            index += 1
            curr = curr.next
        new_head = new_tail.next
        new_tail.next = None
        old_tail.next = head
        return new_head


s = Solution()
head = ListNode.from_list([1, 2, 3, 4, 5])
result = s.rotateRight(head, 52)
ListNode.print_list_node(result)

