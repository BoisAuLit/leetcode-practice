from typing import List
from TreeNode import TreeNode


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
