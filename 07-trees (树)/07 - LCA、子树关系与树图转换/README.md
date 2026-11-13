# Level 1 · 07 LCA、子树关系与树图转换

## 核心定义
前面几章都在「沿着树的方向」走。这一章开始处理**节点之间的关系**：
谁是谁的祖先、谁是谁的子树、以及**把树当成图**来走。

## ① Lowest Common Ancestor

### LC-0236（一般二叉树）—— 后序回溯
```python
def lca(node, p, q):
    if not node or node is p or node is q:
        return node                      # 找到其中一个就往上报
    l = lca(node.left, p, q)
    r = lca(node.right, p, q)
    if l and r: return node              # 两侧各找到一个 ⟹ 当前就是分叉点
    return l or r                        # 只有一侧有 ⟹ 把它往上传
```
**为什么正确**：
- `l and r` 都非空，说明 p、q 分别在两棵子树里，当前节点是它们**最深的**公共祖先。
- 只有一侧非空，说明两个都在那一侧（或只找到一个），把候选继续上报。
- 题目保证 p、q **都存在**，所以不需要额外验证 —— 这个前提要主动说出来。
  （如果不保证存在，上面的代码会在只有 p 时错误返回 p。）

复杂度 O(n) 时间、O(h) 空间。

### LC-0235（BST）—— 靠值域往下走
```python
while root:
    if p.val < root.val and q.val < root.val: root = root.left
    elif p.val > root.val and q.val > root.val: root = root.right
    else: return root                    # 分叉点
```
O(h)，**不需要回溯**。对照见 Level 1 `04` 的 README。

### LC-1650（带 parent 指针）—— 换头对齐
节点有 `parent` 指针，于是「从节点往上到根」就是一条链表，
求 LCA 就变成了**两条链表求交点**（LC-0160）：
```python
a, b = p, q
while a is not b:
    a = a.parent if a else q
    b = b.parent if b else p
return a
```
**它不是 LC-0236 的同一份实现** —— 方向相反（向上走而不是向下递归）。
另一种做法是把 p 的所有祖先放进 set，再沿 q 往上找第一个在 set 里的。

## ② 子树结构匹配（LC-0572）

**复用 LC-0100 Same Tree**：对主树的每个节点，判断以它为根的子树是否和目标树相同。
```python
def isSubtree(s, t):
    if not s: return False
    if isSameTree(s, t): return True
    return isSubtree(s.left, t) or isSubtree(s.right, t)
```

**复杂度不要说成 O(n)**：朴素做法是 **O(n × m)**
（n 是主树节点数，m 是目标树节点数）。
进阶做法可以把两棵树序列化成带 null 标记的字符串，用字符串匹配（KMP）做到 O(n + m)，
但要小心「子串匹配 ≠ 子树匹配」，必须用分隔符避免值的前缀混淆。

**LC-0100 vs LC-0572**：前者比两棵**整树**，后者在主树里**找位置**。
这就是为什么后者要套一层外循环。

## ③ Tree to Graph（LC-0863）—— 本章最重要的思维转换

> **树只有指向孩子的指针，但题目要求从某个节点向三个方向扩散：left、right、parent。**

解法：
1. 先 DFS 一遍，建立 `child -> parent` 的映射（或者直接建邻接表）。
2. 从 target 节点出发做 **BFS**，每一步可以走 left / right / parent 三个方向。
3. **必须维护 visited** —— 否则会沿着 parent 回去、再沿 child 回来，来回震荡。
4. 走 K 层时队列里剩下的就是答案。

复杂度 O(n) 时间、O(n) 空间（parent map + visited）。

**核心认知：树是一种特殊的图（连通、无环、n-1 条边）。**
一旦问题涉及「向上走」或「任意两点间距离」，就应该立刻想到把它当图处理。
这个思路直通 [11-graphs (图论)](<../../11-graphs (图论)/README.md>)。

## 题目

| # | 题 | 优先级 | 关键点 |
|---|---|---|---|
| 01/01 | LC-0236 LCA of a Binary Tree | P0 | 后序回溯；依赖「p、q 都存在」 |
| 01/02 | LC-1650 LCA III（带 parent） | P1 | 换头对齐，等价于链表求交点 |
| 02/01 | LC-0572 Subtree of Another Tree | P0 | 复用 Same Tree；**O(n×m)** |
| 03/01 | LC-0863 All Nodes Distance K | P1 | 建 parent map + BFS + visited |

## 常见错误
- LC-0236 在 p 或 q 不保证存在时直接用标准模板。
- LC-0572 声称复杂度 O(n)。
- LC-0572 用「序列化后判子串」却不加分隔符（`[12]` 会匹配进 `[1,12]`）。
- LC-0863 忘了 visited ⟹ 在 parent / child 之间来回走。
- LC-1650 套用 LC-0236 的向下递归（方向就不对）。

## 复习时的 Pattern Recognition
> 「两个节点的最近公共祖先」→ 有 BST 性质用值域，有 parent 用换头，否则后序回溯。
> 「一棵树是不是另一棵的子树」→ Same Tree + 外层遍历。
> 「距离某节点 K 步的所有节点」「需要向上走」→ **把树转成图**。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1644 Lowest Common Ancestor of a Binary Tree II](<./01 - Lowest Common Ancestor/03 - LC-1644 - Lowest Common Ancestor of a Binary Tree II>) | `07 - LCA、子树关系与树图转换/01 - Lowest Common Ancestor` | p/q 可能不在树里：0236 不能提前 return，要走完全树 + 计数 found==2 | 0236 的隐含假设被拿掉；Premium 题 |
| [LC-1676 Lowest Common Ancestor of a Binary Tree IV](<./01 - Lowest Common Ancestor/04 - LC-1676 - Lowest Common Ancestor of a Binary Tree IV>) | `07 - LCA、子树关系与树图转换/01 - Lowest Common Ancestor` | 0236 的「is p or is q」换成「in 集合」，其余一字不改；LCA 满足结合律 | k 个节点的 LCA；Premium 题 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
