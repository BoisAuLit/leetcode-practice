from typing import Optional
from ListNode import ListNode


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            carry, digit = divmod(v1 + v2 + carry, 10)
            curr.next = ListNode(digit)
            curr = curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next


# # Test case 1: 345 + 465 = 807
# l1 = ListNode.from_list([2, 4, 3])
# l2 = ListNode.from_list([5, 6, 4])
# s = Solution()
# result = s.addTwoNumbers(l1, l2)
# ListNode.print_list_node(result)
