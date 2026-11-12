
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/14-intervals (区间)' && claude "$(cat <<'PROMPT'
请直接执行当前 Intervals（区间）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试与 Online Assessment（OA）。

请将该目录建设为一套：

- 高面试价值
- 高算法迁移性
- Pattern 分类清晰
- 学习顺序合理
- 能够减少机械记忆
- 包含简短正确性证明
- 适合长期复习和扩展

的 Intervals 学习体系。

这是一项实际的文件系统重构任务，不是规划任务。

请直接进行目录创建、文件迁移、NC 正式化、新题生成、第二轮独立审核、README 编写及完整性验证。

==================================================
一、核心学习目标
==================================================

我希望重点掌握少量可复用的 Interval Patterns：

1. Sort + Merge（排序与合并）
2. Insert Interval（区间插入）
3. Interval Containment（区间包含）
4. Two Pointers Intersection（双指针求交集）
5. K-way Interval Merge（多路区间归并）
6. End-time Greedy（按结束时间贪心）
7. Interval Scheduling（区间调度）
8. Minimum Resource Allocation（最少资源分配）
9. Sweep Line（扫描线）
10. Difference Array（差分数组）
11. Offline Queries（离线查询）
12. Heap with Active Intervals（活动区间优先队列）
13. Dynamic Booking（动态区间预订）
14. Interval Endpoint Semantics（区间端点语义）

特别强调：

不能将所有 Interval 问题都当成 Merge Intervals。

必须区分：

- 合并全部区间
- 插入一个新区间
- 求两个区间序列的交集
- 选择最多不重叠区间
- 计算最少会议室数量
- 查询覆盖某个位置的最短区间
- 在线判断新预订是否冲突

这些问题具有不同的目标函数和算法不变量。

==================================================
二、文件夹层级与排序原则
==================================================

优先使用：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

确实有需要时，可以增加 Level 4。

但不要为了层级数量而创建无意义的目录。

所有同级正式学习目录使用连续编号：

01 - ...
02 - ...
03 - ...

排序根据：

1. 学习依赖关系
2. 面试代表性
3. 算法迁移性
4. 正确性证明的可复用性
5. 难度递进
6. 记忆成本

不得机械按 LeetCode 题号排序。

Level 3 命名格式：

01 - LC-0056 - Merge Intervals
02 - LC-0057 - Insert Interval

每个 Level 2 中独立从 01 开始编号。

以下目录不参与算法编号：

_resources
_neetcode
_original_sources
_alternative_solutions
_conflicts
_audit

每道题在当前专题内只保留一个正式学习位置。

==================================================
三、第一轮 Level 1 分类
==================================================

建议建立 5 个 Level 1：

01 - 区间合并、插入与范围整理
02 - 双指针区间交集与多路合并
03 - 不重叠区间与贪心调度
04 - 重叠计数、扫描线与资源分配
05 - 离线区间查询与动态预订

下面是完整目标题库。

==================================================
LEVEL 1
01 - 区间合并、插入与范围整理
==================================================

核心：

Sorting
Interval Union
Interval Insertion
Containment
Range Gaps

--------------------------------------------------
Level 2：
01 - 标准区间合并与插入

题目顺序：

LC-0056 - Merge Intervals
LC-0057 - Insert Interval

教学重点：

LC-56：

这是整个 Intervals 专题最基础的核心题。

先按 start 排序。

维护已合并区间的最右端点。

对于当前区间 [start, end]：

如果与上一个合并区间重叠，
扩展其 right endpoint。

否则创建新的独立区间。

必须解释：

- 为什么需要先排序
- 为什么只需要与最后一个合并区间比较
- 为什么重叠时取 max(end)
- 为什么不需要检查之前全部区间
- 什么情况下端点相等也需要合并
- 时间复杂度为什么是 O(n log n)

LC-57：

给定已经按 start 排序、互不重叠的区间，
插入一个新区间。

推荐按照三个阶段：

1. 完全位于新区间左侧
2. 与新区间重叠
3. 完全位于新区间右侧

必须解释：

为什么可以使用 O(n) 时间完成插入？

为什么不一定需要把全部区间重新排序？

必须正确处理：
- 空 intervals
- 插入最前面
- 插入最后面
- 新区间覆盖多个旧区间
- 新区间被已有区间包含
- 端点相等

LC-56 和 LC-57 应作为同一组核心模板。

--------------------------------------------------
Level 2：
02 - 区间包含与冗余消除

题目顺序：

LC-1288 - Remove Covered Intervals

教学重点：

判断某个区间是否被其他区间完全包含。

