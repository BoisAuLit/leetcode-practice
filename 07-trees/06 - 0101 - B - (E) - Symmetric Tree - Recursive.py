from TreeNode import TreeNode


class Solution:
    def isSymmetric(self, root):
        def dfs(t1, t2):
            if not t1 and not t2:
                return True
            if bool(t1) != bool(t2):
                return False
            return (
                (t1.val == t2.val)
                and dfs(t1.right, t2.left)
                and dfs(t1.left, t2.right)
            )

        return dfs(root.left, root.right)


# # Test case 1: Expecting True
# s = Solution()
# node = TreeNode.from_list([1, 2, 2, 3, 4, 4, 3])
# TreeNode.printTree(node)
# result = s.isSymmetric(node)
# print(result)

# Test case 2: Expecting False
s = Solution()
node = TreeNode.from_list([1, 2, 2, None, 3, None, 3])
TreeNode.printTree(node)
result = s.isSymmetric(node)
print(result)
