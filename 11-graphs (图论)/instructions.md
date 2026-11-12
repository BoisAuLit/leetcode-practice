
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/11-graphs (图论)' && claude "$(cat <<'PROMPT'
请直接执行当前 Graphs（图论）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试和 Online Assessment（OA）。

这次任务比普通专题复杂得多。

当前 Graphs 目录已经包含：
- 165 个目录
- 523 个文件
- 7 个原有学习阶段
- 图论基础手册与大量算法模板
- Dijkstra 已经完成的一轮多级目录重构
- 多套不同算法求解同一道题的实现
- MST、Union-Find、DFS/BFS、Topological Sort 等大量交叉知识

请在保护全部学习成果的前提下，建立清晰、可长期复习、低记忆负担的图论知识体系。

不要只输出规划。请实际执行文件操作。

==================================================
一、核心设计目标
==================================================

请按照以下优先级设计目录：

1. Learning Dependencies（学习依赖）
2. Interview Relevance（面试价值）
3. Transferability（算法迁移性）
4. Pattern Recognition（题型识别）
5. Correctness Invariants（正确性不变量）
6. Minimal Memorization（最小记忆负担）

不要追求题目总数最大化。

图论算法种类很多，但我希望优先精通：

- Graph Representation
- DFS
- BFS
- Multi-source BFS
- Union-Find / DSU
- Topological Sort / Kahn
- Dijkstra
- Bellman-Ford
- Kruskal
- Prim 的基本原理

以下内容可以根据面试价值决定学习深度：

- 0-1 BFS
- Minimax / Maximin Paths
- Three-color DFS
- DAG DP
- Bipartite Graph
- Eulerian Path
- Tarjan Bridges
- Rerooting DP
- Persistent DSU
- Floyd-Warshall

尤其注意：

我已经决定不再系统投入精力学习 Floyd-Warshall。
请保留现有代码和资料，但标记为 P2 参考知识。

不要把所有图论算法都设置为必须掌握。

==================================================
二、Level 1 -> Level N 目录规范
==================================================

当前根目录：

11-graphs (图论)

优先采用：

Level 1：图论算法家族
Level 2：具体 Pattern
Level 3：具体 LeetCode 题目

如果某个算法家族需要进一步细分，
可以使用 Level 4 或 Level 5。

尤其是已经重构过的 Dijkstra 子目录，
允许保留原有的较深层级。

规则：

- 所有同级正式学习目录必须连续编号。
- 编号使用 01、02、03 等前缀。
- 每个父目录下独立重新编号。
- 编号代表推荐学习顺序，不代表 LC 题号顺序。
- 同类基础题排在高阶变体之前。
- 高频代表题优先于低迁移性题。
- 禁止为每道题都创造一个独立的算法类别。
- 资源目录不参与算法层级编号。

正式题目文件夹格式：

01 - LC-0200 - Number of Islands
02 - LC-0695 - Max Area of Island

保留官方英文题名。

不要因为文件夹重新编号而修改题目内容。

允许使用 _resources、_neetcode、_alternative_solutions、
_conflicts、_audit 等非学习目录。

==================================================
三、总体 Level 1 分类
==================================================

第一轮优先建立以下 8 个 Level 1：

01 - 图建模与基础遍历 (Graph Modeling)
02 - DFS BFS 与无权最短路 (Unweighted Graph Search)
03 - Union-Find 与连通性 (Disjoint Set Union)
04 - Topological Sort 与 DAG (Directed Acyclic Graph)
05 - 带权最短路 (Weighted Shortest Paths)
06 - 最小生成树与离线阈值连通 (MST and Offline Connectivity)
07 - 特殊图结构与路径 (Special Graph Algorithms)
08 - 函数图与树上图论 (Functional Graph and Tree Algorithms)

请优先保留原有阶段式学习逻辑。

允许基于实际内容调整 Level 2，
但不要在没有充分理由时颠覆上述 Level 1 结构。

==================================================
四、Level 1 详细题目安排
==================================================

以下每个 Level 2 中的 LC 编号按推荐顺序排列。

请自动读取对应的官方题名，
为最末级题目目录生成连续编号。

如果目录已存在，优先安全迁移。

--------------------------------------------------
LEVEL 1
01 - 图建模与基础遍历 (Graph Modeling)
--------------------------------------------------

Level 2：
01 - 显式图建模、可达性与遍历

题目顺序：

LC-1971 - Find if Path Exists in Graph
LC-0841 - Keys and Rooms
LC-0133 - Clone Graph
LC-1466 - Reorder Routes to Make All Paths Lead to the City Zero
LC-0797 - All Paths From Source to Target

教学重点：

1971：
最基础的 Reachability。
从 Edge List 构建 Adjacency List。
使用 DFS/BFS 判断能否到达目标。

841：
Graph Traversal + Visited。
房间钥匙对应有向边。

133：
Clone Graph。
Hash Map：original_node -> cloned_node。
解释为什么必须先登记已克隆节点再遍历邻居。

1466：
利用有向边和反向可遍历关系建模。
沿无向树结构遍历，统计需要调整的边。

797：
枚举 DAG 中所有从源点到终点的路径。
DFS + Path Backtracking。
这是 All Paths Enumeration，不是最短路径。

--------------------------------------------------

Level 2：
02 - In-degree Out-degree 与图关系建模

题目顺序：

LC-0997 - Find the Town Judge
LC-0277 - Find the Celebrity

教学重点：

997：
入度、出度。
理解节点的全局信任关系。

277：
Greedy Candidate Elimination + Verification。
虽然可从入出度角度理解，
但标准解法不必构建完整图。

标记 P2。

必须区分：
图的邻接关系
与节点的 Degree Summary。

==================================================
LEVEL 1
02 - DFS BFS 与无权最短路
==================================================

这是核心基础阶段。

必须解释：

DFS 与 BFS 都可以求可达性。

但在无权图或所有边同权的图中，
BFS 才能通过层数保证最少边数的路径。

普通 DFS 不直接保证最短路径。

--------------------------------------------------

Level 2：
01 - Flood Fill 与 Connected Components

题目顺序：

LC-0200 - Number of Islands
LC-0695 - Max Area of Island
LC-0547 - Number of Provinces

教学重点：

