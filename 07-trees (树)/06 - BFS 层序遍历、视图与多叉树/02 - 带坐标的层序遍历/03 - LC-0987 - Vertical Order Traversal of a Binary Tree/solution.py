"""LC-0987 - Vertical Order Traversal of a Binary Tree

Level 1 · 06 BFS 层序遍历、视图与多叉树 → Level 2 · 02 带坐标的层序遍历

题目在问：给每个节点坐标 `(row, col)`（左子 col−1、右子 col+1、row+1），按 col 从小到大输出每一列；
**同一列按 row 排，同 row 同 col 的按值排**。

### 和 LC-0314 Vertical Order 的唯一区别就是 tie-break

| | LC-0314 | LC-0987 |
|---|---|---|
| 同列顺序 | 从上到下，**同层按从左到右（BFS 顺序）** | 从上到下，**同层按值从小到大** |
| 解法 | BFS + 按 col 分桶，天然得到顺序 | 必须显式排序 `(row, val)`，或者分桶后对 (row, val) 排 |

所以 0314 用 BFS 不用排序；0987 无论 BFS 还是 DFS 都要排一次 —— 这是面试里要主动说出的差异。

### 两种骨架

1. **收集三元组再排序**：DFS/BFS 收集 `(col, row, val)`，整体 `sort()` 后按 col 切组。O(n log n)，代码最短。
2. **按 col 分桶 + 每桶排序**：`cols[col].append((row, val))`，最后对每个桶排。总复杂度同样 O(n log n)，
   但当列很多、每列很短时排序成本更低；也更接近 0314 的写法，便于对照。

`min_col / max_col` 一边遍历一边记，输出时 `range(min_col, max_col + 1)` 就不需要对 key 排序。
"""
from collections import defaultdict, deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


##################################################################################################
##### ! Solution 1: BFS 带坐标 + 按 col 分桶 + 每桶按 (row, val) 排序
##### ! 时间复杂度: O(n log n)（最坏所有节点一列）   空间复杂度: O(n)
##### ! 适用：面试标准答案。和 LC-0314 的 BFS 骨架完全一样，只多了「桶内排序」这一行 —— 把差异说出来
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        cols = defaultdict(list)                       # ! col → [(row, val), ...]
        q = deque([(root, 0, 0)])
        min_col = max_col = 0
        while q:
            node, row, col = q.popleft()
            cols[col].append((row, node.val))
            min_col, max_col = min(min_col, col), max(max_col, col)
            if node.left:
                q.append((node.left, row + 1, col - 1))
            if node.right:
                q.append((node.right, row + 1, col + 1))
        # ! 同列按 (row, val) 排；0314 这里不排序（保持 BFS 顺序），这是两题唯一的差别
        return [[v for _, v in sorted(cols[c])] for c in range(min_col, max_col + 1)]


##################################################################################################
##### ! Solution 2: DFS 收集 (col, row, val) 三元组，整体排序后按 col 切组
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：代码最短的写法；排序键 (col, row, val) 一次把三层顺序全部定好，再用 groupby 切开
##################################################################################################


class Solution_2:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        from itertools import groupby
        triples = []

        def dfs(node, row, col):
            if not node:
                return
            triples.append((col, row, node.val))
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)
        triples.sort()                                 # ! (col, row, val) 字典序 = 题目要求的三层顺序
        return [[v for _, _, v in grp] for _, grp in groupby(triples, key=lambda t: t[0])]


##################################################################################################
##### ! Solution 3: 显式按 row 分层再按 val 排（把排序键拆开写，便于看清 tie-break 的两层）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：面试官追问「同列同行怎么排」时，这个写法把 row 分组和 val 排序分成两步，最容易口述
##################################################################################################


class Solution_3:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        grid = defaultdict(lambda: defaultdict(list))  # ! grid[col][row] = [vals]
        q = deque([(root, 0, 0)])
        while q:
            node, row, col = q.popleft()
            grid[col][row].append(node.val)
            if node.left:
                q.append((node.left, row + 1, col - 1))
            if node.right:
                q.append((node.right, row + 1, col + 1))
        out = []
        for col in sorted(grid):
            column = []
            for row in sorted(grid[col]):              # ! 先按 row
                column.extend(sorted(grid[col][row]))  # ! 同 row 再按 val
            out.append(column)
        return out


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """LeetCode 风格的层序数组 → 树。"""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    import random
    cases = [
        ([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
        ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
        ([1, 2, 3, 4, 6, 5, 7], [[4], [2], [1, 5, 6], [3], [7]]),      # ! 同行同列 5,6 要按值排 → 和上一例结果一样
        ([1], [[1]]),
    ]
    for vals, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().verticalTraversal(build(vals))
            assert got == want, (cls.__name__, vals, got, want)

    # ! 随机树对拍：三种实现必须一致
    random.seed(987)
    for _ in range(300):
        n = random.randint(1, 40)
        vals = [random.randint(0, 9) for _ in range(n)]
        for i in range(1, n):
            if random.random() < 0.25:
                vals[i] = None
        root = build(vals)
        outs = [cls().verticalTraversal(root) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (vals, outs)
    print("所有测试通过 ✓")
