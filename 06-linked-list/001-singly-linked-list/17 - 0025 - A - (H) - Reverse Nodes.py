from typing import Optional, Tuple
from ListNode import ListNode


class Solution:
    # Reverse a segment of LinkedList
    # Return [finished, new_head, new_tail]
    def reverseSingleGroup(
        self, head: ListNode, k: int
    ) -> Tuple[bool, ListNode, ListNode]:
        tail = head
        curr = head
        prev = None
        for _ in range(k):
            if not curr:
                return True, prev, None
            tmp_next = curr.next
            curr.next = prev
            prev = curr
            curr = tmp_next
        tail.next = curr
        return False, prev, tail

    def reverseKGroup(
        self, head: Optional[ListNode], k: int
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        curr = head
        while True:
            finished, new_head, new_tail = self.reverseSingleGroup(curr, k)
            if finished:
                self.reverseSingleGroup(new_head, k)
                break
            prev.next = new_head
            curr = new_tail.next
            prev = new_tail
        return dummy.next


s = Solution()

node = ListNode.from_list([1, 2, 3, 4, 5])
k = 2
result = s.reverseKGroup(node, k)
ListNode.print_list_node(result)
