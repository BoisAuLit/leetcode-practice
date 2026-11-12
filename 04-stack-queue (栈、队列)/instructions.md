
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/04-stack-queue (栈、队列)' && claude "$(cat <<'PROMPT'
请直接执行当前 Stack & Queue（栈、队列）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试与 Online Assessment（OA）。

请将当前目录建设成高质量、低记忆负担、便于长期复习的 Stack & Queue 学习体系。

你必须实际执行文件操作，而不是只生成计划。

==================================================
一、总体目标
==================================================

完成以下任务：

1. 审计全部已有题目和学习资料。
2. 设计合理的 Level 1 -> Level N 分类体系。
3. 移动、重命名并重新编号已有题目。
4. 补齐缺失的经典 Stack / Queue 面试题。
5. 单独建立 Monotonic Stack 学习体系。
6. 单独建立 Monotonic Deque 学习体系。
7. 区分 Stack、Queue、BFS、Parsing 和 DP。
8. 检查跨专题重复，尽量避免重复存储题目。
9. 独立审核 ChatGPT 的推荐，发现真正重要的遗漏题目。
10. 生成 README、代码模板和复习索引。
11. 最终检查 Git 状态和全部文件完整性。

学习原则：

- Interview Relevance（面试价值）
- Pattern Recognition（题型识别）
- Transferability（迁移能力）
- Learning Progression（循序渐进）
- Low Memorization Overhead（降低记忆负担）

不追求 LeetCode 题目数量最大化。

优先掌握少量核心算法和它们最有代表性的变体。

不能因为一个题目带 Stack / Queue 标签，就自动认为它值得加入核心题库。

==================================================
二、多层级分类规则
==================================================

使用以下层级：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目
Level 4：仅在确实有必要时使用

每一级使用连续数字前缀：

01 - ...
02 - ...
03 - ...

编号必须表达学习顺序、面试重要性和教学依赖关系。

不要根据 LC 题号机械排序。

Level 3 命名：

01 - LC-XXXX - Official English Title
02 - LC-YYYY - Official English Title

每个 Level 2 内的 Level 3 从 01 重新编号。

若某个类别只有一个代表题，可以保留该 Level 2，但不要为这道题继续制造无意义的 Level 4。

资源目录如 _neetcode、_resources 不计入算法层级。

==================================================
三、目标 Level 1 分类及题目
==================================================

以下是本次第一轮推荐结构。

原则上使用 7 个 Level 1。

允许你在独立审核后调整分类，但必须有明确、可解释的教学理由。

--------------------------------------------------
LEVEL 1
01 - 基础栈、括号与消除 (Stack Fundamentals)
--------------------------------------------------

核心：
LIFO / Matching / Simulation / Cancellation

Level 2:
01 - 括号匹配、修复与有效区间

Level 3：

01 - LC-0020 - Valid Parentheses
02 - LC-1249 - Minimum Remove to Make Valid Parentheses
03 - LC-0032 - Longest Valid Parentheses

教学重点：

LC-20：
- Stack Matching
- Push opening bracket
- Pop matching closing bracket
- 为什么 LIFO 适合嵌套结构

LC-1249：
- 使用栈记录未匹配括号的位置
- 删除无效括号
- 理解位置索引与括号匹配

LC-32：
- Stack of Indices
- Sentinel Index
- 计算最长连续有效括号区间
- 与 LC-20 的区别：不只是判断是否合法，而是求连续区间最大长度

注意：
LC-32 也可以使用 DP。
本专题优先讲解 Stack 版本。

Level 2:
02 - 栈模拟、消除与状态恢复

Level 3：

01 - LC-1047 - Remove All Adjacent Duplicates In String
02 - LC-0735 - Asteroid Collision
03 - LC-0946 - Validate Stack Sequences
04 - LC-0071 - Simplify Path

教学重点：

LC-1047：
相邻元素抵消。
当前元素和 Stack Top 相同则 Pop，否则 Push。

LC-735：
使用栈模拟连续碰撞。
一个新元素可能触发多次 Pop。
重点讲解 While Loop 和碰撞终止条件。