- DFS/BFS 统计连通分量
- Grid -> Implicit Graph
- Visited 的作用
- 同一个连通块只处理一次
- 连通块数量与连通块大小的区别

LC-200 是签名题。

LC-547 可以对照 Union-Find 解法，
但本组优先 DFS/BFS。

--------------------------------------------------

Level 2：
02 - Boundary-first 与 Reverse Reachability

题目顺序：

LC-0130 - Surrounded Regions
LC-0417 - Pacific Atlantic Water Flow
LC-1020 - Number of Enclaves
LC-1254 - Number of Closed Islands

教学重点：

从边界反向搜索。

必须解释：

为什么直接寻找内部封闭区域，
有时不如从外部边界开始搜索？

LC-417：
从两个海洋边界反向搜索可到达区域。

LC-130、1020、1254：
学习边界相连、封闭区域的区别。

不要为这些题分别记忆四套 DFS 模板。

--------------------------------------------------

Level 2：
03 - Single-source BFS 最少步数

题目顺序：

LC-1091 - Shortest Path in Binary Matrix
LC-1926 - Nearest Exit from Entrance in Maze
LC-1197 - Minimum Knight Moves

教学重点：

BFS Layer = Shortest Number of Steps。

维护：
queue
visited
distance / level

区分：
- Queue 中存储的状态
- BFS 层数
- 进入队列时标记 visited
- 出队时才处理的特殊情况

LC-1197 属于状态空间搜索，
可标 P1/P2。

--------------------------------------------------

Level 2：
04 - Multi-source BFS 与扩散

题目顺序：

LC-0994 - Rotting Oranges
LC-0542 - 01 Matrix
LC-0286 - Walls and Gates
LC-1162 - As Far from Land as Possible
LC-0934 - Shortest Bridge

教学重点：

所有有效源点一起入队。

为什么这等价于从一个虚拟源点
向所有真实源点连接零成本边？

为什么一次 BFS 可以同时计算
到最近源点的距离？

LC-934：
需要先标记一个岛屿，
然后利用 BFS 扩展寻找另一个岛屿。

必须说明它是 DFS/BFS 联合建模，
并非简单地将所有陆地同时视为源点。

--------------------------------------------------

Level 2：
05 - Repeated BFS 与多起点距离汇总

题目顺序：

LC-0317 - Shortest Distance from All Buildings

教学重点：

分别从多个 Building 执行 BFS，
累计可达空地的距离与可达建筑数量。

特别注意：

Repeated BFS From Multiple Sources
与 Multi-source BFS 是两种不同模式。

前者：
需要计算每个目标位置到所有源点的距离之和。

后者：
常用于寻找最近源点距离。

不能混淆。

--------------------------------------------------

Level 2：
06 - Implicit State Graph 与状态 BFS

题目顺序：

LC-0752 - Open the Lock
LC-0127 - Word Ladder
LC-0433 - Minimum Genetic Mutation
LC-0909 - Snakes and Ladders
LC-0773 - Sliding Puzzle

新增：

LC-0815 - Bus Routes
LC-1293 - Shortest Path in a Grid with Obstacles Elimination

教学重点：

一个 State 可以视为一个 Graph Node。

752：
锁的每一种组合就是节点。
一次拨轮就是一条边。

127：
单词是节点。
一次合法字符变换就是一条边。

815：
站点与路线形成隐式关系。
可以将公交线路作为 BFS 状态，
也可以使用站点与线路之间的映射。

必须避免重复展开同一条 Route。

1293：
状态不能只有 (row, col)。

还需要记录剩余可消除的障碍数量。

例如：

(row, col, remaining_k)

必须解释：
为什么到达同一个格子，
但剩余资源不同，
不能直接认为是同一个状态？

可以介绍 Dominance Pruning，
但必须保证剪枝正确。

其他两道作为该组 P1 进阶题。

--------------------------------------------------

Level 2：
07 - 图遍历中的附加信息传递

题目顺序：

LC-0399 - Evaluate Division
LC-1376 - Time Needed to Inform All Employees
LC-2101 - Detonate the Maximum Bombs

教学重点：

399：
边上带有乘法权重。
可以沿路径累乘进行查询。

注意：
这不是普通加法最短路径。

1376：
树形组织结构上的传播时间。

2101：
根据炸弹爆炸范围建立有向边，
从不同起点计算可到达节点数量。

重点理解：
图边如何由实际题目约束推导出来。

--------------------------------------------------

Level 2：
08 - Nested Structure DFS

题目顺序：

LC-0339 - Nested List Weight Sum
LC-0364 - Nested List Weight Sum II

教学重点：

嵌套结构遍历与深度信息。

这两题属于 DFS 的跨专题应用，
不是典型 Graph Connectivity。

优先标记 P2，保留旧资料即可。

==================================================
LEVEL 1
03 - Union-Find 与连通性
==================================================

核心：

Disjoint Set Union（并查集）

必须熟练理解：

parent
size / rank
find
union
component_count

建议使用：

Path Compression
Union by Size

重要不变量：

union(u,v) 返回 True
表示本次确实合并了两个原本不同的连通分量。

必须明确：

Union-Find 擅长动态合并和连通性查询。

但它不直接提供两点间的最短路径。

--------------------------------------------------

Level 2：
01 - 连通分量计数与有效树

题目顺序：

LC-0323 - Number of Connected Components in an Undirected Graph
LC-0261 - Graph Valid Tree
LC-1319 - Number of Operations to Make Network Connected
LC-2316 - Count Unreachable Pairs of Nodes in an Undirected Graph

教学重点：

为什么：

components = n - successful_unions

在初始化每个节点单独成块的情况下成立？

LC-261：
树必须连通且无环。

LC-2316：
从连通块 Size 计算跨块点对数量。

重点学习：
Union-Find 如何维护连通块数量与大小。

--------------------------------------------------

Level 2：
02 - Union-Find 判环与冗余边

题目顺序：

LC-0684 - Redundant Connection
LC-0685 - Redundant Connection II
LC-1559 - Detect Cycles in 2D Grid

教学重点：

684：
无向图中 union 失败表示当前边形成环。

685：
有向图问题，还涉及节点入度为 2。
不能简单照搬 LC-684 的逻辑。

1559：
Grid Cycle Detection。
可以使用 DFS + Parent 或 DSU。

