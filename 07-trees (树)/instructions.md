
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/07-trees (树)' && claude "$(cat <<'PROMPT'
请直接执行当前 Trees（树）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请建立一套：
- 高面试价值
- 高算法迁移性
- 理论结构清晰
- 学习顺序合理
- 尽可能减少记忆负担
- 适合长期复习
- 可以持续扩充

的 Trees 算法学习体系。

你必须实际执行目录重构、新题创建、已有文件迁移、文档生成和最终验收，而不是只提供规划。

==================================================
一、最重要的学习目标
==================================================

我不希望将几十道 Tree 题分别记忆。

我希望理解少量核心递归模式，
并且能够通过它们推导大部分经典 Tree 面试题。

重点掌握：

1. Preorder Traversal（前序遍历）
2. Inorder Traversal（中序遍历）
3. Postorder Traversal（后序遍历）
4. Top-down DFS（自顶向下 DFS）
5. Bottom-up DFS（自底向上 DFS）
6. Tree DP（树形动态规划）
7. BFS Level Order（层序遍历）
8. BST Ordering Invariant（BST 有序不变量）
9. Root-to-Leaf Path（根到叶路径）
10. Prefix Sum on Trees（树上前缀和）
11. Lowest Common Ancestor（最近公共祖先）
12. Tree Construction（树构造）
13. Serialization / Deserialization（序列化与反序列化）
14. Tree Pointer Rewiring（树指针重连）
15. Tree to Graph（树转图）

必须重点解释：

DFS(node) 究竟应该返回什么？

例如：

- 返回节点数量
- 返回高度
- 返回布尔值
- 返回最大单向路径收益
- 返回多个 DP 状态
- 不返回结果，而是更新外部答案

这些不同的返回值是 Tree DFS 的关键。

不要把所有树题都简化成无意义的：

dfs(node.left)
dfs(node.right)

必须说明递归状态如何定义，以及为什么正确。

==================================================
二、Level 1 -> Level N 分类规则
==================================================

本次推荐：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

必要时才使用 Level 4。

不要为了分类好看而创建无意义的深层文件夹。

所有同级目录必须使用连续数字前缀：

01 - ...
02 - ...
03 - ...

排序标准依次考虑：

1. 学习依赖关系
2. 算法核心性
3. FAANG / Big Tech 面试代表性
4. 知识迁移能力
5. 题目难度递进
6. 对其他题目的复用价值

不要按照 LeetCode 题号机械排序。

Level 3 命名格式：

01 - LC-XXXX - Official English Title
02 - LC-YYYY - Official English Title

每个 Level 2 内重新从 01 编号。

对已有 NC 来源统一使用 _neetcode/ 归档。

允许在有充分教学理由时调整下面的分类，
但不能把分类变成大量只有一道题的碎片化目录。

==================================================
三、推荐 Level 1 -> Level 3 结构
==================================================

第一轮推荐 8 个 Level 1。

--------------------------------------------------
LEVEL 1
01 - 二叉树基础遍历与递归 (Tree Fundamentals)
--------------------------------------------------

核心：
Preorder / Inorder / Postorder
DFS Recursion
Recursive Base Case
Tree Structural Comparison

Level 2：
01 - DFS 三种基本遍历

Level 3：

01 - LC-0144 - Binary Tree Preorder Traversal
02 - LC-0094 - Binary Tree Inorder Traversal
03 - LC-0145 - Binary Tree Postorder Traversal

教学重点：

144：
Preorder = Root -> Left -> Right。

94：
Inorder = Left -> Root -> Right。

145：
Postorder = Left -> Right -> Root。

必须解释：

- 为什么遍历顺序不同
- DFS Recursive Call Stack
- 显式 Stack 与递归栈的关系
- 递归函数的 Base Case
- BST 中 Inorder 为什么产生有序结果

三道题优先复用一个递归框架。

可以补充迭代版本，但不要要求机械记忆大量不同写法。

--------------------------------------------------

Level 2：
02 - 基础递归、结构比较与树高度

Level 3：

01 - LC-0104 - Maximum Depth of Binary Tree
02 - LC-0100 - Same Tree
03 - LC-0226 - Invert Binary Tree
04 - LC-0101 - Symmetric Tree
05 - LC-0111 - Minimum Depth of Binary Tree

教学重点：

104：
dfs(node) 返回当前子树高度。

100：
同时递归比较两棵树。
重点理解结构与节点值都要相同。

226：
交换左右子树。
理解递归过程中的指针修改。

101：
Mirror DFS。
左子树的 left 对应右子树的 right。

111：
最小深度。
必须正确处理只有单侧孩子的节点。