LC-946：
模拟 Push / Pop 顺序。
理解栈中尚未被弹出的元素代表什么。

LC-71：
Path Normalization。
使用栈维护有效目录。
正确处理 "."、".." 和重复斜杠。

这组题的共同思想：
Stack 保存尚未完成处理、未来可能被抵消或恢复的状态。

但不要强行把所有题的代码写成相同结构。

--------------------------------------------------
LEVEL 1
02 - 单调栈及其变体 (Monotonic Stack)
--------------------------------------------------

这是本次重构最重要的新增知识体系。

必须单独建立，不能把相关题目混进普通 Stack。

核心：
Monotonic Increasing Stack
Monotonic Decreasing Stack
Next Greater / Next Smaller
Boundary Contribution

Level 2:
01 - Next Greater 与 Next Smaller

Level 3：

01 - LC-0496 - Next Greater Element I
02 - LC-0739 - Daily Temperatures
03 - LC-0503 - Next Greater Element II
04 - LC-0901 - Online Stock Span

教学重点：

LC-496：
最标准的 Next Greater Element。
用单调栈确定右侧第一个更大元素。
使用 Hash Map 存储查询结果。

LC-739：
单调递减的索引栈。
遇到更高温度时结算之前的日期。
解释为什么保存 Index 而不是 Value。

LC-503：
Circular Array。
遍历两轮，使用 i % n。
理解为什么第二轮只需处理循环关系。
避免重复入栈产生错误。

LC-901：
Online Monotonic Stack。
处理连续不大于当天价格的历史区间。
使用 (price, span) 聚合信息。
理解每个元素入栈和出栈次数均为常数次。

必须讲清楚：
- Increasing Stack 与 Decreasing Stack
- 严格与非严格单调
- Pop Condition
- 为什么 Pop 掉的元素以后不再有用
- 为什么总时间是 Amortized O(n)

Level 2:
02 - Histogram、边界与贡献计算

Level 3：

01 - LC-0084 - Largest Rectangle in Histogram
02 - LC-0907 - Sum of Subarray Minimums

教学重点：

LC-84：
Monotonic Increasing Stack。
求每根柱子可以扩展到的左右边界。
面积 = height * width。
重点讲解 Sentinel 和边界索引。

LC-907：
Contribution Technique（贡献法）。
对每个元素计算它作为子数组最小值的贡献。
使用 Previous Less / Next Less Boundaries。

必须准确解释重复元素的处理：
一侧使用严格不等式，
另一侧使用非严格不等式，
避免重复计数。

不要把 LC-907 简单地说成与 LC-84 完全相同的题。
它们共享单调边界思想，但最终计算目标不同。

Level 2:
03 - 排序贪心与单调栈

Level 3：

01 - LC-0853 - Car Fleet
02 - LC-0402 - Remove K Digits

教学重点：

LC-853：
先按照车辆位置排序。
计算车辆到达终点的时间。
从靠近终点的车辆开始扫描。
用单调关系判断是否形成新的车队。

可以使用 Stack，也可以用 Running Maximum Time。
必须解释为什么两种表示等价。

LC-402：
Greedy + Monotonic Stack。
当新数字更小时，优先删除前面较大的数字。
控制删除次数 k。
处理剩余删除次数和 Leading Zeros。

重点理解：
为什么优先消除较高位上的较大数字。

--------------------------------------------------
LEVEL 1
03 - 表达式计算与嵌套解析 (Expression Parsing)
--------------------------------------------------

核心：
Stack Evaluation / Operator Precedence / Nested Structures

Level 2:
01 - 逆波兰表达式

Level 3：

01 - LC-0150 - Evaluate Reverse Polish Notation

教学重点：

Postfix Notation（后缀表达式）。
操作数入栈，遇到运算符取出两个操作数。
注意减法和除法的操作数顺序。

Python 整数除法需要符合题目要求的向零截断。
不能直接使用会向下取整的 // 处理所有负数情况。

Level 2:
02 - 中缀表达式与运算符优先级

Level 3：

