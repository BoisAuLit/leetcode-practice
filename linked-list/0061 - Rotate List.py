from typing import Optional
from ListNode import ListNode, print_list_node


class Solution:
    def rotateRight(
        self, head: Optional[ListNode], k: int
    ) -> Optional[ListNode]:
        if not head:
            return head
        length = 0
        tmp_head = head
        while tmp_head:
            length += 1
            tmp_head = tmp_head.next

        k = k % length
        if k == 0:
            return head
        prev = tmp_head = head
        for i in range(length-k):
            prev = tmp_head
            tmp_head = tmp_head.next

        new_head = tmp_head
        prev.next = None

        while tmp_head.next:
            tmp_head = tmp_head.next
        tmp_head.next = head

        return new_head


s = Solution()
input_ = ListNode.from_list([1, 2, 3, 4, 5])
result = s.rotateRight(input_, 2)
print_list_node(result)
