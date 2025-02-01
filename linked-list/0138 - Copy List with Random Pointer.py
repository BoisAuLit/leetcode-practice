from typing import Optional

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""


class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return None
        mapping = dict()
        tmp_head = head
        prev = new_head = Node(0)
        while tmp_head:
            new_node = Node(tmp_head.val)

            if tmp_head.random is not None:
                new_node.random = id(tmp_head.random)

            prev.next = new_node
            prev = new_node
            mapping[id(tmp_head)] = (tmp_head, new_node)
            tmp_head = tmp_head.next
        
        tmp_head = new_head.next
        while tmp_head:
            if tmp_head.random is not None:
                tmp_head.random = mapping[tmp_head.random][1]
            tmp_head = tmp_head.next
        return new_head.next


n1 = Node(7)
n2 = Node(13)
n3 = Node(11)
n4 = Node(10)
n5 = Node(1)

n1.next = n2
n1.random = None

n2.next = n3
n2.random = n1

n3.next = n4
n3.random = n5

n4.next = n5
n4.random = n3


n5.next = None
n5.random = n1


s = Solution()
input_ = n1
result = s.copyRandomList(input_)
print(result.next.next.random.val)
