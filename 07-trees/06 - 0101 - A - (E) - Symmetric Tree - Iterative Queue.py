from TreeNode import TreeNode
from collections import deque


# Python3
class Solution:
    def isSymmetric(self, root):
        queue = deque([root, root])
        while queue:
            t1 = queue.popleft()
            t2 = queue.popleft()
            if not t1 and not t2:
                continue
            if not t1 or not t2:
                return False
            if t1.val != t2.val:
                return False
            queue.append(t1.left)
            queue.append(t2.right)
            queue.append(t1.right)
            queue.append(t2.left)
        return True


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
