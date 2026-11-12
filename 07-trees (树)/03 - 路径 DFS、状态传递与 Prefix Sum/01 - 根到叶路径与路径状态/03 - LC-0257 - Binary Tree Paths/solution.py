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

# class Solution:
#     def binaryTreePaths(self, root):
#         """
#         Let N be the number of nodes in the tree
#         - Time complexity: O(N)
#         - Space complexity: O(N)
#         """
#         if not root:
#             return []
        
#         paths = []
#         stack = [(root, str(root.val))]

#         while stack:
#             node, path = stack.pop()
#             if not node.left and not node.right:
#                 paths.append(path)
#             if node.left:
#                 stack.append((node.left, path + '->' + str(node.left.val)))
#             if node.right:
#                 stack.append((node.right, path + '->' + str(node.right.val)))
        
#         return paths


class Inorder_Traversal:
    def traverse(self, root):
        if not root:
            return
        stack = [root]
        while stack:
            node = stack.pop()
            print(node.val)
            if node.left:
                stack.append(node.left)      # ! 修正：原来写的是 node.left.val，压进去的是 int，
            if node.right:                   # !   下一轮 node.val 就会 AttributeError（整个文件跑不起来）
                stack.append(node.right)     # ! 另注：这个类叫 Inorder_Traversal，但用栈这样写其实是 Preorder

s = Inorder_Traversal()
input_ = TreeNode.from_list([1, 2, 3, 4, 5, 6, 7])
s.traverse(input_)
# input_.printTree()
# result = s.XXXXXXXXXXXXX(input_)
# print(result)
