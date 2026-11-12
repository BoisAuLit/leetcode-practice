
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/09-heap (堆)' && claude "$(cat <<'PROMPT'
请直接执行当前 Heap / Priority Queue（堆、优先队列）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试和 Online Assessment（OA）。

请将当前目录建设成一套：
- 面试价值高
- 算法迁移性强
- 知识结构清晰
- 学习顺序合理
- 记忆成本低
- 可以长期复习
- 支持未来继续扩充

的 Heap / Priority Queue 学习体系。

请实际执行文件重构和题目创建，不要只输出规划。

==================================================
一、核心学习目标
==================================================

我不希望把几十道 Heap 题当成几十套独立算法。

我希望围绕少量重要 Pattern 建立长期记忆：

1. Min Heap（最小堆）
2. Max Heap（最大堆）
3. Top K / Kth Largest
4. Size-K Heap（固定大小的堆）
5. K-way Merge（多路归并）
6. Best-first Candidate Expansion（最优候选扩展）
7. Two Heaps（双堆）
8. Heap + Greedy（堆与贪心）
9. Marginal Gain（边际收益）
10. Scheduling Simulation（任务调度模拟）
11. Event-driven Heap（事件优先队列）
12. Heap + Hash Map
13. Lazy Deletion（延迟删除）
14. Priority Updates（动态优先级更新）

重点理解：

Heap 为什么适合反复寻找当前最小值或最大值？

Heap 为什么不保证内部所有元素完全有序？

什么时候应该使用固定大小为 k 的 Min Heap？

什么时候使用 Max Heap？

什么时候使用两个 Heap？

为什么许多 Heap + Greedy 题的关键，
其实是证明每次选择局部最优是安全的？

为什么 Heap 无法高效删除任意指定元素，
因此有时需要 Lazy Deletion？

请将这些问题组织成可复用的学习模式。

==================================================
二、Level 1 -> Level N 命名规则
==================================================

优先使用：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：具体 LeetCode 题目

只有确实有必要时才增加 Level 4。

同级文件夹使用连续编号：

01 - ...
02 - ...
03 - ...

排序综合考虑：

1. 教学依赖关系
2. FAANG / Big Tech 面试代表性
3. 算法迁移价值
4. 循序渐进
5. 解法的复用性
6. 记忆成本

不能按 LeetCode 题号机械排序。

题目文件夹命名：

01 - LC-XXXX - Official English Title
02 - LC-YYYY - Official English Title

每个 Level 2 中的题目编号独立从 01 开始。

非算法分类目录如：
_resources
_neetcode
_conflicts
utils

不参与编号。

==================================================
三、目标 Level 1 / Level 2 / Level 3
==================================================

第一轮建议 7 个 Level 1。

可以在第二轮独立审核时调整，
但所有调整必须有明确教学依据。

--------------------------------------------------
LEVEL 1
01 - Heap 基础与 Top K
--------------------------------------------------

核心：

Heap Push / Pop
Min Heap / Max Heap
Top K
Kth Largest
Streaming Selection

Level 2：
01 - 基础 Heap 与反复取极值

Level 3：

01 - LC-1046 - Last Stone Weight

教学重点：

这是基础 Max Heap 的代表题。

反复取出两个最大值，
根据规则计算结果，
必要时将新值放回 Heap。

Python heapq 默认是 Min Heap。

应介绍如何通过取负数模拟 Max Heap。

必须解释：

- heapq.heappush
- heapq.heappop
- heapq.heapify
- 为什么每次 Pop 的都是当前最小值
- 最大堆的负数模拟
- 如何正确处理空 Heap 和只剩一个元素

--------------------------------------------------

Level 2：
02 - Kth Largest 与固定大小 Heap

Level 3：

01 - LC-0703 - Kth Largest Element in a Stream
02 - LC-0215 - Kth Largest Element in an Array
03 - LC-0973 - K Closest Points to Origin

教学重点：

LC-703：

维护大小不超过 k 的 Min Heap。

Heap 保存目前见过的 k 个最大元素。

当已经有至少 k 个元素时，
Heap Top 就是第 k 大。

必须解释为什么是 Min Heap，
而不是 Max Heap。

LC-215：

在静态数组中寻找第 k 大。

可以使用：
Size-K Min Heap，O(n log k)。

还可以比较 Quickselect，
但不要求在 Heap 专题机械记忆 Quickselect。

LC-973：

K Closest Points。

可维护大小为 k 的 Max Heap，
保存当前距离原点最近的 k 个点。

比较：

- 存储全部点的 Min Heap
- 维护 k 个点的 Max Heap