01 - LC-0227 - Basic Calculator II
02 - LC-0224 - Basic Calculator

教学重点：

LC-227：
加减乘除。
Operator Precedence。
延迟处理加减，优先结算乘除。

LC-224：
括号嵌套。
正负号和当前计算状态。
遇到括号保存外层上下文。

必须解释两题的不同约束。
不能误认为它们只是在同一份代码中加一个括号判断。

Level 2:
03 - 嵌套字符串与迭代器

Level 3：

01 - LC-0394 - Decode String
02 - LC-0341 - Flatten Nested List Iterator

教学重点：

LC-394：
栈保存上一层字符串及重复次数。
遇到 ] 时恢复上一层状态。

LC-341：
Nested Iterator。
可以使用 Stack / Lazy Expansion。
理解迭代器的 hasNext / next 契约。

如果选择 Lazy Approach，
必须保证 next 和 hasNext 的行为正确。

--------------------------------------------------
LEVEL 1
04 - Stack 与 Queue 数据结构设计 (Design)
--------------------------------------------------

核心：
Stack / Queue Implementation
Auxiliary State
Circular Buffer
Amortized Analysis

Level 2:
01 - 带额外状态的 Stack

Level 3：

01 - LC-0155 - Min Stack

教学重点：

Stack + Minimum Tracking。
支持 push、pop、top、getMin。
所有操作要求 O(1)。

可以使用两个 Stack 或保存 (value, current_min)。
优先选择最清晰、易复述的解法。

Level 2:
02 - FIFO 队列与循环结构

Level 3：

01 - LC-0346 - Moving Average from Data Stream
02 - LC-0622 - Design Circular Queue

教学重点：

LC-346：
Fixed Capacity Queue。
维护 Running Sum。
理解为什么不需要每次遍历全部窗口元素。
此题可能是 Premium，保留已有资料。

LC-622：
Circular Queue / Ring Buffer。
head、tail、size、capacity。
正确处理环形下标、队满和队空。

Level 2:
03 - Stack 与 Queue 相互实现

Level 3：

01 - LC-0232 - Implement Queue using Stacks
02 - LC-0225 - Implement Stack using Queues

教学重点：

LC-232：
使用 Input Stack 和 Output Stack。
解释为什么每个元素最多经过有限次转移。
理解 Amortized O(1)。

LC-225：
使用一个或两个 Queue 模拟 Stack。
理解 Rotation 和 LIFO 语义。

不能将两者错误地认为是完全对称的代码实现。

--------------------------------------------------
LEVEL 1
05 - 单调队列与滑动窗口 (Monotonic Deque)
--------------------------------------------------

核心：
Monotonic Deque
Window Extremum
Prefix Sum + Deque

必须区分：
Monotonic Stack 与 Monotonic Deque 不是同一个模板。

Level 2:
01 - 窗口最大值与最大最小值

代表题：

LC-0239 - Sliding Window Maximum
LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

特别注意跨专题去重：

这两道题可能已经在：

03-sliding-window (滑动窗口)

中存在。

请先递归扫描仓库。

如果已经存在：
- 不重复生成 PDF 和 solution.py。
- 在这个 Level 2 的 README.md 中建立相对路径引用。
- 记录它们是本章 Monotonic Deque 的核心交叉题。

如果全仓库不存在：
- 在当前 Level 2 中创建正式题目文件夹。
- 将其纳入 P0 / P1 练习。

教学重点：

LC-239：
单调递减 Deque。
保存 Index。
删除过期的窗口元素。
维护最大值候选。

LC-1438：
使用两个 Deque。
一个维护最大值，一个维护最小值。
满足 max - min <= limit。

Level 2:
02 - Prefix Sum 与单调队列

Level 3：

01 - LC-0862 - Shortest Subarray with Sum at Least K

教学重点：

Prefix Sum + Monotonic Deque。

数组可能存在负数。
因此普通的正数 Sliding Window 方法不再适用。

维护前缀和索引的单调性，
使用 Deque 求满足条件的最短子数组。

