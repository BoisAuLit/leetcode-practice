
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/13-greedy (贪心)' && claude "$(cat <<'PROMPT'
请直接执行当前 Greedy（贪心）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试与 Online Assessment（OA）。

请将当前目录建设为：
- 高面试价值
- 高算法迁移性
- 算法模式清晰
- 循序渐进
- 最小化机械记忆
- 具备严谨正确性证明
- 适合长期复习

的 Greedy 学习体系。

这是实际的文件系统重构任务，不是单纯的规划。

请执行文件迁移、目录编号、新题生成、README 编写、第二轮独立审核和完整性验收。

==================================================
一、最重要的学习原则
==================================================

Greedy 的核心不是：
每次选择一个看起来最大的或最小的元素。

必须证明当前选择是安全的。

请重点学习：

1. Greedy Choice Property（贪心选择性质）
2. Exchange Argument（交换论证）
3. Staying Ahead（领先性证明）
4. Greedy Invariant（贪心不变量）
5. Feasibility（可行性）
6. Farthest Reach（最远可达位置）
7. Interval Coverage（区间覆盖）
8. Sorting by Priority（排序确定优先级）
9. Earliest Deadline First（最早截止时间优先）
10. Local Constraint Satisfaction（局部约束满足）
11. Greedy + Stack
12. Greedy + Heap
13. Greedy + Ordered Set
14. Lexicographic Optimization（字典序优化）

每种 Greedy Pattern 必须回答：

Q1. 当前有哪些合法选择？
Q2. 当前采用什么贪心规则？
Q3. 为什么该选择不会损害全局最优？
Q4. 能否通过 Exchange Argument 证明？
Q5. 是否存在需要维护的不变量？
Q6. 什么情况下当前选择会导致失败？
Q7. 能否构造一个反例推翻错误的贪心规则？
Q8. 是否有比 Greedy 更自然的算法？
Q9. 是否仅仅在使用 Sorting、Stack、Heap，
    而不是依赖一个真正的贪心证明？

不要把所有 Greedy 题写成相同模板。

==================================================
二、Level 1 -> Level N 目录规范
==================================================

主要使用：

Level 1：Greedy 算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

确有必要时可以增加 Level 4。

同级正式学习文件夹使用：

01 - ...
02 - ...
03 - ...

排序依据：

1. 学习依赖关系
2. 面试代表性
3. 算法迁移价值
4. 正确性证明的复用价值
5. 难度递进
6. 记忆成本

不要按 LC 题号排序。

Level 3 目录命名：

01 - LC-0055 - Jump Game
02 - LC-0045 - Jump Game II

每个 Level 2 内部重新从 01 编号。

资源目录：
_resources
_neetcode
_original_sources
_alternative_solutions
_conflicts
_audit

不参与算法分类编号。

==================================================
三、第一轮完整目录结构
==================================================

原则上建立以下 6 个 Level 1：

01 - 跳跃、可达性与区间覆盖
02 - 局部决策与可行性维护
03 - 排序贪心、频率与资源分配
04 - 区间调度与有序集合
05 - 字符串、字典序与栈贪心
06 - 跨专题与低优先级存档

根据实际审计可以适当调整，
但不能无理由增加大量碎片化分类。

==================================================
LEVEL 1
01 - 跳跃、可达性与区间覆盖
==================================================

核心：

Reachability
Farthest Reach
Minimum Jumps
Greedy Layer Expansion
Interval Coverage

--------------------------------------------------
Level 2：
01 - 最远可达位置与可行性

Level 3：

01 - LC-0055 - Jump Game

教学重点：

定义：

farthest = 当前已经确认可以到达的最远位置。

遍历每一个可到达的位置 i，
更新：

farthest = max(farthest, i + nums[i])

必须解释：

- 为什么 i > farthest 表示无法继续
- 为什么不需要尝试每条跳跃路径
- 为什么向前扫描时保持最远可达位置是安全的
- 为什么 O(n) 时间、O(1) 空间

特别保护：

solution.py
solution_retry.py

不能只保留其中一份。

--------------------------------------------------
Level 2：
02 - 最少跳跃与最远覆盖

Level 3：

01 - LC-0045 - Jump Game II
02 - LC-1024 - Video Stitching

教学重点：

LC-45：

经典 Greedy Layer Expansion。

维护：

current_end
farthest
jumps

current_end：
当前跳跃次数能够覆盖的最远边界。

farthest：
从当前覆盖范围中的位置出发，
下一跳能够到达的最远位置。

当扫描到 current_end 时，
需要增加一次跳跃次数，
并将当前边界更新为 farthest。

必须解释：

- 为什么这个过程类似 BFS Layers
- 为什么不需要真正构造 Graph
- 为什么选择最远扩展是最优的
- 如何处理最后一个位置
- 如何处理无法继续推进的情况

特别注意原题保证或不保证可达的约束。

不能无条件把当前实现推广到所有不可达输入。

LC-1024：

Minimum Interval Coverage。

将视频片段表示成区间：

[start, end]

目标是使用最少区间覆盖：

[0, time]

根据 start 排序。