重点解释两种方案的时间、空间复杂度。

不需要计算平方根。
比较 x*x + y*y 即可。

--------------------------------------------------

Level 2：
03 - Top K Frequency 与 Tie Breaking

Level 3：

01 - LC-0692 - Top K Frequent Words

教学重点：

Frequency Map + Heap。

先统计每个单词出现次数。

然后选出前 k 个最高频单词。

必须正确处理：

频率较高的排前面；
频率相同时，字典序较小的排前面。

解释：

- Heap Tuple 的比较规则
- Min Heap / Max Heap 的选择
- 使用完整 Heap 和 Size-K Heap 的区别
- Tie-breaking 为什么影响正确性

对于 Python：

如果自定义比较器过于复杂，
可以先提供清晰正确的 Heap 实现，
并解释其他优化方案。

本题属于 P1。

额外跨专题知识：

LC-0347 - Top K Frequent Elements

可能已经存在于：
01-arrays-hashing (数组、哈希表)。

请只读检查整个仓库。

如果存在：
建立 README 相对路径索引。

不需要重复生成 LC-347 的完整题目资料。

==================================================
LEVEL 1
02 - K-way Merge 与候选扩展
==================================================

核心：

Merge Sorted Streams
Min Heap Frontier
Best-first Enumeration
Index State Tracking

Level 2：
01 - 多路有序序列合并

Level 3：

01 - LC-0378 - Kth Smallest Element in a Sorted Matrix

教学重点：

矩阵的每一行、每一列都有序。

本专题优先提供 Heap-based K-way Merge。

可以把每一行视为一条有序序列。

Heap 维护每行当前尚未取出的最小候选。

每弹出一个元素，
就将该行的下一个元素加入 Heap。

重点理解：

为什么不需要把整个矩阵展开并排序？

为什么 Heap 中只需要保留各行的候选前沿？

注意：
此题还可以使用 Binary Search on Answer。
必须在 README 中说明这种替代方法。

但本专题核心是 K-way Merge。

另外：

LC-0023 - Merge k Sorted Lists

可能已经存在于 Linked List 专题。

如果存在：
不要复制该题，
而是在当前 Level 2 README 中建立索引。

它也是 K-way Merge 的重要代表题。

--------------------------------------------------

Level 2：
02 - 有序候选集合的按需扩展

Level 3：

01 - LC-0373 - Find K Pairs with Smallest Sums

教学重点：

给定两个已经有序的数组。

目标是寻找 k 个和最小的数对。

不能直接枚举 n*m 个组合再排序。

使用 Min Heap 管理当前最小的候选 Pair。

必须解释：

- Heap 中保存 (pair_sum, i, j)
- 如何利用两个数组的有序性
- 如何初始化有效的候选前沿
- 弹出一个 Pair 后应该加入哪些后继
- 如何避免重复的索引对
- 为什么不用枚举全部笛卡尔积
- 如何处理重复数值但不同索引的 Pair

优先提供易于证明且复杂度良好的实现。

例如：
把每个 nums1[i] 对应的一系列
nums1[i] + nums2[j]
看作有序序列。

初始化每条序列的首个候选，
按需将其下一个候选加入 Heap。

最多初始化 min(k, len(nums1)) 条序列。

重点学习：
Heap 维护 Frontier（候选边界）。

这与 LC-378 有直接迁移关系。

==================================================
LEVEL 1
03 - Two Heaps 与动态中位数
==================================================

核心：

Two Heaps
Median Maintenance
Balance Invariant
Online Data Stream

Level 2：
01 - 动态中位数与双堆平衡

Level 3：

01 - LC-0295 - Find Median from Data Stream

教学重点：

使用两个 Heap：

small：Max Heap，保存较小的一半数字。
large：Min Heap，保存较大的一半数字。

必须维护：

1. small 中所有元素 <= large 中所有元素。
2. 两个 Heap 的大小差不超过 1。
3. 根据元素总数奇偶性正确计算 Median。

重点解释：

为什么单个 Heap 不足以高效维护 Median？

为什么需要一个 Max Heap 和一个 Min Heap？

如何插入新值并重新平衡？

为什么插入是 O(log n)，
查询 Median 可以是 O(1)？

Python 的 Max Heap 使用负数模拟时，
如何避免符号错误？

当前还有：

NC - Find Median From Data Stream

请将完整 NC 来源归档到正式 LC-295 的 _neetcode/。

保留原有 JPEG 图解。

--------------------------------------------------

额外候选：

LC-0480 - Sliding Window Median

这是 Two Heaps + Lazy Deletion 的重要进阶题。

但它比 LC-295 复杂很多。