不要错误地直接使用：
1 + min(left_depth, right_depth)
而忽略空孩子的特殊情况。

这一组题目的主要目标是熟悉递归，而不是背诵五套不同算法。

==================================================
LEVEL 1
02 - 后序信息汇总与 Tree DP (Bottom-up DFS)
==================================================

核心：

Postorder DFS
Subtree Aggregation
Return Value Design
Tree DP
Global / Nonlocal Answer

Level 2：
01 - 高度、平衡与子树统计

Level 3：

01 - LC-0110 - Balanced Binary Tree
02 - LC-0543 - Diameter of Binary Tree
03 - LC-0222 - Count Complete Tree Nodes

教学重点：

110：
Bottom-up Height。

每个节点需要知道左右子树高度，
才能判断当前子树是否平衡。

推荐单次 DFS，使用明确的异常状态或 sentinel 表示不平衡。

543：
Diameter = left_height + right_height。

注意：
Diameter 计算的是边的数量，而不是节点数量。

dfs 返回高度，
同时更新全局最大直径。

必须解释：
递归返回值和最终答案不是同一个东西。

222：
利用 Complete Binary Tree 的特殊结构。

可以学习普通 O(n) 计数，
再了解使用左右高度与完全树性质的优化。

必须说明优化依赖完全二叉树约束。

标记 P1，不必将所有优化细节加入核心必背模板。

--------------------------------------------------

Level 2：
02 - 路径收益与多状态 Tree DP

Level 3：

01 - LC-0124 - Binary Tree Maximum Path Sum
02 - LC-0337 - House Robber III

教学重点：

124：
这是最重要的 Bottom-up DFS Hard 题之一。

dfs(node) 返回：

从当前节点向下延伸的最大单向路径收益。

而全局答案可以同时包含：

left_gain + node.val + right_gain

必须解释：

为什么返回给父节点的路径只能选择一侧？

为什么更新全局答案时可以同时选择左右两侧？

为什么需要 max(0, gain)？

为什么全负数树也必须正确处理？

337：
Tree DP。

对每个节点返回两个状态：

rob
skip

rob：
选择当前节点，因此不能选择直接孩子。

skip：
不选择当前节点，可以选择各孩子的最优状态。

重点学习：

dfs(node) -> (rob, skip)

它是 Tree DP 多返回状态的经典例子。

不要求额外记忆大量其他 Tree DP 题。

==================================================
LEVEL 1
03 - 路径 DFS、状态传递与 Prefix Sum
==================================================

核心：

Top-down DFS
Path Tracking
Backtracking
Root-to-Leaf
Prefix Sum on Tree

Level 2：
01 - 根到叶路径与路径状态

Level 3：

01 - LC-0112 - Path Sum
02 - LC-0113 - Path Sum II
03 - LC-0257 - Binary Tree Paths
04 - LC-0129 - Sum Root to Leaf Numbers

教学重点：

112：
Root-to-Leaf Path Sum。

递归传递剩余 target，
到叶节点时判断是否满足。

113：
从判断路径是否存在，
变为返回所有满足条件的路径。

需要：
Path List + Backtracking。

必须解释：
append 后为什么需要 pop，
以及什么时候需要复制 Path。

257：
记录所有 Root-to-Leaf 路径。
可以通过 DFS 传递路径字符串。

129：
递归维护十进制路径数字：

next_value = current * 10 + node.val

到叶节点时累计结果。

这几题共享 Top-down DFS，
但返回值和 Path State 不同。

--------------------------------------------------

Level 2：
02 - 路径上的状态与约束

Level 3：

01 - LC-1448 - Count Good Nodes in Binary Tree

教学重点：

在 DFS 中维护从 root 到当前节点的最大值。

如果 node.val >= path_max，
该节点属于 Good Node。

然后向子节点传递更新后的最大值。

理解 Top-down State Propagation。

此题是经典 DFS 模式。

--------------------------------------------------

Level 2：
03 - 树上 Prefix Sum 与路径计数

Level 3：

01 - LC-0437 - Path Sum III

教学重点：

Prefix Sum + DFS + Backtracking。

路径可以从任意祖先开始，
但必须沿父节点到子节点方向向下。

维护：

prefix_sum
prefix_count

对于当前前缀和 s，
查找此前出现的：

s - targetSum

用于统计合法路径。

必须解释：

- 为什么初始化 prefix_count[0] = 1
- 为什么要在 DFS 返回时撤销当前前缀和的计数
- 为什么不能把不同分支的前缀和混在一起
- 为什么普通正数 Sliding Window 不适合解决本题

目标 O(n) 期望时间。

这是数组 Prefix Sum 向 Tree DFS 迁移的重要题目。