重点理解：
- Prefix Sum 的差值公式
- 为什么可以弹出队首
- 为什么可以弹出队尾
- 为什么时间复杂度是 O(n)

LC-862 属于 P1 进阶题。

不需要为了它单独记忆所有 Prefix Sum 变体。

==================================================
LEVEL 1
06 - Queue 与 BFS (Breadth-First Search)
==================================================

注意：

Queue 是数据结构。
BFS 是使用 Queue 实现的一种搜索算法。

必须清楚区分两者。

Level 2:
01 - Grid Traversal 与 Multi-source BFS

Level 3：

01 - LC-0733 - Flood Fill
02 - LC-0286 - Walls and Gates

额外候选：
LC-0994 - Rotting Oranges

教学重点：

LC-733：
Grid BFS。
维护访问状态和上下左右四个方向。

LC-286：
Multi-source BFS。
所有 Gates 同时入队。
按 BFS 层次计算最近距离。

LC-994：
Multi-source BFS + Level Counting。
从所有腐烂橘子同时扩散。

如果 LC-994 已经存在于 Graph BFS 专题，
请建立跨专题索引，不重复生成。

如果全仓库不存在，可以在当前分类中新增。

Level 2:
02 - State BFS 与无权最短路径

Level 3：

01 - LC-0279 - Perfect Squares

额外候选：
LC-0752 - Open the Lock

教学重点：

LC-279：
将整数剩余值视为 BFS 状态。
每次减去一个平方数。
求最少步数。

必须注明：
这题也可以使用 Dynamic Programming。
BFS 不是唯一正确解法。

LC-752：
把锁的字符串编码看成 Graph State。
每次旋转一位构成一条边。
使用 BFS 求最少操作次数。

如果 LC-752 已存在于 Graph 专题，
建立索引而非重复创建。

如果全仓库不存在，可以考虑新增。

对于 BFS 分类：

必须检查其他 Graph / BFS 专题的已有文件。

不要为了 Stack & Queue 专题的完整性，
把整个 Graph BFS 题库重新复制过来。

本专题主要用于说明 Queue 的典型应用。

==================================================
LEVEL 1
07 - 低优先级与跨专题存档 (Archive)
==================================================

目的：
保留原有学习成果，但避免偏门题目占据核心学习路线。

Level 2:
01 - 简单括号计数与特殊贪心

Level 3：

01 - LC-1021 - Remove Outermost Parentheses
02 - LC-1717 - Maximum Score From Removing Substrings

说明：

LC-1021：
使用 Depth Counter 即可解决。
不一定需要真正维护 Stack。

LC-1717：
Greedy + Stack-based Removal。
处理不同子串删除收益。
与普通相邻抵消有所不同。

保留原有代码，标记 P2。

Level 2:
02 - 复杂表达式解析

Level 3：

01 - LC-0736 - Parse Lisp Expression

说明：

复杂嵌套作用域解析。
与普通计算器题相比，涉及变量绑定和环境管理。

标记 P2。
当前不要求将其作为核心模板记忆。

Level 2:
03 - Dynamic Programming 与时间队列

Level 3：

01 - LC-2327 - Number of People Aware of a Secret

说明：

本题更偏向 Dynamic Programming / Time-based Simulation。

可以使用 Queue 或 Prefix Sum 优化，
但它并非基础队列模板题。

标记 P2。

完整保留现有资料，
在 README 中指出其更合适的算法主归属。

==================================================
四、明确建议新增的题目
==================================================

本次 ChatGPT 推荐优先补充：

LC-0735 - Asteroid Collision
LC-0946 - Validate Stack Sequences

LC-0496 - Next Greater Element I
LC-0739 - Daily Temperatures
LC-0503 - Next Greater Element II
LC-0901 - Online Stock Span

LC-0084 - Largest Rectangle in Histogram
LC-0907 - Sum of Subarray Minimums

LC-0853 - Car Fleet
LC-0402 - Remove K Digits

LC-0232 - Implement Queue using Stacks
LC-0862 - Shortest Subarray with Sum at Least K

共 12 道明确新增候选。

对于每一道题：