本专题保留原有实现，
不强制记忆不同算法的全部版本。

--------------------------------------------------

Level 2：
03 - 等价关系、分组与连通块重组

题目顺序：

LC-0721 - Accounts Merge
LC-0990 - Satisfiability of Equality Equations
LC-1061 - Lexicographically Smallest Equivalent String
LC-1202 - Smallest String With Swaps

教学重点：

利用 DSU 将元素分为 Equivalence Classes。

721：
Email Identity -> Account Group。

990：
先合并相等关系，
再检查不等关系是否矛盾。

1061：
在每个等价类维护代表字符的选择规则。

1202：
相同连通块内可以交换位置，
对每组独立构造最优字符分配。

--------------------------------------------------

Level 2：
04 - 特殊 Graph Modeling + Union-Find

题目顺序：

LC-0947 - Most Stones Removed with Same Row or Column
LC-0827 - Making A Large Island
LC-0952 - Largest Component Size by Common Factor
LC-1627 - Graph Connectivity With Threshold

新增：

LC-0959 - Regions Cut By Slashes

教学重点：

947：
可以将 Row 和 Column 作为图节点。
解释为什么需要避免行列编号冲突。

827：
给岛屿编号、计算连通块大小，
再考虑连接不同岛屿。

952：
通过公共质因子构建连通关系。

1627：
通过因数与倍数关系进行合并。

959：
将一个网格单元拆成多个局部区域节点，
再通过 DSU 合并相邻区域。

主要学习：
现实对象 -> DSU Node 的建模过程。

LC-959 为 P1，
其他复杂建模题可根据实际价值标 P1/P2。

--------------------------------------------------

Level 2：
05 - Dynamic Connectivity 与按时间处理

题目顺序：

LC-0305 - Number of Islands II
LC-1101 - The Earliest Moment When Everyone Become Friends
LC-2092 - Find All People With Secret

教学重点：

305：
动态加陆地。
只合并新出现的有效相邻节点。

1101：
按时间排序事件，
逐渐合并连通分量。

2092：
按照会议时间进行分组。

同一时间内，
信息可以沿该时间的连通关系传播。

但不同时间组之间不能错误地保留
不应该永久存在的临时连通关系。

必须解释：
为什么需要分组处理、临时连通性
以及必要的 Reset 或等价 BFS 处理。

不能直接套普通永久合并 DSU。

--------------------------------------------------

Level 2：
06 - 多个并查集与边类型贪心

题目顺序：

LC-1579 - Remove Max Number of Edges to Keep Graph Fully Traversable

教学重点：

两个 DSU：
Alice
Bob

优先处理双方共用边，
再分别处理专属边。

这是 Dual DSU + Greedy。

虽然曾放在 MST 分类，
但不属于经典最小权生成树问题。

请迁入此分类，并完整保留所有原始资料。

==================================================
LEVEL 1
04 - Topological Sort 与 DAG
==================================================

核心：

Directed Graph
Cycle Detection
Kahn's Algorithm
In-degree
DAG DP

必须区分：

- 判断是否存在环
- 找到拓扑排序
- 按拓扑层数计算轮次
- 在 DAG 上进行 DP
- 三色 DFS 检测有向环

--------------------------------------------------

Level 2：
01 - Kahn 拓扑排序与依赖关系

题目顺序：

LC-0207 - Course Schedule
LC-0210 - Course Schedule II
LC-0269 - Alien Dictionary
LC-2115 - Find All Possible Recipes from Given Supplies
LC-0444 - Sequence Reconstruction

教学重点：

207：
检测有向环。
成功处理节点数等于 n，则可完成全部课程。

210：
输出实际拓扑序列。

269：
从相邻单词提取正确的先后关系。
注意 Prefix Invalid Case。

2115：
动态释放满足前置依赖的 Recipe。

444：
判断是否能唯一重建指定序列。
注意唯一性及题目输入约束。

核心模板：
Kahn + Queue + In-degree。

不能为每道题重新发明一套拓扑算法。

--------------------------------------------------

Level 2：
02 - 层数、学期与零入度

题目顺序：

LC-1136 - Parallel Courses
LC-1557 - Minimum Number of Vertices to Reach All Nodes

教学重点：

1136：
Kahn BFS 的层数代表所需学期数。

1557：
DAG 中所有入度为 0 的节点必须作为起点。

1557 不需要完整执行 Topological Sort。
它主要是 Degree 的简化应用。

--------------------------------------------------

Level 2：
03 - DAG DP 与祖先信息传播

题目顺序：

LC-0329 - Longest Increasing Path in a Matrix
LC-2050 - Parallel Courses III
LC-1857 - Largest Color Value in a Directed Graph
LC-1462 - Course Schedule IV
LC-1203 - Sort Items by Groups Respecting Dependencies

新增：

LC-2192 - All Ancestors of a Node in a Directed Acyclic Graph

教学重点：

329：
数值严格递增构成 DAG。

优先理解 DFS + Memoization，
再介绍 Kahn Topological Sort 方案。

2050：
DAG 上的最长依赖完成时间。
Topological DP。

1857：
对每个节点维护颜色计数状态。
需要处理有向环。

1462：
先修关系的传递性。
可以使用 DAG 上的信息传播等方法。

1203：
需要同时处理 Group 内部和 Group 之间的依赖。
属于高阶 Topological Sort。

2192：
在拓扑序下传播 Ancestor Sets。

必须解释：

为什么处理一个节点时，
所有前驱的祖先信息已经完成？

不要把 DAG DP
和普通 BFS 最短路径混淆。

LC-1203 标记 P2 进阶。

--------------------------------------------------

Level 2：
04 - Three-color DFS 有向图判环

题目顺序：

LC-0802 - Find Eventual Safe States
LC-1059 - All Paths from Source Lead to Destination

教学重点：

WHITE：未访问
GRAY：当前 DFS 路径上
BLACK：已处理

重要：

遇到 GRAY 节点表示当前 DFS 搜索路径存在回边，
从而发现有向环。

LC-1059：
还需要正确处理：
- 非目标终点
- 环
- 所有路径必须到达指定 destination

不能只检查是否可以找到某一条路径。

--------------------------------------------------

Level 2：
05 - 无向树剥叶与 Tree Centers

