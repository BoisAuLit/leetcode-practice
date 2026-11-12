# 07 · Trees（树）

> 树题几乎都是**同一个 DFS 骨架**。真正的区别只有一个问题：
> ## **`dfs(node)` 应该返回什么？**
> 把这个问题答清楚，90% 的树题就不需要单独背了。

本专题共 **49 道题**，8 个 Level 1。

## 一、`dfs` 返回什么 —— 本专题的总纲

| 返回值类型 | 典型题 | 语义 |
|---|---|---|
| **int（高度 / 深度）** | LC-0104、LC-0110 | 这棵子树有多高 |
| **int（计数）** | LC-0222、LC-0250 | 这棵子树里有多少个满足条件的节点 |
| **bool** | LC-0100、LC-0101、LC-0098 | 这棵子树满不满足某个性质 |
| **int（单向路径收益）** | **LC-0124** | 从我往下延伸、只能选一侧的最大收益 |
| **tuple（多状态 DP）** | **LC-0337** | `(抢我, 不抢我)` 两个状态一起返回 |
| **node（候选答案）** | LC-0236 | 这棵子树里找到的 LCA 候选 |
| **不返回，更新外部答案** | LC-0543、LC-1448、LC-0437 | 返回值给父亲用，答案存在 nonlocal 里 |

**最关键的认知（LC-0543 / LC-0124 都靠它）**：
> **递归的返回值**和**最终答案**常常不是同一个东西。
> LC-0543 返回「高度」，但答案是「左高 + 右高」的最大值；
> LC-0124 返回「单向最大收益」，但答案可以同时用上左右两侧。
> 返回值必须是「父亲能用的东西」，答案则在每个节点处单独结算。

## 二、两个遍历方向

| | Top-down（自顶向下） | Bottom-up（自底向上） |
|---|---|---|
| 信息流 | 父 → 子，沿路**携带状态** | 子 → 父，**汇总**子树信息 |
| 遍历序 | Preorder | **Postorder** |
| 典型题 | LC-0112/0113/0129/1448/1026 | LC-0104/0110/0543/0124/0337 |
| 要不要回溯 | **状态是可变对象时要**（LC-0113 的 path） | 不需要 |
| 一句话 | 「我把我知道的告诉孩子」 | 「我等孩子算完再汇总」 |

**回溯的判据**：传下去的状态是**不可变**的（int / str）⟹ 不用回溯（LC-0129、LC-0257）；
是**可变**的（list / dict）⟹ 进入时改、离开时必须改回来（LC-0113、LC-0437）。

## 三、目录地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | 二叉树基础遍历与递归 | 8 | [→](<01 - 二叉树基础遍历与递归 (Tree Fundamentals)/README.md>) |
| 02 | 后序信息汇总与 Tree DP | 5 | [→](<02 - 后序信息汇总与 Tree DP (Bottom-up DFS)/README.md>) |
| 03 | 路径 DFS、状态传递与 Prefix Sum | 7 | [→](<03 - 路径 DFS、状态传递与 Prefix Sum/README.md>) |
| 04 | BST 有序性质与操作 | 10 | [→](<04 - BST 有序性质与操作 (Binary Search Tree)/README.md>) |
| 05 | 树构造、序列化与结构修改 | 5 | [→](<05 - 树构造、序列化与结构修改/README.md>) |
| 06 | BFS 层序遍历、视图与多叉树 | 8 | [→](<06 - BFS 层序遍历、视图与多叉树/README.md>) |
| 07 | LCA、子树关系与树图转换 | 4 | [→](<07 - LCA、子树关系与树图转换/README.md>) |
| 08 | 低优先级与特殊题型存档 | 2 | [→](<08 - 低优先级与特殊题型存档/README.md>) |

