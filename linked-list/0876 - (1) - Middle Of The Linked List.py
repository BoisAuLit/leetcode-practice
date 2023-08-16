from typing import Optional

"""
Time complexity: O(n)
Space complexity: O(1)
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head.next:
            return head
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow.next if fast.next else slow


s = Solution()
input_ = ListNode(
    1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))
)  # Expecting 3
# input_ = ListNode(
#     1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6)))))
# )  # Expecting 4
result = s.middleNode(input_)
print(result.val)

"""
Runtime
- 52 ms
- Beats 23.39%

Memory
- 16.3 MB
- Beats 70.81%
"""