题目顺序：

LC-0310 - Minimum Height Trees

教学重点：

逐步删除度数为 1 的叶节点。
最后剩下一个或两个 Tree Centers。

虽然形式上类似 Kahn 的 Queue + Degree，
但它处理的是无向树剥叶。

不要误认为它是普通有向 DAG Topological Sort。

==================================================
LEVEL 1
05 - 带权最短路 (Weighted Shortest Paths)
==================================================

特别重要：

当前：

05-shortest-path (...)/dijkstra/

已经完成一次专门的目录重构。

其内部拥有五个分类：

01 - Dijkstra 标准加法最短路
02 - Dijkstra 非加法路径代价变体
03 - Dijkstra 最短路计数与结果组合
04 - Dijkstra 网格建图与特殊边权
05 - Dijkstra 状态扩展与时间约束

必须完整保留这五个内部分类、
排序、文件、README 和学习资料。

不要重新生成或覆盖整个 Dijkstra 专题。

优先通过移动整个子树的方式，
将其纳入新的 Level 1 结构。

--------------------------------------------------

Level 2：
01 - Dijkstra 核心与变体

将现有 dijkstra 子树纳入本分类。

保留全部原题，包括：

LC-0743
LC-1334
LC-2642
LC-2976
LC-1631
LC-1514
LC-0778
LC-2812
LC-1976
LC-3123
LC-2203
LC-1786
LC-2290
LC-1368
LC-0505
LC-0787
LC-1928
LC-2577

其中：

LC-1786
必须理解 Dijkstra + DFS/DP 路径计数。

LC-1976
需要维护最短路方案数。

LC-1514
最大概率路径与普通加法最短路不同。

LC-1631
Minimax Path。

LC-2812
Multi-source BFS + Maximin。

不要把这些写成完全相同的 Relaxation。

--------------------------------------------------

Level 2：
02 - Bellman-Ford 与有限边数最短路

现有：

LC-0787 - Cheapest Flights Within K Stops

教学重点：

Bellman-Ford Relaxation。

对于最多 k 次中转，
限制使用的边数为 k+1。

推荐 Snapshot / Previous Round Distances。

必须解释：
每一轮只读取上一轮结果，
为什么可以防止一轮中使用过多边。

普通 In-place Bellman-Ford 与 Snapshot 版本的区别。

不要把这两个实现的约束混淆。

虽然 LC-787 也有 Dijkstra State Expansion 解法，
但本专题优先推荐 Bellman-Ford + Snapshot。

--------------------------------------------------

Level 2：
03 - 0-1 BFS 与特殊边权

现有：

LC-1368
LC-2290
LC-3552

教学重点：

当边权只有 0 和 1 时，
可以使用 Deque：

weight=0 -> appendleft
weight=1 -> append

必须解释：
为什么 Deque 可以保持适当的距离处理顺序？

LC-3552：
Grid + Portal Teleportation。
重点避免重复展开同一类传送门。

注意：

LC-1368 和 LC-2290
已经在 Dijkstra 子树中存在。

这是有教学意义的不同算法实现。

必须保留两者。

可以通过算法变体存档和跨分类索引整理，
但不能丢掉 0-1 BFS 代码。

--------------------------------------------------

Level 2：
04 - Bottleneck / Minimax / Maximin

现有：

LC-1102 - Path With Maximum Minimum Value
LC-1631 - Path With Minimum Effort

并建立与以下题目的交叉索引：

LC-0778
LC-2812

教学重点：

Minimax：
最小化路径中最大的边代价。

Maximin：
最大化路径中最小的安全值。

不能混淆：

min(max(...))
max(min(...))

这些算法可以使用 Dijkstra-like Greedy，
也可能通过 DSU / Kruskal Process 解决。

不要将它们错误地当成普通加法最短路。

LC-1631 当前已在 Dijkstra 子目录中存在。
不同实现必须安全保存。

--------------------------------------------------

Level 2：
05 - All-pairs Shortest Path 参考资料

现有：

LC-1334
LC-2976

当前另有 Floyd-Warshall 实现。

请完整保留已有 Floyd 文件。

但是：

这是 P2 参考分类，
不是我当前准备长期记忆的核心算法。

我更希望优先使用重复运行标准 Dijkstra
来理解这些题目的最短路意义。

不要把 Floyd-Warshall
重新提升为必须系统学习的算法。

不要把旧模板或旧学习笔记删除。

==================================================
五、同题多算法的特殊处理规则
==================================================

目前发现至少六个重复 LC 编号：

0787
1334
1368
1631
2290
2976

这六个重复来源非常重要。

请先读取各版本 solution.py。

只有确认具体算法后才能确定归属。

一个题目可以有多个不同算法版本。

但是整个 Graphs 学习索引中，
应指定一个 Primary Learning Location。

其他实现标记为：

Alternative Algorithm / Reference Implementation。

优先处理方式：

A. 保留一个正式题目主目录。
B. 保留其他不同算法的全部原始文件。
C. 可以使用 _alternative_solutions/ 归档不同版本。
D. 在其他算法家族的 README 中建立引用。
E. 不需要为相同题目反复生成 PDF。

不过，对于已经完成深度整理的 Dijkstra 子树，
不要为了消除重复编号而破坏现有结构。

如果迁移其他版本会影响大量已整理的路径，
允许保留明确标记的 Algorithm Variant 目录。

但必须在 README 中列出：

LC ID
Primary Pattern
Primary Path
Alternative Pattern
Alternative Path
为什么保留两个版本

判断去重时，
必须依据文件实际内容与算法，
不能只依据 LeetCode 编号。

绝对不能把 Bellman-Ford、
Dijkstra、0-1 BFS、Floyd 的实现
错误地当成完全相同的重复文件删除。

==================================================
LEVEL 1
06 - 最小生成树与离线阈值连通
==================================================

本阶段的核心是：

Minimum Spanning Tree
Kruskal
Prim
Sorted Edge Processing
Threshold Connectivity

必须区分：

A. 真正要求一棵 MST 的问题
B. 只是利用 Kruskal 的边排序与 DSU 合并过程

--------------------------------------------------

Level 2：
01 - 最小生成树基础与建模

题目顺序：

