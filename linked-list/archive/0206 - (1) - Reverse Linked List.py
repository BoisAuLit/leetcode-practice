from typing import Optional
from ListNode import ListNode, print_list_node

"""
Time complexity: O(n)
Space complexity: O(1)
"""

# Solution 1 --> Iterative
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
    
# Solution 2 --> Recursive
# class Solution:
#     def reverse_list_helper(
#         self, current_node: Optional[ListNode], next_node: Optional[ListNode]
#     ) -> Optional[ListNode]:
#         if not next_node:
#             return current_node
#         next_next_node = next_node.next
#         next_node.next = current_node
#         return self.reverse_list_helper(next_node, next_next_node)

#     def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
#         if not head:
#             return None
#         return self.reverse_list_helper(None, head)


s = Solution()
input_ = ListNode.from_list([1, 2, 3, 4, 5])
print_list_node(input_)

result = s.reverseList(input_)
print_list_node(result)
