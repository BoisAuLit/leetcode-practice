from typing import List, Optional


# Definition for a Node.
class Node:
    def __init__(
        self, val: Optional[int] = None, children: Optional[List["Node"]] = None
    ):
        self.val = val
        self.children = children


class Solution:
    def levelOrder(self, root: "Node") -> List[List[int]]:
        if not root:
            return []
        level = [root]
        result = []
        while level:
            new_level = []
            values = []
            for node in level:
                values.append(node.val)
                if node.children:
                    new_level.extend(node.children)
            result.append(values)
            level = new_level
        return result
