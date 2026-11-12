
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/17-design (设计)' && claude "$(cat <<'PROMPT'
请直接执行当前 Design（数据结构设计）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试与 Online Assessment（OA）。

请建立一套：

- 高面试价值
- 高算法迁移性
- 结构清晰
- 接口与状态设计严谨
- 操作复杂度明确
- 记忆成本尽可能低
- 适合长期学习与复习

的 Data Structure Design 学习体系。

这是实际的文件系统操作任务，不是单纯的规划任务。

请实际执行：
目录重构、文件迁移、新题生成、
README 编写、独立审核和完整性验证。

==================================================
一、最重要的学习目标
==================================================

Data Structure Design 的核心不是背诵类的代码。

我希望掌握：

1. API Contract（接口约定）
2. Internal State（内部状态）
3. Data Structure Invariant（数据结构不变量）
4. Time Complexity（时间复杂度）
5. Space Complexity（空间复杂度）
6. Amortized Analysis（摊还分析）
7. Hash Map + Linked List
8. Array + Hash Map
9. Queue / Deque
10. Sliding Window on Data Streams
11. Timestamp-based State
12. Buffer Management（缓冲区管理）
13. State Persistence Across Calls（跨调用状态保持）
14. Incremental Aggregation（增量聚合）
15. Eviction Policy（淘汰策略）
16. Lazy Cleanup（延迟清理）

每道题应首先回答：

Q1. 对外提供哪些方法？
Q2. 每个方法承诺什么行为？
Q3. 需要保存哪些内部状态？
Q4. 每个内部状态分别解决什么问题？
Q5. 如何保持状态之间的一致性？
Q6. 某个方法修改状态后，哪些不变量仍须成立？
Q7. 目标时间复杂度是什么？
Q8. 实际 Python 实现是否达到目标复杂度？
Q9. 是否需要处理重复调用、删除、过期和边界情况？
Q10. 是否有更简单且符合题目约束的方案？

本专题主要是 LeetCode Data Structure Design。

它和大规模分布式 System Design 不完全相同。

不要强行加入：
Distributed Cache
Consistent Hashing
Distributed Rate Limiter
Kafka
Redis Cluster
等复杂分布式系统实现。

这些可以在 README 建立概念联系，
但不属于本次 LeetCode 核心任务。

==================================================
二、Level 1 -> Level N 分类规则
==================================================

优先采用：

Level 1：Data Structure Design 家族
Level 2：具体 Design Pattern
Level 3：LeetCode 题目

必要时允许 Level 4。

但不要为每道题单独创造一个算法家族。

所有同级正式学习目录必须连续编号：

01 - ...
02 - ...
03 - ...

排序依据：

1. 学习依赖关系
2. 数据结构核心性
3. 面试代表性
4. 迁移价值
5. 操作复杂度要求
6. 实现难度
7. 记忆成本

不要按照题号机械排序。

Level 3 命名格式：

01 - LC-0705 - Design HashSet
02 - LC-0706 - Design HashMap

每个 Level 2 内重新从 01 编号。

以下目录不参与学习分类编号：

_resources
_original_sources
_alternative_solutions
_conflicts
_audit
_neetcode

一个题目在当前专题只保留一个正式主目录。

==================================================
三、第一轮建议的六个 Level 1
==================================================

01 - Hash Structures 与稀疏数据设计
02 - Cache 与 O(1) 淘汰策略
03 - Randomized Data Structures
04 - 时间窗口、计数器与限流
05 - 有状态 API、缓冲区与模拟
06 - SQL 与非设计题目存档

下面给出全部第一轮题目及教学要求。

==================================================
LEVEL 1
01 - Hash Structures 与稀疏数据设计
==================================================

核心：

Hashing
Collision Resolution
Bucket
Key-value Mapping
Sparse Representation

--------------------------------------------------
Level 2：
01 - HashSet 与 HashMap 基础实现

题目顺序：

LC-0705 - Design HashSet
LC-0706 - Design HashMap

教学重点：

LC-705：

实现：

MyHashSet()
add(key)
remove(key)
contains(key)

必须真正展示某种 HashSet 内部实现。

例如：

A. Direct Addressing
B. Hash Buckets + Separate Chaining

不能直接使用 Python 内建 set，
然后声称完成了 HashSet 设计练习。

但可以将 Python set 作为对照。

必须解释：

- Key 如何映射到 Bucket
- Hash Collision 是什么意思
- 为什么不同 Key 可能进入相同 Bucket
- 如何正确处理重复 add
- 如何删除不存在的 Key
- 如何处理空 Bucket
- 什么时候 Direct Addressing 合理

LC-706：

实现：

MyHashMap()
put(key,value)
get(key)
remove(key)

重点理解：

Key -> Value Mapping。

可使用：
Buckets + Separate Chaining。

必须解释：

- 同一个 Key 再次 put 应更新 Value
- 为什么不能把相同 Hash Bucket 中的所有 Key 当成同一个 Key
- Hash Collision 如何处理
- 删除 Key 时如何定位具体条目
- 为什么 HashMap 与 HashSet 的状态略有不同

重点讨论：

Average-case vs Worst-case Complexity。

不能无条件声称普通哈希结构
在任何输入与碰撞情况下都是 O(1)。

如果使用题目 Key Range 的特殊性质，
可以介绍 Direct Addressing，
但必须如实说明空间代价。

可以介绍：
Hash Table Load Factor
Hash Table Resizing

但不要求实现完整的工业级 HashMap。

LC-706 原始 note.md 必须完整保留。