1. 先检查当前目录是否已存在。
2. 再检查全仓库是否已存在。
3. 如果当前目录已有，直接复用。
4. 如果其他专题已有，优先建立跨专题引用。
5. 如果不存在，使用现有题目生成能力创建。

标准文件：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

请直接调用本仓库已有的 LeetCode 生成工具。

你已经具备根据题号创建完整题目资料的能力，
不需要重新设计 PDF 生成流程。

不要覆盖现有的 solution.py。

对于跨专题相关题：
LC-0239
LC-1438
LC-0994
LC-0752

按照上面的规则检查、索引或补充。

==================================================
五、Claude Code 第二轮独立审核
==================================================

上面的推荐是第一轮筛选。

你还必须进行第二轮独立审核。

参考：
- NeetCode 150
- NeetCode 250
- Blind 75
- Grind 75 / Grind 169
- LeetCode Top Interview 150
- 其他可靠的算法面试题单

重点检查是否覆盖：

STACK:
1. LIFO Fundamentals
2. Parentheses Matching
3. Stack Simulation
4. Adjacent Cancellation
5. Nested Structure Parsing
6. RPN Evaluation
7. Infix Expression Evaluation
8. Min Stack
9. Next Greater Element
10. Next Smaller Element
11. Monotonic Stack
12. Histogram Boundaries
13. Contribution Technique
14. Greedy Monotonic Stack

QUEUE:
15. FIFO Queue
16. Circular Queue
17. Stack/Queue Conversion
18. Sliding Window Monotonic Deque
19. Prefix Sum + Monotonic Deque
20. BFS Queue
21. Multi-source BFS
22. BFS Shortest Path

还应检查以下备选题：

LC-0085 - Maximal Rectangle
LC-0316 - Remove Duplicate Letters
LC-2104 - Sum of Subarray Ranges
LC-0641 - Design Circular Deque
LC-0933 - Number of Recent Calls
LC-0649 - Dota2 Senate
LC-1544 - Make The String Great

这些只是审核候选，不要求全部新增。

新增条件：

1. 具有经典面试代表性。
2. 引入真正有用的新 Pattern。
3. 不是简单重复已有题。
4. 有较高迁移性。
5. 与当前学习目标直接相关。
6. 可以清晰说明新增后的教学收益。

建议独立新增最多 5 道。

如果发现超过 5 道候选：
优先新增最有价值的 5 道，
其他放入 README 的 Future Candidates。

不要因为题目数量少就盲目补充。

特别注意：

LC-0022 - Generate Parentheses
虽然常被列入 Stack 题单，
但标准生成解法的核心是 Backtracking。

如果已有 Backtracking 专题，
建立交叉索引即可，
不必为本专题复制该题。

==================================================
六、NC 与 LC 重复题目
==================================================

现有：

NC - Evaluate Reverse Polish Notation
LC-0150 - Evaluate Reverse Polish Notation

NC - Min Stack
LC-0155 - Min Stack

请先验证题面和解法对应关系。

如果确认是同一道题：

1. 保留标准 LC Level 3 文件夹。
2. 将 NC 原始目录的全部内容移动到该 LC 目录下的 _neetcode/。
3. 保留两个来源的 solution.py。
4. 保留 PDF、metadata 和自定义附件。
5. 不覆盖任何已有学习笔记。
6. 在 README 中注明不同版本是否有教学差异。

NC 版本不单独占据第二个正式题目位置。

==================================================
七、原始文件与 Git 安全
==================================================

当前仓库已有大量未提交修改和未跟踪文件。

必须严格保护所有现有数据。

执行前：

1. pwd
2. tree
3. git status
4. 递归列出当前专题所有文件
5. 建立旧路径到新路径的映射
6. 记录现有文件大小和 SHA-256
7. 检查潜在的同名冲突

当前专题已有 23 个题目来源文件夹，
其中包含 2 组 NC / LC 重复题。

去重前不要删除任何目录。

特别保护：

LC-0032：
asset-explanation-claude.png
asset-explanation.jpeg

LC-0227：
note.md

