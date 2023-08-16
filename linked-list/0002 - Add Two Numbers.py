from ListNode import ListNode, print_list_node
from typing import Optional

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:

        tmp1 = l1
        tmp2 = l2
        carry = 0
        head = current = ListNode()
        while tmp1 and tmp2:
            carry, digit = divmod(tmp1.val + tmp2.val + carry, 10)
            current.next = ListNode(digit)
            current = current.next
            tmp1 = tmp1.next
            tmp2 = tmp2.next
        remaining = tmp1 if tmp1 else tmp2
        while remaining:
            carry, digit = divmod(remaining.val + carry, 10)
            current.next = ListNode(digit)
            current = current.next
            remaining = remaining.next
        if carry:
            current.next = ListNode(1)
        return head.next


s = Solution()

# Expecting [7, 0, 8]
l1 = ListNode.from_list([2, 4, 3])
l2 = ListNode.from_list([5, 6, 4])
result = s.addTwoNumbers(l1, l2)

print_list_node(result)