--------------------------------------------------
Level 2：
02 - Sparse Representation 与高效内积

题目顺序：

LC-1570 - Dot Product of Two Sparse Vectors

教学重点：

Sparse Vector（稀疏向量）。

绝大部分元素为 0。

核心思想：
不必总是保存所有零元素。

可以采用：

A. Hash Map：
index -> nonzero_value

B. Sorted Pairs：
(index,value)

对于 Dot Product：

sum(a[i] * b[i])

只需要处理两个向量在相同下标处
都具有非零数值的位置。

必须解释：

- 为什么稀疏表示可以节省空间
- 为什么 Dictionary 表示适合按索引查找
- 为什么有序 Pair 列表适合 Two Pointers
- 如何处理长度相同但非零位置不同的两个向量
- 如何正确处理负数与零
- 不同表示的时间和空间复杂度差别

不能声称任意两个 Sparse Vectors
都必须用同一种实现。

重点理解：

Storage Representation
决定可用的高效操作。

建立与 Arrays & Hashing
以及 Two Pointers 专题的跨专题索引。

==================================================
LEVEL 1
02 - Cache 与 O(1) 淘汰策略
==================================================

核心：

Cache
Hash Map
Doubly Linked List
Eviction
Recency
Frequency
O(1) Updates

--------------------------------------------------
Level 2：
01 - LRU Cache

题目顺序：

LC-0146 - LRU Cache

教学重点：

这是整个 Design 专题最重要的核心题之一。

实现：

LRUCache(capacity)
get(key)
put(key,value)

目标：
get、put 平均 O(1) 时间。

推荐核心数据结构：

Hash Map + Doubly Linked List。

Hash Map：
key -> node

Doubly Linked List：
维护最近使用顺序。

必须解释：

- 为什么单纯 Hash Map 不够
- 为什么普通数组移动元素不是 O(1)
- 为什么 Doubly Linked List 可以 O(1) 删除已知 Node
- 为什么 Hash Map 能帮助 O(1) 找到 Node
- 为什么访问某个 Key 后要更新其最近使用位置
- 为什么容量满时应删除最久未使用的 Key

建议用 Dummy Head / Dummy Tail
简化边界处理。

必须明确 Node 顺序：

哪端表示 Most Recently Used？
哪端表示 Least Recently Used？

并在所有方法中保持一致。

核心辅助操作：

remove_node
add_to_mru
evict_lru

可以根据实现自行命名，
但状态变化必须清晰。

重要测试：

1. capacity=1
2. 重复访问同一个 Key
3. put 已存在的 Key
4. 更新 Value
5. 超出 Capacity 时淘汰
6. 淘汰后再次访问
7. 反复删除与重新插入

如果题目保证 capacity > 0，
可以注明该约束。

同时可在稳健性测试中考虑 capacity=0，
但不要把非题目要求的输入
错误地写成官方必测场景。

另外：

Linked List 专题中已有：
NC - LRU Cache。

请只读检查那个专题。

当前 Design 的 LC-146
作为主要学习位置之一保留。

不要修改 Linked List 专题。

在 README 中建立相对路径交叉引用。

--------------------------------------------------
Level 2：
02 - LFU Cache 与频率桶

题目顺序：

LC-0460 - LFU Cache

教学重点：

这是 P2 高级进阶题，
不要求成为核心必背。

实现：

LFUCache(capacity)
get(key)
put(key,value)

当缓存已满：

优先淘汰访问频率最低的 Key。

如果频率相同：

淘汰该频率组中最久未使用的 Key。

因此：

LFU != LRU。

必须同时维护：

Frequency（频率）
Recency（最近使用顺序）

可以使用：

key_to_state
freq_to_ordered_nodes
min_freq

其中每个 Frequency Bucket
需要维护相同频率下的 LRU 顺序。

推荐清晰地使用：

Hash Map + OrderedDict

或者：

Hash Map + Frequency Bucket Doubly Linked Lists。

优先选择可读性高、正确性易于验证的方案。

如果使用 Python OrderedDict，
必须明确它提供的操作及复杂度前提。

必须解释：

- 为什么单个 Hash Map 不足以处理 LFU 淘汰
- 为什么频率相同时还需要 LRU Tie-breaking
- 为什么每次 get 可能更新频率
- 为什么更新已存在 Key 的 Value 也会影响使用频率
- 为什么插入新 Key 的频率为 1
- 为什么需要 min_freq
- 某个频率桶清空后 min_freq 如何更新
- Capacity 为 0 时如何处理

如果使用 Frequency Buckets，
get / put 的目标是平均 O(1)。

不能用每次遍历全部 Key 寻找最低频率
的 O(n) 实现，
然后声称达到目标复杂度。

LC-460 的作用是理解：
LRU -> LFU
如何通过额外状态扩展缓存策略。

不是要求机械记忆两个完全无关的框架。

==================================================
LEVEL 1
03 - Randomized Data Structures
==================================================

核心：

Array + Hash Map
Index Mapping
Swap-and-Pop
Uniform Random Selection
Average O(1)

Level 2：
01 - O(1) 插入、删除与均匀随机访问

题目顺序：

LC-0380 - Insert Delete GetRandom O(1)

教学重点：

这是本次最重要的新增题。

实现：

RandomizedSet()
insert(val)
remove(val)
getRandom()

要求：

insert：平均 O(1)
remove：平均 O(1)
getRandom：O(1)

关键设计：

Array：
支持 O(1) 下标随机访问。

Hash Map：
value -> index

删除元素时：