```
01 基础遍历与递归/
  01 DFS 三种基本遍历/      144  094  145
  02 基础递归、结构比较与树高度/ 104  100  226  101  111
02 后序汇总与 Tree DP/
  01 高度、平衡与子树统计/   110  543(NC→)  222
  02 路径收益与多状态 Tree DP/ 124(NC→)  337←新
03 路径 DFS 与 Prefix Sum/
  01 根到叶路径与路径状态/   112  113←新  257  129←新
  02 路径上的状态与约束/     1448(NC→)  1026←新₂
  03 树上 Prefix Sum 与路径计数/ 437←新
04 BST/
  01 搜索、验证与顺序统计/   700←新  098(NC→)  230(NC→)  235(NC→)  938←新₂
  02 构造、插入与删除/       108  1008  701←新₂  450←新
  03 Inorder Iterator/       173←新
05 构造、序列化与结构修改/
  01 根据遍历序列重建树/     105(NC→)  106
  02 序列化与有效性验证/     297(NC→)  331
  03 原地展开与指针重连/     114←新
06 BFS 层序、视图与多叉树/
  01 标准层序与每层结果/     102  103←新  199(NC→)
  02 带坐标的层序遍历/       314  662←新₂
  03 N-ary Tree 层序遍历/    429
  04 同层 Next Pointer/      116  117←新₂
07 LCA、子树关系与树图转换/
  01 Lowest Common Ancestor/ 236  1650
  02 子树结构匹配/           572(NC→)
  03 Tree to Graph 与距离搜索/ 863
08 低优先级与存档/           250  404
_resources/  docs/  tutorials/（4 份 BST/DFS/BFS 教程 + TreeNode.py）  utils/
```

## 四、核心模板

**T1 · DFS 三种遍历（同一个骨架，只是访问时机不同）**
```python
def dfs(node):
    if not node: return
    # 前序：这里访问
    dfs(node.left)
    # 中序：这里访问      ← BST 中序 = 升序，这是整个 04 章的基础
    dfs(node.right)
    # 后序：这里访问      ← 需要孩子的信息时，只能在这里
```

**T2 · Bottom-up 汇总（返回值 ≠ 答案）**
```python
self.ans = 0
def dfs(node):
    if not node: return 0
    l, r = dfs(node.left), dfs(node.right)
    self.ans = max(self.ans, l + r)      # 答案：可以用上两侧
    return 1 + max(l, r)                 # 返回：给父亲用，只能选一侧
```

**T3 · Top-down 携带状态**
```python
def dfs(node, state):
    if not node: return
    state = update(state, node)
    if is_leaf(node): settle(state)
    dfs(node.left, state); dfs(node.right, state)
```

**T4 · 分层 BFS**
```python
q = deque([root])
while q:
    for _ in range(len(q)):        # 进层时先固定住本层节点数
        node = q.popleft()
        ...
```

**T5 · BST 上下界验证（LC-0098 的正确写法）**
```python
def valid(node, lo, hi):
    if not node: return True
    if not (lo < node.val < hi): return False
    return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
```
**只检查「当前节点和它的直接左右孩子」是错的** —— BST 不变量约束的是**整棵子树**。

**T6 · 树转图 + BFS（LC-0863）**
先建 `child -> parent` 映射，然后把树当成无向图从目标节点做 BFS，**必须维护 visited**。

| 模板 | 时间 | 空间 |
|---|---|---|
| T1–T3 DFS | O(n) | O(h) 递归栈（退化 O(n)） |
| T4 BFS | O(n) | O(w) 最大层宽 |
| T5 BST 搜索/插入/删除 | **O(h)** | O(h) |
| LC-0173 迭代器 | next 摊还 O(1) | **O(h)** |
| LC-0437 树上前缀和 | O(n) 期望 | O(h) |

## 五、P0 / P1 / P2

**P0（核心必练）** LC-0104、LC-0226、LC-0100、LC-0101、LC-0102、LC-0199、LC-0110、
LC-0543、LC-0124、LC-0098、LC-0230、LC-0235、LC-0236、LC-0105、LC-0297、LC-0572、LC-1448