本次不要默认创建。

请在第二轮审核时决定是否值得新增。

如果新增，应作为 P2，
并与 Sliding Window 专题建立交叉引用。

==================================================
LEVEL 1
04 - Heap + Greedy 资源优化与选择
==================================================

核心：

Greedy Choice
Optimal Merge
Resource Allocation
Marginal Gain
Sort + Heap

Level 2：
01 - Optimal Merge Pattern

Level 3：

01 - LC-1167 - Minimum Cost to Connect Sticks

教学重点：

每次将两根木棍连接，
代价是它们长度之和。

连接后的木棍可以继续参与后续连接。

使用 Min Heap，
反复选择当前最短的两根木棍。

必须解释：

为什么应该优先合并最小的两个元素？

这与 Huffman Coding
的 Optimal Merge Pattern 存在联系。

给出简洁的 Greedy Exchange Argument。

此题可能是 Premium，
必须保留已有题面与解法。

--------------------------------------------------

Level 2：
02 - 有限资源的最优分配

Level 3：

01 - LC-1642 - Furthest Building You Can Reach

教学重点：

Bricks 和 Ladders 是两种资源。

Ladder 适合承担较大的正高度差。
Bricks 适合承担较小的正高度差。

使用 Min Heap 维护当前由 Ladder
承担的高度差。

当 Heap 大小超过 ladders 数量时，
弹出最小高度差并使用 Bricks 支付。

必须解释：

为什么把 Ladder 留给最大跳跃是安全的？

为什么可以在向前扫描时重新分配已有资源？

这是 Greedy + Heap 的重要代表题。

--------------------------------------------------

Level 2：
03 - 频率重排与边际收益

Level 3：

01 - LC-0767 - Reorganize String
02 - LC-1792 - Maximum Average Pass Ratio

教学重点：

LC-767：

Frequency Map + Max Heap。

每次优先选择当前剩余最多的字符，
但不能产生相邻相同字符。

可以使用：
- 每次取两个不同字符
- 或者暂存上一轮尚不能重新使用的字符

必须正确处理无法构造合法字符串的情况。

解释为何单纯反复弹出最大频率字符
可能违反相邻约束。

LC-1792：

Marginal Gain（边际收益）。

对每一个班级计算：
增加一个保证通过的学生后，
通过率能够提升多少。

每次使用 Max Heap，
选择当前收益最大的班级。

必须解释：

为什么优先选择当前最大边际收益？

为什么每次分配后需要重新计算收益？

为什么不应该仅根据当前通过率排序？

注意浮点数精度与 Heap 比较规则。

--------------------------------------------------

Level 2：
04 - 排序与 Heap 的组合选择

Level 3：

01 - LC-0502 - IPO
02 - LC-2542 - Maximum Subsequence Score

教学重点：

LC-502：

先根据所需资本组织项目。

当前资本为 w。

只允许从 capital[i] <= w 的项目中选择。

使用 Max Heap，
从当前可执行的项目中选出最大利润。

最多执行 k 个项目。

重点理解：

Sorting + Available Candidate Heap。

为什么不能直接把所有利润放进 Heap，
然后忽略资本约束？

LC-2542：

先根据 nums2 的数值排序。

枚举当前选择集合的最小 nums2，
同时使用 Size-K Min Heap
维护最大的 k 个 nums1。

维护 nums1 的总和。

计算：

score = sum(nums1_selected) * min(nums2_selected)

必须说明：

为什么排序后可以固定当前最小 nums2？

为什么 Heap 只需保存 k 个最大 nums1？

为什么这是一种 Sort + Heap + Greedy 模式？

两道题虽然都结合 Sorting 与 Heap，
但维护的候选集合和不变量不同。

不能错误地讲成完全相同的模板。

==================================================
LEVEL 1
05 - Heap + Scheduling 任务调度
==================================================

核心：

Scheduling
Event Simulation
Available Tasks
Cooldown
Resource Allocation
Earliest Deadline First

Level 2：
01 - Frequency Scheduling 与 Cooldown

Level 3：

01 - LC-0621 - Task Scheduler

教学重点：

任务有冷却间隔 n。

可以使用：
Frequency Counting + Max Heap + Cooldown Queue。

也可以使用经典贪心计数公式。

必须说明：

- Cooldown 的含义
- 任务何时可以重新执行
- 为什么不能连续执行同类任务
- Heap 与 Queue 在模拟中分别承担什么职责

特别注意：

这题的数学 Greedy Formula 往往更简洁。

不要为了强行使用 Heap，
就把 Heap Simulation 说成唯一最优方法。

