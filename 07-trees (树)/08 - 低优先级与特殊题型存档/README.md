# Level 1 · 08 低优先级与特殊题型存档

## 用途
保留已有学习成果，但不把它们放进核心必刷路线。本章全部 **P2**。
所有文件在本次重构中**一个字节都没改**，只是换了位置。

## 01 - 特殊子树性质与叶节点统计

### LC-0250 Count Univalue Subtrees（P2）
统计「所有节点值都相同」的子树个数。

**Postorder DFS**，返回值设计是关键：
`dfs(node)` 返回「以 node 为根的子树是不是 univalue」，
同时用一个 nonlocal 计数器累加。

```python
def dfs(node):
    if not node: return True            # 空子树算 univalue（这样叶子才能被正确判定）
    l, r = dfs(node.left), dfs(node.right)
    if not l or not r: return False
    if node.left and node.left.val != node.val:  return False
    if node.right and node.right.val != node.val: return False
    count += 1
    return True
```

两个细节：
- **必须先无条件递归左右**（不能用短路 `l and r`），否则子树里的计数会被跳过。
- **空子树返回 True** 是让叶节点能顺利判定为 univalue 的关键。

它是「Bottom-up 返回 bool + 外部计数」这个模式的练习，
和 LC-0110 Balanced Binary Tree 的结构很像。本题可能是 Premium。

### LC-0404 Sum of Left Leaves（P2）
对所有**左叶节点**求和。

唯一的坑：「是不是左孩子」这个信息**节点自己不知道**，必须由父亲告诉它。
所以要么给 dfs 多传一个 `is_left` 参数，要么在父亲那里判断：
```python
if node.left and not node.left.left and not node.left.right:
    total += node.left.val          # 父亲来判断「我的左孩子是不是叶子」
```
后一种更简洁。这是「有些信息只能自顶向下传递」的小例子。

## 为什么这两道不进核心路线

| 题 | 原因 |
|---|---|
| LC-0250 | Premium 题；它的 Bottom-up 返回 bool 模式已被 LC-0110 完整覆盖 |
| LC-0404 | 技能点太小（只是「父亲判断孩子」），不构成独立 Pattern |

两题都适合当作**递归信息传递的热身**，但不值得占用核心复习时间。

## 保留承诺
本目录下所有 `solution.py`、`metadata.json`、PDF、`note.md`
在本次重构中**未作任何修改**，仅调整了所在路径。