LC-0394：
note.md

及所有其他：
PDF、图片、Python 代码、自定义文件。

禁止：

git reset
git clean
git restore .
git checkout -- .
rm -rf
覆盖已有 solution.py
删除用户笔记
强制重写 PDF
删除未跟踪文件
修改其他专题文件

本次不要自动 git add、git commit 或 git push。

优先使用普通安全重命名或移动，
避免不必要地更改 Git 暂存区。

如果需要移动已跟踪文件，应保证 Git 能识别最终路径变化。

若发生同名冲突：

- 不允许丢弃任何版本。
- 相同内容可去重，但需有来源清单。
- 不同内容必须全部保留。
- 可使用 _conflicts/ 保存冲突版本。
- 必须在最终报告中说明。

旧目录确认全部迁移且为空后才可删除空目录。

任何写入操作都必须限制在当前：

04-stack-queue (栈、队列)

目录内部。

允许只读扫描整个 leetcode-practice 仓库，
用于发现已有题目和跨专题引用。

==================================================
八、生成 README 学习体系
==================================================

必须创建：

A. 当前根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 创建必要的简短 README.md

根目录 README：

1. Stack & Queue 知识地图。
2. 各 Level 1 的学习目标。
3. 各 Level 2 的算法不变量。
4. 所有题目的推荐学习顺序。
5. P0 / P1 / P2 优先级。
6. 标准代码模板。
7. 各模板的时间与空间复杂度。
8. Stack vs Queue vs Deque。
9. Stack vs Monotonic Stack。
10. Monotonic Stack vs Monotonic Deque。
11. BFS 为什么使用 Queue。
12. 跨专题索引。
13. 第二轮审核的补充结果。

每个 Level 1 README：

- 核心定义
- 1–3 个决定性观察
- Loop Invariant（循环不变量）
- Push / Pop 规则
- 正确性解释
- 典型 Python 模板
- 代表题目
- 常见错误
- 复习时的 Pattern Recognition 提示

特别为 Monotonic Stack 编写对照表：

问题类型 | 栈的单调方向 | Pop 条件 | 栈中保存的信息

包括：
- Next Greater
- Next Smaller
- Previous Greater
- Histogram Area
- Contribution Counting
- Greedy Removal

注意：

单调方向会受到扫描方向、严格不等号及实现习惯影响。

不要用未经限定的绝对规则描述所有实现。

应该通过一个具体的 Python 模板和不变量说明其正确性。

README 使用中文主导、中英文结合技术风格。

例如：

Monotonic Stack（单调栈）
Amortized Analysis（摊还分析）
Next Greater Element（下一个更大元素）
Sentinel（哨兵）
Stack Invariant（栈不变量）

目标是帮助长期记忆与复习，而不是堆砌名词。

==================================================
九、P0 / P1 / P2 优先级
==================================================

P0 = 核心必练
P1 = 重要变体
P2 = 进阶专题、低优先级或存档

以下题目优先标记 P0：

LC-0020 - Valid Parentheses
LC-0155 - Min Stack
LC-0150 - Evaluate Reverse Polish Notation
LC-1047 - Remove All Adjacent Duplicates In String
LC-0735 - Asteroid Collision
LC-0496 - Next Greater Element I
LC-0739 - Daily Temperatures
LC-0084 - Largest Rectangle in Histogram
LC-0853 - Car Fleet
LC-0394 - Decode String
LC-0227 - Basic Calculator II

以下可作为 P1：

LC-1249
LC-0032
LC-0071
LC-0946
LC-0503
LC-0901
LC-0907
LC-0402
LC-0224
LC-0341
LC-0232
LC-0225
LC-0346
LC-0622
LC-0862

BFS 题按照既有 Graph 专题的优先级协调，
不要全部重新列为 Stack 核心必练。

LC-239 和 LC-1438 如果已在 Sliding Window：
通过跨专题索引纳入本专题的学习路线。

以下建议 P2：

LC-1021
LC-1717
LC-0736
LC-2327

你可以根据实际题目价值适当调整，
但必须给出理由。

