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

# Solution 1 --> Recursive, Half-Palindrome
class Solution:

    def isPalindrome(self, head: ListNode) -> bool:
        if head is None:
            return True

        # Find the end of first half and reverse second half.
        first_half_end = self.end_of_first_half(head)
        second_half_start = self.reverse_list(first_half_end.next)

        # Check whether or not there's a palindrome.
        result = True
        first_position = head
        second_position = second_half_start
        while result and second_position is not None:
            if first_position.val != second_position.val:
                result = False
            first_position = first_position.next
            second_position = second_position.next

        # Restore the list and return the result.
        first_half_end.next = self.reverse_list(second_half_start)
        return result    

    def end_of_first_half(self, head):
        fast = head
        slow = head
        while fast.next is not None and fast.next.next is not None:
            fast = fast.next.next
            slow = slow.next
        return slow

    def reverse_list(self, head):
        previous = None
        current = head
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        return previous

# Solution 2 --> Recursive
# class Solution:
#     def isPalindrome(self, head: Optional[ListNode]) -> bool:
#         self.front_pointer = head

#         def isPalindromRecursive(recursiveHead: Optional[ListNode]) -> bool:
#             if recursiveHead is None:
#                 return True
#             next_ = isPalindromRecursive(recursiveHead.next)
#             valid = recursiveHead.val == self.front_pointer.val
#             self.front_pointer = self.front_pointer.next
#             return next_ and valid

#         return isPalindromRecursive(head)

s = Solution()
# Expecting True
input_ = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))

# Expecting False
# input_ = ListNode(1, ListNode(2))

result = s.isPalindrome(input_)
print(result)
