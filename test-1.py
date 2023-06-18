from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Test:
    def print_treenode_preorder(self, t: TreeNode) -> None:
        deq = deque([t])
        while deq:
            node = deq.popleft()
            if node:
                print(node.val)
                deq.append(node.left)
                deq.append(node.right)


# Test case 1, TreeNode is not None
treeNode = TreeNode(1, TreeNode(3, TreeNode(7), TreeNode(9)), TreeNode(5))
# Test case 2, TreeNode is None
# treeNode = None
test = Test()
test.print_treenode_preorder(treeNode)