不要把所有题目都设为 P0。

在 README 中单独生成：

1. P0 最小核心路线
2. P0 + P1 标准面试路线
3. P2 扩展与存档路线

==================================================
十、文件夹排序与学习顺序
==================================================

要求：

1. Level 1 按算法学习优先级排序。
2. Level 2 按具体 Pattern 的学习依赖排序。
3. Level 3 按代表性、重要性、难度递进排序。
4. 不允许按题号排序。
5. 所有编号必须连续。
6. 不能存在两个不同位置的相同主题目。
7. 已有题目不得因调整分类而丢失。
8. 新增题目要插入最合适的位置，而不是全部放到最后。
9. 如果跨专题题只建立索引，不创建空的假题目文件夹。
10. 第二轮新增题目后，要重新检查并调整整个目录的编号。

举例：

02 - 单调栈及其变体 (Monotonic Stack)/
  01 - Next Greater 与 Next Smaller/
    01 - LC-0496 - Next Greater Element I/
    02 - LC-0739 - Daily Temperatures/
    03 - LC-0503 - Next Greater Element II/
    04 - LC-0901 - Online Stock Span/
  02 - Histogram、边界与贡献计算/
    01 - LC-0084 - Largest Rectangle in Histogram/
    02 - LC-0907 - Sum of Subarray Minimums/

请将整个专题整理为同样清晰的结构。

==================================================
十一、数量与完整性验收
==================================================

当前原始题目来源文件夹：23 个。

其中：
2 组 NC / LC 重复题。

因此现有不同题目约 21 道，
以实际文件和题目内容审计为准。

第一轮推荐新增：12 道。

如果全部缺失且适合在本专题创建，
预计形成约 33 道不同题目的核心及存档集合。

额外跨专题索引和第二轮补充可以改变最终数量。

绝对不要强行凑齐数量。

最终必须验证：

- 所有旧文件都有新位置。
- 原有代码没有丢失。
- NC / LC 两套来源完整保存。
- Level 1 / Level 2 / Level 3 编号连续。
- 所有新题有正确 metadata。
- 所有新题有完整的题目 PDF。
- 所有新题有 solution.py。
- 所有代码与题目对应正确。
- README 中的路径真实存在。
- 不存在意外重复题目。
- 不存在残留的旧非空分类目录。
- 当前目录以外没有被修改。
- Git 中的原有未提交内容没有被覆盖。

如果发现文件生成失败：
保留已有文件，记录具体原因。
不能创建虚假的空文件来满足数量。

==================================================
十二、实际执行流程
==================================================

请按照以下顺序执行：

1. 扫描当前目录。
2. 审计 Git 工作区。
3. 记录全部原始文件。
4. 验证现有题目内容。
5. 检查跨专题题目。
6. 设计最终迁移映射。
7. 创建新的 Level 1 / Level 2。
8. 迁移旧题目并重新编号。
9. 整理 NC / LC 重复来源。
10. 新增推荐的 12 道候选题中真正缺失的题。
11. 处理 Monotonic Deque 和 BFS 跨专题索引。
12. 进行第二轮独立题库审核。
13. 补充少量确实有价值的遗漏题目。
14. 生成 README 和 Python 模板。
15. 进行题目及文件完整性验证。
16. 校验迁移前后的文件清单与哈希。
17. 校验编号和排序。
18. 清理安全确认的空旧目录。
19. 输出最终 tree。
20. 生成最终审计报告。

最终报告至少包含：

- 完整最终 tree。
- 7 个 Level 1 分类及实际数量。
- 每个 Level 2 的算法目标。
- 所有迁移的旧题。
- 第一轮新增成功的题。
- 第二轮独立新增的题。
- 没有添加的候选及理由。
- 跨专题索引。
- NC / LC 去重结果。
- 原始文件保留验证结果。
- P0 / P1 / P2 统计。
- Git 状态和文件变更摘要。
- 失败或未完成项目。
- 最终建议的复习顺序。

请直接执行实际文件操作。

不要仅仅给我一个目录规划。
PROMPT
)"