1. 找到待删除元素的 Index。
2. 取得数组最后一个元素。
3. 必要时将最后一个元素移动到待删除位置。
4. 更新最后一个元素的 Index Mapping。
5. 删除数组末尾元素。
6. 删除待移除元素的 Hash Map 记录。

这称为：

Swap-and-Pop。

必须解释：

为什么不能使用 list.remove(val)
然后声称 O(1)？

为什么删除时使用最后一个元素填补空位
可以避免 O(n) 元素移动？

为什么数组和 Hash Map 中的信息
必须保持一致？

为什么从数组中均匀随机选取 Index
可以保证每个当前元素有相同概率被选中？

重要边界：

- 插入重复元素
- 删除不存在的元素
- 删除最后一个元素
- 删除不是最后一个的元素
- 删除后重新插入
- 删除后只剩一个元素
- 多次 getRandom

特别检查：

当待删除元素恰好是数组最后一个元素时，
不能因为错误的 Mapping 更新顺序
留下无效记录。

Randomness Testing：

对于给定随机种子，
测试 getRandom 返回值属于当前集合。

可以通过大量抽样做基本分布合理性检查。

但是不能把有限次随机实验
当成均匀性严格证明。

必须给出理论说明：

为什么索引均匀 -> 元素均匀。

==================================================
LEVEL 1
04 - 时间窗口、计数器与限流
==================================================

核心：

Sliding Window on Stream
Deque
Timestamp Expiration
Rate Limiting
Amortized Analysis

--------------------------------------------------
Level 2：
01 - Recent Calls 与流式时间窗口

题目顺序：

LC-0933 - Number of Recent Calls
LC-0362 - Design Hit Counter

教学重点：

LC-933：

实现：

RecentCounter()
ping(t)

返回：

[t - 3000, t]

闭区间内的 Ping 数量。

题目中的时间戳按严格递增顺序到达。

使用 Deque：

1. append 当前时间戳。
2. 从队首移除小于 t - 3000 的旧时间戳。
3. 返回 Deque 长度。

必须解释：

为什么可以只从队首删除？

为什么不会出现更旧元素留在队尾？

为什么每个时间戳最多入队一次、出队一次？

因此虽然一次调用可能移除多个元素，
但所有调用总成本可以通过摊还分析理解。

LC-362：

Design Hit Counter。

统计最近 300 秒内的 Hit 数量。

时间窗口：

[t - 299, t]

因此：

timestamp <= t - 300

的记录必须过期。

必须区分它与 LC-933 的窗口长度：

LC-933：3000。
LC-362：300。

LC-362 允许相同 Timestamp 下多次 Hit。

可以使用：

A. Deque of Timestamps

或者：

B. Deque of (timestamp, count)

后者可以压缩同一秒的大量 Hit。

如果需要更小的固定内存，
可以讨论 300 个时间桶的 Circular Buffer，
但必须明确它依赖时间戳语义和数据范围。

不要声称 Deque 方案在任意流量下
都保持 O(1) 空间。

空间取决于有效窗口内的记录数量，
或被压缩后的时间桶数量。

必须讲清楚：

Amortized O(1) 和 Worst-case O(1)
不是完全相同的复杂度承诺。

--------------------------------------------------
Level 2：
02 - 消息去重与时间限流

题目顺序：

LC-0359 - Logger Rate Limiter

教学重点：

实现：

Logger()
shouldPrintMessage(timestamp,message)

同一条 Message 打印后，
在接下来 10 秒内不能再次打印。

使用：

Hash Map：
message -> next_allowed_time

当：

timestamp >= next_allowed_time

可以打印，并更新：

next_allowed_time = timestamp + 10

否则不允许打印。

必须解释：

为什么应该根据上一次实际允许打印的时间
进行更新？

为什么被拒绝打印的消息
不能自动延长其冷却时间？

必须正确处理：

timestamp = last_print + 9
timestamp = last_print + 10

同时注意题目保证时间戳
按非递减顺序输入。

基本 Hash Map 方案
不会自动删除过期的 Message Key。

因此如果消息种类不断增长，
内存也可能不断增长。

可以介绍：

Hash Map + Queue 清理过期记录

但必须注意：
如果加入过期清理，
不能删除已经被后续新打印更新过的状态。

应验证旧 Queue Entry
是否仍对应当前有效状态。

这是最值得学习的：

Timestamp State + Rate Limiting

基础题。

不要将这道题直接扩展成复杂的
Distributed Token Bucket / Leaky Bucket 系统。

可在 README 简要对比概念，
但不强制实现。

==================================================
LEVEL 1
05 - 有状态 API、缓冲区与模拟
==================================================

核心：

Stateful Object
Internal Cursor
Buffer Management
API Sequence
Incremental Aggregation
State Machine

--------------------------------------------------
Level 2：
01 - Buffered Reader 与跨调用状态

题目顺序：

LC-0157 - Read N Characters Given Read4
LC-0158 - Read N Characters Given read4 II - Call Multiple Times

教学重点：

LC-157：

只能通过 read4 API
读取底层文件数据。

实现：

read(buf,n)

需要从文件中读出最多 n 个字符。

每次 read4 最多返回四个字符。

必须解释：

- read4 返回实际读取的字符数
- 为什么不能假定每次返回 4
- 为什么最后一次可能少于 4
- 为什么不能把多读出的字符写入用户输出之外
- 什么情况下应结束读取

LC-157 主要针对单次 read 调用。

LC-158：

与 LC-157 的关键区别：

read(buf,n) 可能调用多次。

一个 read4 调用可能读取超过
当前 read 实际需要的字符数量。

