"""LC-0061 - Rotate List

合并自 2 个解法文件:
  1. 15 - 0061 - A - Rotate List - Iterate once.py
  2. 15 - 0061 - B - Rotate List - Iterate twice.py
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# Solution 1: Iterate_once    (原文件: 15 - 0061 - A - Rotate List - Iterate once.py)
# ============================================================================

class Solution_1_Iterate_once:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length = 0
        curr = head
        nodes = []
        while curr:
            length += 1
            nodes.append(curr)
            curr = curr.next
        k %= length
        if k == 0:
            return head
        nodes[length-k-1].next = None
        nodes[-1].next = nodes[0]
        return nodes[length-k]

# ============================================================================
# Solution 2: Iterate_twice    (原文件: 15 - 0061 - B - Rotate List - Iterate twice.py)
# ============================================================================

class Solution_2_Iterate_twice:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        length = 0
        curr = head
        old_tail = None
        while curr:
            length += 1
            if not curr.next:
                old_tail = curr
            curr = curr.next
        k %= length
        if k == 0:
            return head
        
        index = 0
        curr = head
        new_tail = None
        while curr:
            if index == length - k - 1:
                new_tail = curr
                break
            index += 1
            curr = curr.next
        new_head = new_tail.next
        new_tail.next = None
        old_tail.next = head
        return new_head


if __name__ == "__main__":

    # --- Solution 1: Iterate_once ---
    s = Solution_1_Iterate_once()
    head = ListNode.from_list([1, 2, 3, 4, 5])
    result = s.rotateRight(head, 52)
    ListNode.print_list_node(result)

    # --- Solution 2: Iterate_twice ---
    s = Solution_2_Iterate_twice()
    head = ListNode.from_list([1, 2, 3, 4, 5])
    result = s.rotateRight(head, 52)
    ListNode.print_list_node(result)