对于当前已覆盖边界，
扫描所有能够连接当前覆盖范围的区间，
选择其中最大的 end。

必须解释：

- 为什么应该选择延伸最远的区间
- 为什么不能简单选择长度最大的区间
- 如何检测覆盖中断
- 如何处理 time 的边界

建立与 LC-45 的对照：

LC-45：
数组位置隐式形成可跳跃区间。

LC-1024：
直接给出了可以选择的覆盖区间。

两者共享：

Current Coverage + Farthest Next Reach

这组应成为核心 Greedy Pattern。

==================================================
LEVEL 1
02 - 局部决策与可行性维护
==================================================

核心：

Running Balance
Feasibility Invariant
Local Greedy Decision
Constrained Selection

--------------------------------------------------
Level 2：
01 - 环形资源平衡与起点选择

Level 3：

01 - LC-0134 - Gas Station

教学重点：

这是本次必须新增的经典 Greedy 题。

定义每个站点的净收益：

diff[i] = gas[i] - cost[i]

首先检查整体资源：

sum(gas) >= sum(cost)

如果不满足则无解。

扫描时维护从当前候选起点开始的累计余额。

如果余额变成负数：

说明当前候选起点无法完成这段路程。

更重要的是需要证明：

当前候选起点到失败位置之间的其他位置，
也都不能作为新的合法起点。

因此可以把下一个位置作为候选起点。

必须给出简短的排除性证明。

不能只说：
余额小于零就换起点。

还必须解释为什么可以跳过整段位置。

这是经典：
Local Failure -> Eliminate Candidate Range。

--------------------------------------------------
Level 2：
02 - 局部资源使用与找零

Level 3：

01 - LC-0605 - Can Place Flowers
02 - LC-0860 - Lemonade Change

教学重点：

LC-605：

从左到右扫描。

只在当前格子和相邻格子满足要求时种花。

必须解释：
为什么尽早在合法位置种花，
不会降低后续可放置的最大数量？

LC-860：

维护收到的 5 美元和 10 美元钞票数量。

当顾客使用 20 美元付款时：

优先：
10 + 5

其次：
5 + 5 + 5

必须解释：

为什么优先使用一张 10 美元钞票，
能够尽可能保留更灵活的 5 美元零钱？

注意这套规则依赖题目的面值与付款约束。

不能推广为任意货币体系都成立的贪心算法。

--------------------------------------------------
Level 2：
03 - 合法候选过滤与条件合并

Level 3：

01 - LC-1899 - Merge Triplets to Form Target Triplet

教学重点：

一个 Triplet 中的某个坐标如果超过 target，
就不应该选择它。

对于所有坐标都不超过 target 的 Triplets，
检查能否分别覆盖 target 的三个坐标。

必须解释：

为什么对于这种逐坐标取最大值操作，
只需要确认每个目标坐标可以被某个合法 Triplet 达到？

本题不需要真的枚举所有合并顺序。

核心：
Candidate Filtering + Feasibility Coverage。

--------------------------------------------------
Level 2：
04 - 双向局部约束与最小分配

Level 3：

01 - LC-0135 - Candy

教学重点：

每个孩子至少获得一颗糖。

评分更高的孩子，
获得的糖数必须严格大于相邻评分较低的孩子。

经典两次扫描：

从左到右：
满足左邻居关系。

从右到左：
满足右邻居关系。

最后结合两侧的最低要求。

可以使用：

candies[i] = max(left_requirement, right_requirement)

必须解释：

- 为什么只从左到右扫描不够
- 为什么只从右到左扫描也不够
- 为什么取两个方向要求的最大值是正确的
- 为什么不必反复模拟直到稳定

这是 Two-pass Greedy 的代表题。

==================================================
LEVEL 1
03 - 排序贪心、频率与资源分配
==================================================

核心：

Sorting + Greedy
Frequency Counting
Grouping
Marginal Cost
Exchange Argument
Modulo Class

--------------------------------------------------
Level 2：
01 - 按收益与成本优先级选择

Level 3：

01 - LC-1710 - Maximum Units on a Truck
02 - LC-1481 - Least Number of Unique Integers after K Removals

教学重点：

LC-1710：

按每箱的单位收益从大到小排序。

优先选择单位价值最高的箱子。

重点解释：
为什么交换成更高收益的箱子不会降低总收益？

LC-1481：

统计每种整数出现的频率。

为了让剩余不同整数数量最少，
优先彻底删除频率最小的整数类别。

必须解释：

为什么消除一个完整类别才会减少 Unique Count？

为什么先删除高频类别通常不是最优？

本题原有 note.md 必须完整保留。

--------------------------------------------------
Level 2：
02 - 连续数字分组与 Frequency Map

Level 3：

01 - LC-0846 - Hand of Straights

当前只有：

NC - Hand of Straights

请正式整理为 LC-0846。

教学重点：

将全部牌划分为相同大小的连续数字组。

从当前最小的未使用数字开始，
必须用它构造一个合法连续组。

使用：
Sorting + Frequency Map

必须解释：

为什么从最小数字开始是必要的？

