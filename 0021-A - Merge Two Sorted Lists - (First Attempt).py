from typing import List
from typing import Union

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
    def mergeTwoLists(
        self, list1: Union[ListNode, None], list2: Union[ListNode, None]
    ) -> Union[ListNode, None]:
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        head = ListNode()
        curr = head
        while True:
            if list1 is None:
                while list2 is not None:
                    ln = ListNode(list2.val)
                    curr.next = ln
                    curr = ln
                    list2 = list2.next
                break
            if list2 is None:
                while list1 is not None:
                    ln = ListNode(list1.val)
                    curr.next = ln
                    curr = ln
                    list1 = list1.next
                break

            if list1.val == list2.val:
                ln1 = ListNode(list1.val)
                ln2 = ListNode(list2.val)
                curr.next = ln1
                ln1.next = ln2
                curr = ln2
                list1 = list1.next
                list2 = list2.next
            elif list1.val < list2.val:
                ln = ListNode(list1.val)
                curr.next = ln
                curr = ln
                list1 = list1.next
            else:
                ln = ListNode(list2.val)
                curr.next = ln
                curr = ln
                list2 = list2.next

        return head.next


s = Solution()

# Test case 1: No empty ListNode
# ln1 = ListNode.from_list([1, 2, 4])
# ln2 = ListNode.from_list([1, 3, 4])
# result = s.mergeTwoLists(ln1, ln2)
# print_list_node(result)

# Test case 2: One of two ListNodes is empty
# ln1 = None
# ln2 = ListNode.from_list([1, 3, 4])
# result = s.mergeTwoLists(ln1, ln2)
# print_list_node(result)

# Test case 3: Two ListNodes are all empty
ln1 = None
ln2 = None
result = s.mergeTwoLists(ln1, ln2)
print_list_node(result)

"""
Runtime
- 55 ms
- Beats 33.48%

Memory
- 16.4 MB
- Beats 8.51%
"""
