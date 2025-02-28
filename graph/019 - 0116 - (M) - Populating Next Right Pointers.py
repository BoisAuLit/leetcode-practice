from typing import Optional

"""
# Definition for a Node.
"""


class Node:
    def __init__(
        self,
        val: int = 0,
        left: "Node" = None,
        right: "Node" = None,
        next: "Node" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: "Optional[Node]") -> "Optional[Node]":
        if not root:
            return root
        level = [root]
        while True:
            for i in range(0, len(level) - 1):
                level[i].next = level[i + 1]

            next_level = []
            for node in level:
                if not node.left:
                    return root
                next_level.append(node.left)
                next_level.append(node.right)

            level = next_level