==================================================
LEVEL 1
04 - BST 有序性质与操作 (Binary Search Tree)
==================================================

核心：

BST Ordering Invariant
Inorder Sorted Order
Lower / Upper Bounds
Search / Insert / Delete
BST Iterator

Level 2：
01 - BST 搜索、验证与顺序统计

Level 3：

01 - LC-0700 - Search in a Binary Search Tree
02 - LC-0098 - Validate Binary Search Tree
03 - LC-0230 - Kth Smallest Element in a BST
04 - LC-0235 - Lowest Common Ancestor of a Binary Search Tree

教学重点：

700：
根据 node.val 与 target 的比较，
只搜索左子树或右子树。

这是 BST 有序性质的基础。

98：
使用上下界：

lower < node.val < upper

必须正确处理整棵子树的范围。

不能只检查当前节点和直接左右孩子。

230：
利用 BST Inorder 有序性质，
找到第 k 小的节点。

解释：
为什么中序遍历可以按从小到大输出。

235：
利用 BST 值域进行 LCA 判断。

如果 p、q 都在左侧，向左走。
如果都在右侧，向右走。
否则当前节点是分叉点。

必须与普通 Binary Tree 的 LC-236 对比。

--------------------------------------------------

Level 2：
02 - BST 构造与删除

Level 3：

01 - LC-0108 - Convert Sorted Array to Binary Search Tree
02 - LC-1008 - Construct Binary Search Tree from Preorder Traversal
03 - LC-0450 - Delete Node in a BST

教学重点：

108：
从有序数组中间选择 Root，
递归构建平衡 BST。

1008：
根据 Preorder 和 BST 性质构造树。

可以使用 Value Bounds，
或者根据 BST 有序性质递归划分。

450：
BST 删除的三种情况：

1. 叶节点
2. 只有一个孩子
3. 有两个孩子

重点解释：
两个孩子时可以使用 Inorder Successor
或者 Inorder Predecessor。

必须确保删除后 BST 不变量仍成立。

LC-450 是值得练习的 BST 指针修改题。

--------------------------------------------------

Level 2：
03 - Inorder Iterator 与惰性遍历

Level 3：

01 - LC-0173 - Binary Search Tree Iterator

教学重点：

Iterative Inorder Traversal。

使用 Stack 保存通往下一个最小节点的路径。

实现：

next()
hasNext()

推荐 Lazy Inorder，
不要直接把整棵树全部遍历到数组中，
否则失去此题设计上的主要教学价值。

重点理解：
为什么栈顶是下一个应返回的节点。

典型空间 O(h)，
next 摊还 O(1)。

==================================================
LEVEL 1
05 - 树构造、序列化与结构修改
==================================================

核心：

Tree Reconstruction
Index Mapping
Serialization
Deserialization
Pointer Rewiring

Level 2：
01 - 根据遍历序列重建树

Level 3：

01 - LC-0105 - Construct Binary Tree from Preorder and Inorder Traversal
02 - LC-0106 - Construct Binary Tree from Inorder and Postorder Traversal

教学重点：

105：
Preorder 第一个节点是 Root。
在 Inorder 中定位 Root。
其左侧属于左子树，右侧属于右子树。

推荐：
Hash Map + Index Ranges

在题目的唯一节点值约束下做到 O(n)。

106：
Postorder 最后一个节点是 Root。
同样利用 Inorder 划分左右子树。

重点对比：
Preorder 与 Postorder 的 Root 位置差异。

两道题复用相同的树构造思想，
不应被当成完全独立的算法。

--------------------------------------------------

Level 2：
02 - 序列化、反序列化与有效性验证

Level 3：

01 - LC-0297 - Serialize and Deserialize Binary Tree
02 - LC-0331 - Verify Preorder Serialization of a Binary Tree

教学重点：

297：
DFS Preorder 或 BFS Level Order 均可。

必须保留 Null Markers，
否则无法唯一恢复一般二叉树结构。

重点解释：
为什么只保存节点值是不够的。

331：
验证 Preorder Serialization。

可以使用 Slot Counting（槽位计数）：
- 初始一个槽位
- 每读取一个节点占用一个槽位
- 非空节点产生两个新槽位
- 空节点不产生新槽位

必须解释：
为什么槽位不能在未读完时不足，
为什么最终必须恰好用完。

不要强行把 LC-331 解释成普通树递归构造题。

--------------------------------------------------

Level 2：
03 - 原地展开与树指针重连

Level 3：

01 - LC-0114 - Flatten Binary Tree to Linked List

教学重点：

将树按 Preorder 顺序原地展开。

要求：
- right 指向下一个节点
- left 变为 None
- 不丢失原来的右子树

可以使用 Reverse Preorder DFS，
或 Iterative Pointer Rewiring。

