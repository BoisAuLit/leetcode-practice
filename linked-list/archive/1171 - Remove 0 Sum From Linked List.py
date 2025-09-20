from typing import Optional, List
import collections
from ListNode import ListNode, print_list_node


class Solution:
    def removeZeroSumSublists(self, head):
        prefix = 0
        seen = {}
        seen[0] = dummy = ListNode(0, head)
        while head:
            prefix += head.val
            seen[prefix] = head
            head = head.next
        head = dummy
        prefix = 0
        while head:
            prefix += head.val
            head.next = seen[prefix].next
            head = head.next
        return dummy.next


s = Solution()

# Expection [3, 1] or [1, 2, 1]
# input_ = ListNode.from_list([1, 2, -3, 3, 1])
# result = s.removeZeroSumSublists(input_)
# print_list_node(result)

# Expection [1, 2, 4]
input_ = ListNode.from_list([1, 2, 3, -3, 4])
result = s.removeZeroSumSublists(input_)
print_list_node(result)

# Expection [1]
# input_ = ListNode.from_list([1, 2, 3, -3, -2])
# result = s.removeZeroSumSublists(input_)
# print_list_node(result)


"""

"""
