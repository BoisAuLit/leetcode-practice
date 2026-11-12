"""LC-0669 - Trim a Binary Search Tree

Level 1 · 04 BST 有序性质与操作 → Level 2 · 02 BST 构造、插入与删除

题目在问：删掉 BST 里所有值不在 `[low, high]` 的节点，保留其余节点的**相对结构**，返回新根。

### 决定性观察：节点出界时，整个一侧子树跟着出界

- `node.val < low`：node 和它的**整个左子树**都 < low，全部丢掉；答案只可能在右子树里 ⟹ `return trim(node.right)`
- `node.val > high`：对称，`return trim(node.left)`
- 在范围内：保留 node，递归修两个孩子，`node.left = trim(node.left); node.right = trim(node.right)`

「返回修剪后的子树根」这种**递归返回值直接赋回给孩子指针**的写法，是 BST 删除类题目（LC-0450、LC-0701）的统一骨架。

### 为什么不需要像 LC-0450 那样找后继

LC-0450 删一个节点要在它的两个孩子都存在时找后继补位，因为**只删它自己、保留两边子树**。
本题出界节点的一整侧子树一起被删，剩下的那一侧子树直接顶上来 —— 没有「两边都要保」的情形，所以不需要后继。
这是面试里值得主动说出来的一句对比。
"""
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: 递归，返回修剪后的子树根
##### ! 时间复杂度: O(n)   空间复杂度: O(h)
##### ! 适用：面试标准答案，五行；利用 BST 性质一次砍掉整侧子树
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        if not root:
            return None
        if root.val < low:
            return self.trimBST(root.right, low, high)    # ! 自己和整个左子树都太小
        if root.val > high:
            return self.trimBST(root.left, low, high)     # ! 自己和整个右子树都太大
        root.left = self.trimBST(root.left, low, high)
        root.right = self.trimBST(root.right, low, high)
        return root


##################################################################################################
##### ! Solution 2: 迭代 —— 先找新根，再分别修左链和右链
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：追问「不用递归」。三步：① 根沿着「出界就换边」往下走到第一个在界内的节点
#####         ② 左链上：若 cur.left.val < low 就 cur.left = cur.left.right，否则 cur 下移
#####         ③ 右链对称。左子树里只可能有「太小」的节点需要删（都 ≤ 新根 ≤ high），所以只检查 low
##################################################################################################


class Solution_2:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        while root and (root.val < low or root.val > high):     # ! ① 找新根
            root = root.right if root.val < low else root.left
        if not root:
            return None
        cur = root                                              # ! ② 左链：只会有「太小」的
        while cur.left:
            if cur.left.val < low:
                cur.left = cur.left.right                       # ! 跳过它和它的整个左子树
            else:
                cur = cur.left
        cur = root                                              # ! ③ 右链：只会有「太大」的
        while cur.right:
            if cur.right.val > high:
                cur.right = cur.right.left
            else:
                cur = cur.right
        return root


##################################################################################################
##### ! Solution 3: 中序收集界内的值再重建（真值基线，不保留结构）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：只用来对拍「值的集合和顺序」—— 它不保留原结构，所以不能当答案；
#####         对拍时比较两边的中序序列，另外用「每个保留节点的原父子关系不变」检查结构
##################################################################################################


class Solution_3:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        vals = []

        def inorder(n):
            if n:
                inorder(n.left)
                if low <= n.val <= high:
                    vals.append(n.val)
                inorder(n.right)

        inorder(root)

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)


def build_bst(vals):
    root = None
    for v in vals:
        if root is None:
            root = TreeNode(v); continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left: cur = cur.left
                else: cur.left = TreeNode(v); break
            else:
                if cur.right: cur = cur.right
                else: cur.right = TreeNode(v); break
    return root


def inorder_vals(n, out=None):
    out = [] if out is None else out
    if n:
        inorder_vals(n.left, out); out.append(n.val); inorder_vals(n.right, out)
    return out


def ancestors_ok(n, low, high):
    """结构检查：修剪后仍是合法 BST，且所有值在界内。"""
    def chk(node, lo, hi):
        return node is None or (lo < node.val < hi and low <= node.val <= high and chk(node.left, lo, node.val) and chk(node.right, node.val, hi))
    return chk(n, float("-inf"), float("inf"))


if __name__ == "__main__":
    import random
    random.seed(669)
    for cls in (Solution_1, Solution_2):
        r = cls().trimBST(build_bst([1, 0, 2]), 1, 2)
        assert inorder_vals(r) == [1, 2]
        r = cls().trimBST(build_bst([3, 0, 4, 2, 1]), 1, 3)
        assert inorder_vals(r) == [1, 2, 3] and r.val == 3 and r.left.val == 2 and r.left.left.val == 1, cls.__name__   # ! 结构：3 → 2 → 1
        assert cls().trimBST(build_bst([5]), 6, 9) is None
        for _ in range(300):
            vals = random.sample(range(50), random.randint(1, 20))
            lo = random.randint(-5, 55); hi = random.randint(lo, 60)
            got = cls().trimBST(build_bst(vals), lo, hi)
            want = inorder_vals(Solution_3().trimBST(build_bst(vals), lo, hi))
            assert inorder_vals(got) == want and ancestors_ok(got, lo, hi), (cls.__name__, vals, lo, hi)
    print("所有测试通过 ✓")
