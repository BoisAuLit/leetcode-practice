from collections import deque

"""
Time complexity: O(n)
Space complexity: O(n)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p, q):
        def check(p, q):
            if not p and not q:
                return True
            if not q or not p:
                return False
            return p.val == q.val

        deq = deque([(p, q)])
        while deq:
            p, q = deq.popleft()
            if not check(p, q):
                return False

            if p:
                deq.append((p.left, q.left))
                deq.append((p.right, q.right))

        return True


t1 = TreeNode(1, TreeNode(3, TreeNode(7), TreeNode(9)), TreeNode(5))
t2 = TreeNode(1, TreeNode(3, TreeNode(7), TreeNode(8)), TreeNode(5))
s = Solution()
output = s.isSameTree(t1, t2)
print(output)
"""

"""