未消费的字符必须保存，
供下一次 read 使用。

推荐内部状态：

buf4
buf4_index
buf4_size

或者等价的内部缓存游标。

必须解释：

为什么如果每次 read 都重新初始化 buf4，
可能丢失预读字符？

为什么必须将内部缓冲区保存在对象实例中？

如何判断：

- 缓冲区还有未消费字符
- 缓冲区已经耗尽，需要调用 read4
- read4 返回 0，已经 EOF

重要测试：

底层数据：
"abcdefg"

连续调用：

read(buf,1)
read(buf,2)
read(buf,3)
read(buf,3)

应返回：
"a"
"bc"
"def"
"g"

最后不足 3 个字符，
只返回实际剩余的字符。

再调用时应返回 0。

测试必须使用可靠的 Mock read4。

不能假定题目执行环境中的 read4
可以在本地直接调用。

LC-158 可能受到 Premium 访问限制。

若无法获得可靠题面，
保留候选索引并报告，
不得伪造标准 PDF。

这组题主要学习：

State Persistence Across API Calls。

--------------------------------------------------
Level 2：
02 - 棋盘状态与历史导航

题目顺序：

LC-0348 - Design Tic-Tac-Toe
LC-1472 - Design Browser History

教学重点：

LC-348：

Design Tic-Tac-Toe。

实现：

TicTacToe(n)
move(row,col,player)

不需要每次扫描整个棋盘判断赢家。

可以维护：

rows
cols
diagonal
anti_diagonal

使用不同玩家对应的正负增量。

当某一行、列或对角线的计数绝对值等于 n，
说明有玩家完成了一整条线。

必须解释：

为什么可以只维护计数？

为什么某个完整获胜线的计数达到 ±n？

为什么每次 move 可以做到 O(1)？

同时注意：
这个方案依赖原题对合法落子过程的保证。

如果需要支持非法或重复落子检测，
则可能需要额外的 Board State。

不能声称仅使用计数就能检测所有非法落子。

LC-1472：

Design Browser History。

实现：

BrowserHistory(homepage)
visit(url)
back(steps)
forward(steps)

推荐：

history Array
current_index

必要时维护当前有效历史边界。

核心规则：

visit(url)
必须删除当前页面之后的 Forward History。

back(steps)
不得越过最早页面。

forward(steps)
不得越过当前历史的最末页面。

必须解释：

为什么 visit 后需要截断 Forward History？

为什么只保存当前 URL 不够？

可以介绍：

A. Array + Cursor
B. Two Stacks

但优先选择清晰可靠的推荐实现。

时间复杂度必须根据实际实现分析。

例如：
Python list 切片删除 Forward History
可能具有 O(n) 成本。

不能把 Array + Cursor 方案的所有方法
无条件声称为 O(1)。

--------------------------------------------------
Level 2：
03 - 多对象状态与增量平均值

题目顺序：

LC-1396 - Design Underground System

教学重点：

实现：

UndergroundSystem()
checkIn(id,stationName,t)
checkOut(id,stationName,t)
getAverageTime(startStation,endStation)

核心状态：

active_checkins：
id -> (start_station,start_time)

route_stats：
(start_station,end_station)
-> (total_duration,trip_count)

当乘客 CheckOut：

1. 根据 id 查找 CheckIn。
2. 计算本次行程 Duration。
3. 更新对应 Route 的 Total Duration。
4. 更新对应 Route 的 Trip Count。
5. 移除当前已完成的 Active Check-in。

当查询平均时间：

average = total_duration / trip_count

必须解释：

为什么不需要保存全部历史行程？

为什么只维护 Sum 与 Count 就足够计算平均值？

为什么 CheckIn 状态和 Route 聚合状态
应该用不同的 Hash Map？

为什么完成 CheckOut 后，
应该删除 Active CheckIn 记录？

为什么 Route Key 必须包含：
Start Station
End Station

并区分方向？

不能将 A->B
和 B->A
自动合并。

这是：

State Tracking + Incremental Aggregation

的重要代表题。

==================================================
LEVEL 1
06 - SQL 与非设计题目存档
==================================================

核心目标是保留原始资料，
但纠正不属于 Data Structure Design 的题目分类。

Level 2：
01 - SQL Aggregation 与 Database Query

题目顺序：

LC-0580 - Count Student Number in Departments

特别重要：

当前目录中：

randomized/
  LC-0580 - Count Student Number in Departments

这个分类明显值得核查。

LC-580 实际是 SQL / Database 问题。

其核心通常是：

LEFT JOIN
GROUP BY
COUNT
ORDER BY

而不是：

Randomization
Random Sampling
RandomizedSet

请执行：

1. 检查 metadata.json。
2. 检查 problem.pdf。
3. 检查 problem_dark.pdf。
4. 检查 solution.py。
5. 验证真实题目是否对应 LC-580。
6. 如果确认是 LC-580，
   将其迁移到此 SQL 存档分类。
7. 保留全部原始文件。
8. 不擅自把原有 solution.py 改成 solution.sql。
9. 不覆盖原始代码或笔记。

在 README 中标记：

Primary Topic：
SQL / Database Query

Secondary Topic：
Aggregation

不应将它纳入 Data Structure Design 核心刷题路线。

如果 solution.py 实际属于其他问题，
而 metadata 或 PDF 属于 LC-580，
必须明确记录文件身份冲突。

不能不经核实就强行统一题目编号。

如果仓库存在 SQL 专题，
只建立相对路径索引。

本次不能修改其他专题。

==================================================
四、第一轮新增的五道题
==================================================

