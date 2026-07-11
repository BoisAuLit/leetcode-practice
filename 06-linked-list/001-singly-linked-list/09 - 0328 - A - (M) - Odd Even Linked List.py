from typing import Optional
from ListNode import ListNode


class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        odd = head
        even = head.next
        even_head = head.next
        while odd and even:
            if not even.next:
                odd.next = None
                break
            third, fourth = even.next, even.next.next
            odd.next = third
            even.next = fourth
            odd, even = third, fourth
        odd.next = even_head
        return head
        


s = Solution()
head = ListNode.from_list([1, 2, 3, 4, 5])
result = s.oddEvenList(head)
ListNode.print_list_node(result)