推荐排序方式：

start 升序
end 降序

即：

intervals.sort(key=lambda x: (x[0], -x[1]))

然后维护此前扫描过的最大 end。

必须解释：

为什么在 start 相同时，
应该优先处理 end 更大的区间？

为什么排序后，
只要当前 end 不超过之前的最大 end，
就可以判定该区间被覆盖？

特别注意：

LC-1288 的原题将区间表示为半开区间，
但包含判定仍然依赖端点的相对大小。

不要把它与 LC-56 的“区间相交需要合并”
混为一谈。

这道题属于 P1。

--------------------------------------------------
Level 2：
03 - 连续整数区间与缺失范围

题目顺序：

LC-0228 - Summary Ranges
LC-0163 - Missing Ranges

教学重点：

LC-228：

将有序且互不重复的整数数组，
压缩成若干最大连续整数区间。

例如：

[0,1,2,4,5,7]

对应：

[0,2]
[4,5]
[7,7]

必须解释：
为什么当 nums[i] != nums[i-1] + 1
时可以结束当前连续区间？

LC-163：

给定 lower、upper 及有序数组，
找出指定范围中的所有缺失区间。

重点处理：
- lower 之前的边界
- 两个相邻值之间的缺口
- upper 之后的边界
- 空数组
- 完全没有缺失值

不能把 LC-228 与 LC-163 当成同一道题。

它们共享有序整数范围扫描思想，
但输出目标不同。

这组题标记 P2（针对核心 Intervals 面试路线）。

==================================================
LEVEL 1
02 - 双指针区间交集与多路合并
==================================================

核心：

Two Pointers
Sorted Interval Streams
Intersection
K-way Merge
Free-time Detection

--------------------------------------------------
Level 2：
01 - 两个有序区间序列求交集

题目顺序：

LC-0986 - Interval List Intersections

教学重点：

这是本次最重要的新增核心题之一。

给定两组：

- 已排序
- 各组内部互不相交

的闭区间。

使用两个指针：

i
j

分别指向两个区间序列中的当前区间。

对于：

A = [a_start, a_end]
B = [b_start, b_end]

交集：

left = max(a_start, b_start)
right = min(a_end, b_end)

如果：

left <= right

则存在有效交集 [left, right]。

之后移动结束端点更早的区间对应指针。

必须提供简短证明：

为什么结束更早的区间，
不可能再与另一组后续区间
产生尚未发现的有效交集？

特别注意：

[1,2] 和 [2,3] 的交集是 [2,2]。

因此这里必须使用：

left <= right

不能误写成：

left < right

目标复杂度：

O(m+n)。

这是 Two Pointers 在 Intervals 中的经典应用。

--------------------------------------------------
Level 2：
02 - 多人时间表与公共空闲区间

题目顺序：

LC-0759 - Employee Free Time

教学重点：

每个员工都有一个已经排序、
内部互不重叠的工作区间列表。

目标是找到所有员工共同的有限空闲区间。

可以使用：

A. Flatten + Sort + Merge

或者：

B. K-way Merge + Min Heap

本专题优先讲清楚：
所有工作区间的并集，
以及并集相邻区间之间的 Gap。

必须解释：

为什么应先合并所有员工的忙碌时间？

为什么两个忙碌区间之间存在正长度间隔，
就代表所有员工都空闲？

为什么零长度 Gap 不应输出？

为什么不输出负无穷和正无穷方向的空闲区间？

如果采用 Heap，
说明如何把每个员工的时间表
视为一个有序 Interval Stream。

这道题也可以建立与：
LC-56 Merge Intervals
LC-23 Merge k Sorted Lists
的跨专题联系。

注意：

LC-759 是 Premium 题目。

必须确认当前仓库是否具有合法可用的题面来源。

如果无法获取可靠题面和标准资料，
不得编造 PDF 或 metadata。

可以只建立学习索引，
并记录题目生成受限的原因。

==================================================
LEVEL 1
03 - 不重叠区间与贪心调度
==================================================

核心：

Interval Scheduling
Conflict Detection
Earliest Finish Time
Maximum Compatible Intervals
Minimum Removals
Minimum Points to Cover Intervals

--------------------------------------------------
Level 2：
01 - 冲突检测与最大兼容区间数量

题目顺序：

LC-0252 - Meeting Rooms
LC-0435 - Non-overlapping Intervals

教学重点：

LC-252：

检查一个人能否参加全部会议。

按照 start 排序，
然后检查相邻会议是否发生重叠。

在正常会议时间语义下：

previous_end <= current_start

