from TreeNode import TreeNode


class Solution_1:
    def buildTree(self, preorder, inorder):

        if not preorder:  # 空 → 没有节点
            return None
        root = TreeNode(preorder[0])  # 钥匙①：根
        mid = inorder.index(preorder[0])  # 钥匙②：根在 inorder 的位置
        # 左边 mid 个 = 左子树；钥匙③：据此切 preorder
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
        return root


"""
✅ This is the preferred solution
"""
class Solution_2:
    def buildTree(self, preorder, inorder):
        idx = {v: i for i, v in enumerate(inorder)}  # 值 → 中序下标，O(1) 查根
        self.p = 0  # preorder 全局指针

        def build(lo, hi):  # 用 inorder[lo..hi] 建子树
            if lo > hi:
                return None
            root = TreeNode(preorder[self.p])
            self.p += 1
            mid = idx[root.val]
            root.left = build(lo, mid - 1)  # ← 必须先建左，再建右
            root.right = build(mid + 1, hi)
            return root

        return build(0, len(inorder) - 1)
