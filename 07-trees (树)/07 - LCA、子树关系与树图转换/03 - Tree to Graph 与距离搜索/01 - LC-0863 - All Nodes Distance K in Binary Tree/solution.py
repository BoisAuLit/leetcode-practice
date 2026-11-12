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


class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        # ! Step 1: Establish pointers to parents from children
        parents_mapping = {}

        def dfs_build_pointer(node: TreeNode):
            if node.left:
                parents_mapping[node.left.val] = node
                dfs_build_pointer(node.left)
            if node.right:
                parents_mapping[node.right.val] = node
                dfs_build_pointer(node.right)

        dfs_build_pointer(root)

        # ! Step 3: Find the result nodes (within certain distance of the target node)
        visited_nodes = set()
        results = []

        def dfs_get_results(node: TreeNode, remaining_distance: int):
            if not node or node.val in visited_nodes:
                return
            visited_nodes.add(node.val)
            if remaining_distance == 0:
                results.append(node.val)
                return
            remaining_distance -= 1
            if node.val in parents_mapping:
                dfs_get_results(parents_mapping[node.val], remaining_distance)
            dfs_get_results(node.left, remaining_distance)
            dfs_get_results(node.right, remaining_distance)

        dfs_get_results(target, k)
        return results


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# node = TreeNode(1)

# node.printTree()

# s = Solution()
# result = s.distanceK(node, TreeNode(1), 3)
# print(result)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


target = TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4)))

node = TreeNode(
    3,
    target,
    TreeNode(1, TreeNode(0), TreeNode(8)),
)

node.printTree()

s = Solution()
result = s.distanceK(node, target, 2)
print(result)
