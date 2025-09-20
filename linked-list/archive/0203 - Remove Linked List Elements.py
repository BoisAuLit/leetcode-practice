from ListNode import ListNode, print_list_node
from typing import Optional


class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        sentinel = ListNode(0)
        sentinel.next = head

        prev, curr = sentinel, head
        while curr:
            if curr.val == val:
                prev.next = curr.next
            else:
                prev = curr
            curr = curr.next

        return sentinel.next


s = Solution()

# Expecting [1, 2, 3, 4, 5]
# input_ = ListNode.from_list([1, 2, 6, 3, 4, 5, 6])
# print_list_node(input_)
# val = 6

# Expecting []
input_ = ListNode.from_list([7, 7, 7, 7])
print_list_node(input_)
val = 7

result = s.removeElements(input_, val)
print_list_node(result)

"""

"""
