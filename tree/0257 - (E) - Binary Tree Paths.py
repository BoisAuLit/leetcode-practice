from TreeNode import TreeNode

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
                stack.append(node.left.val)
            if node.right:
                stack.append(node.right.val)

s = Inorder_Traversal()
input_ = TreeNode.from_list([1, 2, 3, 4, 5, 6, 7])
s.traverse(input_)
# input_.printTree()
# result = s.XXXXXXXXXXXXX(input_)
# print(result)
