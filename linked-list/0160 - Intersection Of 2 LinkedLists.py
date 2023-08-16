from ListNode import ListNode, print_list_node
from typing import Optional

"""
0Time complexity: O()
Space complexity: O()
"""


class Solution:
    def getLinkedListLength(self, head: Optional[ListNode]) -> int:
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        m = self.getLinkedListLength(headA)
        n = self.getLinkedListLength(headB)
        longer = headA if m > n else headB
        shorter = headB if longer == headA else headA

        count = abs(m - n)
        while count > 0:
            longer = longer.next
            count -= 1
        while shorter:
            if longer == shorter:
                return shorter
            shorter = shorter.next
            longer = longer.next
        return None


s = Solution()

# Two ListNode having the same tail, expecting
tail = ListNode.from_list([2, 4])
headA = ListNode(1, ListNode(9, ListNode(1, tail)))
headB = ListNode(3, tail)


# print_list_node(headA)
# print_list_node(headB)
result = s.getIntersectionNode(headA, headB)
print_list_node(result)
