from typing import List, Optional
from ListNode import ListNode, print_list_node

"""
Time complexity: O(n)
Space complexity: O(1)
"""

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        head_copy = head
        while head:
            curr = head
            while curr.next and curr.val == curr.next.val:
                curr = curr.next
            curr = curr.next
            head.next = curr
            head = head.next
        return head_copy


s = Solution()
input_ = ListNode.from_list([1, 5, 8, 8, 8, 9, 11, 11, 13, 15])
result = s.deleteDuplicates(input_)
print_list_node(result)


"""
Runtime
- 57 ms
- Beats 49.85%

Memory
- 16.5 MB
- Beats 9.70%
"""
