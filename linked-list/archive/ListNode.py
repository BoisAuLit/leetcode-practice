from __future__ import annotations
from typing import List

class ListNode:
    def __init__(self, val=0, next_=None):
        self.val = val
        self.next = next_

    @staticmethod
    def from_list(list_: List[int]) -> ListNode:
        head = ListNode()
        curr = head
        for number in list_:
            new_node = ListNode(number)
            curr.next = new_node
            curr = new_node
        return head.next


def print_list_node(ln: ListNode):
    if ln is None:
        print("Empty ListNode")
        return
    list_ = []
    while ln is not None:
        list_.append(ln.val)
        ln = ln.next
    print("ListNode ->", list_)
