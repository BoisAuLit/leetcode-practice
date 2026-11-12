class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    # ! 以下三个辅助方法是本次重构补上的（原文件缺失导致示例代码无法运行），取自 utils/TreeNode.py
    @staticmethod
    def from_list(values):
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])
        queue = [root]
        i = 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = TreeNode(values[i])
                    queue.append(node.left)
                i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = TreeNode(values[i])
                    queue.append(node.right)
                i += 1
        return root

    @staticmethod
    def to_list(root):
        if not root:
            return []
        out, queue = [], [root]
        while queue:
            node = queue.pop(0)
            if node:
                out.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                out.append(None)
        while out and out[-1] is None:
            out.pop()
        return out

    def printTree(self):
        print("TreeNode ->", TreeNode.to_list(self))

from typing import List
from collections import defaultdict, deque

"""
Time complexity: O(N) --> N is the number of nodes
Space complexity: O(N)
"""


class Solution:
    def verticalOrder(self, root: TreeNode) -> List[List[int]]:
        if root is None:
            return []

        columnTable = defaultdict(list)
        min_column = max_column = 0
        queue = deque([(root, 0)])

        while queue:
            node, column = queue.popleft()

            if node is not None:
                columnTable[column].append(node.val)
                min_column = min(min_column, column)
                max_column = max(max_column, column)

                queue.append((node.left, column - 1))
                queue.append((node.right, column + 1))

        return [columnTable[x] for x in range(min_column, max_column + 1)]


list_ = [3, 9, 20, None, None, 15, 7]
treeNode = TreeNode.from_list(list_)
treeNode.printTree()

print()

s = Solution()
result = s.verticalOrder(treeNode)
print(result)