优先选择清楚、可靠、便于证明的方案。

解释：
Tree Traversal 与 In-place Mutation 的关系。

==================================================
LEVEL 1
06 - BFS 层序遍历、视图与多叉树
==================================================

核心：

Queue BFS
Level Processing
Tree Views
Node Coordinates
N-ary Tree

Level 2：
01 - 标准层序与每层结果

Level 3：

01 - LC-0102 - Binary Tree Level Order Traversal
02 - LC-0103 - Binary Tree Zigzag Level Order Traversal
03 - LC-0199 - Binary Tree Right Side View

教学重点：

102：
标准 BFS Queue。
每轮通过 len(queue) 确定当前层节点数量。

103：
在 Level Order 基础上，
交替改变每一层结果的方向。

199：
每层只取最右侧可见节点。

必须区分：
BFS 按层遍历
和 DFS 递归遍历。

重点理解 Queue 的 FIFO 特性。

--------------------------------------------------

Level 2：
02 - 带坐标的层序遍历

Level 3：

01 - LC-0314 - Binary Tree Vertical Order Traversal

教学重点：

使用列坐标：
root column = 0
left -> column - 1
right -> column + 1

按列组织节点。

必须正确处理：
同列、同行节点的顺序。

LC-314 与 LC-987 Vertical Order Traversal
虽然相关，但排序规则不同。

不要直接混淆它们。

本题可能是 Premium，保留全部旧资料。

--------------------------------------------------

Level 2：
03 - N-ary Tree 层序遍历

Level 3：

01 - LC-0429 - N-ary Tree Level Order Traversal

教学重点：

与 Binary Tree BFS 的核心相同。

不同点：
每个节点可能有任意数量的 children。

重点展示如何复用原本的 BFS 模板。

--------------------------------------------------

Level 2：
04 - 同层 Next Pointer 连接

Level 3：

01 - LC-0116 - Populating Next Right Pointers in Each Node

教学重点：

Perfect Binary Tree。

使用 BFS 可以逐层连接 next 指针。

也可以利用已有 next 指针和完美二叉树结构，
实现 O(1) 额外空间。

必须说明两种方法的空间复杂度不同。

不能将 BFS Queue 版本声称为 O(1) 空间。

==================================================
LEVEL 1
07 - LCA、子树关系与树图转换
==================================================

核心：

Lowest Common Ancestor
Subtree Matching
Parent Pointers
Tree to Graph
Distance Search

Level 2：
01 - Lowest Common Ancestor

Level 3：

01 - LC-0236 - Lowest Common Ancestor of a Binary Tree
02 - LC-1650 - Lowest Common Ancestor of a Binary Tree III

教学重点：

236：
普通 Binary Tree 不具有 BST 的有序搜索性质。

使用 DFS：
- 当前节点为空 -> None
- 当前节点是 p 或 q -> 当前节点
- 左右子树分别返回候选
- 两侧都有结果 -> 当前节点为 LCA

注意题目对 p、q 存在性的保证。

1650：
节点带 parent 指针。

可以利用类似 Linked List Intersection 的
双指针换头思想寻找共同祖先。

说明：
它不是普通 LC-236 的相同实现。

也可以讨论 Ancestor Set 方法。

--------------------------------------------------

Level 2：
02 - 子树结构匹配

Level 3：

01 - LC-0572 - Subtree of Another Tree

教学重点：

复用 LC-100 Same Tree。

对主树的每个候选节点，
判断以它为 Root 的子树是否和目标树相同。

重点说明：

Same Tree 和 Subtree of Another Tree
的区别。

讨论普通朴素方案的复杂度，
不要无条件声称 O(n)。

--------------------------------------------------

Level 2：
03 - Tree to Graph 与距离搜索

Level 3：

01 - LC-0863 - All Nodes Distance K in Binary Tree

教学重点：

原始 Tree 通常只有指向孩子的指针。

为了从任意目标节点向：
- Left
- Right
- Parent

三个方向搜索，
需要构建 Parent Map 或使用其他等价方法。

随后使用 BFS 搜索距离恰好为 K 的节点。

重点理解：
Tree 可以视为一种特殊 Graph。

必须维护 visited，
避免沿 Parent / Child 关系反复访问节点。

==================================================
LEVEL 1
08 - 低优先级与特殊题型存档
==================================================

保留现有学习成果，但不强迫将其视为核心必刷。

Level 2：
01 - 特殊子树性质与叶节点统计

Level 3：

01 - LC-0250 - Count Univalue Subtrees
02 - LC-0404 - Sum of Left Leaves

教学说明：

250：
Postorder DFS。
判断当前子树是否所有节点具有相同值。
可以复用 Bottom-up Return Value 思想。

