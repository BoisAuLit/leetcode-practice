from typing import Optional

"""
Time complexity: O(n)
Space complexity: O(1)
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while slow and slow.next and fast and fast.next and fast.next.next:
            if slow.next == fast.next.next:
                return True
            slow = slow.next
            fast = fast.next.next
        return False

"""
Runtime
- 67ms
- Beats 75.86%

Memory
20.35mb
- Beats 75.47%
"""
