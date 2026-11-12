"""LC-0113 - Path Sum II

Level 1 · 03 路径 DFS、状态传递与 Prefix Sum —— Root-to-Leaf + **回溯（Backtracking）**
题目在问：返回**所有**根到叶路径，使路径和等于 targetSum。

和 LC-0112 的区别（这就是本题新增的东西）：
  - **LC-0112** 只问「存不存在」⟹ 返回 bool，找到一条就能立刻 return，不需要记路径。
  - **LC-0113** 要「列出全部」⟹ 必须**维护当前路径**，而且不能提前退出。
  维护路径就带来了本题唯一的新技能：**回溯**。

决定性观察：
  1. 用一个共享的 `path` 列表，进入节点时 `append`，**离开节点时必须 `pop`**。
     不 pop 的话，兄弟分支会看到哥哥分支残留的节点。
  2. 命中答案时必须 **`res.append(path[:])` 拷贝一份**。
     直接 `res.append(path)` 存的是**同一个列表对象的引用**，
     后续的 append/pop 会把已经存进结果的路径也改掉 —— 最后全部变成空列表。
     **这是本题 90% 的 bug 来源。**
  3. 叶节点的定义是 `not node.left and not node.right`，
     **不是** `node is None`。在 None 处判断会让「单侧孩子」的节点被误判成叶子。

Loop Invariant：进入 `dfs(node)` 时，`path` 恰好是从 root 到 node 的父节点的路径；
      函数返回时，`path` 必须恢复成进入时的样子（这就是回溯的契约）。

```python
def dfs(node, remain):
    if not node: return
    path.append(node.val)
    remain -= node.val
    if not node.left and not node.right and remain == 0:
        res.append(path[:])          # ★ 必须拷贝
    dfs(node.left, remain)
    dfs(node.right, remain)
    path.pop()                       # ★ 必须回溯
```

复杂度：O(n) 遍历，但**拷贝路径**最坏 O(n) 一次，总共 O(n²)（例如一条链上全是答案）。
      空间 O(h) 递归栈 + O(结果总长度)。
      不要笼统地说 O(n) —— 面试里这个细节会被追问。

边界：
  - 空树 → `[]`
  - 负数节点值（target 可能被「超过」后又降回来，所以**不能剪枝说「和已经大于 target 就返回」**）
  - 根就是叶且等于 target
  - 存在多条答案路径
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def from_list(values):
        """LeetCode 的层序数组表示（None 表示空位）-> 树根。"""
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])
        queue, i = [root], 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = TreeNode(values[i]); queue.append(node.left)
                i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = TreeNode(values[i]); queue.append(node.right)
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
                out.append(node.val); queue.append(node.left); queue.append(node.right)
            else:
                out.append(None)
        while out and out[-1] is None:
            out.pop()
        return out

##################################################################################################
##### ! Solution 1: DFS + 共享 path + 回溯（append / pop 配对）
##### ! 时间复杂度: O(n^2) 最坏（拷贝路径）   空间复杂度: O(h) 递归栈
##### ! 适用：所有「列出全部满足条件的根到叶路径」的题；回溯模板的入门题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(node, remain):
            if not node:
                return
            path.append(node.val)
            remain -= node.val
            if not node.left and not node.right and remain == 0:   # ! 叶子判断：左右都空
                res.append(path[:])                                 # ! 必须拷贝！
            dfs(node.left, remain)
            dfs(node.right, remain)
            path.pop()                                              # ! 回溯：恢复现场

        dfs(root, targetSum)
        return res


##################################################################################################
##### ! Solution 2: 每层传一个新列表（不用回溯，代价是更多内存分配）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2) 最坏
##### ! 适用：写起来不会忘记 pop；但每个节点都新建列表，常数更差
##################################################################################################


class Solution_2:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res: List[List[int]] = []

        def dfs(node, remain, path):
            if not node:
                return
            path = path + [node.val]       # ! 新建列表，天然隔离了兄弟分支
            remain -= node.val
            if not node.left and not node.right and remain == 0:
                res.append(path)
            dfs(node.left, remain, path)
            dfs(node.right, remain, path)

        dfs(root, targetSum, [])
        return res


##################################################################################################
##### ! Solution 3: 显式栈的迭代 DFS（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：正确性参照；也展示了「递归栈 = 显式栈 + 手动保存状态」
##################################################################################################


class Solution_3:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if not root:
            return []
        res = []
        stack = [(root, targetSum - root.val, [root.val])]
        while stack:
            node, remain, path = stack.pop()
            if not node.left and not node.right and remain == 0:
                res.append(path)
            if node.right:
                stack.append((node.right, remain - node.right.val, path + [node.right.val]))
            if node.left:
                stack.append((node.left, remain - node.left.val, path + [node.left.val]))
        return res


if __name__ == "__main__":
    import random

    cases = [([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22),
             ([1, 2, 3], 5), ([], 0), ([1, 2], 1), ([1], 1),
             ([-2, None, -3], -5)]
    for vals, t in cases:
        a = Solution_1().pathSum(TreeNode.from_list(vals), t)
        b = Solution_2().pathSum(TreeNode.from_list(vals), t)
        c = Solution_3().pathSum(TreeNode.from_list(vals), t)
        assert sorted(a) == sorted(b) == sorted(c), (vals, t, a, b, c)
        print(f"{vals}, target={t} -> {a}")

    for _ in range(500):                 # ! 随机树（含负数）三方对拍
        vals = [random.choice([random.randint(-3, 3), None]) for _ in range(random.randint(0, 10))]
        if vals and vals[0] is None:
            vals[0] = 1
        t = random.randint(-5, 5)
        a = Solution_1().pathSum(TreeNode.from_list(vals), t)
        b = Solution_2().pathSum(TreeNode.from_list(vals), t)
        c = Solution_3().pathSum(TreeNode.from_list(vals), t)
        assert sorted(a) == sorted(b) == sorted(c), (vals, t, a, b, c)
    print("随机对拍 500 组通过 ✓（含负数，验证不能用「和超了就剪枝」）")