404：
DFS + Left Child Information。
对所有左叶节点求和。

两题能够练习递归信息传递，
但不需要单独记忆复杂的新模板。

标记 P2。

不得删除任何已有代码或资料。

==================================================
四、现有 NC 题目正式化
==================================================

当前存在 NC 专用来源题目：

NC - Kth Smallest Integer in BST
NC - Valid Binary Search Tree
NC - Construct Binary Tree from Preorder and Inorder Traversal
NC - Serialize and Deserialize Binary Tree
NC - Binary Tree Maximum Path Sum
NC - Count Good Nodes in Binary Tree
NC - Diameter of Binary Tree
NC - Subtree of Another Tree
NC - Lowest Common Ancestor in Binary Search Tree
NC - Binary Tree Right Side View

对应正式 LC 编号：

LC-0230
LC-0098
LC-0105
LC-0297
LC-0124
LC-1448
LC-0543
LC-0572
LC-0235
LC-0199

请逐一验证题面与代码。

若当前专题中尚无正式 LC 目录：
- 创建正式 LC Level 3。
- 将 NC 全部原始文件放入 _neetcode/。
- 使用现有题目生成工具补齐标准 LC 文件。
- 保留 NC 原有实现。

当前还存在以下 NC / LC 重复：

NC - Balanced Binary Tree -> LC-0110
NC - Invert Binary Tree -> LC-0226
NC - Maximum Depth of Binary Tree -> LC-0104
NC - Same Binary Tree -> LC-0100
NC - Binary Tree Level Order Traversal -> LC-0102

这五组必须合并到同一个正式 LC Level 3，
原始 NC 文件完整保存在 _neetcode/。

每道题最多占据一个正式 Level 3 位置。

但必须保留所有来源版本。

禁止以一个版本覆盖另一个版本的 solution.py。

如果 NC 与 LC 解法不同，
在对应 README 中简单说明差异。

==================================================
五、本次明确新增的 9 道题目
==================================================

第一轮建议新增：

LC-0437 - Path Sum III
LC-0114 - Flatten Binary Tree to Linked List
LC-0173 - Binary Search Tree Iterator
LC-0450 - Delete Node in a BST
LC-0337 - House Robber III
LC-0113 - Path Sum II
LC-0103 - Binary Tree Zigzag Level Order Traversal
LC-0700 - Search in a Binary Search Tree
LC-0129 - Sum Root to Leaf Numbers

先检查是否已存在于当前目录或其他专题。

对真正缺失的题目，
使用仓库原有的 LeetCode 题目生成能力创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据 LeetCode 题号自动生成题目资料的能力，
请直接复用原有工作流。

注意：

- 不能用空文件凑数。
- 不能伪造题面。
- 不能把错误题号的 metadata 复制给新题。
- 不允许覆盖已有 solution.py。
- 新题应采用清晰、标准、易复述的 Python 解法。
- 解法应与所属 Pattern 一致。

对于题目多解法的情况，
优先提供一份主推荐实现，
其他方法通过简短笔记对比即可。

不要为了完整性而给每题生成大量重复代码。

==================================================
六、Claude Code 第二轮独立审核
==================================================

上面的清单是 ChatGPT 的第一轮筛选。

请你进行独立的第二轮审核。

目标不是单纯增加题目，
而是发现当前学习体系中是否存在重要知识缺口。

参考：

- NeetCode 150
- NeetCode 250
- Blind 75
- Grind 75 / Grind 169
- LeetCode Top Interview 150
- 其他可靠的 Tree 面试题单

如果具备网络访问，请核对：
官方题号、名称、难度、约束与常见解法。

不能编造公司内部面试出现频率。

必须检查下列 Pattern 的覆盖情况：

1. Preorder / Inorder / Postorder
2. Iterative DFS
3. BFS Level Order
4. Tree Height
5. Diameter
6. Bottom-up Aggregation
7. Tree DP
8. Root-to-Leaf Paths
9. Backtracking
10. Prefix Sum on Trees
11. BST Range Validation
12. BST Search / Insert / Delete
13. BST Inorder Order Statistics
14. BST Iterator
15. LCA for BST
16. LCA for General Binary Tree
17. Parent Pointer LCA
18. Tree Construction
19. Serialization / Deserialization
20. Subtree Matching
21. Tree Pointer Rewiring
22. Tree as Graph
23. N-ary Tree BFS
24. Node Coordinate Traversal

额外审核候选：