LC-1584 - Min Cost to Connect All Points
LC-1135 - Connecting Cities With Minimum Cost
LC-1168 - Optimize Water Distribution in a Village

教学重点：

1584：
MST 教科书。

可以使用：
Kruskal + Union-Find
或
Prim。

应解释两者的核心差别。

在完全图或稠密图条件下，
数组版 Prim O(V^2) 可以是合理方案。

1135：
稀疏图 MST。
可以使用 Kruskal 或 Prim。

1168：
虚拟源点。
将建水井转化为连接虚拟节点的边。

最重要的思想：
建模成 MST，
而不是机械背诵每个解法。

--------------------------------------------------

Level 2：
02 - MST Edge Classification

题目顺序：

LC-1489 - Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

教学重点：

Critical Edge
Pseudo-critical Edge

可以通过强制排除或强制包含一条边，
再运行 Kruskal 判断 MST 代价。

这是高阶题，标记 P2。

--------------------------------------------------

Level 2：
03 - Kruskal Process 与离线阈值连通

题目顺序：

LC-1697 - Checking Existence of Edge Length Limited Paths
LC-1970 - Last Day Where You Can Still Cross
LC-2421 - Number of Good Paths
LC-1724 - Checking Existence of Edge Length Limited Paths II

教学重点：

1697：
先按边权排序，再按 Query Limit 排序。

只合并边权严格小于 Limit 的边。

离线处理多个连通性查询。

此题是重要的 Offline DSU 代表。

1970：
可以使用 Reverse Time + DSU。
也可以讨论 Binary Search + BFS。

2421：
按照节点值分组处理，
配合 DSU 计算合法路径。

1724：
Persistent Union-Find / Versioned Connectivity。

这是高级数据结构问题，
不能直接当作普通离线 Kruskal 题。

必须标记 P2。

不要要求我为这一道偏专门的题目
额外记忆复杂的持久化数据结构模板。

特别强调：

这整个 Level 2 不一定输出真正的 MST。

重点是 Sorted Events + DSU Union Process。

--------------------------------------------------

MST 相关的真实应用和原有教程：

kruskal_applications.py
原有 MST 五层讲解
Cut Property 图片
Prim / Kruskal 图解

必须完整保留在对应 _resources 中。

不能当作普通题目文件删除。

==================================================
LEVEL 1
07 - 特殊图结构与路径
==================================================

Level 2：
01 - Bipartite Graph 与二染色

题目顺序：

LC-0785 - Is Graph Bipartite
LC-0886 - Possible Bipartition

教学重点：

BFS / DFS Two-coloring。

每条边的两端必须颜色不同。

解释为什么出现颜色冲突
就意味着不能二分。

LC-886：
先将不喜欢关系建模为无向图。

--------------------------------------------------

Level 2：
02 - Eulerian Path 与边使用约束

题目顺序：

LC-0332 - Reconstruct Itinerary
LC-2097 - Valid Arrangement of Pairs

教学重点：

Hierholzer's Algorithm。

必须解释：

- 为什么是每条边恰好使用一次
- 与普通 DFS 遍历节点的区别
- 有向图中的入度与出度条件
- 后序记录路径的原因
- 最后为什么需要反转结果
- LC-332 的字典序最小要求

此算法属于 P1 进阶，
不要求在学习图论初期强行掌握。

--------------------------------------------------

Level 2：
03 - Tarjan Bridges 与割点

题目顺序：

LC-1192 - Critical Connections in a Network
LC-1568 - Minimum Number of Days to Disconnect Island

教学重点：

Discovery Time
Low-link Value
Bridge

桥的判定：

low[v] > disc[u]

必须解释：
为什么该条件表明子树 v
不存在绕过边 (u,v) 回到 u 或其祖先的路径。

LC-1568：
可以使用割点分析，
也可能使用其他基于题目约束的正确解法。

不得假定该题必须使用完整 Tarjan 模板。

Tarjan Bridges 属于 P1/P2 进阶。

不要混淆：
Tarjan Bridges
Tarjan SCC
Floyd Cycle Detection

三者不是同一个算法。

==================================================
LEVEL 1
08 - 函数图与树上图论
==================================================

该类作为独立的进阶家族保留。

--------------------------------------------------

Level 2：
01 - Functional Graph

题目顺序：

LC-2359 - Find Closest Node to Given Two Nodes
LC-2360 - Longest Cycle in a Graph

教学重点：

Functional Graph：
每个节点最多有一条出边。

与一般 Directed Graph 不同，
函数图的特殊结构可以简化遍历和环处理。

2359：
从两个起点分别计算到其他节点的距离。

2360：
在函数图中检测环并计算最长环长。

可以使用：
DFS
Visited Timestamp
Functional Graph Cycle Detection

重点与 Linked List Floyd Cycle Detection 交叉引用。

不要无必要地记忆很多不同版本。

--------------------------------------------------

Level 2：
02 - Tree Diameter 与 Rerooting DP

题目顺序：

LC-1245 - Tree Diameter
LC-0834 - Sum of Distances in Tree

教学重点：

1245：
树上直径。
可以使用两次 BFS / DFS。

必须解释为什么在树上成立，
不能无条件推广为任意图的直径算法。

834：
Rerooting DP（换根动态规划）。

先通过一次 DFS 计算：
- 子树大小
- 初始根的距离总和

再通过第二次 DFS 将根转移到相邻节点。

重点解释换根公式，
不要把它当成普通 BFS 模板。

标记 P1/P2 进阶。

如果 Trees 或 DP 专题已有同题，
使用 README 建立跨专题索引。

==================================================
六、明确新增的四道题
==================================================

本次 ChatGPT 第一轮建议新增：

LC-1293 - Shortest Path in a Grid with Obstacles Elimination
LC-0815 - Bus Routes
LC-0959 - Regions Cut By Slashes
LC-2192 - All Ancestors of a Node in a Directed Acyclic Graph

新增前：

1. 检查当前 Graphs 目录。
2. 只读检查整个仓库。
3. 验证题号、题名、题目约束和算法。
4. 避免覆盖已有版本。
5. 确定正确的 Level 1 / Level 2。

对于真正缺失的题目，
使用本仓库已有的 LeetCode 生成工作流创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据题号创建完整题目文件的能力。

请直接复用。

不要创建空白 PDF 或虚假 metadata。

