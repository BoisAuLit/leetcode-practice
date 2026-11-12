# Count Univalue Subtrees 笔记

### 📝 2026-09-27 - retry 1

```python
class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        self.count = 0   # 用 self 挂一个计数器,避免 nonlocal;dfs 每确认一棵 uni-value 子树就 +1

        def dfs(node) -> bool:
            # dfs 只回答一个问题:"以 node 为根的这棵子树,是不是 uni-value?"
            # 它不负责数数,数数是顺便在确认的那一刻做的(见下面 count += 1)

            if node is None:
                # 空树视为 uni-value。
                # 原因:空树对父节点的判断不构成任何阻碍——
                # 父节点缺一个孩子,不应该因此被判为"不是 uni-value"。
                return True

            # ===== 关键顺序:先把两个孩子的子树问清楚,再判断自己 =====
            # 这是自底向上(后序遍历):叶子先出结果,一层层往上传。
            # 必须分两行写、两边都调用,不能写成 dfs(node.left) and dfs(node.right):
            # and 会短路,左边一旦是 False 右边就不会被遍历,右子树里的 uni-value 子树全漏数。
            isLeftUniValue = dfs(node.left)
            isRightUniValue = dfs(node.right)

            if isLeftUniValue and isRightUniValue:
                # 走到这里说明:左子树内部全部同值,右子树内部全部同值。
                # 所以只剩一个问题:它们的值和我一样吗?
                # 因为左子树已经"全部等于 node.left.val",
                # 我只需要和 node.left.val 比一次,就等于和整棵左子树比过了。
                # ← 这就是你原来那版漏掉的前提:你直接和孩子比值,
                #    却没先确认"孩子那棵子树自己是不是同值",
                #    于是 [5,5,null,1] 里根节点看到左孩子是 5 就误判了。
                if node.left and node.val != node.left.val:
                    return False          # 左孩子存在且值不同 → 我不是 uni-value
                if node.right and node.val != node.right.val:
                    return False          # 右孩子存在且值不同 → 我不是 uni-value

                # 三个条件全部满足:左子树同值、右子树同值、孩子的值等于我。
                # 此刻可以确定"以我为根的子树是 uni-value",计数 +1,并把 True 传给父节点。
                self.count += 1
                return True

            # 只要有一个孩子的子树不是 uni-value,我这棵就不可能是——
            # 因为我的子树包含它的子树,它里面已经有两种值了。
            # 返回 False,这个 False 会一路传到根,所有祖先都不再计数。
            return False

        dfs(root)
        return self.count
```
