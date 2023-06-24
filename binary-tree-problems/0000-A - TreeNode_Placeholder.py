from __future__ import annotations
from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def from_list(l: List) -> TreeNode:
        if not l:
            return None
        head = TreeNode(l[0])
        current_layer = [head]
        index = 1
        all_indices = range(len(l))
        finished = False
        while not finished:
            next_layer = []
            for node in current_layer:
                if index in all_indices:
                    if l[index] is not None:
                        left_node = TreeNode(l[index])
                        node.left = left_node
                        next_layer.append(left_node)
                else:
                    finished = True
                    break
                if index + 1 in all_indices:
                    if l[index + 1] is not None:
                        right_node = TreeNode(l[index + 1])
                        node.right = right_node
                        next_layer.append(right_node)
                else:
                    finished = True
                    break
                index += 2
            current_layer = next_layer
        return head


input_ = [1, None, 2, 3, None, 2, None, 2, 3]
result = TreeNode.from_list(input_)
print(result)
print(10)