如果生成工具无法完成某道题，
记录失败原因。

不允许为了凑题目数量而伪造内容。

==================================================
七、NC-only 题目正式化
==================================================

当前存在：

NC - Longest Increasing Path in Matrix

它对应：

LC-0329 - Longest Increasing Path in a Matrix

请验证题面和 solution.py。

确认后：

1. 创建正式 LC-0329 题目目录。
2. 生成缺失的标准 LC 文件。
3. 将现有 NC 原始资料保存到 _neetcode/。
4. 保留所有原有图片、PDF、metadata 和代码。
5. 不得覆盖原始 NC solution.py。

特别保留：

asset-NC-07 - LC-0329 - Explanation.jpg

并将该题归入 DAG DP，
同时解释 DFS + Memoization 是推荐解法之一。

==================================================
八、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 第一轮审核。

你还必须独立进行第二轮审核。

目的：
进一步检查整个 Graphs 面试知识体系，
确认是否遗漏真正高价值的 Pattern。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
可信的 Graph Algorithms 学习资料

如果有网络访问，核对题目名称、
约束、典型解法和学习价值。

不要编造 FAANG 内部面试出现频率。

请重点审核：

1. Graph Representation
2. DFS / BFS
3. Connected Components
4. Flood Fill
5. Reverse Reachability
6. Single-source BFS
7. Multi-source BFS
8. State-space BFS
9. BFS with Additional State
10. Union-Find
11. Dynamic Connectivity
12. Offline DSU
13. Topological Sort
14. Three-color DFS
15. DAG DP
16. Dijkstra
17. Bellman-Ford
18. 0-1 BFS
19. Minimax / Maximin
20. Kruskal
21. Prim
22. Bipartite Coloring
23. Eulerian Path
24. Tarjan Bridges
25. Functional Graph
26. Tree Diameter
27. Rerooting DP

额外候选：

LC-0847 - Shortest Path Visiting All Nodes
LC-0924 - Minimize Malware Spread
LC-1519 - Number of Nodes in the Sub-Tree With the Same Label
LC-0684 - Redundant Connection（已有，禁止重复）
LC-1263 - Minimum Moves to Move a Box to Their Target Location
LC-1631 - Path With Minimum Effort（已有，禁止重复）

这些只是审核候选。

必须考虑：

- 是否确实填补知识缺口？
- 是否具有明显的面试代表性？
- 是否增加独立、可迁移的技巧？
- 是否只是已有题目的相似训练？
- 是否已有其他专题提供完整实现？
- 是否会显著增加学习负担？

允许独立新增最多 4 道不同题目。

如果发现超过 4 道值得推荐，
只新增最有价值的 4 道，
其余放进 README 的 Future Candidates。

如没有真正重要的遗漏，可以不新增。

尤其不要因为图论范围很广，
就把以下内容全部加入核心学习路线：

- Network Flow / Max Flow
- Min-cost Max-flow
- Heavy-light Decomposition
- Persistent DSU
- Advanced SCC Algorithms
- Floyd-Warshall
- 极偏门的图论竞赛技巧

可以在 README 保留概念索引，
但不应自动扩展成庞大题库。

==================================================
九、P0 P1 P2 优先级
==================================================

P0：
最值得熟练掌握的核心面试题。

P1：
重要变体与进阶应用。

P2：
特殊算法、低频题、复杂组合与参考资料。

建议以下题目优先列入 P0：

Graph Modeling：
LC-1971
LC-0133

DFS/BFS：
LC-0200
LC-0695
LC-0130
LC-0417
LC-0994
LC-0542
LC-0752
LC-0127

Union-Find：
LC-0323
LC-0261
LC-0684
LC-0721

Topological Sort：
LC-0207
LC-0210
LC-0269

Shortest Paths：
LC-0743
LC-0787
LC-1631

MST：
LC-1584

建议以下题目作为 P1 重要补充：

LC-0841
LC-1466
LC-1091
LC-0286
LC-0934
LC-0317
LC-0815
LC-1293
LC-0305
LC-2092
LC-0959
LC-0802
LC-0329
LC-2050
LC-2192
LC-1514
LC-1976
LC-1334
LC-1368
LC-2290
LC-1135
LC-1168
LC-1697
LC-0785
LC-0332
LC-1192

以上是教学优先级建议，
不是声称这些题拥有精确的公司出题频次。

特别说明：

LC-1192、332 等进阶算法
可以先理解原理，后续再独立实现。

以下类型应倾向 P2：

- Floyd-Warshall 专项
- Persistent DSU
- 高难度 MST Edge Classification
- 复杂 Group Topological Sort
- 特殊函数图循环题
- 特殊 Eulerian Path 组合题
- 高阶 Rerooting DP
- 低迁移性或高度重复的 Graph 题

请根据实际题目逐个标记 P0/P1/P2。

不能只按 Easy/Medium/Hard 决定优先级。

README 必须给出：

A. P0 最小必刷路线
B. P0 + P1 标准面试路线
C. P2 进阶与存档路线

每道题还要标记：

Primary Pattern
Secondary Patterns
Core Invariant
Recommended Algorithm

==================================================
十、图论知识决策树
==================================================

必须在根 README 中编写：

Graph Pattern Recognition Guide。

至少回答：

Q1：
题目能否建模为节点和边？
如何定义节点与边？

Q2：
只需要判断是否可达？
-> DFS / BFS。

Q3：
需要统计连通块？
-> DFS / BFS / Union-Find。

Q4：
是否动态添加边并反复查询连通性？
-> Union-Find。

Q5：
是否要找无权图中的最少步数？
-> BFS。

Q6：
是否有多个源点，要求到最近源点的距离？
-> Multi-source BFS。

Q7：
是否有额外资源、钥匙、次数或状态约束？
-> State-space BFS / Expanded State。

Q8：
是否存在有向依赖关系？
-> Topological Sort / Kahn。

Q9：
是否需要检测有向环？
-> Kahn / Three-color DFS。

Q10：
是否要求带权图中的最短路径？
-> 根据边权条件选择 Dijkstra 或 Bellman-Ford。

Q11：
所有边权是否只有 0/1？
-> 可以考虑 0-1 BFS。

Q12：
路径代价是否为沿途最大或最小值？
-> 考虑 Minimax / Maximin。