为什么不能任意选择一个数字作为组起点？

为什么每张牌的使用次数必须正确减少？

不能简单用 Set 代替 Frequency Map，
因为可能有重复牌。

--------------------------------------------------
Level 2：
03 - 排序差额与最小成本分配

Level 3：

01 - LC-1029 - Two City Scheduling

教学重点：

给定每个人去城市 A、B 的成本。

必须恰好各安排 n 人。

可以先假设所有人都去 B，
然后考虑将其中 n 人改去 A 的成本差：

delta = costA - costB

按 delta 升序选择 n 人前往 A。

也可以直接排序后，
前 n 人去 A，其余去 B。

必须给出 Exchange Argument：

如果某两个被分配到不同城市的人
具有更优的交换安排，
原安排就不是最优。

这解释了为什么按照成本差排序是正确的。

注意：
不是单纯优先选择 costA 最小的人。

--------------------------------------------------
Level 2：
04 - 频率、余数与 MEX

Level 3：

01 - LC-2598 - Smallest Missing Non-negative Integer After Operations

教学重点：

允许通过给元素增加或减少 value 的整数倍
来改变数值。

一个元素的模 value 余数类别保持不变。

维护：

freq[num % value]

尝试依次构造：

0, 1, 2, ...

每构造一个值，
就消耗对应余数类别中的一个可用元素。

第一次没有可用元素时，
得到最大可实现的 MEX。

必须解释：

- 为什么余数是不可改变的不变量
- 为什么优先填补较小非负整数是正确的
- 为什么不必实际修改原数组
- 为什么会出现某个余数类别耗尽

该题标记 P1/P2，
不需要作为一般 Greedy 的核心必背题。

--------------------------------------------------
特别问题：

LC-2651 和 LC-2561 的文件混淆。

如果真实题目内容对应：

LC-2561 - Rearranging Fruits

可以将其归入本 Level 1 下的：

05 - 频率平衡与最小交换代价

但必须先完成题目身份核验。

如果对应：

LC-2651 - Calculate Delayed Arrival Time

则它不属于排序贪心。

应保留在低优先级存档。

不能未经核对直接修改编号。

==================================================
LEVEL 1
04 - 区间调度与有序集合
==================================================

核心：

Event Scheduling
Earliest Deadline First
Heap Scheduling
Ordered Set
Greedy Resource Assignment

--------------------------------------------------
Level 2：
01 - 最早截止时间优先

Level 3：

01 - LC-1353 - Maximum Number of Events That Can Be Attended

教学重点：

先按照开始日期排序。

每一天，将已经开始的活动加入 Min Heap。

Heap 按结束日期升序排列。

去除已经过期的活动。

优先参加结束时间最早的活动。

必须解释：

为什么 Earliest Deadline First
有利于为未来的事件保留更多选择空间？

为什么不能简单按开始时间排序后逐个参加？

为什么每天只能参加一个活动？

本题在 Heap 专题也可能存在正式版本。

必须只读检查跨专题重复，
并建立相对路径引用。

由于当前 Greedy 目录已经有原始文件，
不得因为其他专题重复而删除本地学习成果。

--------------------------------------------------
Level 2：
02 - 带时间约束的资源分配

Level 3：

01 - LC-1488 - Avoid Flood in The City

教学重点：

某个湖再次下雨之前，
必须安排一个晴天清空这个湖。

可以使用：

Hash Map + Ordered Set / Sorted Days。

记录湖上次下雨的日期。

当同一个湖再次下雨时，
寻找上次下雨后尚未使用的最早晴天。

必须解释：

- 为什么要寻找满足时间约束的晴天
- 为什么优先使用最早可行晴天
- 如何处理没有可行晴天
- 如何处理未被使用的晴天
- 如何避免同一天被多个湖重复使用

注意 Python 标准库：

bisect 可以进行 O(log n) 查找，
但从普通 list 中间删除元素可能是 O(n)。

不能因为使用 bisect 就自动声称
整个算法是 O(n log n)。

如果原有代码使用 SortedList，
必须说明它是否依赖第三方 sortedcontainers。

保留原始 solution.py。

如果提供新的推荐实现，
应清楚记录依赖和真实复杂度。

这道题属于进阶 Greedy + Data Structure，
标记 P1/P2。

==================================================
LEVEL 1
05 - 字符串、字典序与栈贪心
==================================================

核心：

Greedy Partition
Lexicographic Optimization
Greedy Stack
Suffix Information
Custom Comparator

--------------------------------------------------
Level 2：
01 - 字符最后出现位置与最少分区

Level 3：

01 - LC-0763 - Partition Labels

当前只有：

NC - Partition Labels

请正式化为 LC-0763。

教学重点：

首先统计每个字符最后出现的位置。

从左到右扫描，
维护当前分区必须覆盖的最远边界：

end = max(end, last_index[s[i]])

当 i == end 时，
可以结束一个分区。

必须解释：

为什么当前分区中的所有字符
都不会在右边重新出现？

为什么在最早合法位置切分是安全的？

这一题与 Interval Merging 有相似性，
但不要求显式构造所有字符区间。

