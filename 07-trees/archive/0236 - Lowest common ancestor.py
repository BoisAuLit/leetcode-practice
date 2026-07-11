from TreeNode import TreeNode

class Solution:
  def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if not root or root == p or root == q:
      return root

    l = self.lowestCommonAncestor(root.left, p, q)
    r = self.lowestCommonAncestor(root.right, p, q)

    if l and r:
      return root
    return l or r

s = Solution()
list_ = [3,5,1,6,2,0,8, None,None,7,4]
root = TreeNode.from_list(list_)
p = root.left
q = root.right


# result = s.XXXXXXXXXXXXX(input_)
# print(result)
# from typing import List

"""
Time complexity: O()
Space complexity: O()
"""