LC-0701 - Insert into a Binary Search Tree
LC-0617 - Merge Two Binary Trees
LC-0938 - Range Sum of BST
LC-0662 - Maximum Width of Binary Tree
LC-0117 - Populating Next Right Pointers in Each Node II
LC-0987 - Vertical Order Traversal of a Binary Tree
LC-0669 - Trim a Binary Search Tree
LC-0530 - Minimum Absolute Difference in BST
LC-0951 - Flip Equivalent Binary Trees
LC-1026 - Maximum Difference Between Node and Ancestor

这些只是候选，不需要全部加入。

允许独立新增最多 5 道。

新增必须同时满足：

1. 具有明确的面试代表性。
2. 具有可迁移的算法思想。
3. 补充已有知识的真实缺口。
4. 不属于高度重复的基础练习。
5. 可以明确放入某个 Pattern。
6. 不会显著增加不必要的记忆负担。

特别注意：

- LC-701 与 LC-700 属于同一 BST 基础家族。
- LC-117 是 LC-116 的重要变体，但不必强制新增。
- LC-987 与 LC-314 相关，排序规则不同。
- LC-530 可以复用 BST Inorder。
- LC-617 是基础递归练习，与已有题部分重复。

如果一个候选只是相同算法的简单重复，
可以不添加。

如果发现大于 5 道真正有价值的题，
只新增最重要的 5 道，
其余放进 README 的 Future Candidates。

允许在具有充分教学价值时，
增加新的 Level 1 或 Level 2。

但不要为了单道题制造大量分类。

==================================================
七、现有理论资料与工具整理
==================================================

当前存在：

docs (资料)/
  NeetCode 题单顺序.md
  TODO explanation.md

tutorials (教程)/
  readme.md
  TreeNode.py
  Tutorial-001-BST-DFS-Recursive.py
  Tutorial-002-BST-DFS-Iterative-Using-Stack.py
  Tutorial-003-BST-Inorder-Preorder-Postorder-Traversal-Use-Cases.py
  Tutorial-004-BST-BFS-Iterative.py

utils/
  show_tree.py
  TreeNode.py

建议将纯理论资源统一放入：

_resources/
  docs/
  tutorials/

但是不能盲目移动 utils/。

操作前必须：

1. 检查教程中的 import。
2. 检查现有 solution.py 的 import。
3. 检查是否存在脚本调用 show_tree.py。
4. 检查两个 TreeNode.py 是否相同。
5. 检查当前相对路径依赖。
6. 检查是否存在 Symbolic Links。

如果移动教程会破坏其运行环境：
允许保留 tutorials 原来的位置，
或者在本专题内部安全修复引用。

不能直接覆盖两个不同的 TreeNode.py。

对于 utils/：
优先保留当前目录位置，
除非确认移动不会破坏任何依赖。

不允许修改其他算法专题中的 TreeNode 定义。

不得删除教程中已经写好的解释和代码。

_resources 是学习资料目录，
不参与 Level 1 的数字编号。

==================================================
八、文件保护与 Git 安全
==================================================

当前 Git 工作区存在大量未提交修改与未跟踪文件。

本任务必须严格保护用户已有成果。

执行前：

1. pwd
2. tree 扫描
3. git status --short
4. 递归记录当前目录所有文件
5. 记录原始文件相对路径
6. 记录文件大小与 SHA-256
7. 识别 Symbolic Links
8. 检查目标路径冲突
9. 创建旧路径到新路径的迁移映射
10. 检查现有 Python 代码中的引用关系

特别保护：

LC-0094：
note.md

LC-0250：
note.md

LC-0116：
asset-0116 开头的原始 Markdown 笔记

LC-0429：
N-ary Tree Level Order 的原始 Markdown 笔记

NC - Binary Tree Right Side View：
note.md

以及全部：
- solution.py
- metadata.json
- problem.pdf
- problem_dark.pdf
- jpg / jpeg / png
- md
- 其他自定义文件

禁止：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖已有文件
删除未跟踪文件
覆盖用户代码
覆盖已有笔记
随意删除理论资料

本次不自动：

git add
git commit
git push

只允许在当前：

07-trees (树)

目录内进行写入、移动和安全删除空目录操作。

可以只读扫描整个 leetcode-practice 仓库，
用于确认跨专题重复题目。

发生同名冲突时：

- 相同文件可以进行可追溯的去重整理。
- 不同内容必须全部保留。
- 需要时创建 _conflicts/。
- 在最终报告中列明所有冲突。
- 不得静默丢弃任何用户文件。

如果生成工具会修改仓库其他目录或公共配置，
必须先寻找不产生越界写入的执行方式。
无法安全限制时不要执行该生成步骤，
并在最终报告中记录。

保证尽可能 Idempotent（幂等）：
重复执行不得生成重复题目、叠加编号或覆盖文件。

==================================================
九、跨专题引用
==================================================