表示没有冲突。

必须解释：

为什么排序后只需比较相邻区间？

这道题是 Interval Conflict Detection 基础。

LC-435：

需要移除最少数量的区间，
让剩余区间互不重叠。

等价于：

最大化保留的不重叠区间数量。

推荐按 end 升序排序。

每次优先选择结束时间最早的兼容区间。

必须给出 Exchange Argument：

如果一个最优解的第一个区间
并不是结束最早的区间，
可以将其替换为结束更早的合法区间，
且不会减少后续可安排区间的数量。

因此选择最早结束的区间是安全的。

必须解释：
为什么这里按照 start 贪心通常不正确？

重点区分：

LC-252：
判断是否全部兼容。

LC-435：
在存在冲突时选择最大兼容子集。

两题共享排序和重叠检测，
但优化目标不同。

--------------------------------------------------
Level 2：
02 - 最少覆盖点与区间射击

题目顺序：

LC-0452 - Minimum Number of Arrows to Burst Balloons

教学重点：

每个气球对应一个闭区间。

一支箭射在某个坐标，
可以击中覆盖该坐标的所有区间。

目标：
使用最少箭数击中全部气球。

推荐：
按照区间结束端点排序。

优先将箭射在当前最早结束区间的右端点。

然后继续扫描，
只有新区间无法被当前箭覆盖时，
才增加新箭。

必须解释：

为什么选择当前最早结束端点是安全的？

为什么一支箭的位置应尽可能保留
对后续区间的覆盖能力？

特别注意：

[1,2] 和 [2,3]

在闭区间语义下共用位置 2，
因此可以用同一支箭击中。

不要把这一题的边界判定
错误地套用到 Meeting Rooms。

建立与 LC-435 的对比：

435：
选择最多不冲突区间。

452：
寻找最少点，使每个区间都包含至少一个选定点。

两题可以共享 End-time Sorting 思想，
但目标和更新规则不同。

==================================================
LEVEL 1
04 - 重叠计数、扫描线与资源分配
==================================================

核心：

Maximum Overlap
Minimum Meeting Rooms
Event Sorting
Sweep Line
Difference Array
Prefix Sum
Capacity Constraints

--------------------------------------------------
Level 2：
01 - 最少会议室与最大并发数

题目顺序：

LC-0253 - Meeting Rooms II

教学重点：

给定多个会议区间，
求同时安排所有会议所需的最少房间数量。

关键观察：

所需会议室数量 =
任意时刻同时进行的最大会议数量。

必须提供两种核心思路：

A. Sorting + Min Heap

按会议开始时间排序。

Heap 保存当前正在使用的会议室结束时间。

如果最早结束会议：

end <= current_start

则可以复用对应会议室。

否则需要新会议室。

B. Sweep Line

将会议开始、结束转换成时间事件。

开始时并发数 +1，
结束时并发数 -1。

记录最大并发数。

必须解释：

当结束和开始发生在相同时间时，
应当允许会议室立即复用。

如果逐事件处理，
应先处理结束事件再处理开始事件。

如果使用同一时间点的净变化进行合并，
必须说明这种事件聚合为何正确。

重点比较：

LC-252：
是否存在会议冲突。

LC-253：
冲突存在时，需要多少个房间。

这不是同一个目标。

额外交叉题：

LC-2406 - Divide Intervals Into Minimum Number of Groups

这道题的区间是闭区间。

当一个区间 end == 另一个区间 start 时，
二者仍然重叠。

因此 LC-2406 复用资源的端点条件
与 LC-253 不同。

如果 LC-2406 已存在于 Heap 专题，
建立跨专题索引。

本次不强制创建重复目录。

--------------------------------------------------
Level 2：
02 - 差分事件与容量约束

题目顺序：

LC-1094 - Car Pooling
LC-2021 - Brightest Position on Street

教学重点：

这两道题用于掌握：

Difference Array（差分数组）
Sweep Line（扫描线）
Prefix Sum（前缀和）

LC-1094：

乘客在指定位置上车和下车。

每次行程提供：

numPassengers
from
to

在：

from：乘客数量增加
to：乘客数量减少

在同一位置下车和上车时，
应正确处理释放容量的时机。

可以使用：

delta[from] += passengers
delta[to] -= passengers

然后按位置扫描累计人数，
判断是否超过 capacity。

必须解释：

为什么不需要逐段模拟每辆车的所有乘客？

为什么 Difference Array 能表示一组区间的影响？

什么时候可以使用固定长度数组，
什么时候应使用 Sorted Events？

LC-2021：

