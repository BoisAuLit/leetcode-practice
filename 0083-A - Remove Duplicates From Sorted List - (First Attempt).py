from typing import List, Optional

"""
Time complexity: O(n)
Space complexity: O(1)
"""


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
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        head_copy = head
        while head:
            curr = head
            while curr.next and curr.val == curr.next.val:
                curr = curr.next
            curr = curr.next
            head.next = curr
            head = head.next
        return head_copy


s = Solution()
input_ = ListNode.from_list([1, 5, 8, 8, 8, 9, 11, 11, 13, 15])
result = s.deleteDuplicates(input_)
print_list_node(result)


"""
Runtime
- 57 ms
- Beats 49.85%

Memory
- 16.5 MB
- Beats 9.70%
"""