这是核心 Greedy Partition 代表题。

--------------------------------------------------
Level 2：
02 - 括号可行性区间

Level 3：

01 - LC-0678 - Valid Parenthesis String

当前只有：

NC - Valid Parenthesis String

请正式化为 LC-0678。

教学重点：

'*' 可以代表：
'('
')'
空字符串

可以用：

low
high

分别维护当前前缀可能存在的
最少和最多未匹配左括号数量。

遇到不同字符时更新上下界。

若 high < 0：
所有可能性都已经无效。

如果 low < 0：
将 low 限制为 0。

最终要求：
low == 0。

必须解释：

为什么维护一个可能状态范围
就能避免枚举每一个 '*' 的三种选择？

为什么只用单个括号计数不够？

这是 Interval of Feasible States
（可行状态区间）思想。

--------------------------------------------------
Level 2：
03 - 最优数字与自定义比较规则

Level 3：

01 - LC-0670 - Maximum Swap
02 - LC-0179 - Largest Number

教学重点：

LC-670：

最多交换两个数位一次，
使最终整数最大。

可以记录每个数字最后出现的位置，
优先改善较高位。

必须解释：
为什么优先改善更高位比改善低位更重要？

LC-179：

对整数转换成的字符串进行排序。

比较两个字符串 a、b 时，
使用：

a + b
b + a

决定拼接顺序。

必须解释为什么不能简单按整数大小排序，
也不能简单按字符串字典序排序。

特别处理全部为零的情况。

这是一类：
Custom Comparator + Greedy Ordering。

--------------------------------------------------
Level 2：
04 - Stack 与字典序最优化

Level 3：

01 - LC-2434 - Using a Robot to Print the Lexicographically Smallest String
02 - LC-3170 - Lexicographically Minimum String After Removing Stars

教学重点：

LC-2434：

Stack + Remaining Suffix Minimum。

根据后续仍然可以获取的最小字符，
决定是否应该从 Stack 输出当前字符。

必须解释：

为什么需要知道未来最小字符？

为什么某些字符应该暂存在 Stack 中？

什么时候输出 Stack Top 是安全的？

LC-3170：

根据每个 '*' 删除当前可用的
字典序最小字符。

还要考虑同一字符出现多次时，
应该删除哪个位置，
才能使最终字符串字典序最小。

可以使用：
Heap / Per-character Index Stack。

必须验证正确的 Tie-breaking 规则。

不能只说：
删除当前最小字符即可。

这两题属于 Greedy + Data Structure 组合，
建议 P1/P2。

--------------------------------------------------
Level 2：
05 - 特殊递归分解与字典序重排

Level 3：

01 - LC-0761 - Special Binary String

教学重点：

将 Special Binary String 分解成合法的嵌套块。

递归处理每个内部块。

随后按照有利于字典序最大化的顺序重排。

必须解释：

- 合法块如何划分
- 为什么块内可以递归处理
- 为什么块之间可以排序
- 为什么最终拼接不会破坏合法性

这是 Recursive Decomposition + Greedy Ordering。

标记 P2。

保留现有 PDF 和 Draw.io 图解。

==================================================
LEVEL 1
06 - 跨专题与低优先级存档
==================================================

这个 Level 1 不是为了删除题目，
而是保留已有学习成果，
同时避免把非典型 Greedy 题作为核心必背。

--------------------------------------------------
Level 2：
01 - Graph Search 而非标准 Greedy

Level 3：

01 - LC-1306 - Jump Game III

教学重点：

虽然它的名字包含 Jump Game，
但核心是 Graph Reachability。

可以使用 DFS/BFS + Visited。

不能因为名字包含 Jump Game，
就把它与 LC-55 / 45 的最远覆盖贪心混为一谈。

应建立 Graphs 专题跨目录引用。

标记 P2（仅针对 Greedy 专题）。

--------------------------------------------------
Level 2：
02 - String Segmentation 与 Jump Game 迁移

Level 3：

01 - LC-3291 - Minimum Number of Valid Strings to Form Target I
02 - LC-3292 - Minimum Number of Valid Strings to Form Target II

教学重点：

这两题的关键在于：

Valid String 是 words 中某个字符串的前缀。

LC-3291：

可以用 Trie + DP。

当得到每个位置能够匹配的
最长合法前缀长度后，
也可以进一步建立最少跳跃问题。

LC-3292：

输入规模更大。

通常需要高效的字符串匹配预处理，
再结合 Greedy / Minimum Jump / Interval Cover。

可考虑：
KMP
Z-function
Rolling Hash
等正确方案。

必须注意：
不同实现的时间复杂度和哈希碰撞风险。

不能把普通字符串暴力匹配
声称为对大规模输入始终高效。

这两道题与：

LC-45 - Jump Game II

存在算法迁移关系。

但是：

计算每个起点的合法前缀长度
并不是 LC-45 原本需要解决的问题。

请建立交叉引用：

Trie
Dynamic Programming
String Matching
Jump Game II

保留原始两套题目和代码。

标记 P2（针对基础 Greedy 学习路线）。

