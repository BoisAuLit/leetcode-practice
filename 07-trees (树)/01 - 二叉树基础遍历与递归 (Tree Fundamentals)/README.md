# Level 1 · 01 二叉树基础遍历与递归 (Tree Fundamentals)

## 核心定义
把递归的三个要素固定下来：**Base Case、递归调用、访问时机**。
三种遍历只是「访问时机」不同，骨架完全一样。

## 决定性观察
1. **一个骨架，三种遍历**：
   ```python
   def dfs(node):
       if not node: return      # Base Case
       # 前序：这里访问（根 → 左 → 右）
       dfs(node.left)
       # 中序：这里访问（左 → 根 → 右）
       dfs(node.right)
       # 后序：这里访问（左 → 右 → 根）
   ```
   **记住访问时机的位置，比记三段代码有用得多。**
2. **什么时候只能用后序**：需要孩子的计算结果时（高度、是否平衡、子树和）。
   前序 / 中序在访问根时孩子还没算完。
3. **BST 的中序 = 升序**。这条性质是整个 Level 1 `04` 的地基，
   LC-0094 看起来最普通，但它是 LC-0098 / LC-0230 / LC-0173 的共同基础。

## 递归栈 vs 显式栈
递归的本质就是编译器帮你维护一个栈。写迭代版时，你手动维护它：
```python
# 迭代前序
stack = [root]
while stack:
    node = stack.pop()
    visit(node)
    if node.right: stack.append(node.right)   # 先压右，后压左 → 左先弹出
    if node.left:  stack.append(node.left)
```
**先压右后压左**是因为栈是后进先出。迭代中序要先一路向左压栈（见 LC-0173）。

## 题目

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0144 Preorder | P1 | 迭代版先压右后压左 |
| 01/02 | LC-0094 Inorder | P1 | **BST 中序 = 升序**；迭代版要一路向左压栈 |
| 01/03 | LC-0145 Postorder | P1 | 迭代版技巧：按「根右左」遍历再整体反转 |
| 02/01 | LC-0104 Maximum Depth | P0 | 最简单的后序汇总：`1 + max(l, r)` |
| 02/02 | LC-0100 Same Tree | P0 | 同时递归两棵树；结构和值都要相同 |
| 02/03 | LC-0226 Invert Binary Tree | P0 | 递归中交换指针；先交换还是先递归都对 |
| 02/04 | LC-0101 Symmetric Tree | P0 | **Mirror DFS**：`left.left` 对 `right.right` |
| 02/05 | LC-0111 Minimum Depth | P1 | **陷阱题**，见下 |

## LC-0111 的陷阱（本章最该记的一条）
```python
return 1 + min(depth(left), depth(right))      # ✗ 错
```
对 `[1, 2]`（只有左孩子）这棵树，右子树深度是 0，上式得 1 —— 但正确答案是 2。
**原因**：最小深度的定义是「根到**叶节点**的最短路径」，
而「没有孩子的一侧」不是叶节点，不构成路径。

正确写法：
```python
if not node.left:  return 1 + depth(node.right)   # 只有右孩子
if not node.right: return 1 + depth(node.left)    # 只有左孩子
return 1 + min(depth(node.left), depth(node.right))
```
（BFS 版更自然：第一个遇到的叶节点所在层就是答案，而且能提前退出。）

## LC-0101 的对称判断
不是「左子树 == 右子树」，而是「左子树 == 右子树的镜像」：
```python
def mirror(a, b):
    if not a and not b: return True
    if not a or not b:  return False
    return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
```
注意最后一行的**交叉**：`a.left ↔ b.right`、`a.right ↔ b.left`。

## 复杂度
全部 O(n) 时间；空间 O(h) 递归栈 —— 平衡树 O(log n)，**退化成链时 O(n)**。

## 常见错误
- LC-0111 直接用 `1 + min(...)`。
- LC-0100 只比较值不比较结构（或反之）。
- LC-0101 忘了交叉比较。
- 迭代前序压栈顺序写反。
- 把「空节点」和「叶节点」搞混：叶节点是 `not node.left and not node.right`。

## 复习时的 Pattern Recognition
> 「遍历输出」「两棵树是否相同 / 对称」「树有多高 / 多浅」「翻转」
> → 本章。先问：**我需要孩子的结果吗？** 需要就写后序。
