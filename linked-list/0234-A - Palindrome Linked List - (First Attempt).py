from typing import Optional

"""
Time complexity: O(n)
Space complexity: O(n)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        list_ = []
        while head:
            list_.append(head.val)
            head = head.next
        return list_ == list_[::-1]


s = Solution()
# Expecting True
input_ = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))

# Expecting False
# input_ = ListNode(1, ListNode(2))

result = s.isPalindrome(input_)
print(result)

"""
Runtime
- 712 ms
- Beats 89.90%

Memory
- 49 MB
- Beats 43.29%
"""