每盏路灯覆盖某个整数坐标范围。

需要求照明亮度最高的最小整数位置。

可以使用：
Event Map / Difference Array。

特别注意：

灯光照亮的整数位置范围包含右端点。

如果使用差分数组，
右端点对应的撤销事件应放在：

right + 1

必须解释：

为什么直接在 right 做减法会出现 Off-by-one Error？

还需要正确处理：
- 负坐标
- 多个事件位于相同坐标
- 最大亮度相同，返回最小位置
- 右端点包含语义

这组题应该让人理解：
Sweep Line 本质上是按坐标处理事件，
而 Difference Array 是其中一种特殊实现。

不能把二者完全等同。

==================================================
LEVEL 1
05 - 离线区间查询与动态预订
==================================================

核心：

Offline Query
Sort Queries
Active Interval Heap
Lazy Removal
Online Interval Insertion
Calendar Booking

--------------------------------------------------
Level 2：
01 - 最短覆盖区间的离线查询

题目顺序：

LC-1851 - Minimum Interval to Include Each Query

教学重点：

这是整个 Interval 专题最值得学习的 Hard 题之一。

给定 intervals 和多个 queries。

对于每个 query，
返回覆盖该 query 的最短区间长度。

若不存在则返回 -1。

区间为闭区间。

长度：

right - left + 1

推荐：

Sorting + Min Heap + Offline Queries。

步骤：

1. 将 intervals 按左端点排序。
2. 将 queries 和原始下标一起排序。
3. 对每个 query：
   将 left <= query 的区间加入 Heap。
4. Heap 保存：
   (interval_length, right_end)
5. 删除 Heap Top 中已经过期的区间。
6. Heap Top 的长度就是当前最小合法长度。
7. 按 query 原始下标恢复答案顺序。

必须解释：

为什么需要 Offline Sorting？

为什么普通逐 Query 扫描全部区间太慢？

为什么 Heap 应当按 Length 排序，
而不是按 Right Endpoint 排序？

为什么仅检查并移除 Heap Top 中的过期区间
就足以保证当前答案正确？

特别注意：

Heap 内部可能仍包含已经过期、
但尚未到达 Heap Top 的记录。

这属于 Lazy Removal。

不能因此声称 Heap 中所有元素始终有效。

正确不变量是：

回答查询前，
Heap Top 必须是当前仍然覆盖 Query 的
最短候选区间。

这是 Intervals + Heap 的重要组合。

--------------------------------------------------
Level 2：
02 - 在线插入与区间冲突检测

题目顺序：

LC-0729 - My Calendar I

教学重点：

实现：

MyCalendar()
book(startTime, endTime)

每次尝试插入一个新预订。

只在不产生重叠的情况下接受。

区间是半开区间：

[startTime, endTime)

因此：

[10,20)
[20,30)

可以同时存在。

最基础方案：

维护已经接受的区间列表。

如果：

start < existing_end
且
end > existing_start

则存在非空交集，需要拒绝预订。

否则插入。

必须解释：

为什么重叠判定需要严格不等号？

为什么端点相等不冲突？

可以介绍：

Sorting + Binary Search
Balanced BST
Ordered Map

等更复杂方案。

但默认只要求清晰正确的基础实现。

若使用普通 Python list：
必须如实说明查找、插入及搬移的复杂度。

不能因为调用 bisect 就认为动态插入整体 O(log n)。

对于题目给定的有限操作次数，
O(n) 单次检查也是合理的基础方案。

==================================================
四、原有 NC-only 题目正式化
==================================================

当前有 9 道不同题目：

LC-0163 - Missing Ranges
LC-0228 - Summary Ranges
LC-2021 - Brightest Position on Street

NC - Insert Interval
NC - Merge Intervals
NC - Meeting Rooms
NC - Meeting Rooms II
NC - Minimum Interval to Include Each Query
NC - Non-overlapping Intervals

其中 6 个 NC-only 对应：

NC - Insert Interval
-> LC-0057 - Insert Interval

NC - Merge Intervals
-> LC-0056 - Merge Intervals

NC - Meeting Rooms
-> LC-0252 - Meeting Rooms

NC - Meeting Rooms II
-> LC-0253 - Meeting Rooms II

NC - Minimum Interval to Include Each Query
-> LC-1851 - Minimum Interval to Include Each Query

NC - Non-overlapping Intervals
-> LC-0435 - Non-overlapping Intervals

必须检查各题的实际题面、
metadata.json 和 solution.py。

确认对应后：