Q13：
是否需要以最小总权值连接所有节点？
-> MST。

Q14：
是否在按边权阈值回答离线连通性查询？
-> Sorted Edges + Union-Find。

Q15：
是否需要给图二染色？
-> Bipartite Graph。

Q16：
是否需要每条边恰好走一次？
-> Eulerian Path。

Q17：
是否需要找移除后导致图断开的关键边？
-> Bridges / Low-link。

Q18：
图是否是 Functional Graph？
-> 利用每个节点最多一条出边的性质。

Q19：
问题是否发生在树上？
-> Tree DFS / BFS / Rerooting DP。

必须说明：

这些是题型识别提示，
不是绝对排他的算法选择规则。

==================================================
十一、核心图论模板
==================================================

保留目前：

00-foundations/templates/

中的全部原始 17 个模板。

不允许直接删除旧模板。

但要建立新的核心模板索引：

Core Templates：

1. Graph Representation
2. DFS Recursive
3. BFS Queue
4. Multi-source BFS
5. Union-Find
6. Kahn Topological Sort
7. Three-color DFS
8. Dijkstra
9. Bellman-Ford
10. Kruskal
11. Prim

Optional Templates：

12. 0-1 BFS
13. Minimax / Maximin
14. Bipartite Coloring
15. Tarjan Bridges
16. Hierholzer
17. Rerooting DP
18. Floyd-Warshall（只保留旧参考，不作为必学）

注意：

这不是要求新增十八套互不相关的代码。

应该优先复用现有模板并建立索引。

重点解释各个算法的：

- 前提条件
- 状态不变量
- 核心操作
- 为什么正确
- 何时不能使用
- 时间复杂度
- 空间复杂度
- 代表题目

不能把 BFS、Dijkstra、Union-Find
错误地描述为只存在代码写法上的差异。

==================================================
十二、现有学习资料保护
==================================================

当前存在大量理论与图解资料：

00-foundations
00-Theory
00 - Theory
README.md
*.md
*.pdf
*.png
*.jpg
*.svg
*.mp4
*.py

必须全部保留。

建议统一规划：

_resources/
  foundations/
  decision-trees/
  handbooks/

同时允许各个 Level 1 保留本地 _resources。

例如：

Topological Sort 里的 William Fiset 视频
继续放在该算法家族自己的资源目录。

MST 的 Cut Property 图解
继续放在 MST 家族自己的资源目录。

Dijkstra 现有的 _resources
必须完整保留其内部文件。

不要把所有理论资料不分算法地
混进一个巨大的公共 resources 文件夹。

在根 README 中为理论资料建立可点击相对链接。

如果已有 Markdown 包含相对路径引用，
迁移时必须检查引用是否失效。

优先保留原始文档内容，
通过新 README 修复索引。

若确实需要修改旧文档中的路径，
必须保留修改前内容或可追溯记录，
并说明原始哈希发生变化的原因。

不得删除图解、视频或手写笔记。

==================================================
十三、Git 与文件系统安全
==================================================

这次非常重要：

当前仓库具有大量未提交修改和未跟踪文件。

严禁任何破坏性操作。

开始之前：

1. 执行 pwd。
2. 执行 tree。
3. 检查 git status --short。
4. 递归记录所有文件。
5. 记录每个普通文件的 SHA-256。
6. 记录 Symbolic Link 的目标字符串。
7. 检查 Python import 和 Markdown 相对链接。
8. 记录全部题目 ID。
9. 建立当前路径到目标路径的映射。
10. 检查所有可能的目标路径冲突。

禁止：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖已有文件
删除未跟踪文件
覆盖任何 solution.py
删除原有 Markdown 学习笔记
删除图片、PDF 或视频
修改其他算法专题

本次不自动：

git add
git commit
git push

全部实际写入必须限制在：

11-graphs (图论)

目录内部。

允许只读检查其他专题。

如果生成工具必须写入仓库外部，
先尝试使用安全的输出路径配置。

如果无法限制写入，
该生成步骤应跳过并在报告中说明。

不要因为生成失败就破坏已有资料。

如果发生目标文件重名：

- 内容不同：必须保留两份。
- 内容相同：允许可追溯归档。
- 禁止静默覆盖。
- 冲突记录写入 _conflicts 或审计报告。

所有已存在的不同算法实现都应保留。

===============================================
十四、迁移与验证策略
===============================================

由于当前有超过 500 个文件，
请采用分阶段安全迁移。

建议先创建：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

Manifest 包括：

- 原始文件路径
- SHA-256
- 文件大小
- 文件类型
- 是否为 Symbolic Link
- 所属 LC 题号
- 预期新路径

注意：
审计文件必须放在当前 Graphs 目录内部。

完成迁移后：

逐一确认所有原始文件内容均被保留。

新题生成产生的新文件不计入原始哈希对比。

对于需要修改的 README，
应记录原始内容与修改理由。

验证必须包括：

- 原始 523 个文件内容可追溯。
- 所有现有 LC 和 NC 题目有明确归属。
- 没有意外删除题目。
- 没有遗漏辅助图片和 Markdown。
- 旧 Dijkstra 五层分类完整。
- Bellman-Ford 解法完整。
- MST 理论文件完整。
- Floyd 参考解法完整。
- 六组重复 LC 的版本完整。
- 各层编号连续。
- 所有相对链接真实存在。
- 当前专题外没有被修改。
- Git 原有未提交修改没有丢失。

不要靠猜测认为迁移成功。

必须实际运行文件检查。

==================================================
十五、数量与验收
==================================================

根据用户提供的 tree：

现有 LeetCode 编号目录出现约 110 次。

其中有 6 个重复题号：

0787
1334
1368
1631
2290
2976

因此不同 LC 编号约 104 个。

另外：
NC - Longest Increasing Path in Matrix
对应 LC-0329，现有无正式 LC 目录。

所以当前约 105 道不同题目。

第一轮建议新增 4 道：

1293
815
959
2192

如果全部成功：

第一轮目标：
109 道不同题目。

参考的初始 Level 1 不同题目分布：

01：7
02：26
03：19
04：15（包含 NC-329）
05：20
06：8
07：6
08：4

合计：105

新增后：

02 增加 2 道
03 增加 1 道
04 增加 1 道