本次建议新增：

LC-0380 - Insert Delete GetRandom O(1)
LC-0460 - LFU Cache
LC-0158 - Read N Characters Given read4 II - Call Multiple Times
LC-1396 - Design Underground System
LC-1472 - Design Browser History

请先只读扫描整个仓库，
确认是否已存在完整题目。

检查：

1. 当前 Design 专题。
2. Linked List。
3. Stack / Queue。
4. Heap。
5. Binary Search。
6. Trie。
7. 其他相关专题。

如果已经有完整主归属，
可以建立跨专题相对路径索引，
避免无意义的重复生成。

如果当前专题确实需要正式题目文件夹，
调用仓库已有 LeetCode 生成工作流创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

必须先检查现有生成工具，
确认其实际能力。

不要假设全部 Premium 题目都能获取。

对于无法获得可靠题面的题目：

- 不伪造 PDF。
- 不创建虚假 metadata。
- 不使用其他题目内容替代。
- 保留候选索引。
- 记录未完成原因。

对于已有 solution.py：
绝对不能覆盖。

新生成的实现应与题目的设计接口严格一致。

==================================================
五、Claude Code 第二轮独立审核
==================================================

上述目录与题目是 ChatGPT 第一轮筛选。

请独立进行第二轮审核。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
可信的 Data Structure Design 面试题单

如果网络可用：
核对题号、英文题名、约束与标准 API。

不得编造 FAANG 内部真实出题概率。

必须审查以下知识覆盖：

1. HashSet
2. HashMap
3. Hash Collision
4. Sparse Representation
5. LRU Cache
6. LFU Cache
7. Doubly Linked List
8. Array + Hash Map
9. Randomized O(1) Operations
10. Streaming Counter
11. Sliding Time Window
12. Rate Limiting
13. Expiration Semantics
14. Buffered Reader
15. Persistent State Across Calls
16. Array Cursor
17. Incremental Aggregation
18. O(1) State Updates
19. Average vs Worst-case Complexity
20. Amortized Analysis
21. Stateful API Sequence Testing

额外候选：

LC-0155 - Min Stack
LC-0622 - Design Circular Queue
LC-0641 - Design Circular Deque
LC-0981 - Time Based Key-Value Store
LC-1146 - Snapshot Array
LC-1797 - Design Authentication Manager
LC-1381 - Design a Stack With Increment Operation
LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed
LC-0432 - All O(1) Data Structure
LC-0355 - Design Twitter
LC-0340? 不要凭题号猜测题目。
LC-3408 - Design Task Manager
LC-0208 - Implement Trie
LC-0729 - My Calendar I
LC-0295 - Find Median from Data Stream

特别注意：

LC-155：
可能已经存在于 Stack 专题。

LC-622、641：
属于 Circular Queue / Deque 的重要设计。
如 Stack & Queue 专题已覆盖，则引用即可。

LC-981：
已有 Binary Search 专题。

LC-355、3408：
与 Heap 专题交叉。

LC-208：
已有 Trie 专题。

LC-729：
已有 Intervals 专题。

LC-295：
已有 Heap 专题。

LC-381：
是 LC-380 允许重复元素的进阶变体。
应先掌握 LC-380 再考虑。

LC-432：
维护所有 Key 的增减计数、
并在 O(1) 查询最大和最小计数。

属于高级复杂结构设计，
不应直接加入核心 P0。

LC-1797：
Expiration / Authentication State，
可能是当前时间窗口设计的有价值扩展。

LC-1146：
Versioned Array / Snapshot，
涉及历史版本访问和 Binary Search，
可作为进阶设计候选。

本次最多独立新增 3 道真正有价值的题目。

新增条件：

1. 有明确的面试代表性。
2. 填补当前重要设计模式缺口。
3. 没有其他专题更合适的现成归属。
4. 具有独立的可迁移知识。
5. 不与现有题高度重复。
6. 学习与记忆成本合理。
7. 可以明确解释 API、状态和复杂度。

如果没有重要遗漏，可以不新增。

候选超过 3 道时，
仅选择最有价值的 3 道，
其余列入 README 的 Future Candidates。

不要为了使 Design 专题显得庞大，
加入几十道高度重复的模拟类题目。

==================================================
六、跨专题引用与避免重复
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0146：
Linked List / LRU Cache。

LC-0155：
Stack / Min Stack。

LC-0208：
Trie / Prefix Tree。

LC-0295：
Heap / Two Heaps。

LC-0355：
Heap / Design Twitter。

LC-0622、0641：
Stack Queue / Circular Buffer。

LC-0729：
Intervals / Dynamic Booking。

LC-0981：
Binary Search / Time-based KV。

LC-1146：
Binary Search / Snapshot。

LC-1570：
Two Pointers / Sparse Representation。

LC-3408：
Heap / Lazy Deletion。

LC-0580：
SQL / Database。

规则：

1. 当前 Design 已有原始文件的题，
   必须保留全部资料。

2. 当前没有、其他专题已经有的题，
   优先通过 README 建立相对路径索引。

3. 不修改其他专题文件。

4. 不无意义地重复下载 PDF。

5. 一个题目可以通过多个算法入口学习。

6. README 应标注：
   Primary Pattern
   Secondary Patterns
   Recommended Data Structure
   Cross-topic References

不要为了对齐所谓完整题单，
就把所有带 Design 标签的题
全部复制进当前目录。

==================================================
七、API Contract 与内部状态对照
==================================================

必须为根 README 生成：

Design API Contract Matrix。

每道题至少记录：

