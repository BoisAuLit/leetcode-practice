from typing import List
from TreeNode import TreeNode
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