允许只读检查整个仓库的其他算法专题。

重点检查：

LC-0109 - Convert Sorted List to Binary Search Tree
可能已经存在于 Linked List。

LC-0270 - Closest Binary Search Tree Value
可能存在于 Binary Search。

LC-0863 - All Nodes Distance K in Binary Tree
可能被 Graph / BFS 专题引用。

LC-0337 - House Robber III
可能属于 DP 专题。

LC-0437 - Path Sum III
与 Prefix Sum 专题具有联系。

LC-0165? 不需要凭猜测新增题目。

不要为了跨专题关系而创建冗余实体目录。

如果其他专题已有题目：
- 不修改外部文件。
- 保留当前专题已存在的完整学习成果。
- 使用 README 相对路径建立引用。
- 标记 Primary Pattern 和 Secondary Pattern。

不要因为跨专题标签而将 Tree 专题拆散。

==================================================
十、README 与学习文档
==================================================

必须生成：

A. Trees 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 生成必要的短 README.md

根目录 README：

1. Trees 知识地图
2. 8 个 Level 1 分类
3. 各个 Level 2 的目标
4. 所有题目及真实相对路径
5. P0 / P1 / P2 优先级
6. Tree DFS 核心模板
7. Tree BFS 核心模板
8. BST 核心模板
9. Bottom-up Tree DP 核心模板
10. LCA 核心模板
11. Construction / Serialization 模板
12. 时间与空间复杂度
13. 跨专题索引
14. 第二轮独立审核结果
15. 最终推荐刷题顺序

特别设计一个：

Tree Pattern Recognition Guide

按照以下问题帮助识别题型：

Q1：
是否需要按层处理节点？
-> BFS

Q2：
是否只需要判断左右子树的性质？
-> Recursive DFS

Q3：
是否需要先知道孩子的信息才能计算父节点？
-> Postorder / Bottom-up DFS

Q4：
是否需要向孩子传递当前路径信息？
-> Top-down DFS

Q5：
是否利用 BST 的有序性质？
-> BST Search / Range Constraints / Inorder

Q6：
是否需要返回多个状态？
-> Tree DP

Q7：
是否需要找到两个节点的共同祖先？
-> LCA

Q8：
是否需要构造或恢复整棵树？
-> Tree Reconstruction / Serialization

每个 Level 1 README：

- 核心定义
- 1–3 个决定性观察
- Loop / Recursive Invariant
- DFS 返回值定义
- 递归状态及 Base Case
- 简短正确性证明
- Python 核心模板
- 常见错误
- 代表题目
- 与相邻 Pattern 的区别

特别要求：

必须解释 Top-down DFS 与 Bottom-up DFS 的区别。

不能把“在代码里先访问左孩子还是右孩子”
当成区分两者的唯一标准。

应该根据：
信息从父节点向孩子传递，
还是从孩子向父节点汇总，
来区分其主要思路。

还必须解释：

- DFS 返回值与 Global Answer 的区别
- 为什么 Tree DP 可以返回 tuple
- 为什么 LCA 的递归结果代表候选祖先
- 为什么 Prefix Sum on Tree 需要回溯计数
- 为什么 BST 的有序性不能用于普通 Binary Tree
- 为什么 BFS 特别适合逐层处理
- 为什么不同树题的空间复杂度可能依赖树高 h

文档语言：

中文主导 + 英文技术术语。

例如：

Top-down DFS（自顶向下深度优先搜索）
Bottom-up DFS（自底向上深度优先搜索）
Recursive Invariant（递归不变量）
Subtree Aggregation（子树信息汇总）
Tree DP（树形动态规划）
Lowest Common Ancestor（最近公共祖先）

理论讲解优先采用：

1. 决定性观察
2. 状态或返回值定义
3. 递归不变量
4. 简短证明
5. Python 模板
6. 代表题目

避免大量空泛理论。

==================================================
十一、P0 / P1 / P2 学习优先级
==================================================

P0：
必须熟练掌握的核心面试题与基础模板。

P1：
重要进阶、可迁移变体。

P2：
低优先级、特殊技巧或存档。

以下优先标记 P0：

LC-0144 - Binary Tree Preorder Traversal
LC-0094 - Binary Tree Inorder Traversal
LC-0145 - Binary Tree Postorder Traversal
LC-0104 - Maximum Depth of Binary Tree
LC-0226 - Invert Binary Tree
LC-0100 - Same Tree
LC-0110 - Balanced Binary Tree
LC-0543 - Diameter of Binary Tree
LC-0124 - Binary Tree Maximum Path Sum
LC-0102 - Binary Tree Level Order Traversal
LC-0199 - Binary Tree Right Side View
LC-1448 - Count Good Nodes in Binary Tree
LC-0098 - Validate Binary Search Tree
LC-0230 - Kth Smallest Element in a BST
LC-0235 - Lowest Common Ancestor of a Binary Search Tree
LC-0236 - Lowest Common Ancestor of a Binary Tree
LC-0105 - Construct Binary Tree from Preorder and Inorder Traversal
LC-0297 - Serialize and Deserialize Binary Tree
LC-0572 - Subtree of Another Tree
LC-0437 - Path Sum III