最终第一轮合计 109 道。

这里统计的是不同题号，
不是物理题目文件夹的数量。

一个题目如果存在两个不同算法实现，
仍然只算一道不同题目。

实际审计中如发现题目身份不匹配，
以真实题目和文件内容为准。

第二轮如发现真正重要的遗漏，
可以新增最多 4 道。

不要为了满足数字而创建虚假文件。

==================================================
十六、README 学习文档
==================================================

请建立：

A. Graphs 根 README.md
B. 每个 Level 1 的 README.md
C. 对重点 Level 2 创建必要的短 README
D. Graph Pattern Recognition Guide
E. Graph Algorithm Comparison Table
F. P0 / P1 / P2 推荐刷题路线

根 README 应重点回答：

1. 什么是 Graph？
2. 有向图与无向图有什么区别？
3. Weighted 和 Unweighted 有什么区别？
4. DFS 与 BFS 有什么区别？
5. BFS 与 Dijkstra 有什么区别？
6. Dijkstra 与 Bellman-Ford 有什么区别？
7. Union-Find 和 DFS 的连通性有什么区别？
8. Topological Sort 为什么要求 DAG？
9. MST 与 Shortest Path 有什么区别？
10. Kruskal 与 Prim 有什么区别？
11. Kahn 与普通 BFS 有什么区别？
12. 0-1 BFS 与普通 BFS 有什么区别？
13. Minimax / Maximin 与普通最短路有何区别？
14. 为什么某些题需要扩展状态？
15. Tree 为什么也是特殊 Graph？

每种算法介绍必须包含：

- 算法定义
- 适用条件
- 状态不变量
- 核心操作
- 简短正确性证明
- Python 核心模板
- 时间复杂度
- 空间复杂度
- 代表题目
- 什么时候不能使用

理论解释风格：

中文主导 + 英文专业术语。

例如：

Graph Traversal（图遍历）
Connected Component（连通分量）
Shortest Path（最短路径）
Relaxation（松弛）
Topological Sort（拓扑排序）
Minimum Spanning Tree（最小生成树）
Disjoint Set Union（并查集）
Bottleneck Path（瓶颈路径）
Strongly Connected Component（强连通分量）

理论讲解优先使用：

1. 1–3 个决定性观察
2. 状态定义
3. 算法不变量
4. 简短证明
5. Python 模板
6. 代表题目

不要生成冗长、重复、空泛的教材。

==================================================
十七、最小核心学习路线
==================================================

在根 README 单独提供：

FAANG Graphs Core Roadmap。

建议按照：

阶段 A：
Graph Representation
-> DFS
-> BFS
-> Connected Components

阶段 B：
Multi-source BFS
-> Implicit State BFS

阶段 C：
Union-Find
-> Cycle Detection
-> Dynamic Connectivity

阶段 D：
Kahn Topological Sort
-> Directed Cycle Detection
-> DAG DP

阶段 E：
Standard Dijkstra
-> Bellman-Ford
-> Dijkstra Variants

阶段 F：
Kruskal
-> Prim
-> Offline Threshold Connectivity

阶段 G：
Bipartite
-> Tarjan Bridges
-> Eulerian Path
-> Functional Graph
-> Rerooting DP

其中阶段 G 的多项内容为选修或进阶。

不要求全部精通才算完成图论准备。

请给我一个真正精简的：

20-25 道最核心 Graph 面试练习题

用于优先复习。

这些题应该覆盖主要算法模式，
而不是挑选 25 道高度重复的图遍历题。

==================================================
十八、实际执行顺序
==================================================

请严格按以下顺序执行：

1. 扫描完整 Graphs 目录。
2. 检查 Git 状态。
3. 建立原始文件 Manifest。
4. 识别每个 LC / NC 题目。
5. 检查六组不同算法实现。
6. 检查已完成的 Dijkstra 目录。
7. 检查所有理论资料与模板。
8. 检查跨专题引用。
9. 制作完整迁移映射。
10. 创建新的 Level 1 / Level 2。
11. 分阶段安全迁移旧题。
12. 保留 Dijkstra 的五层内部结构。
13. 整理不同算法版本。
14. 将 LC-1579 移入 DSU 家族。
15. 将 LC-329 正式化。
16. 整理 LC-1724 的进阶归属。
17. 创建第一轮新增的四道题。
18. 进行 Claude Code 独立的第二轮审核。
19. 只添加确实有价值的遗漏题。
20. 按最终学习顺序重新编号。
21. 整理理论资料和模板。
22. 生成根 README。
23. 生成各 Level 1 README。
24. 创建 Graph Algorithm Comparison Table。
25. 创建 Pattern Recognition Guide。
26. 创建最小核心刷题路线。
27. 验证旧文件及所有原始哈希。
28. 验证 Dijkstra 和 MST 的原始资料。
29. 验证题目编号及算法归属。
30. 验证相对链接。
31. 检查 Git 状态。
32. 仅清理确认已空的遗留目录。
33. 输出最终 tree。
34. 输出详细验收报告。

==================================================
十九、最终报告
==================================================

报告必须包含：

1. 最终完整 tree。
2. 8 个 Level 1 的实际结构。
3. 每个 Level 2 的教学目标。
4. 所有旧题目的迁移情况。
5. 六组重复 LC 的处理结果。
6. Dijkstra 子树保护结果。
7. Union-Find / MST 重新分类结果。
8. LC-329 正式化结果。
9. ChatGPT 推荐新增的四道题。
10. Claude Code 自主新增的题目。
11. 未新增但值得考虑的候选题。
12. P0 / P1 / P2 数量。
13. 核心 20-25 道题推荐路线。
14. 原始文件完整性与哈希验证。
15. 理论资料与模板完整性。
16. 跨专题索引。
17. Git 变更摘要。
18. 无法完成的步骤及原因。

特别要求：

不要因为目录复杂而放弃重构。

如果某个局部无法安全迁移，
保留它的原始内容并清楚报告，
继续完成其他安全可执行的部分。

整个任务应尽量 Idempotent（幂等）。

重复执行不会：
- 叠加编号
- 产生重复题目
- 覆盖原始代码
- 删除重要资料
- 破坏已经整理好的 Dijkstra

请直接开始完整 Graphs 专题重构。
PROMPT
)"
