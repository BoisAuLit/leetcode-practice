from typing import List

"""
Time complexity: O(n+m)
Space complexity: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next_=None):
        self.val = val
        self.next = next_

    @staticmethod
    def from_list(l: List[int]):
        head = ListNode()
        curr = head
        for number in l:
            new_node = ListNode(number)
            curr.next = new_node
            curr = new_node
        return head.next


def print_list_node(ln: ListNode):
    if ln is None:
        print("Empty ListNode")
        return
    l = []
    while ln is not None:
        l.append(ln.val)
        ln = ln.next
    print("ListNode ->", l)


class Solution:
    def mergeTwoLists(self, l1, l2):
        head = ListNode()
        curr = head
        while l1 and l2:
            if l1.val <= l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next

        curr.next = l1 or l2
        return head.next


s = Solution()

# Test case 1: No empty ListNode
ln1 = ListNode.from_list([1, 2, 4])
ln2 = ListNode.from_list([1, 3, 4])
result = s.mergeTwoLists(ln1, ln2)
print_list_node(result)

# Test case 2: One of two ListNodes is empty
# ln1 = None
# ln2 = ListNode.from_list([1, 3, 4])
# result = s.mergeTwoLists(ln1, ln2)
# print_list_node(result)

# Test case 3: Two ListNodes are all empty
# ln1 = None
# ln2 = None
# result = s.mergeTwoLists(ln1, ln2)
# print_list_node(result)

"""
Runtime
- 41 ms
- Beats 84.8%

Memory
- 16.1 MB
- Beats 75.70%
"""