- Constructor
- Public Methods
- Return Values
- Internal State
- Mutation Rules
- Invariant
- Time Complexity
- Space Complexity
- Critical Edge Cases

例如：

LC-146：

API：
get, put

内部状态：
Hash Map + Doubly Linked List

不变量：
链表顺序反映访问新旧程度。

LC-380：

API：
insert, remove, getRandom

内部状态：
Array + Value-to-Index Map

不变量：
每个数组元素的 Index Mapping 正确。

LC-933：

API：
ping

内部状态：
Deque

不变量：
所有保留时间戳都属于有效时间窗口。

LC-157 / LC-158：

API：
read

内部状态：
Buffer / Cursor

不变量：
不能重复消费字符，
也不能丢弃未来仍需读取的字符。

LC-1396：

API：
checkIn, checkOut, getAverageTime

内部状态：
Active Trips + Route Statistics

不变量：
已完成行程对 Total Duration 和 Count
产生一次且仅一次的贡献。

重点是：
每个方法执行后，状态还必须满足什么？

==================================================
八、复杂度与 Python 实现细节
==================================================

这是本次最重要的教学要求之一。

必须严格分析：

1. Python dict 平均 O(1) 操作。
2. Hash Collision 与最坏情况。
3. Python list append / pop() 的摊还复杂度。
4. Python list.pop(index) 与 list.remove 的 O(n) 移动成本。
5. Python deque 从两端操作的效率。
6. Doubly Linked List 已知节点删除的 O(1)。
7. OrderedDict 的相关操作。
8. Heap 不支持高效任意元素删除的问题。
9. Sliding Window Queue 的摊还复杂度。
10. 时间桶计数和内存使用的关系。
11. Array Slicing 的潜在 O(n) 成本。
12. Random Choice 的前提。
13. 内存与状态数量的关系。

不要因为代码短就声称 O(1)。

不要因为题目属于 Design，
就假设必须使用复杂数据结构。

对于符合约束的基础解法，
可以优先选择清晰、简单的实现，
并说明它与更复杂方案的权衡。

==================================================
九、时间语义和边界正确性
==================================================

特别检查：

LC-933：

窗口：
[t-3000,t]

LC-362：

窗口：
[t-299,t]

LC-359：

相同 Message：
在上一次允许打印后满 10 秒才能再次打印。

必须给出准确的测试。

例如：

LC-933：

ping(1)
ping(3001)

在 t=3001 时，
timestamp=1 仍然在有效窗口内。

ping(3002)

此时 timestamp=1 过期。

LC-362：

hit(1)
getHits(300)

timestamp=1 仍然有效。

getHits(301)

timestamp=1 应过期。

LC-359：

shouldPrintMessage(1,"foo") -> True
shouldPrintMessage(10,"foo") -> False
shouldPrintMessage(11,"foo") -> True

必须正确区分：

Inclusive Boundary
Exclusive Boundary
Expiration Time
Last Accepted Event

这些时间边界直接决定设计是否正确。

==================================================
十、测试策略
==================================================

不能只运行一个示例就声称 Design 题正确。

必须创建或运行适当的
Stateful API Sequence Tests。

测试应覆盖：

【HashSet / HashMap】

- 重复插入
- 更新存在的 Key
- 删除不存在的 Key
- Hash Collision
- 边界 Key

【LRU】

- 访问导致顺序变化
- 更新已有 Key
- 容量满时淘汰
- 最近使用顺序正确
- Capacity 边界

【LFU】

- 不同频率
- 相同频率的 LRU 决胜
- get 更新频率
- put 更新已有 Key
- min_freq 更新
- Capacity=0

【RandomizedSet】

- Duplicate Insert
- Remove Missing
- Swap-and-Pop
- Delete Last Element
- Reinsert
- Random Validity

【Time Counters】

- 窗口左边界
- 窗口右边界
- 同一时间重复命中
- 大量过期记录
- 按题目规定的时间顺序输入

【Reader】

- Empty File
- n=0
- read4 返回不足 4
- 文件读完
- Multiple Reads
- Buffer Leftovers

【Browser History】

- Back 到最前面
- Forward 到最末尾
- Back 之后 Visit
- Forward History 被清空
- 重复 Back / Forward

【Underground System】

- 多个乘客
- 同一路线多次行程
- 不同路线
- 不同方向
- 平均值正确
- Checkout 后状态清理

如果需要：
可以编写本专题内部的临时或正式测试脚本。

不能修改其他算法专题。

测试必须使用真正的题目 API 约定。

不能虚构不受题目支持的接口。

==================================================
十一、Git 安全与现有资料保护
==================================================

当前 Git 仓库有大量未提交修改和未跟踪文件。

必须特别保护已有学习资料。

执行前：

1. pwd。
2. 检查当前 tree。
3. git status --short。
4. 递归记录所有原始文件。
5. 计算普通文件的 SHA-256。
6. 记录文件大小。
7. 识别 Symbolic Links。
8. 检查所有 solution.py。
9. 核查题号与 metadata。
10. 检查已有 Markdown 相对链接。
11. 检查 Python import 和依赖。
12. 建立完整迁移映射。

建议在当前目录内部创建：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

所有文件必须限制在当前：

17-design (设计)

目录内部。

允许只读扫描其他专题。

特别保护：

LC-0706 - Design HashMap：
note.md

以及全部原始：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
Markdown
PDF
图片
自定义文件

LC-580 的原始文件必须完整保留，
不能因其实际是 SQL 题而删除。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖任何已有文件
删除未跟踪文件
覆盖用户原始 solution.py
删除学习笔记
删除 PDF 或图解
修改其他算法专题