当前 NC - Task Scheduler
应正式整理为 LC-0621。

保留已有图解。

--------------------------------------------------

Level 2：
02 - 动态任务与事件优先级

Level 3：

01 - LC-1834 - Single-Threaded CPU
02 - LC-1353 - Maximum Number of Events That Can Be Attended
03 - LC-2402 - Meeting Rooms III

教学重点：

LC-1834：

任务有：
enqueue_time
processing_time
original_index

先按 enqueue_time 排序。

将已经到达的任务加入 Min Heap。

Heap 按照：
(processing_time, original_index)
决定任务优先级。

CPU 空闲且没有可执行任务时，
应直接把当前时间跳到下一任务的到达时间。

必须解释：
为什么需要同时维护事件时间和可执行任务集合。

LC-1353：

事件有开始日和截止日。

按开始时间排序。

当天所有已经开始且尚未过期的事件
放入 Min Heap。

Heap 按最早结束日期排序。

每天优先参加截止时间最早的事件。

必须解释：
为什么 Earliest Deadline First 是安全的贪心选择。

注意：
不能把已过期事件留在 Heap 中继续处理。

LC-2402：

会议室调度。

需要两个 Min Heap：

available_rooms：
保存当前空闲房间编号。

busy_rooms：
保存 (end_time, room_id)。

先按会议原始开始时间排序。

优先使用编号最小的空闲房间。

没有空闲房间时，
将会议延迟到最早释放的房间，
并保持原会议时长不变。

必须解释：

- 为什么两个 Heap 的排序键不同
- 为什么需要先释放已经结束的会议室
- 为什么要保留原始会议时长
- 为什么需要按会议原始开始时间处理
- 如何正确处理相同结束时间的房间
- 如何统计每个房间被使用的次数

这是一个很有价值的复杂 Heap Scheduling 题，
但应在熟练掌握 LC-1834 后学习。

==================================================
LEVEL 1
06 - Heap + Hash Map 数据结构设计
==================================================

核心：

Heap-based Design
Hash Map
Lazy Deletion
Version Validation
K-way Timeline Merge

Level 2：
01 - 社交信息流与多路合并

Level 3：

01 - LC-0355 - Design Twitter

当前存在：

NC - Design Twitter

请先核对题面与代码，
正式整理为 LC-0355。

将 NC 来源完整保存在 _neetcode/。

保留其 note.md。

教学重点：

实现：

postTweet
getNewsFeed
follow
unfollow

需要结合：

Hash Map
Set
Heap
Timestamp

getNewsFeed：
从用户自己和关注用户的 Tweet Streams
中获取最近 10 条。

优先解释：

将每个用户的 Tweet List
看作按时间降序排列的有序序列。

使用 Max Heap 进行 K-way Merge。

不必每次把所有历史推文全部放进 Heap。

必须解释：
- 时间戳如何维护
- 关注关系如何维护
- 为什么只需要最近 10 条
- 多路归并如何按需推进
- 为什么不会把旧推文当成最新推文

本题是 Heap + System Design 的经典组合。

--------------------------------------------------

Level 2：
02 - 动态优先级与 Lazy Deletion

Level 3：

01 - LC-3408 - Design Task Manager

教学重点：

实现：

add
edit
rmv
execTop

使用：

Heap + Hash Map

管理任务的最新有效状态。

因为 Python heapq
不支持高效删除任意指定元素，
可以采用 Lazy Deletion。

修改任务时：
更新 Hash Map 中的当前任务状态，
并向 Heap 中加入新的优先级记录。

执行任务时：
不断跳过与当前 Hash Map 状态不一致、
已经删除或已失效的 Heap Entry。

必须正确处理：
- priority 最高优先
- priority 相同时 taskId 较大者优先
- edit 后旧 Heap Entry 的失效
- rmv 后旧 Heap Entry 的失效
- 重复修改同一任务
- 执行后任务的删除
- 空 Heap 返回 -1

特别检查：
如果任务可以在历史记录之后重新使用相同 ID，
或者某些状态可能重新出现，
需要保证旧记录不会意外复活。

可以通过 Version / Generation 等方法防止问题。

不要误认为修改 Dictionary
会自动更新已经存在于 Heap 中的 Tuple。

在 README 中讲清楚：

Lazy Deletion 与物理删除的区别。

还应说明：
懒删除可能积累失效记录，
因此 Heap 空间不一定始终等于当前有效任务数量。

==================================================
LEVEL 1
07 - 跨专题与低优先级存档
==================================================

用于保留已有题目，
但不把所有带 Heap 标签的题列入主线。

Level 2：
01 - 简单排序或计数可替代的问题

