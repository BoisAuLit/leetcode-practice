from typing import Optional
from collections import deque


class Node:
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
    @staticmethod
    def print_doubly(node) -> None:
        while node:
            print(node.val)
            node = node.next


class Solution:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        # ! This is very important
        if not head:
            return head
        stack = deque([head])

        dummy = Node(0, None, None, None)
        prev = dummy
        while stack:
            curr = stack.pop()
            prev.next = curr
            curr.prev = prev

            if curr.next:
                stack.append(curr.next)
            if curr.child:
                stack.append(curr.child)
                curr.child = None
            prev = curr
        dummy.next.prev = None
        return dummy.next


n1 = Node(1, None, None, None)
n2 = Node(2, None, None, None)
n3 = Node(3, None, None, None)
n4 = Node(4, None, None, None)
n5 = Node(5, None, None, None)
n6 = Node(6, None, None, None)
n7 = Node(7, None, None, None)
n8 = Node(8, None, None, None)
n9 = Node(9, None, None, None)
n10 = Node(10, None, None, None)
n11 = Node(11, None, None, None)
n12 = Node(12, None, None, None)

n1.next = n2
n2.prev = n1

n2.next = n3
n3.prev = n2

n3.next = n4
n4.prev = n3

n4.next = n5
n5.prev = n4

n5.next = n6
n6.prev = n5

# ----------------------

n7.next = n8
n8.prev = n7

n8.next = n9
n9.prev = n8

n9.next = n10
n10.prev = n9

# ----------------------

n11.next = n12
n12.prev = n11

# ----------------------

n3.child = n7

n8.child = n11

s = Solution()
head = n1
result = s.flatten(head)
Node.print_doubly(result)