--------------------------------------------------
Level 2：
03 - 题号冲突与非 Greedy 归档

原有：

LC-2651 - Calculate Delayed Arrival Time

但该目录中存在：

asset-005 - 2561 - A - 1 - Rearranging Fruits.pdf
asset-005 - 2561 - A - 2 - Rearranging Fruits.pdf

这是严重的题目身份不一致问题。

请严格执行：

第一步：
读取 metadata.json。

第二步：
读取 solution.py。

第三步：
检查 problem.pdf 与 problem_dark.pdf
实际对应的题目。

第四步：
检查两个 asset PDF 的内容。

第五步：
对照官方 LeetCode：
2651 = Calculate Delayed Arrival Time
2561 = Rearranging Fruits

然后分类处理：

情况 A：

如果 metadata、problem.pdf、solution.py
对应 LC-2561：

则正式目录应当使用：
LC-2561 - Rearranging Fruits。

保留原始错误命名来源的记录，
不要丢弃任何 PDF、代码或笔记。

分类归入排序贪心与最小交换代价。

情况 B：

如果正式题目内容对应 LC-2651，
但两个 PDF 对应 LC-2561：

则保留 LC-2651 的所有题目文件。

将不匹配的 PDF 安全归档到
当前 Greedy 目录内部的相关资源目录，
或明确标记来源的 _foreign_assets。

不得删除 PDF。

不要直接把这些 PDF 当成 LC-2651 的讲解。

情况 C：

如果不同文件分别对应不同题目：

必须保留所有不同来源。

根据可验证内容，
分别建立正确题目归属或安全归档。

不能简单选择一个题号并覆盖另一个。

情况 D：

如果当前无法确认题目身份：

保持原始文件不变，
将该冲突记录到 _audit，
并在最终报告中标记为待人工确认。

绝对不能未经核实直接重命名。

如果真实是 LC-2651：

它属于简单的 Modular Arithmetic，
不是重要 Greedy 题。

标记 P2 存档。

==================================================
四、LC-45 重复来源处理
==================================================

当前同时有：

jump-game/
  Jump Game II - Cluster/
    LC-0045 - Jump Game II/

以及：

jump-game/
  LC-0045 - Jump Game II/

它们是同一题号的两个来源。

但可能包含不同的学习资料。

请：

1. 分别读取两个 metadata.json。
2. 分别读取两个 solution.py。
3. 检查全部 PDF 与 JPEG。
4. 检查两份代码是否相同。
5. 建立清晰的迁移映射。
6. 保留一个正式 LC-0045 题目目录。
7. 将另一套资料归档到：
   _original_sources/ 或 _alternative_solutions/。
8. 不允许覆盖同名文件。
9. 在 README 中说明不同版本的解法差异。

特别保留：

asset-02 - Explanation.jpeg

不能因为两套文件夹有相同 LC 编号
就删除其中一个目录的学习资料。

另外：

Jump Game II - Cluster/
还有：

LC-3291
LC-3292

它们是不同题目，
绝不能与 LC-45 合并为同一道题。

只应调整分类并建立交叉引用。

==================================================
五、NC-only 正式化
==================================================

当前存在四个 NC-only 来源：

NC - Hand of Straights
NC - Merge Triplets to Form Target
NC - Partition Labels
NC - Valid Parenthesis String

对应：

LC-0846 - Hand of Straights
LC-1899 - Merge Triplets to Form Target Triplet
LC-0763 - Partition Labels
LC-0678 - Valid Parenthesis String

请核对实际题面。

确认后：

1. 创建正式 LC Level 3 题目目录。
2. 通过现有工具生成标准 LeetCode 文件。
3. 将原 NC 文件完整归档到 _neetcode/。
4. 保留原始 NC solution.py。
5. 保留原始 metadata.json。
6. 保留 PDF 和所有附件。
7. 不得覆盖任何用户代码。

特别保护：

NC - Merge Triplets：
asset-06 - Explanation.png

NC - Valid Parenthesis String：
asset-08 - Explanation.jpg

所有 NC 版本都必须可追溯。

==================================================
六、第一轮新增的五道题
==================================================

明确建议新增：

LC-0134 - Gas Station
LC-0860 - Lemonade Change
LC-1024 - Video Stitching
LC-1029 - Two City Scheduling
LC-0135 - Candy

新增前先检查：

1. 当前 Greedy 目录是否已有。
2. 全仓库其他专题是否已有。
3. 是否存在正式题目文件。
4. 当前专题是否具有合理主归属。

如果当前 Greedy 目录确实缺失，
并且需要在本专题创建正式题目，
使用仓库现有生成工具创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备依据 LeetCode 题号
生成这些标准文件的能力。

请直接复用现有工作流。

如果其他专题已有完整题目，
应评估使用 README 跨专题索引，
而不是无意义重复生成。

禁止：

- 空白 PDF
- 错误题号的 metadata
- 复制其他题目的 problem.pdf
- 覆盖原有 solution.py
- 删除用户的注释或笔记

如果生成失败：
保留原有数据，
在最终报告中说明失败原因。

==================================================
七、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 的第一轮推荐。