Level 3：

01 - LC-1337 - The K Weakest Rows in a Matrix

说明：

可以计算每行士兵数量，
再根据：
(soldier_count, row_index)
排序。

也可以使用 Heap。

但它主要是基础排序、计数和 Top K 的练习，
不需要单独记忆新的 Heap 模板。

标记 P2。

--------------------------------------------------

Level 2：
02 - Ordered Set 与相邻元素查询

Level 3：

01 - LC-2817 - Minimum Absolute Difference Between Elements With Constraint

说明：

本题要在动态维护的候选集合中，
寻找最接近当前元素的数值。

常见解法使用：

Ordered Set / Balanced BST
Predecessor / Successor Query

或者支持有序插入和二分查找的数据结构。

它不属于普通 Heap 最擅长解决的问题。

因为：
Heap 只能高效提供全局最小或最大元素，
不能直接高效获取任意目标附近的前驱与后继。

必须在 README 中解释这一差异。

保留已有 JPEG 图解、代码和所有题目资料。

标记 P2。

不要为了保持 Heap 分类而强迫重写成堆解法。

==================================================
四、NC-only 题正式化
==================================================

当前存在以下 NC 题目：

NC - Design Twitter
NC - Last Stone Weight
NC - Task Scheduler
NC - K Closest Points to Origin
NC - Kth Largest Element in a Stream
NC - Kth Largest Element in an Array
NC - Find Median From Data Stream

对应：

LC-0355
LC-1046
LC-0621
LC-0973
LC-0703
LC-0215
LC-0295

请检查题面与原有代码。

其中：

LC-295 已经有正式 LC 版本。

其他六道目前需要检查是否只有 NC 来源。

如果是 NC-only：

1. 建立正式 LC Level 3 目录。
2. 通过现有工具生成标准 LC 文件。
3. 将原 NC 来源全部保存在 _neetcode/。
4. 保留原有 solution.py。
5. 保留 NC metadata 和 PDF。
6. 保留所有笔记与图片。
7. 不得把 NC metadata 冒充成 LC 官方 metadata。

如果已经有 LC 目录：

将 NC 来源完整归档到已有 LC 目录内。

不同来源的代码不能互相覆盖。

==================================================
五、本次明确建议新增的题目
==================================================

第一轮建议新增 7 道不同题目：

LC-0692 - Top K Frequent Words
LC-0373 - Find K Pairs with Smallest Sums
LC-0502 - IPO
LC-2542 - Maximum Subsequence Score
LC-1834 - Single-Threaded CPU
LC-1353 - Maximum Number of Events That Can Be Attended
LC-2402 - Meeting Rooms III

优先核对：
- LeetCode 题号
- Official English Title
- 难度
- 输入约束
- 推荐解法

如果本专题中没有，
且其他专题也没有更适合的主归属，
使用已有 LeetCode 题目生成工具创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据题号生成题目完整文件的能力，
请直接复用。

绝不能覆盖原有 solution.py。

不要生成空 PDF、
虚假的 metadata 或错误题目内容。

如果生成失败，
记录失败原因并保留已有成果。

==================================================
六、Claude Code 第二轮独立审核
==================================================

上述题目是 ChatGPT 第一轮筛选。

你必须独立进行第二轮审核，
确保不会遗漏高价值 Heap 面试 Pattern。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可信的面试题单

如果具备网络访问，
核对最新的题目编号、题名与解法。

不要编造 FAANG 内部真实出题频率。

必须检查以下知识点：

1. Min Heap
2. Max Heap
3. Heapify
4. Top K
5. Kth Largest
6. Size-K Heap
7. Streaming Top K
8. Frequency + Heap
9. K-way Merge
10. Heap Frontier Expansion
11. Two Heaps
12. Median Maintenance
13. Optimal Merge
14. Greedy Resource Allocation
15. Marginal Gain Optimization
16. Sorting + Heap
17. CPU Scheduling
18. Event Scheduling
19. Two Heaps for Resource Scheduling
20. Lazy Deletion
21. Dynamic Priority Updates
22. Heap + Hash Map Design
23. Tie Breaking
24. Amortized Complexity

额外候选：

LC-0253 - Meeting Rooms II
LC-0480 - Sliding Window Median
LC-0632 - Smallest Range Covering Elements from K Lists
LC-2462 - Total Cost to Hire K Workers
LC-0857 - Minimum Cost to Hire K Workers
LC-0218 - The Skyline Problem
LC-2406 - Divide Intervals Into Minimum Number of Groups
LC-0347 - Top K Frequent Elements
LC-0023 - Merge k Sorted Lists

