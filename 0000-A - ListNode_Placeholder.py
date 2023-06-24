from __future__ import annotations
from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next_=None):
        self.val = val
        self.next = next_

    @staticmethod
    def from_list(l: List[int]) -> ListNode:
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