说明：
前三道遍历题是基础技能，
不代表需要分别背三套复杂代码。

以下优先标记 P1：

LC-0101
LC-0112
LC-0113
LC-0129
LC-0337
LC-0700
LC-0108
LC-0450
LC-0173
LC-0106
LC-0114
LC-0103
LC-0863
LC-0165? 不存在此指定题，请忽略此行。
LC-1650
LC-0116

以下优先考虑 P2：

LC-0111
LC-0222
LC-0250
LC-0404
LC-0257
LC-1008
LC-0331
LC-0314
LC-0429

可以根据实际教学价值调整，
但必须说明理由。

不能把所有题目都标记为 P0。

README 必须分别给出：

1. P0 最小核心学习路线
2. P0 + P1 标准面试准备路线
3. P2 拓展与存档路线

P0 列表也应区分：
- 必须理解的基本遍历能力
- 必须独立完成的代表算法题

不要建议我把每一道树题当成独立算法背下来。

==================================================
十二、题目数量与最终验收
==================================================

根据当前 tree 初步统计：

当前约 40 个题目来源文件夹。

其中 5 组 NC / LC 重复。

因此约 35 道不同题目。

第一轮明确新增：
9 道。

所以第一轮目标约为：
44 道不同题目。

预期 Level 1 分布：

01：8 道
02：5 道
03：6 道
04：8 道
05：5 道
06：6 道
07：4 道
08：2 道

合计 44 道。

这不包括 _neetcode 的重复来源目录。

第二轮如果增加有价值的新题，
总数量可以合理增加。

如果跨专题已有某题，并选择只建立索引，
最终实体目录数量可以低于 44。

必须以实际文件审计结果为准。

绝对不能为了凑数量而生成假题目或空文件。

最终必须检查：

1. 所有旧题目有明确的新路径。
2. 所有旧文件内容完整保留。
3. NC / LC 的归档正确。
4. 题号和英文题名正确。
5. 题目与所属 Pattern 一致。
6. Level 1 编号连续。
7. Level 2 编号连续。
8. Level 3 编号连续。
9. 每个新题包含标准文件。
10. README 引用路径真实存在。
11. tutorials 和 utils 没有被破坏。
12. 原始 note.md、图片、其他附件没有丢失。
13. 不存在无意义的重复题目。
14. 旧文件哈希一致。
15. 当前 Trees 目录以外没有被修改。
16. Git 原有未提交内容没有被覆盖。

==================================================
十三、执行顺序
==================================================

请直接执行以下任务：

1. 扫描当前 Trees 目录。
2. 检查 Git 状态。
3. 记录全部原始文件与哈希。
4. 检查 utils、tutorials 的依赖。
5. 验证原有 NC / LC 题目。
6. 只读检查其他专题的重复题。
7. 建立完整迁移映射。
8. 创建 8 个 Level 1。
9. 创建对应 Level 2。
10. 迁移现有题目。
11. 归档 NC 重复来源。
12. 将 NC-only 题整理为正式 LC 目录。
13. 创建明确新增的 9 道题。
14. 检查旧题缺失文件。
15. 安全整理理论资料。
16. 进行第二轮独立题目审核。
17. 补充真正重要的遗漏题。
18. 重新校验所有目录编号。
19. 生成根目录与各分类 README。
20. 验证递归模板和 Python 代码。
21. 检查全部原始文件的哈希。
22. 检查跨专题链接。
23. 清理确认已经空置的旧目录。
24. 运行最终 tree。
25. 检查最终 Git 状态。
26. 输出完整验收报告。

最终报告必须包括：

- 完整最终 tree
- Level 1 / Level 2 分类
- 已有题目的迁移位置
- NC / LC 正式化情况
- ChatGPT 推荐新增的 9 道题
- Claude Code 第二轮新增的题
- 未来值得考虑但未增加的候选题
- P0 / P1 / P2 数量
- 原始文件保留校验结果
- tutorials / utils 完整性
- 新增题目的文件完整性
- Git 变更摘要
- 未完成任务及原因
- 最终推荐学习顺序

不要只生成计划或告诉我应该怎么做。

请在以上安全约束下直接执行完整目录重构。
PROMPT
)"