对于每个候选：

1. 检查是否属于核心 Heap Pattern。
2. 检查是否已存在于其他专题。
3. 判断是否真正弥补了知识缺口。
4. 检查是否只是已有题目的重复训练。
5. 衡量其面试价值与学习成本。
6. 决定 P0 / P1 / P2。

重要：

LC-253 和 LC-2406
与会议室/区间分配关系密切。

如果已存在于 Intervals 专题，
优先建立跨专题索引。

LC-347 可能已经存在于 Arrays & Hashing。

LC-23 已经很可能位于 Linked List。

LC-480 是 Two Heaps + Lazy Deletion，
具有教学价值，但实现复杂，
不要默认将它列入 P0。

LC-218 是 Sweep Line + Heap 的复杂组合，
是否新增需要充分考虑其学习成本。

允许独立新增最多 4 道真正有价值的题。

如果发现更多，
选出最有价值的 4 道，
其他放入 README 的 Future Candidates。

可以在有必要时新增 Level 1 或 Level 2。

但必须解释：
新增类别与现有类别在算法不变量上的真实差异。

不要因为一道题有 Heap 标签，
就创建一个独立算法家族。

==================================================
七、跨专题去重
==================================================

允许对整个 leetcode-practice 仓库进行只读扫描。

重点检查：

LC-0023 -> Linked List
LC-0347 -> Arrays & Hashing
LC-0253 -> Intervals
LC-2406 -> Intervals / Heap
LC-0480 -> Sliding Window
LC-0378 -> Binary Search
LC-2817 -> Ordered Set / Binary Search

规则：

本次只能修改：

09-heap (堆)

内部。

如果某题已存在于其他专题：

- 优先保留其原有 Primary Pattern。
- 在当前 README 中添加相对路径索引。
- 不修改其他专题文件。
- 不无意义地重复下载相同题目资料。

如果当前 Heap 目录已经拥有该题的原始文件：

必须保留当前原始学习成果，
不能以跨专题重复为理由删除。

说明每道交叉题的：
Primary Pattern
Secondary Pattern

减少重复记忆，而不是抹除已有学习历史。

==================================================
八、理论资料、模板与工具整理
==================================================

当前存在：

introduction (堆入门)/
  00 - Introduction.pdf
  01 - How does heap look like.py
  02 - Heap operations.py
  04 - Min Heap In Python.py
  05 - Max Heap in Python.py
  06 - Min Heap vs Max Heap in Python.pdf
  07 - heapreplace & heappushpop.pdf

top-k (Top K)/
  多个 Method PDF 与 Python 模板
  kth-largest-smallest/
    两个教学 PDF

utils/
  00 - 究极 cheatsheet.jpg
  00 - Max Heap.png
  00 - Min Heap.png

请先检查全部文件及其引用关系。

建议将纯教学资料整理到：

_resources/
  introduction/
  top-k-templates/
  cheatsheets/

保留原始文件名与内容。

特别注意：

top-k 目录同时包含题目文件夹和教程文件。

必须区分两者：

LeetCode 题目移动到正式 Level 3。
教程、PDF、示例脚本移动到 _resources。

不能因为迁移题目而遗漏其他教程文件。

如果 utils 中存在运行时代码依赖，
需要保留相关路径或安全修复引用。

不能为了目录外观破坏已有工具。

README 应建立理论资料和模板的相对路径索引。

==================================================
九、Git 安全与原文件保护
==================================================

当前仓库存在大量未提交修改及未跟踪文件。

必须特别保护。

执行前：

1. pwd
2. tree
3. git status --short
4. 扫描当前专题所有文件
5. 保存所有原始文件路径清单
6. 为普通文件记录 SHA-256
7. 检查 Symbolic Links
8. 检查重名冲突
9. 检查已有 Python 的 import 依赖
10. 建立完整迁移映射

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖文件
删除未跟踪文件
删除原有代码
覆盖用户笔记
修改当前专题以外的文件

不要自动：

git add
git commit
git push

优先进行安全文件系统移动，
不要无必要地修改 Git 暂存区。

特别保护：

NC - Design Twitter：
note.md

NC - Task Scheduler：
asset-05 - Task Scheduler - Explanation.jpg

NC - Find Median From Data Stream：
asset-07 - Find Median From Data Stream - Explanation.jpeg

LC-2817：
原有 JPEG 图解

以及所有其他：
Python
PDF
PNG
JPEG
Markdown
自定义附件

如果目标文件已经存在但内容不同：
两个版本必须全部保留。

可以使用 _conflicts/ 保存冲突文件。

禁止静默覆盖。

