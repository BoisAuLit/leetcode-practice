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
    def connect(self, root):
        if not root:
            return root
        level = [root]
        while level[0].left:
            next_level = [y for x in level for y in [x.left, x.right]]
            for idx, node in enumerate(next_level[:-1]):
                node.next = next_level[idx + 1]
            level = next_level
        return root