你必须再进行一次独立审核。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可靠的 Greedy 面试题单

如有网络访问：
核对最新题目编号、题名、约束和典型解法。

不得编造 FAANG 真实出题频率。

重点审核是否覆盖：

1. Greedy Choice Property
2. Exchange Argument
3. Staying Ahead
4. Running Balance
5. Jump Game Reachability
6. Jump Game II Minimum Steps
7. Minimum Interval Coverage
8. Sorting by Gain / Cost
9. Frequency Greedy
10. Two-pass Greedy
11. Greedy with Hash Map
12. Greedy with Heap
13. Earliest Deadline First
14. Ordered Set Scheduling
15. Greedy String Partition
16. Lexicographic Greedy
17. Greedy Stack
18. Feasibility Range
19. Modular Invariant
20. Greedy vs DP
21. Greedy vs BFS

另外审核以下候选：

LC-0435 - Non-overlapping Intervals
LC-0452 - Minimum Number of Arrows to Burst Balloons
LC-1326 - Minimum Number of Taps to Open to Water a Garden
LC-0406 - Queue Reconstruction by Height
LC-0330 - Patching Array
LC-0621 - Task Scheduler
LC-0881 - Boats to Save People
LC-1642 - Furthest Building You Can Reach
LC-2561 - Rearranging Fruits（仅在题目身份核实后）
LC-0649 - Dota2 Senate

注意：

LC-435、452：
可能已经位于 Intervals 专题。
若已有完整资料，建立交叉索引即可。

LC-1326：
与 Jump Game II / Interval Coverage
有很高的 Pattern 相似度。

LC-881：
通常更适合 Two Pointers。

LC-621、1642：
Heap + Greedy。
可能已经在 Heap 专题。

LC-2561：
属于更特殊的交换成本最优化，
不要在未确认现有目录真实内容前重复创建。

LC-406：
Sorting + Insertion Greedy，
适合讨论交换证明，但不是必须新增。

LC-330：
特殊覆盖不变量，
与连续可构造范围相关，
适合作为候选进阶题。

LC-649：
Queue / Simulation + Greedy，
不一定要加入本专题主线。

自主新增最多 4 道。

每一道新增题必须说明：

A. 填补了哪个重要 Pattern？
B. 有什么可迁移的贪心思想？
C. 为什么不只是已有题目的重复训练？
D. 为什么值得增加学习成本？
E. 当前仓库是否已存在？
F. 最适合哪个 Level 1 / Level 2？
G. P0、P1、P2 哪一级？

如果没有真正有价值的遗漏，
可以不新增。

不要求把整个 Greedy 标签题库全部补齐。

==================================================
八、跨专题去重与算法归属
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0053 -> Dynamic Programming / Kadane
LC-0135 -> 是否已有 Greedy 或其他专题
LC-0134 -> 是否已有其他来源
LC-0045 -> 本专题已有重复
LC-0130? 不属于该 Greedy 主线
LC-1306 -> Graph DFS/BFS
LC-3291 -> Trie / DP
LC-3292 -> String Matching / Greedy
LC-1353 -> Heap
LC-0435 -> Intervals
LC-0452 -> Intervals
LC-0881 -> Two Pointers
LC-0621 -> Heap / Scheduling
LC-1642 -> Heap + Greedy
LC-0763 -> Interval-style String Partition

规则：

1. 已有当前专题原始文件，全部保留。
2. 当前没有、其他专题已有的，
   优先通过 README 建立相对路径链接。
3. 不修改其他专题。
4. 不强迫所有 Greedy 题都归入当前目录。
5. 一个题目可以有多个算法解法。
6. 一个题目可以有多个跨专题学习入口。
7. 但在当前 Greedy 专题内只保留一个正式主目录。

README 需记录：

Primary Pattern
Secondary Patterns
Recommended Algorithm
Alternative Algorithm
Cross-topic Reference

减少重复记忆，而不是删除学习成果。

==================================================
九、Git 与文件安全
==================================================

当前 Git 工作区存在大量未提交修改、
未跟踪文件和已有学习成果。

必须严谨保护。

开始前：

1. pwd
2. tree
3. git status --short
4. 扫描当前专题全部文件
5. 记录原始相对路径
6. 记录文件大小和 SHA-256
7. 检查符号链接
8. 检查 Python import
9. 检查 Markdown 相对链接
10. 识别重复题号
11. 识别 metadata 与题面冲突
12. 建立完整迁移映射

建议生成：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

审计文件必须位于当前 Greedy 目录内部。

必须记录原有文件与新路径的对应关系。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖任何现有文件
删除未跟踪文件
覆盖原有 solution.py
丢弃 solution_retry.py
删除 PDF、图片或 Draw.io
修改其他算法专题

不自动：

git add
git commit
git push

只允许写入：

13-greedy (贪心)

目录内部。

允许只读检查整个仓库。

移动文件时不得通过符号链接
对当前目录以外的目标进行写入。

遇到同名冲突：

- 不同内容必须全部保留。
- 相同内容也必须保留可追溯来源。
- 必要时使用 _conflicts/。
- 在最终报告中说明。