1. 建立正式 LC Level 3 目录。
2. 保留 NC 原始资料在 _neetcode/。
3. 使用现有生成工作流补齐正式 LC 文件。
4. 不覆盖 NC 原始 solution.py。
5. 不覆盖 NC metadata.json 或 PDF。
6. 保留全部笔记、图解和附件。
7. 同一道题只占据一个正式 Level 3 位置。

特别保护：

NC - Insert Interval：
note.md

NC - Merge Intervals：
asset-02 - Explanation.jpeg

NC - Minimum Interval to Include Each Query：
asset-06 - Explanation.pdf

NC - Non-overlapping Intervals：
asset-03 - Explanation.pdf

LC-2021：
explanation.md
note.md

以及所有其他现有文件。

注意：

LC-252、253、163、759 可能涉及 Premium 访问限制。

对于已有 NC 来源，
必须保留可访问的原始资料。

如果无法合法获得正式 LC 题面，
可以创建正式题号目录并归档 NC 来源，
但不能伪造标准 PDF 或声称生成成功。

在报告中明确记录缺失的标准文件。

==================================================
五、第一轮明确新增的六道题
==================================================

建议新增：

LC-0986 - Interval List Intersections
LC-0452 - Minimum Number of Arrows to Burst Balloons
LC-1288 - Remove Covered Intervals
LC-1094 - Car Pooling
LC-0729 - My Calendar I
LC-0759 - Employee Free Time

执行前：

1. 检查当前 Intervals 目录。
2. 只读扫描整个仓库。
3. 验证是否已有完整题目。
4. 核对官方题号和名称。
5. 检查是否存在跨专题重复。
6. 确定主归属。

如果真正缺失：
调用现有的 LeetCode 题目生成工具。

标准文件：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你可以复用仓库已有的题目生成能力。

不能未经验证就假定生成工具一定支持
全部 Premium 题目。

禁止：

- 伪造题面
- 生成空白 PDF
- 把其他题目的 PDF 复制为当前题目
- 覆盖原有 solution.py
- 删除旧笔记
- 修改仓库其他专题

如果生成工具失败：
记录失败原因，
保留成功完成的文件，
继续处理其余安全任务。

==================================================
六、Claude Code 第二轮独立审核
==================================================

上述推荐是 ChatGPT 第一轮筛选。

你还必须独立审核题库。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可靠的 Intervals 学习资料

如网络访问可用，
请核对题号、题名和典型解法。

不要编造 FAANG 实际出题频次。

必须检查：

1. Interval Sorting
2. Merge Intervals
3. Insert Interval
4. Interval Containment
5. Interval Intersection
6. Two-pointer Interval Scan
7. K-way Interval Merge
8. Interval Scheduling
9. Earliest Finish Time Greedy
10. Minimum Removals
11. Minimum Covering Points
12. Maximum Concurrent Overlap
13. Meeting Rooms
14. Sweep Line
15. Difference Array
16. Coordinate Events
17. Offline Interval Queries
18. Heap with Active Intervals
19. Lazy Removal
20. Online Interval Booking
21. Half-open vs Closed Boundaries

额外审核候选：

LC-1229 - Meeting Scheduler
LC-2406 - Divide Intervals Into Minimum Number of Groups
LC-0731 - My Calendar II
LC-0732 - My Calendar III
LC-1109 - Corporate Flight Bookings
LC-0352 - Data Stream as Disjoint Intervals
LC-1272 - Remove Interval
LC-1326 - Minimum Number of Taps to Open to Water a Garden
LC-2276 - Count Integers in Intervals
LC-218 - The Skyline Problem

这些只是候选，不要求全部新增。

重点判断：

LC-1229：
可以复用 LC-986 的 Two Pointers。

LC-2406：
与 Meeting Rooms II 相关，
但端点语义不同。

LC-731：
在线预订中允许双重预订，
但禁止三重预订。

LC-732：
动态维护最大重叠数量。

LC-1109：
标准 Difference Array，
与 LC-1094 类似。

LC-352：
动态维护离散区间并集。

LC-1272：
区间差集 / Subtraction。

LC-1326：
与 Greedy 的最少区间覆盖相关。

LC-2276：
动态区间并集计数，
可能涉及较复杂的数据结构。

LC-218：
Sweep Line + Heap，
学习成本较高。

自主新增最多 4 道。

新增条件：

A. 明确填补现有 Pattern 缺口。
B. 具有较高的面试代表性。
C. 可迁移性高。
D. 不与现有题高度重复。
E. 记忆成本合理。
F. 能说明正确性不变量。
G. 没有其他专题更合适的主归属。