允许只读扫描整个仓库，
但所有新增、移动、重命名和删除空目录操作
必须限制在当前 Heap 专题内部。

如果生成工具无法避免对其他目录写入，
跳过不安全的生成步骤并记录原因。

对于 Symbolic Links，
不得通过链接写入外部文件。

尽量保证 Idempotence（幂等性）。

重复执行不得：
- 重复创建题目
- 叠加编号
- 重复复制 NC 来源
- 覆盖文件
- 丢失资料

==================================================
十、README 与核心模板
==================================================

必须创建：

A. Heap 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对重要 Level 2 创建必要的短 README

根目录 README：

1. Heap 知识地图
2. 7 个 Level 1 家族
3. 各 Level 2 Pattern
4. 所有题目及其相对路径
5. P0 / P1 / P2 优先级
6. 核心 Python Heap 模板
7. Pattern Recognition Guide
8. 主要复杂度分析
9. Heap 与其他数据结构的区别
10. 跨专题索引
11. 第二轮独立审核结果
12. 最终推荐学习顺序

核心 Python 模板至少包括：

Template 1：
Min Heap
heapify / heappush / heappop

Template 2：
Max Heap
使用负数模拟

Template 3：
Size-K Min Heap
维护当前 k 个最大元素

Template 4：
K-way Merge
保存 (value, source_index, element_index)

Template 5：
Two Heaps
维护在线 Median

Template 6：
Heap + Greedy
按照当前优先级执行决策

Template 7：
Scheduling
Sorted Arrivals + Available Heap

Template 8：
Lazy Deletion
Heap + Hash Map + Version / Validation

必须讲解：

- heappushpop 与 heapreplace 的区别
- Python Heap Tuple 的排序规则
- 当 Priority 相等时如何处理 Tie Breaking
- 为什么不能比较不支持排序的自定义 Node 对象
- 为什么可以用 (priority, counter, object) 避免比较对象
- 为什么 Heapify 是 O(n)
- Push / Pop 为什么是 O(log n)
- Peek 为什么是 O(1)
- 维护 k 个元素与维护 n 个元素的复杂度区别
- Python heapq 没有普通的 Decrease-Key 操作
- 为什么 Lazy Deletion 可以安全跳过过期元素
- 为什么重复入堆可能增加空间使用

注意：
不能将所有 Heap 操作都声称为 O(log n)。

也不能把所有 Heap 题的复杂度统一写成 O(n log n)。

必须根据具体 Heap 大小与操作次数分析。

==================================================
十一、Pattern Recognition Guide
==================================================

在 README 中创建简短的识别指南。

例如：

Q1：
是否需要反复获取当前最大或最小元素？
-> Heap。

Q2：
是否只需要维护最大的 k 个元素？
-> Size-K Min Heap。

Q3：
是否需要从多个有序序列中持续取出最小元素？
-> K-way Merge。

Q4：
是否需要在线维护数据流中位数？
-> Two Heaps。

Q5：
是否需要根据某个不断变化的优先级选择任务？
-> Heap + Greedy。

Q6：
是否有任务到达时间、执行时间或资源释放时间？
-> Scheduling + Heap。

Q7：
是否需要修改已经入堆元素的优先级？
-> Heap + Hash Map + Lazy Deletion，
   或根据需求使用其他支持更新的数据结构。

Q8：
是否需要任意值附近的前驱或后继？
-> Ordered Set，而不是普通 Heap。

Q9：
是否只需要一次性得到全部排序结果？
-> Sorting 可能更简单。

Q10：
是否需要维护一个窗口的最大或最小值，
并且删除过期位置？
-> Monotonic Deque 可能更适合。

重点是：
什么时候 Heap 有优势，
什么时候其他数据结构更简单。

==================================================
十二、理论讲解风格
==================================================

使用中文主导、英文专业术语辅助。

例如：

Heap（堆）
Priority Queue（优先队列）
Min Heap（最小堆）
Max Heap（最大堆）
Heap Invariant（堆不变量）
K-way Merge（多路归并）
Lazy Deletion（延迟删除）
Marginal Gain（边际收益）
Greedy Exchange Argument（贪心交换论证）
Amortized Analysis（摊还分析）

每种 Pattern 都使用：

1. 1–3 个决定性观察
2. 核心不变量
3. 为什么需要 Heap
4. Push / Pop 规则
5. 简短正确性证明
6. Python 模板
7. 时间与空间复杂度
8. 代表题目
9. 常见错误

优先解释算法原理和可迁移思想。

不要把所有题目写成冗长教程，
也不要重复复制大量类似代码。