不要自动：

git add
git commit
git push

如果新目标路径发生文件冲突：

- 不同内容必须保留全部版本。
- 不能简单选择“较新”的文件覆盖。
- 可使用 _conflicts/ 或来源专用目录。
- 记录迁移关系和内容哈希。
- 不允许静默删除来源。

移动符号链接时不得跟随链接
修改当前专题之外的目标。

如果生成工具会写入其他目录，
必须先确认有安全的输出路径配置。

无法限制外部写入时，
跳过相应生成步骤并报告原因。

尽可能保证 Idempotence（幂等性）。

重复运行不能：

- 叠加编号
- 重复创建同题目录
- 重新覆盖学习资料
- 重复归档来源
- 丢失自定义文件

只有确认旧目录已经空置，
才允许安全移除该空目录。

==================================================
十二、README 学习文档
==================================================

必须创建：

A. Design 根目录 README.md。
B. 六个 Level 1 README.md。
C. 重要 Level 2 的短 README.md。
D. Design API Contract Matrix。
E. Data Structure Selection Guide。
F. Design Invariants Cheat Sheet。
G. Stateful API Testing Guide。
H. P0 / P1 / P2 Roadmap。

根目录 README 至少包含：

1. Data Structure Design 知识地图。
2. 六个 Level 1 的目标。
3. 所有 Level 2 / Level 3。
4. 所有题目的真实相对路径。
5. 每道题的 API。
6. 内部数据结构选择。
7. 操作复杂度对照。
8. HashMap + Linked List。
9. Array + HashMap。
10. Queue + Sliding Window。
11. Buffer + Cursor。
12. Incremental Aggregation。
13. 平均与摊还复杂度的区别。
14. 跨专题索引。
15. 第二轮审核结果。
16. 最终学习顺序。

每个 Pattern 应包含：

1. 1–3 个决定性观察。
2. API Contract。
3. Internal State。
4. Core Invariant。
5. Method Operations。
6. 简短正确性证明。
7. Python 核心模板。
8. 时间与空间复杂度。
9. 关键边界测试。
10. 代表题目。
11. 与相邻 Design Pattern 的区别。

必须特别比较：

LRU vs LFU
HashMap vs Array + HashMap
Queue Window vs Timestamp Map
Single-call Reader vs Multi-call Reader
Full History Storage vs Incremental Aggregation

不能只介绍代码怎么写，
必须解释为什么选择这些数据结构。

==================================================
十三、Data Structure Selection Guide
==================================================

请在 README 建立：

Q1：
是否需要通过 Key 快速查找某个 Value？
-> Hash Map。

Q2：
是否需要快速判断 Key 是否存在？
-> Hash Set。

Q3：
是否需要 O(1) 删除已知元素，
同时保持访问顺序？
-> Hash Map + Doubly Linked List。

Q4：
是否需要 O(1) 插入、删除与均匀随机选择？
-> Array + Hash Map。

Q5：
是否需要反复移除最旧的时间戳？
-> Queue / Deque。

Q6：
是否需要根据 Frequency + Recency 淘汰元素？
-> Frequency Buckets + LRU Ordering。

Q7：
是否需要在连续 API 调用之间保存未消费数据？
-> Persistent Buffer + Cursor。

Q8：
是否需要前进、后退、丢弃未来历史？
-> Array + Cursor 或 Two Stacks。

Q9：
是否要累计历史平均值，
但不需要查询每一条历史记录？
-> Running Sum + Count。

Q10：
是否只需维护当前可用对象的优先级？
-> Heap + Hash Map 等结构，
   根据更新与删除需求判断。

强调：

选择数据结构是由所需操作决定的。

同一种业务描述
可以存在多种正确的内部结构。

==================================================
十四、理论讲解风格
==================================================

使用中文主导 + 英文专业术语。

例如：

Data Structure Design（数据结构设计）
API Contract（接口约定）
Internal State（内部状态）
Data Structure Invariant（数据结构不变量）
Amortized Analysis（摊还分析）
Hash Collision（哈希冲突）
Doubly Linked List（双向链表）
Eviction Policy（淘汰策略）
Stateful API（有状态接口）
Incremental Aggregation（增量聚合）

每个 Pattern 先回答：

- 为什么选择这种数据结构？
- 需要维护什么状态？
- 为什么状态不变量成立？
- API 调用后如何更新状态？
- 复杂度如何证明？

然后给出 Python 模板和边界测试。

避免冗长空泛的理论。

不要把每道题都写成完全独立的教材。

==================================================
十五、P0 / P1 / P2
==================================================

P0：
优先熟练掌握的核心设计题。

建议：

LC-0705 - Design HashSet
LC-0706 - Design HashMap
LC-0146 - LRU Cache
LC-0380 - Insert Delete GetRandom O(1)
LC-0933 - Number of Recent Calls
LC-0362 - Design Hit Counter

P1：
重要 API 与状态设计变体。

建议：

LC-1570 - Dot Product of Two Sparse Vectors
LC-0359 - Logger Rate Limiter
LC-0157 - Read N Characters Given Read4
LC-0158 - Read N Characters Given read4 II - Call Multiple Times
LC-0348 - Design Tic-Tac-Toe
LC-1396 - Design Underground System
LC-1472 - Design Browser History

P2：
高级复杂实现或跨专题存档。

建议：

LC-0460 - LFU Cache
LC-0580 - Count Student Number in Departments

其中：

LC-580 必须标记为非 Data Structure Design。