**P1（重要变体）** LC-0144/0094/0145、LC-0111、LC-0112、LC-0113、LC-0129、LC-0437、
LC-0337、LC-0222、LC-0700、LC-0108、LC-0450、LC-0173、LC-0106、LC-0114、LC-0103、
LC-0116、LC-0117、LC-0429、LC-1650、LC-0863、LC-0257

**P2（低优先级 / 存档）** LC-0250、LC-0404、LC-0331、LC-0314、LC-1008、LC-0662、
LC-0938、LC-0701、LC-1026

### 推荐学习顺序
```
A 递归入门   104 → 226 → 100 → 101 → 111 → 144/094/145
B 后序汇总   110 → 543 → 124 → 337 → 222
C 路径 DFS   112 → 113 → 257 → 129 → 1448 → 1026 → 437
D BST        700 → 098 → 230 → 235 → 938 → 108 → 1008 → 701 → 450 → 173
E 构造序列化 105 → 106 → 297 → 331 → 114
F BFS        102 → 103 → 199 → 314 → 662 → 429 → 116 → 117
G LCA 与图   236 → 1650 → 572 → 863
H 存档       250 → 404
```

## 六、容易混淆的成对题（本专题最该先看的部分）

| 一对 | 区别 |
|---|---|
| **LC-0104 vs LC-0111** | 最小深度**不能**写 `1 + min(left, right)` —— 单侧为空时那一侧不是路径，要取非空侧 |
| **LC-0543 vs LC-0124** | 543 返回高度、答案是 `l+r`；124 返回收益、答案是 `l+val+r`，且收益要 `max(0, gain)` |
| **LC-0100 vs LC-0572** | Same Tree 比两棵整树；Subtree 要对主树**每个节点**调一次 Same Tree，复杂度 O(n·m) 不是 O(n) |
| **LC-0235 vs LC-0236** | BST 版靠值域一路往下走 O(h)；一般二叉树版必须后序回溯找分叉点 |
| **LC-0116 vs LC-0117** | 116 的 O(1) 解法**依赖完美二叉树**；117 必须用 dummy+tail 沿上一层 next 链走 |
| **LC-0314 vs LC-0987** | 两者的排序规则不同（987 同行同列还要按值排序），**不要混用代码** |
| **LC-0105 vs LC-0106** | 前序的根在**头**，后序的根在**尾**；都靠中序切分左右子树 |
| **LC-0450 vs LC-0701** | 插入永远挂叶子；删除可能要给「两个孩子」的节点找中序后继当替身 |

## 七、跨专题索引

| LC | 关系 | 位置 |
|---|---|---|
| LC-0109 Sorted List → BST | 链表 + 树构造 | [06-linked-list](<../06-linked-list (链表)/07 - 低优先级与跨专题存档/02 - 跨专题结构与状态循环/01 - LC-0109 - Convert Sorted List to Binary Search Tree>) |
| LC-0270 Closest BST Value | BST 搜索，主归属更适合本专题 | [05-binary-search](<../05-binary-search (二分查找)/06 - 低优先级与跨专题存档 (Archive)/01 - BST 性质与最近值/01 - LC-0270 - Closest Binary Search Tree Value>) |
| LC-0863 | 树转图 + BFS | 本专题；图论主线见 [11-graphs](<../11-graphs (图论)/>) |
| LC-0437 | 树上前缀和 | 本专题；数组版前缀和见 [01-arrays-hashing](<../01-arrays-hashing (数组、哈希表)/>) |

## 八、NC / LC 处理结果

原目录有 **10 个 NC 来源**：

- **1 组真重复**：`NC - Same Binary Tree` 与 `LC-0100 - Same Tree` 并存。
  按仓库规则「LC / NC 重复时只保留 LeetCode 版」，NC 目录已删除；
  但 NC 版里有一个 LC 版**没有的迭代栈 DFS**（用户自己标了 ✅ Preferred method），
  已一字未改地并入 LC-0100 作为 `Solution_NC_DFS_Iterative_Stack`，并随机对拍验证一致。
