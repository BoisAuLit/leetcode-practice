from typing import Optional, List


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
        result = []
        level = [root]
        while level:
            next_level = []
            values = []
            for node in level:
                values.append(node.val)
                next_level.extend(node.children)
            result.append(values)
            level = next_level
        return result

