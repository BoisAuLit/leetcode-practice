from typing import Optional

"""
Time complexity: O()
Space complexity: O()
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        pass


s = Solution()
# Expecting True
input_ = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))

# Expecting False
# input_ = ListNode(1, ListNode(2))

result = s.isPalindrome(input_)
print(result)