- **9 个孤儿 NC**（仓库里没有对应的 LC 目录）：全部**升格**为正式 LC 编号，
  目录改名 + `metadata.id` 改成 `LC-xxxx`，**`practice` 复习记录原样保留**
  （LC-0199 保留了 1 条）。原有的 solution.py、note.md 一个字节都没改。

| 原 NC | 升格为 |
|---|---|
| NC - Diameter of Binary Tree | LC-0543 |
| NC - Binary Tree Maximum Path Sum | LC-0124 |
| NC - Count Good Nodes in Binary Tree | LC-1448 |
| NC - Valid Binary Search Tree | LC-0098 |
| NC - Kth Smallest Integer in BST | LC-0230 |
| NC - Lowest Common Ancestor in BST | LC-0235 |
| NC - Construct Binary Tree from Preorder and Inorder | LC-0105 |
| NC - Serialize and Deserialize Binary Tree | LC-0297 |
| NC - Binary Tree Right Side View | LC-0199 |
| NC - Subtree of Another Tree | LC-0572 |

## 九、第二轮独立审核结果

**自主新增 5 道**（上限 5）：

| 题 | Pattern | 为什么值得加 |
|---|---|---|
| **LC-0117** Populating Next Right Pointers II | BFS / O(1) 空间链式连接 | **它是 LC-0116 的反例**：116 的 O(1) 解法依赖「完美二叉树」，117 一旦允许缺孩子就全盘失效。有了它才知道 116 的前提是什么 |
| **LC-0701** Insert into a BST | BST 插入 | 本章原有「查/验/删」独缺「插」。插入永远挂叶子，正好反衬出删除为什么要找替身，BST 的 CRUD 由此完整 |
| **LC-0938** Range Sum of BST | BST 剪枝 | 把 BST 不变量从「定位一个值」升级到「裁剪整棵子树」，直接迁移到 LC-0669 Trim BST |
| **LC-1026** Max Difference Node & Ancestor | Top-down 双状态 | LC-1448 向下传一个状态，本题传 `(min, max)` 两个，把 Top-down 状态传递推广到一组标量 |
| **LC-0662** Maximum Width of Binary Tree | 堆式编号 | 引入 `left=2i+1, right=2i+2` 这套「树→数组下标」的坐标，和 LC-0314 的「列坐标」互补；并演示了编号归一化防溢出 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-0617 Merge Two Binary Trees | 就是同时遍历两棵树，LC-0100 已覆盖该技能 |
| LC-0987 Vertical Order Traversal | 和已有的 LC-0314 高度重合，只差一条排序规则；已在 README 里说明两者差异 |
| LC-0669 Trim a Binary Search Tree | 和新增的 LC-0938 用的是同一个剪枝 |
| LC-0530 Minimum Absolute Difference in BST | 就是「中序相邻差值」，LC-0230 的中序技巧已覆盖 |
| LC-0951 Flip Equivalent Binary Trees | LC-0100 的变体，额外收益有限 |

## 十、原有资料与修复

- `docs (资料)`、`tutorials (教程)`（4 份 BST/DFS/BFS 教程 + TreeNode.py）、`utils`
  整体搬到 [`_resources/`](<_resources>)，**内容未改**。
- **修复了 9 个原本跑不起来的 solution.py**（迁移前基线 28 通过 / 8 失败）：
  8 个是 `TreeNode` 未定义或缺 `from_list` / `printTree`；
  1 个（LC-0257）是用户的 `Inorder_Traversal` 辅助类里把 `node.left.val` 压进了栈
  （应该压 `node.left`），导致 `AttributeError`。
  **全部只补充定义 / 修正该行，没有改动任何解法逻辑。**
  迁移后：**50 / 50 全部通过**。
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`。

完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