如果没有明显遗漏，
可以不新增。

如果候选超过四道，
仅新增最重要的四道，
其他放进 README 的 Future Candidates。

不要为了一道特殊题，
无限扩张整个 Intervals 题库。

==================================================
七、跨专题去重
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0986：
可能已经在 Two Pointers 专题。

LC-0452：
可能在 Greedy 专题。

LC-1094：
可能在 Prefix Sum / Difference Array。

LC-0759：
可能在 Heap / K-way Merge。

LC-1353：
Heap + Greedy Scheduling。

LC-2406：
Heap / Meeting Rooms。

LC-2402：
Meeting Rooms III，
可能已在 Heap 专题。

LC-1326：
Greedy Interval Coverage。

LC-2021：
可能与 Difference Array / Sweep Line 交叉。

规则：

如果当前专题已经存在原始学习成果：
必须保留。

如果当前没有、其他专题已经存在：
优先建立 README 相对路径引用。

不要修改其他专题文件。

README 必须标记：

Primary Pattern
Secondary Patterns
Recommended Algorithm
Alternative Algorithm
Cross-topic Reference

同一题可以跨专题复习，
但不需要机械复制多套标准 PDF。

==================================================
八、Interval Endpoint Semantics
==================================================

这是本次最重要的正确性要求之一。

请单独建立：

Interval Endpoint Semantics Cheat Sheet。

必须区分：

【Closed Interval】

[a,b]

a、b 都属于区间。

例如 LC-986、452、1851、2406。

交集的非空条件：

max(a_start,b_start)
<=
min(a_end,b_end)

端点相等可能仍然有交集。

【Half-open Interval】

[a,b)

包含 a，不包含 b。

例如 LC-729。

两个时间区间：

[10,20)
[20,30)

没有冲突。

【Meeting Scheduling】

会议在结束时间立即释放房间。

因此：

previous_end <= current_start

可以复用资源。

【Difference Array】

如果离散整数范围右端点包含在内，
应考虑在 right+1 处撤销影响。

如果是：
[start,end)

则通常可以在 end 处撤销影响。

特别注意：

不能仅根据输入是 [a,b] 的数组表示，
就假定端点一定是闭区间。

必须阅读每道题的实际语义。

请提供至少六个边界测试：

1. 端点相等。
2. 完全包含。
3. 完全相同的区间。
4. 零长度交集。
5. 空输入。
6. 不存在任何重叠。

根据题目约束，
补充其他必要边界测试。

==================================================
九、Greedy 正确性证明
==================================================

对以下题目必须提供简短证明：

LC-435：
为什么选择结束最早的兼容区间？

LC-452：
为什么将箭放在最早结束位置？

LC-986：
为什么移动结束更早的那个区间指针？

LC-56：
为什么合并后只需维护当前最右端点？

LC-1288：
为什么 start 升序、end 降序足以判断覆盖？

LC-1851：
为什么当前有效 Heap Top 可以提供最短覆盖长度？

不能只写：

“因为贪心，所以这样做正确。”

必须给出明确的 Invariant 或 Exchange Argument。

README 应提供：

- 贪心规则
- 不变量
- 正确性理由
- 一个错误选择策略的反例

特别比较：

Merge Intervals：
目标是求并集。

Non-overlapping Intervals：
目标是最大化可保留的互不相交区间数。

Minimum Arrows：
目标是最小化击中全部区间需要的点数。

Meeting Rooms II：
目标是最大并发数。

这四类的优化目标完全不同。

==================================================
十、理论资料、NC 来源及 Git 安全
==================================================

当前 Git 仓库有大量未提交修改及未跟踪文件。

必须严格保护全部已有成果。

执行前：

1. pwd
2. tree
3. git status --short
4. 递归扫描所有原始文件
5. 建立相对路径清单
6. 为普通文件记录 SHA-256
7. 检查 Symbolic Links
8. 检查现有 README 与代码依赖
9. 检查文件名冲突
10. 设计迁移映射

建议在当前目录内生成：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖已有文件
删除未跟踪文件
覆盖原始 solution.py
覆盖 note.md
删除图片、PDF 或说明文档
修改其他算法专题

不自动：

git add
git commit
git push

所有写入必须限制在：

14-intervals (区间)

内部。

可以只读扫描整个仓库。

如果生成工具需要写入外部目录：
先寻找将输出限制到本专题的方式。

无法安全限制时，
跳过相应生成操作并记录原因。

遇到目标文件冲突：

