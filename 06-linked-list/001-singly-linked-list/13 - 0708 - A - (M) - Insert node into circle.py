from typing import Optional


class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


"""
Time complexiy: O(N)
Space complexiy: O(1)


Requirements:

If input node is not null, return it in the end.
If input node is null, return new node (circular itself) 
"""


class Solution:
    def insert(self, head: "Optional[Node]", insertVal: int) -> "Node":
        node = Node(insertVal)

        # ! When initial linked list is empty (Special case 1)
        if not head:
            node.next = node
            return node

        curr = head.next
        while True:
            v1, v2 = curr.val, curr.next.val
            x = insertVal

            # ! If the value to be inserted equals to the value of current node
            # ! Ruling out the equality case in the beginning helps us save a lot of time.
            if v1 == x:
                break
            # ! If we did a circle, it means that all elements are the same
            if curr is head:
                break
            """
            Two cases:
            Case 1: x is in perfect position: between current and next node
            Case 2:
                Case 2.1: X is at tail, bigger than tail
                Case 2.2: X is at tail, smaller than head
            """
            if v1 < x < v2 or (v1 > v2 and (v1 < x or x < v2)):
                break
            curr = curr.next
        curr.next, node.next = node, curr.next
        return head


# Test case 1: [3, 4, 1]
# n1 = Node(3)
# n2 = Node(4)
# n3 = Node(1)

# n1.next = n2
# n2.next = n3
# n3.next = n1

# s = Solution()
# s.insert(n1, 2)

# Test case 2: [3, 3, 3]
n1 = Node(3)
n2 = Node(3)
n3 = Node(3)
n1.next = n2
n2.next = n3
n3.next = n1
s = Solution()
s.insert(n1, 0)
print(10)
