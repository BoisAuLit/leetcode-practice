# Level 1 · 03 路径 DFS、状态传递与 Prefix Sum

## 核心定义
**Top-down**：父亲把「沿路积累的状态」交给孩子，孩子继续加工。
和 Level 1 `02` 的 Bottom-up 正好相反。

## 决定性观察
1. 状态可以是**标量**（剩余 target、当前数字、路径最大值），也可以是**容器**（路径列表、前缀和表）。
2. **要不要回溯，取决于状态是不是可变对象**：

| 状态类型 | 例子 | 要回溯吗 |
|---|---|---|
| int / str（不可变，按值传） | LC-0112 的 remain、LC-0129 的 cur、LC-0257 的路径字符串 | **不用** —— 每层都是新局部变量 |
| list / dict（可变，共享） | LC-0113 的 path、LC-0437 的 prefix_count | **必须** —— 进入时改，离开时改回去 |

3. 结算时机几乎都在**叶节点**（`not node.left and not node.right`），
   **不是** `node is None`。在 None 处结算会让单侧孩子的节点被算两次。

## 四道 Top-down 路径题的对照

| 题 | 向下传什么 | 结算 | 回溯 |
|---|---|---|---|
| LC-0112 Path Sum | 剩余 target | 叶节点判 `remain == 0` | 不用 |
| LC-0113 Path Sum II | 剩余 target + **路径列表** | 叶节点 `res.append(path[:])` | **必须** |
| LC-0257 Binary Tree Paths | 路径字符串 | 叶节点 | 不用 |
| LC-0129 Sum Root to Leaf | `cur*10 + val` | 叶节点累加 | 不用 |

### LC-0113 的两个经典 bug
```python
res.append(path)      # ✗ 存的是同一个列表对象的引用，后续 pop 会把它改空
res.append(path[:])   # ✓ 必须拷贝
```
```python
dfs(node.left); dfs(node.right)    # 忘了 path.pop() ⟹ 兄弟分支看到哥哥的残留
```

### 为什么不能「和超过 target 就剪枝」
节点值**可以是负数**，后面可能再降回来。这个剪枝只在「全正数」时才成立。

## LC-0437 树上前缀和（本章最有价值的一题）
把数组的「前缀和 + 哈希表数子数组」整套搬到树上：

```python
count = defaultdict(int); count[0] = 1      # ★ 空前缀，代表路径从 root 开始
def dfs(node, s):
    if not node: return
    s += node.val
    res += count[s - target]                # 先查祖先
    count[s] += 1                           # 再把自己记进去，供子孙使用
    dfs(node.left, s); dfs(node.right, s)
    count[s] -= 1                           # ★ 回溯：离开这条链就撤销
```

三个必须理解的点：
1. **`count[0] = 1`**：不初始化就会漏掉所有「从根开始」的路径。
2. **返回时 `count[s] -= 1`**：左子树的前缀和不能被右子树看见 ——
   它们**不在同一条根到节点的链上**，不构成合法路径。
3. **先查后加**：保证不会把自己当成自己的祖先（target == 0 时尤其关键）。

**为什么不能用滑动窗口**：节点值可以为负，前缀和沿路径不单调。
这和 LC-0862（数组含负数时滑窗失效）是同一个道理。

复杂度 O(n) 期望；朴素的「每个节点各跑一次 DFS」是 O(n²)（链状树）。

## Top-down 状态传递的两道题

| 题 | 传什么 | 结算 |
|---|---|---|
| LC-1448 Count Good Nodes | 路径最大值（1 个标量） | 每个节点判 `val >= path_max` 就计数 |
| LC-1026 Max Diff Node & Ancestor | 路径 `(min, max)`（2 个标量） | `hi - lo` 取最大 |

两者是「传一个标量」到「传一组标量」的自然推广。

## 题目

| # | 题 | 优先级 |
|---|---|---|
| 01/01 | LC-0112 Path Sum | P1 |
| 01/02 | LC-0113 Path Sum II | P1 |
| 01/03 | LC-0257 Binary Tree Paths | P1 |
| 01/04 | LC-0129 Sum Root to Leaf Numbers | P1 |
| 02/01 | LC-1448 Count Good Nodes in Binary Tree | P0 |
| 02/02 | LC-1026 Maximum Difference Between Node and Ancestor | P2 |
| 03/01 | LC-0437 Path Sum III | P1 |

## 复杂度提醒
LC-0113 最坏 **O(n²)**（拷贝路径），不是 O(n)。
LC-0437 的树上前缀和是 O(n)，朴素双层 DFS 是 O(n²)。

## 复习时的 Pattern Recognition
> 「根到叶的路径满足…」「沿路累积一个值」「从任意祖先往下的路径计数」
> → Top-down。先确定**传什么状态**，再确定**要不要回溯**。


---

## 2026-11-11 新增题目（对照大厂高频题单补的缺口）

| 题 | 位置 | 信号 → 模式 | 备注 |
|---|---|---|---|
| [LC-1457 Pseudo-Palindromic Paths in a Binary Tree](<./01 - 根到叶路径与路径状态/05 - LC-1457 - Pseudo-Palindromic Paths in a Binary Tree>) | `03 - 路径 DFS、状态传递与 Prefix Sum/01 - 根到叶路径与路径状态` | 奇偶计数压成 9 位 bitmask；叶子处 mask & (mask-1) == 0 | LC-0112 骨架 + 位运算 |

每道题的 `solution.py` 都带：全部主流解法（各自的复杂度与适用场景）、一个 ⭐️ Preferred、和一段对独立真值基线的随机对拍。
