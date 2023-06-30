from typing import Optional

"""
Time complexity: O(n)
Space complexity: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        self.front_pointer = head

        def isPalindromRecursive(recursiveHead: Optional[ListNode]) -> bool:
            if recursiveHead is None:
                return True
            next_ = isPalindromRecursive(recursiveHead.next)
            valid = recursiveHead.val == self.front_pointer.val
            self.front_pointer = self.front_pointer.next
            return next_ and valid

        return isPalindromRecursive(head)


s = Solution()
# Expecting True
input_ = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))

# Expecting False
# input_ = ListNode(1, ListNode(2))

result = s.isPalindrome(input_)
print(result)

"""
Runtime
- 963 ms
- Beats 7.70%

Memory
- 135.2 MB
- Beats 5.4%
"""
