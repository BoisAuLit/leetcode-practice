from typing import Optional


class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return head

        # Creating a new weaved list of original and copied nodes.
        p1 = head
        while p1:
            # Cloned node
            new_node = Node(p1.val, None, None)

            # Inserting the cloned node just next to the original node.
            # If A->B->C is the original linked list,
            # Linked list after weaving cloned nodes would be A->A'->B->B'->C->C'
            new_node.next = p1.next
            p1.next = new_node
            p1 = new_node.next

        p1 = head

        # Now link the random pointers of the new nodes created.
        # Iterate the newly created list and use the original nodes random pointers,
        # to assign references to random pointers for cloned nodes.
        while p1:
            p1.next.random = p1.random.next if p1.random else None
            p1 = p1.next.next

        # Unweave the linked list to get back the original linked list and the cloned list.
        # i.e. A->A'->B->B'->C->C' would be broken to A->B->C and A'->B'->C'
        p1 = head  # A->B->C
        p2 = head.next  # A'->B'->C'
        result = head.next
        while p1:
            p1.next = p1.next.next
            p2.next = p2.next.next if p2.next else None
            p1 = p1.next
            p2 = p2.next
        return result