==================================================
十三、P0 / P1 / P2 优先级
==================================================

P0：
核心必练，代表最重要的 Heap 模式。

P1：
重要组合与进阶应用。

P2：
低优先级、特殊技巧或跨专题存档。

建议 P0：

LC-1046 - Last Stone Weight
LC-0703 - Kth Largest Element in a Stream
LC-0215 - Kth Largest Element in an Array
LC-0973 - K Closest Points to Origin
LC-0373 - Find K Pairs with Smallest Sums
LC-0295 - Find Median from Data Stream
LC-1167 - Minimum Cost to Connect Sticks
LC-0621 - Task Scheduler
LC-1834 - Single-Threaded CPU
LC-0355 - Design Twitter

建议 P1：

LC-0692
LC-0378
LC-1642
LC-0767
LC-1792
LC-0502
LC-2542
LC-1353
LC-2402
LC-3408

建议 P2：

LC-1337
LC-2817

如果第二轮独立审核新增题目，
请重新评估优先级。

P0 表示当前学习路线的重要程度，
不代表任何公司有固定出题概率。

README 必须建立：

P0：
最小核心题库。

P0 + P1：
完整 Heap 面试准备路线。

P2：
进阶与存档。

不要将所有题目都列为 P0。

==================================================
十四、数量及完整性检查
==================================================

当前 tree 中：

原始题目来源文件夹约 16 个。

其中 LC-295 与 NC Median
属于同一道题的不同来源。

因此现有约 15 道不同题目。

第一轮建议新增 7 道：

692
373
502
2542
1834
1353
2402

若全部新增，预计：

22 道不同题目。

第一轮 Level 1 分布：

01：5 道
02：2 道
03：1 道
04：6 道
05：4 道
06：2 道
07：2 道

总计：22 道。

其他跨专题索引不计入实体题目数量。

NC-only 正式化不应重复计算为新题。

第二轮审核可适当增加，
但最多自主新增 4 道。

不得为了满足数量而创建虚假题目。

必须检查：

1. 所有旧题目有正确的新路径。
2. 所有旧文件完整保留。
3. NC 来源无丢失。
4. 所有 LC 题号正确。
5. 所有官方英文名称正确。
6. 算法分类与题目相符。
7. Level 1 编号连续。
8. Level 2 编号连续。
9. Level 3 编号连续。
10. 新题标准文件完整。
11. 原有教程和图片完整。
12. README 相对路径正确。
13. 跨专题引用有效。
14. 原始文件 SHA-256 一致。
15. 不存在非预期重复文件夹。
16. 当前 Heap 目录之外没有写入。
17. Git 原有未提交内容没有被破坏。

==================================================
十五、执行顺序
==================================================

请直接执行以下步骤：

1. pwd。
2. 扫描当前 tree。
3. 检查 Git 状态。
4. 保存全部原始文件清单。
5. 记录原始文件 SHA-256。
6. 检查符号链接及 Python 导入依赖。
7. 核对所有现有 LC / NC 题目。
8. 只读扫描其他专题的重复题目。
9. 建立旧目录到新目录的迁移映射。
10. 创建 7 个 Level 1。
11. 创建对应 Level 2。
12. 安全迁移所有旧题。
13. 为 Level 3 重新编号。
14. 将 NC-only 题正式化为 LC 目录。
15. 归档 NC / LC 重复来源。
16. 生成第一轮明确新增的 7 道题。
17. 安全整理 Heap 理论教程。
18. 独立进行第二轮题库审核。
19. 必要时新增少量高价值题目。
20. 更新最终排序和编号。
21. 创建根目录及各 Level 1 README。
22. 创建 Pattern Recognition Guide。
23. 检查 Python 核心模板的正确性。
24. 检查所有旧文件哈希。
25. 检查新增题目资料。
26. 验证所有跨专题链接。
27. 安全清理已经确认空置的旧目录。
28. 运行最终 tree。
29. 检查最终 Git 状态。
30. 输出完整验收报告。

最终报告至少包含：

- 完整最终 tree
- Level 1 / Level 2 分类
- 各分类的算法学习目标
- 迁移的全部旧题
- NC-only 正式化结果
- NC / LC 去重结果
- ChatGPT 推荐的新增题
- Claude Code 独立新增的题
- 未新增但值得考虑的候选
- P0 / P1 / P2 数量
- 跨专题索引
- 原始文件校验结果
- 理论资料迁移结果
- Git 变更摘要
- 失败或未完成的步骤
- 最终建议的复习顺序

不要仅仅生成方案。

请在以上安全限制下直接完成整个 Heap 专题重构。
PROMPT
)"
