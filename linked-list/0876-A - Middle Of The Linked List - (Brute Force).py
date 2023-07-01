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
        count = 0
        tmp_head = head
        while tmp_head:
            count += 1
            tmp_head = tmp_head.next

        mid = count // 2 + 1
        count_2 = 0
        while head:
            count_2 += 1
            if count_2 == mid:
                return head
            head = head.next


s = Solution()
# input_ = ListNode(
#     1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))
# )  # Expecting 3
input_ = ListNode(
    1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6)))))
)  # Expecting 4
result = s.middleNode(input_)
print(result.val)

"""
Runtime
- 47 ms
- Bewats 57.86%

Memory
- 16.2 MB
- Beats 70.81%
"""