旧目录确认迁移完毕并且为空后，
才允许安全删除空目录。

不能使用批量破坏性清理命令。

要尽可能保证 Idempotence（幂等性）：

重复运行不能：
- 叠加编号
- 重复创建同题目录
- 重复归档 NC
- 覆盖文件
- 遗失学习附件

==================================================
十、特别保护的原有资料
==================================================

必须完整保留：

docs (资料)/
  04 - Explanation.png

LC-0045：
  asset-02 - Explanation.jpeg
  两套原始 solution.py

LC-0055：
  solution_retry.py

LC-1488：
  asset-006 - 1488 - A - Avoid Flood in The City.jpeg

LC-2598：
  asset-007 - 2598 - A - Smallest Missing Non-Neg Integer.pdf

LC-0179：
  asset-008 - 0179 - A - Largest Number.pdf

LC-1353：
  asset-001 - 1353 - A - Max Nb of Events Attended.pdf

LC-1481：
  note.md

LC-0761：
  两个 PDF / Draw.io 资料

LC-2434：
  原有 JPEG 图解

LC-3170：
  原有 PDF 图解

NC - Merge Triplets：
  asset-06 - Explanation.png

NC - Valid Parenthesis String：
  asset-08 - Explanation.jpg

LC-2651 目录内：
  两个带有 2561 编号的 PDF

以及其他全部：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
note.md
图片
Markdown
Draw.io
自定义文件

理论图解可以整理至：

_resources/
  docs/

但不能删除或覆盖原图。

==================================================
十一、README 学习体系
==================================================

必须创建：

A. 当前 Greedy 根目录 README.md
B. 每个 Level 1 的 README.md
C. 重要 Level 2 的简短 README.md
D. Greedy Pattern Recognition Guide
E. Greedy Proof Cheat Sheet
F. Greedy vs DP Comparison
G. FAANG Greedy Core Roadmap

根目录 README 包含：

1. Greedy 知识地图
2. 所有 Level 1 / Level 2
3. 所有题目及相对路径
4. P0 / P1 / P2
5. Greedy 的适用条件
6. Exchange Argument
7. Staying Ahead
8. Greedy Invariant
9. Jump Game 模板
10. Sorting Greedy 模板
11. Interval Coverage 模板
12. String Greedy 模板
13. Heap / Ordered Set 的跨专题作用
14. Greedy 与 DP 的区别
15. 哪些题实际上不是 Greedy
16. 第二轮审核结果
17. 推荐复习顺序

每个 Level 1 README：

1. 核心定义
2. 1–3 个决定性观察
3. Greedy Choice
4. Greedy Invariant
5. 正确性证明
6. 简短 Python 模板
7. 时间复杂度
8. 空间复杂度
9. 代表题目
10. 典型反例
11. 与相邻 Pattern 的区别

特别强调：

没有可靠贪心证明的情况下，
不能因为解法运行很快或通过少量样例，
就认定 Greedy 一定正确。

==================================================
十二、核心 Python 模板
==================================================

README 至少包括：

Template 1：
Farthest Reach - Jump Game

Template 2：
Layered Greedy - Jump Game II

Template 3：
Minimum Interval Coverage

Template 4：
Running Balance - Gas Station

Template 5：
Sort by Gain / Cost

Template 6：
Greedy Frequency Counting

Template 7：
Earliest Deadline First + Min Heap

Template 8：
Greedy Partition by Last Occurrence

Template 9：
Feasible Range - Valid Parenthesis String

Template 10：
Greedy Stack + Suffix Information

但这十个模板不代表
需要背诵十套完全独立的代码。

应重点讲解：

- 各模板保持什么不变量
- 当前选择的依据是什么
- 为什么局部选择安全
- 哪些模板其实可以互相转化

特别对比：

LC-55：
只需判断是否可以到达。

LC-45：
求最少跳跃次数。

LC-1024：
求最少区间数量。

虽然目标不同，
但都可以使用最远覆盖的思想。

==================================================
十三、正确性证明要求
==================================================

请在 README 中用具体例子解释：

【Exchange Argument】

假设存在一个最优解，
但它没有采用 Greedy Choice。

尝试将某个局部决策
替换为 Greedy Choice。

证明替换后：
- 仍然合法
- 目标值不变或更优

由此说明存在采用贪心选择的最优解。

代表题：

LC-1029
LC-1710
LC-846

【Staying Ahead】

比较 Greedy 与其他可能解法。

证明在每一步，
Greedy 保持的某个关键指标
始终不落后于其他策略。

代表题：

LC-45
LC-1024

【Feasibility Invariant】

维护当前扫描过程中
所有可能的合法状态。

代表题：

LC-55
LC-678
LC-134

注意：

这些只是常见证明方式，
不是所有题目都可以机械套用。

要结合每道题的具体约束解释。

==================================================
十四、P0 P1 P2 优先级
==================================================

P0：
最重要的经典 Greedy 面试题及核心模式。

建议 P0：

LC-0055 - Jump Game
LC-0045 - Jump Game II
LC-0134 - Gas Station
LC-0846 - Hand of Straights
LC-1899 - Merge Triplets to Form Target Triplet
LC-0763 - Partition Labels
LC-0678 - Valid Parenthesis String