第二轮可以调整优先级，
但必须说明理由。

P0 是学习优先级，
不是企业内部真实出题频次。

README 提供：

P0：核心面试路线。
P0 + P1：完整设计题准备。
P2：高级进阶与存档。

不要将所有 Design 题都标记 P0。

==================================================
十六、数量与完整性验证
==================================================

当前提供的 tree：

16 个目录。
41 个文件。

其中题目来源：

10 道。

已存在：

LC-0146
LC-0157
LC-0348
LC-0705
LC-0706
LC-1570
LC-0580
LC-0359
LC-0362
LC-0933

目前没有已知的 NC-only 题目。

也没有已知的同题 LC / NC 双来源。

第一轮建议新增：

LC-0380
LC-0460
LC-0158
LC-1396
LC-1472

如果全部成功：

第一轮共有：

15 道不同题目。

预期 Level 1 分布：

01：3 道
02：2 道
03：1 道
04：3 道
05：5 道
06：1 道

总计：15 道。

其中 LC-580 是非设计题存档。

如果某些新题已经在其他专题，
只建立索引而不重复生成，
最终实体题目目录数可以少于 15。

第二轮最多新增 3 道不同题目。

不能为了达到数量制造虚假文件。

最终必须验证：

1. 原始 10 道题都有正确归属。
2. 原始 41 个文件全部可追溯。
3. LC-580 被正确识别为 SQL 题。
4. 5 道新题均已处理。
5. 题号与官方英文题名正确。
6. 各级编号连续。
7. 原有 solution.py 完整保留。
8. 原有 PDF、note.md 完整。
9. 新题标准文件存在，或记录限制。
10. README 相对路径有效。
11. HashMap / Cache / Counter 实现通过测试。
12. LC-380 删除与随机测试通过。
13. LC-158 跨调用 Buffer 测试通过。
14. 旧文件 SHA-256 一致。
15. 当前 Design 目录以外没有写入。
16. Git 原有未提交内容未丢失。
17. 第二轮审核记录完整。

如果无法完成某项检查，
在最终报告中明确说明，
不能未经验证就声称通过。

==================================================
十七、最小核心学习路线
==================================================

请在根 README 创建：

Data Structure Design Core Roadmap。

推荐：

阶段 A：
Hash Structures

LC-705 -> LC-706 -> LC-1570

阶段 B：
Array / Hash Map 组合

LC-380

阶段 C：
LRU Cache

LC-146

阶段 D：
Stream Counters

LC-933 -> LC-362 -> LC-359

阶段 E：
Stateful Interfaces

LC-348 -> LC-1472 -> LC-1396

阶段 F：
Buffer Management

LC-157 -> LC-158

阶段 G：
Advanced Cache

LC-460

阶段 G 为选修进阶。

LC-580 只保留在 SQL 存档，
不进入 Data Structure Design 核心路线。

另外请输出：

6–8 道最核心 Design 面试题。

优先覆盖不同内部结构组合，
避免推荐大量相似的简单计数类。

==================================================
十八、实际执行步骤
==================================================

请直接执行：

1. pwd。
2. 扫描完整目录。
3. 检查 Git 状态。
4. 记录原始文件 Manifest。
5. 计算 SHA-256。
6. 检查符号链接。
7. 读取原有 10 道题的 metadata 和 solution。
8. 验证 LC-580 的实际身份。
9. 检查 LC-146 与 Linked List 的跨专题关系。
10. 只读检查仓库的其他 Design 题。
11. 建立完整迁移映射。
12. 创建 6 个 Level 1。
13. 创建对应 Level 2。
14. 安全迁移原有题目。
15. 为所有 Level 3 重新编号。
16. 创建 LC-380。
17. 创建 LC-460。
18. 创建 LC-158。
19. 创建 LC-1396。
20. 创建 LC-1472。
21. 独立进行第二轮题库审核。
22. 必要时新增最多 3 道高价值题。
23. 根据审核结果调整目录与编号。
24. 创建根目录 README。
25. 创建六个 Level 1 README。
26. 创建 Design API Contract Matrix。
27. 创建 Data Structure Selection Guide。
28. 创建 Design Invariants Cheat Sheet。
29. 创建 Stateful API Testing Guide。
30. 创建 P0 / P1 / P2 Roadmap。
31. 检查新增 Python 代码语法。
32. 执行符合题目接口的 API Sequence Tests。
33. 测试时间窗口边界。
34. 测试缓存淘汰策略。
35. 测试 RandomizedSet。
36. 测试 Reader 跨调用状态。
37. 检查旧文件哈希。
38. 检查 README 相对路径。
39. 验证所有目录编号连续。
40. 安全清理已确认空置的旧目录。
41. 运行最终 tree。
42. 再次检查 Git 状态。
43. 输出完整验收报告。

最终报告必须包括：

- 完整最终 tree
- 六个 Level 1
- 所有 Level 2 Pattern
- 原有 10 道题目的迁移结果
- LC-580 SQL 分类修正
- 第一轮新增的 5 道题
- 第二轮自主新增题
- 未新增候选及原因
- P0 / P1 / P2 统计
- API Contract Matrix
- 核心 6–8 题路线
- 跨专题索引
- 旧文件 SHA-256 验证
- 新增实现的测试结果
- Git 变更摘要
- 未完成或失败项目及原因

如果遇到文件损坏风险或越界写入风险，
保持该部分原始文件不变，
清楚报告问题，
继续完成其他安全任务。

不要只输出目录规划。

请在上述安全约束下直接执行
Design 专题的完整重构。
PROMPT
)"
