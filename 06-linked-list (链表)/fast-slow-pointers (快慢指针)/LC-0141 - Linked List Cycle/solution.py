"""LC-0141 - Linked List Cycle

合并自 2 个解法文件:
  1. 02 - 0141 - A - Linked List Cycle - Floyd's Algorithm.py
  2. 18 - 0141 - (1) - Linked List Cycle.py
"""

from typing import Optional


# ============================================================================
# Solution 1: Floyd_s_Algorithm    (原文件: 02 - 0141 - A - Linked List Cycle - Floyd's Algorithm.py)
# ============================================================================

class Solution_1_Floyd_s_Algorithm:
    def hasCycle(self, head: ListNode) -> bool:
        if head is None:
            return False
        slow = head
        fast = head.next
        while slow != fast:
            if fast is None or fast.next is None:
                return False
            slow = slow.next
            fast = fast.next.next
        return True

# ============================================================================
# Solution 2: Linked_List_Cycle    (原文件: 18 - 0141 - (1) - Linked List Cycle.py)
# ============================================================================

# Time complexity: O(n)
# Space complexity: O(1)

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution_2_Linked_List_Cycle:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while slow and slow.next and fast and fast.next and fast.next.next:
            if slow.next == fast.next.next:
                return True
            slow = slow.next
            fast = fast.next.next
        return False