- 不同内容必须全部保留。
- 相同内容也需要记录来源。
- 使用 _conflicts/ 或来源目录归档。
- 不能静默覆盖或删除。

原有：

LC-2021：
explanation.md
note.md

和所有 NC 来源的附加资料，
必须完全保留。

旧目录必须确认全部迁移且为空，
才允许安全清理。

整个流程尽可能 Idempotent（幂等）。

重复执行不应：
- 叠加编号
- 重复生成题目
- 重复归档 NC
- 覆盖原文件
- 丢失资料

==================================================
十一、README 学习文档
==================================================

必须创建：

A. 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对重要 Level 2 建立必要的短 README
D. Interval Pattern Recognition Guide
E. Endpoint Semantics Cheat Sheet
F. Interval Algorithm Comparison Table
G. P0 / P1 / P2 Roadmap

根 README 应包含：

1. Intervals 完整知识地图。
2. 五个 Level 1 的学习目标。
3. 各 Level 2 的不变量。
4. 所有题目及真实相对路径。
5. P0 / P1 / P2。
6. Merge / Insert 模板。
7. Two-pointer Intersection 模板。
8. End-time Greedy 模板。
9. Meeting Rooms + Heap 模板。
10. Sweep Line / Difference Array 模板。
11. Offline Query + Min Heap 模板。
12. Dynamic Calendar 模板。
13. 区间端点对照表。
14. 跨专题索引。
15. 第二轮独立审核结果。
16. 最终建议的学习顺序。

每个 Level 1 README：

- 核心定义
- 1–3 个决定性观察
- 核心不变量
- 为什么使用这种排序
- 当前选择规则
- 简短正确性证明
- Python 模板
- 时间与空间复杂度
- 代表题目
- 典型边界情况
- 错误策略反例
- 相邻 Pattern 对比

文档风格：

中文主导 + 英文技术术语。

例如：

Interval Merging（区间合并）
Interval Intersection（区间交集）
Earliest Finish Time（最早结束时间）
Sweep Line（扫描线）
Difference Array（差分数组）
Offline Query（离线查询）
Active Intervals（活动区间）
Half-open Interval（半开区间）
Endpoint Semantics（端点语义）

不要写冗长、重复、空泛的理论。

==================================================
十二、核心 Python 模板
==================================================

至少建立以下模板索引：

Template 1：
Sort + Merge Intervals

Template 2：
Insert Interval with Three Phases

Template 3：
Two-pointer Interval Intersection

Template 4：
End-time Greedy Scheduling

Template 5：
Meeting Rooms with Min Heap

Template 6：
Sweep Line / Event Sorting

Template 7：
Difference Array + Prefix Sum

Template 8：
Offline Queries + Min Heap

Template 9：
Dynamic Interval Booking

但这些不是要求背九套完全独立的代码。

README 必须解释：

- 哪些题共享同一个核心模板
- 哪些题只改变比较条件
- 哪些题必须更换优化目标
- 哪些题需要 Heap
- 哪些题只需要 Sorting + Scan
- 哪些题需要对 Query 离线排序
- 哪些题应当用真正的动态区间数据结构

尤其不允许把所有题目的时间复杂度
都写成 O(n log n)。

必须按实际排序、Heap 操作和查询数量计算。

==================================================
十三、Pattern Recognition Guide
==================================================

请建立简洁的决策指南。

Q1：
是否需要合并所有重叠区间？
-> Sort + Merge。

Q2：
是否向已排序、互不重叠的区间中
插入一个新区间？
-> Insert Interval。

Q3：
是否需要找出两个有序区间序列的交集？
-> Two Pointers。

Q4：
是否要最大化不冲突区间数量？
-> End-time Greedy。

Q5：
是否要用尽可能少的点覆盖所有区间？
-> End-time Greedy / Minimum Points。

Q6：
是否要判断所有会议能否安排在一个房间？
-> Conflict Detection。

Q7：
是否要求安排全部会议需要的最少房间数？
-> Maximum Overlap / Min Heap / Sweep Line。

Q8：
是否涉及大量区间开始和结束事件？
-> Sweep Line。

Q9：
是否需要累计区间对坐标的影响？
-> Difference Array。

Q10：
是否要回答多个查询点对应的最小覆盖区间？
-> Offline Sorting + Min Heap。

Q11：
是否要动态新增区间并拒绝冲突？
-> Calendar Design。

Q12：
区间端点是否允许相等？
-> 先核对 Closed / Half-open Semantics。

强调：
这些规则不是互斥的。
一个题可能结合多个 Pattern。

==================================================
十四、P0 P1 P2 优先级
==================================================

