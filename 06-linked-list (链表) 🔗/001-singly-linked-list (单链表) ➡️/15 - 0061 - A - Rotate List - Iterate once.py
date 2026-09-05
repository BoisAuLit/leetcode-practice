from typing import Optional
from ListNode import ListNode

class Solution:
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

s = Solution()
head = ListNode.from_list([1, 2, 3, 4, 5])
result = s.rotateRight(head, 52)
ListNode.print_list_node(result)