P1：

LC-0605
LC-0860
LC-1024
LC-1029
LC-0135
LC-1710
LC-1481
LC-1353
LC-0670
LC-0179
LC-2434
LC-2598

P2：

LC-1488
LC-3170
LC-0761
LC-1306
LC-3291
LC-3292
LC-2651（如经核实确实对应 2651）

如果实际是 LC-2561：
重新评估其优先级，
通常作为 P2 高阶 Greedy。

第二轮审核可以调整优先级，
但必须说明原因。

不要把所有题目都标记 P0。

P0 表示当前算法学习价值，
不代表确切的企业出题概率。

根 README 必须给出：

1. P0 核心路线
2. P0 + P1 标准面试准备路线
3. P2 进阶与存档

==================================================
十五、第二轮题目审核后的数量
==================================================

当前 tree 的初步统计：

22 个题目来源目录。

其中：
LC-0045 有两个来源目录。

因此根据目录名称推算：
21 道不同题目。

当前 NC-only：
4 道。

第一轮新增：
5 道。

如果全部新增且不存在跨专题去重：
预计 26 道不同题目。

必须注意：

由于 LC-2651 / LC-2561 的编号冲突，
最终应以实际文件内容核对后的
真实题目集合为准。

不能为了维持 26 的数量而篡改题目身份。

预期分布：

Level 1 01：3 道
Level 1 02：5 道
Level 1 03：5 道
Level 1 04：2 道
Level 1 05：7 道
Level 1 06：4 道

合计：26 道。

如果将经核实的 LC-2561
从 Level 1 06 移入 Level 1 03，
则两类数量需要相应调整。

如果第二轮新增真正有价值的题，
数量也可以增加。

禁止强行凑数字。

==================================================
十六、跨专题与最小核心路线
==================================================

在根 README 中建立：

Greedy Core Roadmap。

推荐：

阶段 A：
局部 Greedy + Running Balance
LC-605 -> LC-134 -> LC-860

阶段 B：
Reachability + Minimum Jumps
LC-55 -> LC-45 -> LC-1024

阶段 C：
Sorting + Exchange Argument
LC-1710 -> LC-1029 -> LC-846

阶段 D：
Feasibility + Partition
LC-1899 -> LC-763 -> LC-678

阶段 E：
Greedy + Data Structure
LC-1353 -> LC-2434 -> LC-1488

阶段 F：
特殊进阶
LC-2598
LC-3170
LC-761
LC-3291
LC-3292

阶段 F 可作为选修。

此外请输出：

10–12 道最核心的 Greedy 面试题。

要覆盖不同算法不变量，
而不是挑选大量相似的简单排序题。

==================================================
十七、实际执行步骤
==================================================

请实际执行：

1. pwd
2. 扫描完整目录
3. 检查 Git 状态
4. 建立原始 Manifest
5. 保存全部原始文件的 SHA-256
6. 检查 Symbolic Links
7. 验证全部旧题的题号与英文题名
8. 特别核查 LC-2651 / LC-2561 冲突
9. 检查 LC-45 两套来源
10. 检查 NC-only 四道题
11. 只读扫描整个仓库的跨专题题目
12. 建立完整迁移映射
13. 创建 6 个 Level 1
14. 创建合理 Level 2
15. 安全迁移所有旧题
16. 安全归档 LC-45 的两个来源
17. 将四道 NC-only 正式化
18. 为全部 Level 3 重新编号
19. 新增五道推荐题中真正缺失的题
20. 进行第二轮独立题库审核
21. 必要时新增最多四道高价值题
22. 根据审核结果调整分类与排序
23. 安全整理理论资料
24. 创建所有 README
25. 创建 Pattern Recognition Guide
26. 创建 Greedy Proof Cheat Sheet
27. 创建 Greedy vs DP 对照
28. 创建 10–12 道核心刷题路线
29. 对新增代码执行语法及样例检查
30. 验证原始文件哈希与迁移路径
31. 验证全部新题文件完整性
32. 验证所有 README 相对链接
33. 检查文件夹编号连续性
34. 仅清理确认已空的遗留目录
35. 运行最终 tree
36. 检查最终 Git 状态
37. 输出完整验收报告

最终报告必须包括：

- 完整最终 tree
- 6 个 Level 1 分类
- 所有 Level 2 Pattern
- 原始题目迁移清单
- LC-45 重复来源处理
- LC-2651 / LC-2561 核查结论
- 四个 NC-only 正式化结果
- 第一轮新增五道题
- 第二轮独立新增题目
- 未新增候选及理由
- P0 / P1 / P2 统计
- 核心 10–12 题学习路线
- 原始文件与哈希验证
- 跨专题索引
- Git 变更摘要
- 失败或未完成项目

如果某项操作存在文件损坏或越界风险，
保留原文件，明确报告，
继续完成其他安全的任务。

不要只给出规划。

请在全部安全约束下直接执行
Greedy 专题的完整目录重构。
PROMPT
)"