P0：
必须熟练掌握的核心 Interval 模式。

建议：

LC-0056 - Merge Intervals
LC-0057 - Insert Interval
LC-0986 - Interval List Intersections
LC-0252 - Meeting Rooms
LC-0253 - Meeting Rooms II
LC-0435 - Non-overlapping Intervals
LC-1851 - Minimum Interval to Include Each Query

P1：

LC-0452 - Minimum Number of Arrows to Burst Balloons
LC-1288 - Remove Covered Intervals
LC-1094 - Car Pooling
LC-0729 - My Calendar I
LC-0759 - Employee Free Time

P2：

LC-0228 - Summary Ranges
LC-0163 - Missing Ranges
LC-2021 - Brightest Position on Street

允许根据独立审核调整。

P0 是教学优先级，
不代表某家公司有确定的出题频次。

README 必须提供：

1. P0 核心路线。
2. P0 + P1 标准面试路线。
3. P2 进阶与存档。

不要将所有题目都标记为 P0。

==================================================
十五、数量与验收
==================================================

当前 tree：

13 个目录。
42 个文件。

其中题目来源文件夹：

9 个。

目前无同题 LC / NC 重复来源。

已有正式 LC 目录：
3 个。

NC-only：
6 个。

当前不同题目：
9 道。

本次第一轮新增：
6 道。

如果全部新增：
共 15 道不同题目。

预期 Level 1 分布：

01：5 道
02：2 道
03：3 道
04：3 道
05：2 道

合计：
15 道。

如果有其他专题的现成主归属，
并仅建立交叉引用，
实体目录数量可以少于 15。

第二轮可以合理新增，
但最多自主新增 4 道。

绝对不能为了凑数量制造假文件。

验收要求：

1. 原始 9 道题均有新路径。
2. 6 个 NC-only 正式化正确。
3. 新增题目有对应的正确内容。
4. LC 题号与英文名称匹配。
5. 原始文件全部保留。
6. 原始文件 SHA-256 一致。
7. Level 1 编号连续。
8. Level 2 编号连续。
9. Level 3 编号连续。
10. NC 来源资料完整。
11. 原有图解和笔记完整。
12. 新题标准文件齐全，或明确报告受限原因。
13. README 相对链接有效。
14. 各题端点语义正确。
15. 新解法通过适当的边界测试。
16. 当前专题外没有发生写入或删除。
17. Git 原有未提交内容没有被覆盖。
18. 第二轮审核结果已记录。

==================================================
十六、实际执行流程
==================================================

请按以下顺序执行：

1. 扫描当前目录。
2. 检查 Git 状态。
3. 保存原始文件 Manifest。
4. 记录 SHA-256。
5. 检查符号链接。
6. 核对六个 NC 题目的正式编号。
7. 只读检查跨专题重复题。
8. 设计最终 Level 1 / Level 2。
9. 建立完整迁移映射。
10. 创建五个 Level 1。
11. 创建所有必要 Level 2。
12. 安全迁移原始题目。
13. 正式化六个 NC-only 题。
14. 保留完整 _neetcode 来源。
15. 为所有 Level 3 重新编号。
16. 新增六道推荐题中真正缺失的题。
17. 核查 Premium 题目访问限制。
18. 进行第二轮独立题库审核。
19. 必要时新增最多四道高价值题。
20. 重新校验目录编号。
21. 创建根目录 README。
22. 创建每个 Level 1 README。
23. 创建 Pattern Recognition Guide。
24. 创建 Endpoint Semantics Cheat Sheet。
25. 创建 Interval Algorithm Comparison Table。
26. 创建 P0/P1/P2 学习路线。
27. 对新增 Python 代码执行语法检查。
28. 测试重要端点条件。
29. 对比全部旧文件哈希。
30. 验证 README 相对链接。
31. 清理确认已空的旧目录。
32. 运行最终 tree。
33. 再次检查 Git 状态。
34. 输出完整验收报告。

最终报告必须包含：

- 完整最终 tree
- 五个 Level 1
- 所有 Level 2 Pattern
- 原始题目迁移情况
- 六个 NC-only 正式化结果
- 第一轮六道新增题
- 第二轮独立新增题
- 未新增候选及原因
- P0/P1/P2 数量
- 跨专题索引
- 端点测试结果
- 旧文件与 SHA-256 验证结果
- Premium 题目生成限制
- Git 变更摘要
- 失败或未完成任务
- 最终建议学习顺序

不要仅输出目录规划。

请在全部安全约束下直接执行
Intervals 专题完整重构。
PROMPT
)"
