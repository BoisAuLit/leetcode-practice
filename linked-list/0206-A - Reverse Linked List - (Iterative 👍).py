from __future__ import annotations
from typing import Optional
from ListNode import ListNode, print_list_node

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        previous = None
        current = head
        while current.next:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        current.next = previous
        return current


s = Solution()
input_ = ListNode.from_list([1, 2, 3, 4, 5])
print_list_node(input_)

result = s.reverseList(input_)
print_list_node(result)

"""
Runtime
- 49 ms
- Beats 77.7%

Memory
- 17.8 MB
- Beats 78.78%
"""
