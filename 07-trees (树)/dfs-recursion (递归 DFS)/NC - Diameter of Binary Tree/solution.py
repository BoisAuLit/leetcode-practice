from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution_DFS_Recursive:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        res = 0

        def dfs(root):
            nonlocal res

            if not root:
                return 0
            left, right = dfs(root.left), dfs(root.right)
            res = max(res, left + right)

            return 1 + max(left, right)

        dfs(root)
        return res


"""
Post order traversal:
- Children first
- Parent second

也就是说，必须先处理完左右孩子，才能计算当前节点。
因为当前节点的高度和直径都依赖左右孩子：如果孩子还没算完，就不能计算父节点。
"""


class Solution_DFS_Iterative_Stack:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        stack = [root]
        """
        ? 为什么预先放入 mp = {None: (0, 0)} ?
        * 因为叶子节点的左右孩子都是 None
        """
        mp = {None: (0, 0)}

        while stack:
            node = stack[-1] # 只是查看栈顶节点，但暂时不弹出。

            """
            ! mp[node] = (height, diameter)
            ! mp[node][0] = 以 node 为根的子树高度
            ! mp[node][1] = 以 node 为根的子树内部最大直径
            
            ##################################################

            '(node.left not in mp)' --> 
            并不只是检查节点是否“见过”。

            它真正表示的是：

            这个子节点的高度和直径是否已经计算完成。
            """
            if node.left and node.left not in mp:
                # 当前节点有左孩子，而且左孩子还没有计算完成，那么先去处理左孩子。
                stack.append(node.left)
            elif node.right and node.right not in mp:
                stack.append(node.right)
            else:
                # 当前节点的左右子树都已经算完了，现在终于可以计算当前节点。
                node = stack.pop()

                # ! 当走到这里的时候, node.left 和 node.right 必然都已经被处理过了,
                # ! 所有 mp[node.left] 和 mp[node.right] 必然都是存在的
                h1, d1 = mp[node.left]
                h2, d2 = mp[node.right]

                mp[node] = (
                    1 + max(h1, h2),
                    max(h1 + h2, d1, d2),
                )

        return mp[root][1]
