
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/18-monotonic-fuck-you (单调栈、单调队列)' && claude "$(cat <<'PROMPT'
请直接执行当前 Monotonic Stack & Monotonic Deque（单调栈、单调队列）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请将这个专题建设成一套：

- 面试价值高
- 算法迁移性强
- 核心 Pattern 清晰
- 不变量和正确性证明明确
- 学习顺序循序渐进
- 记忆成本尽可能低
- 能长期复习和扩展

的 Monotonic Stack / Deque 学习体系。

这是实际文件系统重构任务。

你需要实际执行目录重构、旧题迁移、NC 正式化、新题生成、独立审核、文档编写和最终验收。

不要仅仅输出一个规划。

==================================================
一、核心学习目标
==================================================

我不希望机械记忆几十道单调栈题。

我更希望真正理解：

1. Monotonic Stack（单调栈）
2. Monotonic Deque（单调双端队列）
3. Next Greater Element（右侧第一个更大元素）
4. Next Smaller Element（右侧第一个更小元素）
5. Previous Greater / Smaller（左侧最近更大/更小）
6. Span（跨度）
7. Monotonic Boundary（单调边界）
8. Histogram Rectangle（柱状图矩形）
9. Contribution Counting（贡献计数）
10. Greedy Monotonic Stack（贪心单调栈）
11. Sliding Window Maximum / Minimum
12. Prefix Sum + Monotonic Deque
13. Strict vs Non-strict Comparison
14. Amortized O(n) Analysis

每种 Pattern 必须回答：

Q1. 为什么要使用单调结构？

Q2. Stack / Deque 中存储的是值、下标还是聚合状态？

Q3. 元素按照什么顺序保持单调？

Q4. 新元素到来时，为什么可以弹出某些旧元素？

Q5. 弹出的元素究竟失去了哪一种未来竞争资格？

Q6. 弹出时是否已经找到了某个元素的答案？

Q7. 为什么有些题使用 <，有些使用 <=？

Q8. 如何处理重复元素？

Q9. 是否需要清除过期的窗口元素？

Q10. 为什么整体复杂度是 O(n)，即使代码包含嵌套 while？

特别强调：

不要把所有单调栈题都解释为
“维护递增或递减序列”。

必须解释：
单调性为什么能帮助排除不可能成为答案的候选。

==================================================
二、Level 1 -> Level N 目录规范
==================================================

优先采用：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

确实需要时，可以增加 Level 4。

但不要制造无意义的分类层级。

所有同级正式学习目录使用连续编号：

01 - ...
02 - ...
03 - ...

编号依据：

1. 学习依赖
2. 面试代表性
3. 核心算法迁移性
4. 不变量复用价值
5. 难度递进
6. 记忆成本

不要按 LeetCode 题号机械排序。

Level 3 命名格式：

01 - LC-0496 - Next Greater Element I
02 - LC-0739 - Daily Temperatures

每个 Level 2 内独立重新编号。

以下目录不参与算法编号：

_resources
_neetcode
_original_sources
_cross_topic_archive
_alternative_solutions
_conflicts
_audit

当前根目录名称比较特殊：

18-monotonic-fuck-you (单调栈、单调队列)

请保持这个根目录名称和路径不变。

不要擅自重命名根目录，
否则可能破坏其他专题的链接。

==================================================
三、第一轮目标 Level 1 分类
==================================================

建议建立五个 Level 1：

01 - 最近更大元素与跨度
02 - 单调边界、矩形与贡献计算
03 - 单调栈与贪心构造
04 - 单调队列与滑动窗口
05 - 单调扫描与跨专题存档

以下是第一轮完整的 16 道不同题目。

可基于实际代码和第二轮审核适当调整 Level 2。

但必须说明调整理由。

==================================================
LEVEL 1
01 - 最近更大元素与跨度
==================================================

核心：

Next Greater Element
Next Greater Index
Circular Array
Previous Greater
Online Span

--------------------------------------------------
Level 2：
01 - Next Greater Element 与索引栈

题目顺序：

LC-0496 - Next Greater Element I
LC-0739 - Daily Temperatures
LC-0503 - Next Greater Element II

教学重点：

LC-496：

最基础的 Next Greater Element。

nums1 是 nums2 中部分元素构成的查询集合，
本题可利用题目中元素唯一的约束。

推荐先遍历 nums2。

使用 Monotonic Decreasing Stack，
为元素寻找右侧第一个严格更大的数。

当当前值大于 Stack Top 时，
弹出 Stack Top，
当前值就是这个被弹出元素的 Next Greater。

通过 Hash Map 保存答案。

必须解释：

为什么当前值首次触发弹出，
就意味着它是右侧第一个更大值？

为什么在此之前的元素都不能作为答案？

为什么题目中的元素唯一性
允许将数值作为 Hash Map Key？

如果允许重复元素，
应该如何改为使用 Index？

LC-739：

Daily Temperatures。

对于每天，
寻找右侧第一个温度严格更高的日期。

推荐 Stack 保存 Index。

遇到更高温度时：

answer[old_index] = current_index - old_index

必须解释：

为什么不是保存温度值？

为什么需要下标差？

为什么等于当前温度不算 Warmer Day？

典型比较：

temperatures[stack[-1]] < current_temperature

必须解释为什么使用严格小于号。

LC-503：

Circular Array Next Greater Element。

数组是循环的。

最后一个元素的右侧，
可以继续从第一个元素开始寻找。

推荐使用：

2*n 次逻辑遍历
以及
i % n

模拟循环数组。

必须解释：

- 为什么需要最多两轮扫描
- 为什么不需要复制整个数组
- 为什么不会将元素自己误当成严格更大值
- 为什么原始数组长度为 n 时，
  总体仍是 O(n) 时间
- 如何避免同一元素被错误地重复加入待解决栈

请提供一种清晰且正确的 Python 实现。

这道题主要是 LC-496 / 739
在 Circular Array 上的自然扩展。

不需要记忆全新数据结构。

--------------------------------------------------
Level 2：
02 - Previous Greater 与流式跨度

题目顺序：

LC-0901 - Online Stock Span

教学重点：

这是本次新增的重要单调栈变体。

实现：

StockSpanner()
next(price)

返回：
从当前日期向左连续追溯，
有多少天的价格都小于或等于今天价格。

必须解释：

为什么应该把以前连续且不高于当前价格的日期
合并成一个 Span？

可以使用 Stack：

(price, span)

每次新价格到来：

span = 1

当：

stack[-1].price <= price

时：

弹出旧状态，
累加它维护的 Span。

最终将：

(price, span)

压入 Stack。

必须解释：

- 为什么可以压缩多个历史元素
- 为什么不必逐个重新比较所有历史日期
- 为什么相等价格应该纳入当前 Span
- 为什么使用 <= 而不是 <
- 为什么整个调用序列的摊还复杂度是 O(n)

注意：

一次 next() 调用可能 Pop 多个元素。

因此不能未经说明就声称每次调用
最坏情况下都是 O(1)。

正确表述通常是：
单次最坏 O(n)，
跨 n 次操作总计 O(n)，
摊还 O(1)。

这道题与 Daily Temperatures
具有非常明确的迁移关系：

Daily Temperatures：
未来元素出现时解决旧问题。

Online Stock Span：
当前元素出现时汇总过去的跨度。

==================================================
LEVEL 1
02 - 单调边界、矩形与贡献计算
==================================================

核心：

Previous Smaller
Next Smaller
Histogram Area
Rectangle Width
Contribution Counting
Duplicate Tie Breaking

--------------------------------------------------
Level 2：
01 - Histogram 与最大矩形

题目顺序：

LC-0084 - Largest Rectangle in Histogram
LC-0085 - Maximal Rectangle

教学重点：

LC-84：

这是整个 Monotonic Stack 专题最重要的题目之一。

给定柱状图高度。

求能够形成的最大矩形面积。

关键观察：

假设某根柱子高度为 h。

如果以 h 为矩形的最低高度，
它可以扩展到：

左侧第一个高度严格更小的柱子之后，
右侧第一个高度严格更小的柱子之前。

因此：

width = right_boundary - left_boundary - 1

area = height * width

推荐使用 Monotonic Increasing Stack。

Stack 保存 Index。

当遇到更低的柱子时，
一些旧柱子的右侧边界已经确定，
因此可以弹出并计算面积。

必须解释：

- 为什么 Stack 保存 Index
- 为什么遇到更低柱子就可以结算面积
- 为什么弹出后新的 Stack Top 是左边界
- 为什么当前下标是右边界
- 为什么矩形宽度需要减 1
- 为什么扫描结束还需要处理剩余柱子
- Sentinel（哨兵）如何简化结算

如果使用末尾虚拟高度 0：
优先不修改调用者传入的原始 heights。

可以通过额外遍历或安全的虚拟值实现。

注意重复高度时：
使用 < 或 <= 的策略需要在代码中一致，
并说明其对边界语义的影响。

不能机械混用不同模板里的比较符号。

LC-85：

Maximal Rectangle。

给定二进制矩阵，
寻找全部为 1 的最大矩形。

核心转化：

每处理一行，
维护各列向上连续为 1 的高度。

若当前格子为 1：
heights[col] += 1

若当前格子为 0：
heights[col] = 0

随后把当前 heights 当成一个 Histogram，
调用 LC-84 的核心算法。

必须解释：

为什么每一行都能形成一个柱状图？

为什么所有矩形都可以在某一行作为底边时被考虑？

为什么遇到 0 时需要清空累计高度？

目标复杂度：

O(rows * cols)。

请将 LC-85 标记 P2 进阶。

它的主要价值是：

Matrix -> Histogram -> Monotonic Stack。

不需要为这道题重新记忆一套独立的矩形算法。

--------------------------------------------------
Level 2：
02 - Subarray 极值贡献计算

题目顺序：

LC-0907 - Sum of Subarray Minimums
LC-2104 - Sum of Subarray Ranges

教学重点：

这两题应放在一起。

LC-907：

求所有非空连续子数组最小值的总和。

不能对每个子数组重复扫描找最小值。

核心换一个角度：

不是枚举每个子数组的最小值，
而是枚举每个元素能作为多少个子数组的最小值。

对于 nums[i]：

假设：

left[i] 是左侧某个有效边界。
right[i] 是右侧某个有效边界。

如果边界定义正确，
它能够贡献的子数组数量为：

(i - left[i]) * (right[i] - i)

于是：

contribution =
nums[i] * (i-left[i]) * (right[i]-i)

必须解释：

- 为什么左侧有 i-left[i] 种起点
- 为什么右侧有 right[i]-i 种终点
- 为什么两侧选择可以相乘
- 为什么需要严格/非严格比较的配对规则
- 为什么重复元素容易导致重复计数

推荐明确选择一种完整约定：

对于计算最小值贡献：

Previous Strictly Smaller
+
Next Smaller or Equal

或者使用方向相反、
但数学上等价的一致约定。

不要两边都随意采用严格比较，
也不要两边都随意采用非严格比较。

必须用：

[1,1]
[2,2,2]

验证重复元素的贡献只被计算一次。

LC-907 的答案需要按照题目要求取模：

10^9 + 7

LC-2104：

Sum of Subarray Ranges。

每个子数组的 Range：

maximum - minimum

因此：

answer =
sum_of_subarray_maximums
-
sum_of_subarray_minimums

可以复用 Contribution Counting。

对于 Maximum Contribution，
使用相应的 Greater Boundaries。

同样必须正确处理重复值的 Tie Breaking。

LC-2104 原题规模较小，
O(n^2) 的直接枚举也可能满足约束。

请保留原始 solution.py，
并在 README 对比：

A. O(n^2) 枚举
B. O(n) 单调栈贡献法

不要为了优化而覆盖已有正确解法。

注意：

LC-2104 通常不需要像 LC-907 一样取模。

不能把两题的输出要求混淆。

==================================================
LEVEL 1
03 - 单调栈与贪心构造
==================================================

核心：

Greedy Monotonic Stack
Lexicographical Optimization
Feasibility of Future Choices
Stack Pop Decisions

Level 2：
01 - 字典序优化与安全删除

题目顺序：

LC-0402 - Remove K Digits
LC-0316 - Remove Duplicate Letters

教学重点：

LC-402：

从数字字符串中删除恰好 k 个数字，
使剩余整数尽可能小。

通常使用 Monotonic Increasing Stack。

当：

当前数字 < Stack Top

且：

仍然允许删除数字

时，
可以 Pop 较大的前置数字。

必须解释：

为什么尽可能降低更高位的数字
通常有利于最小化最终结果？

为什么删除次数限制很重要？

为什么如果扫描结束仍有删除额度，
需要从末尾继续删除？

为什么最后要去除 Leading Zeros？

为什么结果为空时返回 "0"？

必须处理：

num = "10", k=2
num = "10200", k=1
num = "1432219", k=3

LC-316：

Remove Duplicate Letters。

目标是输出包含原字符串
每种不同字符恰好一次的
字典序最小 Subsequence。

不能简单遇到更小字符就 Pop。

因为被 Pop 的字符以后
必须还有机会重新加入结果。

推荐维护：

Stack
in_stack Set
last_occurrence Map

当 Stack Top 比当前字符大，
且 Stack Top 以后还会再次出现时，
才可以弹出。

必须解释：

为什么还要检查未来是否会出现？

为什么某个字符已经在 Stack 中时
不应该再次添加？

为什么最终每种不同字符必须恰好出现一次？

为什么保留原始相对顺序是必须的？

比较：

LC-402：
有精确的删除次数限制 k。

LC-316：
必须保留每种字符恰好一次。

二者都利用 Greedy Stack，
但安全删除的条件不同。

请建立与 Greedy 专题的跨专题索引。

==================================================
LEVEL 1
04 - 单调队列与滑动窗口
==================================================

核心：

Monotonic Deque
Window Expiration
Sliding Window Extrema
Max/Min Deques
Prefix Sum Dominance

--------------------------------------------------
Level 2：
01 - 固定窗口最大值

题目顺序：

LC-0239 - Sliding Window Maximum

教学重点：

这是整个 Monotonic Deque 专题最重要的题目。

窗口大小固定为 k。

维护 Deque：

保存当前窗口中
仍有可能成为最大值的元素下标。

推荐使用递减值顺序。

当新元素到来时：

1. 移除队首已经过期的 Index。
2. 从队尾移除不再具有竞争价值的候选。
3. 将当前 Index 加入 Deque。
4. 当形成完整窗口后，
   队首就是当前最大值所在位置。

必须解释：

为什么存储 Index 而不是只存 Value？

为什么需要同时支持：
popleft()
pop()

为什么队首代表当前最大值？

为什么队尾某些较小元素可以永久删除？

为什么等值元素的处理必须与具体实现一致？

复杂度：

O(n) 时间。

因为每个下标最多进入 Deque 一次、
被移除一次。

不能因为内部存在 while
就错误地声称 O(n^2)。

本题已存在 note.md，
必须完整保留。

与 Sliding Window 专题建立跨专题引用。

--------------------------------------------------
Level 2：
02 - 可变窗口最大值与最小值

题目顺序：

LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

教学重点：

目标：

寻找最长连续子数组，
满足：

max(window) - min(window) <= limit

使用两个 Deque：

max_deque：
维护窗口最大值候选。

min_deque：
维护窗口最小值候选。

当右端点扩展时：
更新两个 Deque。

如果当前窗口不满足：

max - min <= limit

就逐步移动左端点，
并删除过期的队首 Index。

必须解释：

为什么一个 Deque 不足以同时维护 Max 和 Min？

为什么窗口无效时移动 Left 是安全的？

为什么需要检查两个 Deque 的队首 Index？

为什么扩展 Right 时，
某些旧候选可以从队尾删除？

核心：
Two Monotonic Deques + Variable Sliding Window。

与 LC-239 的区别：

239：
窗口长度固定。

1438：
窗口长度可变化，
由 Max-Min 约束控制。

这道题应标记 P1。

--------------------------------------------------
Level 2：
03 - 前缀和与最短合法子数组

题目顺序：

LC-0862 - Shortest Subarray with Sum at Least K

教学重点：

这是 Monotonic Deque 的高级代表题。

数组中可以出现负数。

目标：

找出最短的非空连续子数组，
使元素之和 >= k。

首先建立 Prefix Sum：

prefix[0] = 0

prefix[i] =
nums[0] + ... + nums[i-1]

则：

sum(nums[j:i]) =
prefix[i] - prefix[j]

目标变成：

寻找 j < i，
满足：

prefix[i] - prefix[j] >= k

并最小化：

i - j

使用 Monotonic Increasing Deque，
保存候选 Prefix Sum Index。

每到一个新的 i：

A. 当队首形成合法的子数组时，
   更新最短长度，并弹出队首。

B. 当当前 Prefix Sum
   小于或等于队尾对应的 Prefix Sum 时，
   弹出队尾被支配的候选。

C. 加入当前 Index。

必须解释：

为什么较晚出现、
但 Prefix Sum 更小或相等的下标，
会支配较早且 Prefix Sum 更大的下标？

为什么一个已经得到合法答案的较早起点，
可以在某种处理顺序下安全从队首删除？

为什么数组中存在负数时，
普通的正数 Sliding Window
不能直接保持单调增长的窗口和？

为什么这不是 LC-239 的简单换皮题？

两个题的 Deque 不变量不同：

239：
保持窗口极值候选。

862：
保持尚有价值的 Prefix Sum 起点候选。

时间复杂度：

O(n)。

空间复杂度：

O(n)。

需要测试：

nums=[1], k=1 -> 1
nums=[1,2], k=4 -> -1
nums=[2,-1,2], k=3 -> 3

还应测试：
负数、零、重复 Prefix Sum、
单元素、无法满足的情况。

本题属于 P1 进阶。

==================================================
LEVEL 1
05 - 单调扫描与跨专题存档
==================================================

此分类用于保存：
可以利用单调关系理解，
但不一定需要标准单调栈或队列的题目。

--------------------------------------------------
Level 2：
01 - Car Fleet 与到达时间单调扫描

题目顺序：

LC-0853 - Car Fleet

当前只有：

NC - Car Fleet

请正式化为 LC-0853。

教学重点：

每辆车都有：

position
speed

目标：
统计到达终点时形成多少个 Car Fleets。

先按照 Position 从大到小排序。

对于每辆车，
计算如果独自行驶，
到达 Target 所需时间：

time = (target-position)/speed

从最接近终点的车向后扫描。

如果后车独立到达所需时间
小于或等于前方车队的到达时间：

它会在终点或之前追上前方车队，
因此合并成同一个 Fleet。

否则：
形成新的 Fleet。

必须解释：

- 为什么要按位置排序
- 为什么不能只按速度排序
- 为什么时间相等时也应合并
- 为什么后车不能超越前车
- 为什么只需要比较当前前方车队的到达时间

可以使用 Stack 保存 Fleet Times。

但是：
本题也可以只维护最后一个 Fleet Time
以及当前 Fleet Count。

必须解释为什么不必强制使用完整 Stack。

这属于：

Sorting + Monotonic Arrival-time Scan。

不要错误地把它讲成 Next Greater Element。

当前 NC 来源中：

asset-Scan 15.jpeg

必须完整保留。

--------------------------------------------------
Level 2：
02 - Suffix Maximum 与右侧可见性

题目顺序：

LC-1762 - Buildings With an Ocean View

教学重点：

每栋楼只有在右侧没有任何
高度大于或等于它的建筑时，
才有 Ocean View。

推荐从右到左扫描。

维护：

max_height_to_right

若：

height > max_height_to_right

则当前建筑拥有 Ocean View。

随后更新最大高度。

必须解释：

为什么需要严格大于？

为什么右侧有同样高度的建筑时
当前建筑没有 Ocean View？

为什么不需要用 Monotonic Stack
也能够在线性时间内解决？

这是 Suffix Maximum 的基础应用。

属于 P2（针对 Monotonic Stack 专题）。

不能为了算法分类
而强制使用不必要的数据结构。

--------------------------------------------------
Level 2：
03 - Greedy 跨专题来源存档

现有：

NC - Gas Station

对应：

LC-0134 - Gas Station

请核对题面及代码。

这是 Greedy + Running Balance 问题，
不是标准 Monotonic Stack / Deque。

当前 Greedy 专题：

13-greedy (贪心)

很可能已经存在正式 LC-134。

请只读检查。

如果 Greedy 专题已有 LC-134：

1. 将当前 NC - Gas Station
   完整归档于本 Level 2 的来源存档。
2. 在 README 中链接 Greedy 的正式题目。
3. 标记 Primary Pattern = Greedy。
4. 不要重新生成一套完整的 LC-134 PDF。
5. 不要修改 Greedy 专题。

如果 Greedy 专题尚未有 LC-134：

保留 NC 原始目录全部内容。

在 README 中登记：
LC-0134 - Gas Station

但本次仍不得写入 Greedy 专题。

此处可以建立：
带有正式 LC 编号的档案目录，
其中只保存原始 NC 来源及交叉引用说明。

不要伪造不存在的正式 LC 文件。

特别保留：

note.md
metadata.json
problem.pdf
problem_dark.pdf
solution.py

不要因其不属于单调栈
就删除学习成果。

==================================================
四、原始 NC 题目的处理
==================================================

当前三个 NC-only 来源：

NC - Car Fleet
NC - Largest Rectangle In Histogram
NC - Gas Station

对应：

LC-0853 - Car Fleet
LC-0084 - Largest Rectangle in Histogram
LC-0134 - Gas Station

其中：

LC-853、LC-84：
属于当前专题的正式学习题。

需要核对后建立标准 LC Level 3，
并在内部 _neetcode/ 保存 NC 全部原始资料。

LC-134：
属于 Greedy，
按照跨专题存档规则处理。

不能仅因为题目来自 NC，
就重复生成其他专题已有的官方资料。

特别保护：

NC - Largest Rectangle In Histogram：

asset-explanation-1.jpeg
asset-explanation-2-claude.jpg
note.md

NC - Car Fleet：

asset-Scan 15.jpeg

NC - Gas Station：

note.md

必须保留所有旧 solution.py。

不能使用新生成的 solution.py
覆盖原始 NC 版本。

如果已有标准 LC-84 或 LC-853
存在于其他专题，
先确认其来源和内容，
再决定只建立链接还是创建本专题主目录。

==================================================
五、第一轮明确新增的六道题
==================================================

本次第一轮建议新增：

LC-0503 - Next Greater Element II
LC-0901 - Online Stock Span
LC-0907 - Sum of Subarray Minimums
LC-0085 - Maximal Rectangle
LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
LC-0862 - Shortest Subarray with Sum at Least K

先检查当前专题与整个仓库。

确认：

1. 是否已有该题。
2. 是否存在其他专题的完整资料。
3. 哪个专题更适合主归属。
4. 是否有可复用的原始实现。
5. 是否需要正式创建本专题目录。

对于本专题确实需要新增的题：

调用仓库已有的 LeetCode 生成工作流。

标准文件：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

必须复用现有仓库的生成能力，
不要未经必要重新设计生成器。

如果题目生成受限：
- 不伪造 metadata。
- 不创建空 PDF。
- 不以其他题目的 PDF 替代。
- 不覆盖用户原始代码。
- 报告未完成原因。

若已有完整题目位于其他专题，
优先考虑建立跨专题索引，
但不能删除当前专题已经存在的原始资料。

==================================================
六、Claude Code 第二轮独立审核
==================================================

上述是 ChatGPT 的第一轮筛选。

请独立进行第二轮审核，
检查是否遗漏真正高价值的单调栈/队列 Pattern。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
可信的 Monotonic Stack / Queue 学习资料

如网络可用：
核对题号、官方英文名称、
题目约束与典型解法。

不要编造 FAANG 内部真实出题频次。

重点检查：

1. Next Greater Element
2. Next Smaller Element
3. Previous Greater / Smaller
4. Monotonic Index Stack
5. Circular Next Greater
6. Online Stock Span
7. Histogram Rectangle
8. Nearest Smaller Boundaries
9. Contribution Counting
10. Duplicate Tie Breaking
11. Greedy Monotonic Stack
12. Lexicographical Optimization
13. Fixed-size Monotonic Deque
14. Variable-size Two Deques
15. Prefix Sum + Monotonic Deque
16. Amortized Linear Complexity
17. Sorting + Monotonic Scan
18. Suffix Maximum without Stack

额外候选：

LC-0042 - Trapping Rain Water
LC-0456 - 132 Pattern
LC-1019 - Next Greater Node In Linked List
LC-1475 - Final Prices With a Special Discount in a Shop
LC-1673 - Find the Most Competitive Subsequence
LC-1944 - Number of Visible People in a Queue
LC-1856 - Maximum Subarray Min-Product
LC-2289 - Steps to Make Array Non-decreasing
LC-1081 - Smallest Subsequence of Distinct Characters
LC-2398 - Maximum Number of Robots Within Budget

这些只是候选，不要求全部添加。

特别注意：

LC-42：
可能已经在 Two Pointers 专题，
也可以使用 Monotonic Stack。
如果已有完整资料，
优先建立跨专题索引。

LC-456：
属于比较有独立价值的 Monotonic Stack 应用，
可评估是否值得增加。

LC-1019：
Next Greater Element on Linked List。
与 LC-739 的核心不变量相似。

LC-1475：
Next Smaller or Equal。
与 Next Greater 模板非常接近，
可用于理解比较符号，
但不一定值得新增。

LC-1673：
Greedy Monotonic Stack。
与 LC-402、LC-316 有明显关联。

LC-1944：
Visibility + Monotonic Stack。
具有额外的可见性约束。

LC-1856：
Monotonic Boundaries + Prefix Sum，
与 LC-84、907 的迁移关系非常直接。

LC-2289：
更复杂的 Monotonic Stack + DP / Round Counting。
学习成本较高。

LC-1081：
本质上与 LC-316 相同，
不应重复创建不同的核心学习题。

LC-2398：
Monotonic Deque + Variable Sliding Window，
可能与 LC-1438 有较多重合。

本次最多自主新增 3 道不同题目。

新增必须满足：

A. 具有清晰的独立 Pattern。
B. 有较高面试代表性。
C. 能明显补充知识缺口。
D. 不只是已有题目的重复训练。
E. 不会显著增加机械记忆负担。
F. 当前仓库没有更合理的现成归属。

如果没有真正需要补充的题，
可以不新增。

如果候选超过 3 道，
只选择最重要的三道，
其余记录在 Future Candidates。

不要将所有带 Monotonic Stack 标签的题
都纳入正式题库。

==================================================
七、单调栈与单调队列的区别
==================================================

根 README 必须建立：

Monotonic Stack vs Monotonic Deque。

必须解释：

【Monotonic Stack】

通常支持：

push
pop
peek

常用于：

- Next Greater
- Next Smaller
- Previous Greater
- Histogram Boundaries
- Greedy Removal

一般不需要从底部删除已经过期的元素。

【Monotonic Deque】

支持：

append
pop
popleft

常用于：

- Sliding Window Maximum
- Sliding Window Minimum
- Window Expiration
- Prefix Sum Candidate Pruning

其中：

从队尾移除：
一般用于维护单调性或删除被支配候选。

从队首移除：
可能用于移除过期状态，
也可能用于结算已经满足条件的最优候选。

必须说明：
不能把所有 popleft()
都解释成“窗口过期”。

例如：

LC-239：
队首下标超出窗口边界时删除。

LC-862：
队首候选形成合法子数组后，
可能通过弹出它寻找更短的答案。

这两种队首删除的原因不同。

==================================================
八、严格比较与重复元素
==================================================

这是本次最重要的正确性检查之一。

请单独生成：

Strict vs Non-strict Comparison Cheat Sheet。

必须覆盖：

Next Greater：

寻找严格大于当前值的元素。

Daily Temperatures：

只接受严格更高的温度。

Online Stock Span：

相同价格也计入连续跨度，
因此相等价格应被合并。

Histogram：

等高柱子的边界处理
需要与所选栈算法一致。

Subarray Minimum Contribution：

左右边界要使用一严格一非严格的规则，
确保重复值不会重复计数。

Subarray Maximum Contribution：

同样需要一致的 Tie Breaking。

Sliding Window Maximum：

保留旧的相等候选，
或者移除旧的相等候选，
都可能是正确实现。

但必须清楚解释下标过期处理，
并保证队首始终对应有效答案。

Buildings With an Ocean View：

右侧有相等高度的建筑也会遮挡视野，
因此需要严格大于后缀最大高度。

Car Fleet：

后车与前方车队的到达时间相同，
仍然能够合并。

请用以下小输入验证相关规则：

[2,2]
[2,2,2]
[1,2,1]
[3,1,2,4]
[5,5,4,5]

在适用的具体题目中验证，
而不是把这些输入强行套入所有题目 API。

==================================================
九、Amortized O(n) 正确性证明
==================================================

必须明确解释：

为什么代码：

for i in range(n):
    while stack and ...:
        stack.pop()

不一定是 O(n^2)。

核心：

每个元素通常最多：

Push 一次
Pop 一次

因此总 Push 次数 O(n)，
总 Pop 次数 O(n)。

虽然某次迭代可以 Pop 很多元素，
但是这些被弹出的元素以后不会再次进入同一个栈。

所以总体复杂度可能是 O(n)。

Monotonic Deque 也类似。

但必须根据具体实现说明：

- 每个元素是否只入队一次
- 是否可能被重复入队
- 每个元素是否最多被移除一次
- 是否有额外排序
- 是否有其他更高成本操作

例如：

LC-503 模拟两轮扫描，
仍然是 O(n)。

LC-853 先排序：
总体 O(n log n)，
不能因为扫描阶段是 O(n)
就声称总算法 O(n)。

LC-85 每行调用 Histogram：
总体 O(rows*cols)。

不要机械地将所有单调题
都写成 O(n) 时间。

==================================================
十、Pattern Recognition Guide
==================================================

根 README 必须创建：

Monotonic Pattern Recognition Guide。

Q1：
是否寻找右侧第一个更大元素？
-> Next Greater Monotonic Stack。

Q2：
是否寻找右侧第一个更小元素？
-> Next Smaller Monotonic Stack。

Q3：
是否需要计算某个元素向左右延伸的有效范围？
-> Previous / Next Boundary Stack。

Q4：
是否需要计算最大柱状图矩形？
-> Increasing Stack + Boundary Width。

Q5：
是否需要统计一个元素
作为多少个子数组的最小值或最大值？
-> Contribution Counting。

Q6：
是否需要不断删除之前较大的字符或数字，
形成字典序最优结果？
-> Greedy Monotonic Stack。

Q7：
是否需要固定大小窗口的最大值？
-> Monotonic Deque。

Q8：
是否需要可变大小窗口的最大值和最小值？
-> Two Monotonic Deques。

Q9：
是否需要找到满足前缀和约束的最短子数组，
且数组可能含负数？
-> Prefix Sum + Monotonic Deque。

Q10：
是否只需要从右向左维护最大值？
-> Suffix Maximum，可能根本不需要 Stack。

Q11：
是否要判断车队追赶与合并？
-> Sorting + Monotonic Arrival-time Scan。

Q12：
是否只是寻找 Gas Station 可行起点？
-> Greedy Running Balance，
   不是标准 Monotonic Stack。

强调：

先判断真正需要解决的目标，
再决定是否使用单调数据结构。

不能因为题目标签出现 Stack
就强行使用 Stack。

==================================================
十一、核心 Python 模板
==================================================

请在 README 中提供少量可复用模板。

Template 1：
Next Greater Element with Index Stack

Template 2：
Previous / Next Smaller Boundaries

Template 3：
Histogram Largest Rectangle

Template 4：
Contribution Counting

Template 5：
Greedy Monotonic Stack

Template 6：
Sliding Window Maximum with Deque

Template 7：
Two Deques for Window Max / Min

Template 8：
Prefix Sum + Monotonic Deque

这些是 Pattern 模板，
不是八套必须机械默写的复杂算法。

每个模板需要说明：

1. Stack / Deque 保存什么？
2. 单调性不变量是什么？
3. 什么条件下 Pop？
4. 为什么可以安全 Pop？
5. 什么时候记录答案？
6. 什么条件下清理队首？
7. 为什么复杂度正确？
8. 哪些题目复用这个模板？

优先给出：

可运行的 Python 参考代码。

所有模板应包含明确的比较符号，
不能使用含糊的伪代码代替关键逻辑。

==================================================
十二、跨专题索引
==================================================

允许只读扫描整个：

leetcode-practice

仓库。

重点检查：

LC-0134 -> Greedy / Gas Station
LC-0239 -> Sliding Window
LC-0316 -> Stack / Greedy
LC-0402 -> Stack / Greedy
LC-0042 -> Two Pointers / Trapping Rain Water
LC-0084 -> Stack / Histogram
LC-0085 -> Matrix / Histogram
LC-0853 -> Stack / Car Fleet
LC-0862 -> Prefix Sum / Sliding Window
LC-1438 -> Sliding Window
LC-2104 -> Subarray / Monotonic Stack
LC-1673 -> Greedy Monotonic Stack
LC-1019 -> Linked List / Next Greater
LC-1081 -> 与 LC-316 相同的问题

原则：

1. 当前专题已经有原始题目资料的，
   必须完整保留。
2. 其他专题已有完整题目，
   优先建立相对路径引用。
3. 不修改其他专题。
4. 不无意义地重复生成 PDF。
5. 一个题目可以有 Primary 和 Secondary Pattern。
6. 同一道题的不同算法实现不能随意覆盖。
7. 跨专题索引不能成为删除原始学习成果的理由。

README 中记录：

LC ID
Primary Pattern
Secondary Pattern
Recommended Algorithm
Cross-topic Reference

==================================================
十三、特别保护现有学习资料
==================================================

当前原始目录有：

14 directories
47 files

必须完整保留。

特别注意根目录：

questions_about_monotonic.md

这是原有学习疑问与知识资料。

必须保留原始内容。

请先阅读它，
然后在新 README 或 FAQ 中
针对其中的问题提供简明解释。

不能删除、覆盖或静默改写原始 Markdown。

当前：

LC-0239 - Sliding Window Maximum

存在：

note.md

必须保留。

当前：

NC - Gas Station

存在：

note.md

必须保留。

当前：

NC - Car Fleet

存在：

asset-Scan 15.jpeg

必须保留。

当前：

NC - Largest Rectangle In Histogram

存在：

asset-explanation-1.jpeg
asset-explanation-2-claude.jpg
note.md

必须全部保留。

所有现有：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
Markdown
JPEG
PNG
自定义附件

均必须保留。

如果新增 LC 标准目录与原有 NC 来源同名，
使用 _neetcode/ 或来源目录归档，
不能覆盖任何已有文件。

==================================================
十四、Git 与文件系统安全
==================================================

当前 Git 仓库存在大量未提交修改和未跟踪文件。

请把所有现有文件视为重要学习成果。

开始前必须：

1. pwd
2. tree
3. git status --short
4. 递归扫描当前专题所有文件
5. 记录原始相对路径
6. 记录普通文件 SHA-256
7. 记录文件大小
8. 检查 Symbolic Links
9. 检查原始 Python import
10. 检查 Markdown 相对链接
11. 验证题目身份
12. 建立完整迁移映射

建议在当前专题内建立：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

所有写入必须限定在：

18-monotonic-fuck-you (单调栈、单调队列)

目录内部。

可以只读扫描仓库其他专题。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖原始 solution.py
覆盖 note.md
覆盖 questions_about_monotonic.md
删除 PDF 或图解
修改其他专题
改名当前专题根目录

不要自动：

git add
git commit
git push

对于路径冲突：

- 不同内容必须保留两个版本。
- 相同内容也必须保留来源记录。
- 必要时使用 _conflicts/。
- 不允许静默覆盖。
- 不允许丢失原始文件。

如果存在符号链接：

禁止通过链接对当前专题以外的目标写入。

如果题目生成工具会写入当前专题外的文件，
先寻找可以限制输出范围的配置。

无法保证安全时：
跳过该步骤并明确说明原因。

旧目录必须确认迁移完整，
并且确实为空之后，
才能安全移除空目录。

尽可能保证 Idempotence（幂等）：

重复执行不能：
- 叠加编号
- 重复建立同一道题
- 重复归档 NC 来源
- 覆盖旧解法
- 丢失任何资料

==================================================
十五、README 学习文档
==================================================

必须创建：

A. Monotonic 根目录 README.md

B. 每个 Level 1 的 README.md

C. 必要的 Level 2 README.md

D. Monotonic Pattern Recognition Guide

E. Monotonic Stack vs Deque Comparison

F. Strict vs Non-strict Comparison Cheat Sheet

G. Contribution Counting Cheat Sheet

H. Amortized Complexity Explanation

I. P0 / P1 / P2 Core Roadmap

J. 原始问题 FAQ（参考 questions_about_monotonic.md）

根 README 应包含：

1. 单调栈与单调队列的核心区别。
2. 五个 Level 1。
3. 所有 Level 2 / Level 3。
4. 全部题目的真实相对路径。
5. P0 / P1 / P2。
6. 为什么单调结构能够安全弹出元素。
7. Stack 保存值还是下标。
8. Increasing vs Decreasing。
9. Next Greater / Smaller。
10. Histogram Boundaries。
11. Contribution Counting。
12. Duplicate Tie Breaking。
13. Greedy Monotonic Stack。
14. Fixed / Variable Sliding Window。
15. Prefix Sum + Monotonic Deque。
16. Amortized Analysis。
17. 跨专题引用。
18. 第二轮审核结果。
19. 最终推荐学习顺序。

每个 Pattern 必须包含：

1. 1–3 个决定性观察。
2. 栈/队列保存的状态。
3. 单调性不变量。
4. Push 与 Pop 条件。
5. 为什么这些操作正确。
6. 简短正确性证明。
7. Python 核心模板。
8. 时间与空间复杂度。
9. 代表题目。
10. 典型边界测试。
11. 与相邻 Pattern 的区别。

==================================================
十六、中文主导的技术解释风格
==================================================

所有学习资料使用：

中文主导 + 英文专业术语。

例如：

Monotonic Stack（单调栈）
Monotonic Deque（单调双端队列）
Next Greater Element（右侧第一个更大元素）
Previous Smaller Element（左侧最近更小元素）
Contribution Counting（贡献计数）
Amortized Analysis（摊还分析）
Dominated Candidate（被支配的候选）
Strict Comparison（严格比较）
Tie Breaking（平局规则）
Prefix Sum（前缀和）
Greedy Stack（贪心单调栈）

理论解释顺序：

1. 先给最重要的观察。
2. 定义栈/队列中的内容。
3. 说明 Pop 的条件。
4. 解释 Pop 为什么安全。
5. 给出简短证明。
6. 给出 Python 模板。
7. 说明复杂度。
8. 用小例子验证。

避免冗长重复的解释。

不希望未来复习时，
需要重新读几十页才能理解一个 Pattern。

==================================================
十七、P0 / P1 / P2
==================================================

P0：
最重要的核心 Monotonic Stack / Deque 题。

建议：

LC-0496 - Next Greater Element I
LC-0739 - Daily Temperatures
LC-0084 - Largest Rectangle in Histogram
LC-0239 - Sliding Window Maximum
LC-0402 - Remove K Digits
LC-0316 - Remove Duplicate Letters

P1：
有价值的独立变体。

建议：

LC-0503 - Next Greater Element II
LC-0901 - Online Stock Span
LC-0907 - Sum of Subarray Minimums
LC-2104 - Sum of Subarray Ranges
LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
LC-0862 - Shortest Subarray with Sum at Least K
LC-0853 - Car Fleet

P2：
扩展应用或跨专题存档。

建议：

LC-0085 - Maximal Rectangle
LC-1762 - Buildings With an Ocean View
LC-0134 - Gas Station

其中：

LC-134 应明确标记：

Primary Pattern = Greedy。

不要加入本专题的核心必刷路线。

LC-1762 可以通过简单 Suffix Maximum 完成，
不要求额外背诵 Stack 模板。

LC-85 属于 LC-84 的二维扩展。

第二轮可以适度调整优先级，
但必须解释原因。

不要仅根据 Hard / Medium
决定优先级。

不要把所有题都标记为 P0。

==================================================
十八、数量与完整性
==================================================

当前 tree：

14 个目录。
47 个文件。

题目来源：

10 道不同题目。

已有正式 LC 来源：

LC-0239
LC-0316
LC-0402
LC-0496
LC-0739
LC-1762
LC-2104

共 7 道。

NC-only：

NC - Gas Station
NC - Car Fleet
NC - Largest Rectangle In Histogram

共 3 道。

对应：

LC-0134
LC-0853
LC-0084

第一轮新增：

LC-0503
LC-0901
LC-0907
LC-0085
LC-1438
LC-0862

共 6 道。

如果全部新增：

第一轮预计 16 道不同题目。

各 Level 1 预期分布：

01：4 道
02：4 道
03：2 道
04：3 道
05：3 道

合计：16 道。

这里包含 LC-134 的跨专题存档。

真正需要作为 Monotonic 核心和重要变体学习的题，
应少于 16 道。

如果某些新题已经完整存在于其他专题，
并仅建立索引，
实际本专题实体目录可能少于 16 个。

但要保证全部 16 个不同题目的
学习归属或引用都有明确记录。

第二轮最多新增 3 道。

不能为了凑数字生成空文件或重复 PDF。

==================================================
十九、重要边界测试
==================================================

必须验证：

【Next Greater】

- 全部递增
- 全部递减
- 全部相等
- 重复最大值
- 没有更大元素
- Circular Wraparound

【Histogram】

- 单根柱子
- 所有高度相同
- 严格递增
- 严格递减
- 中间有 0
- 多个局部低谷

【Contribution Counting】

- [1,1]
- [2,2,2]
- [3,1,2,4]
- 含负数的 LC-2104
- 需要取模的 LC-907

【Greedy Stack】

- k 等于字符串长度
- 末尾连续删除
- 重复字符
- 前导零
- 未来不再出现的字符

【Monotonic Deque】

- k=1
- k=n
- 所有元素相等
- 队首过期
- 多个元素连续从队尾弹出
- 负数与重复 Prefix Sum

【Car Fleet】

- 后车追上前车
- 后车无法追上
- 恰好在 Target 追上
- 多辆车合并
- 相同速度

测试必须符合具体题目约束。

不能假设所有题目接受空数组、
重复 Position 或其他不合法输入。

==================================================
二十、最终核心学习路线
==================================================

请生成：

Monotonic Stack & Deque Core Roadmap。

建议：

阶段 A：
Next Greater

LC-496 -> LC-739 -> LC-503

阶段 B：
Previous / Span

LC-901

阶段 C：
Histogram Boundaries

LC-84 -> LC-85

阶段 D：
Contribution Counting

LC-907 -> LC-2104

阶段 E：
Greedy Monotonic Stack

LC-402 -> LC-316

阶段 F：
Monotonic Deque

LC-239 -> LC-1438 -> LC-862

阶段 G：
Related Monotonic Scan

LC-853 -> LC-1762

LC-134 只做 Greedy 跨专题索引。

其中：

LC-85、1762 可以作为 P2 进阶。

LC-862 需要掌握 Prefix Sum 后再练习。

另外输出：

6–8 道真正最核心的单调栈/队列面试题。

要求：

- 覆盖不同的单调不变量。
- 不大量选择重复 Next Greater 题。
- 兼顾 Stack 与 Deque。
- 包含一个贡献计数代表题。
- 包含一个 Histogram 代表题。
- 不包含跨专题的 LC-134。

==================================================
二十一、实际执行顺序
==================================================

请直接执行：

1. pwd。
2. 扫描完整 tree。
3. 检查 Git 状态。
4. 记录原始 47 个文件。
5. 计算原始文件 SHA-256。
6. 检查 Symbolic Links。
7. 读取 questions_about_monotonic.md。
8. 核对所有现有题目。
9. 核对三个 NC 来源的正式题号。
10. 只读检查全仓库跨专题重复。
11. 特别检查 Greedy 专题的 LC-134。
12. 建立完整迁移映射。
13. 创建五个 Level 1。
14. 创建对应 Level 2。
15. 安全迁移原始题目。
16. 为 Level 3 重新编号。
17. 正式化 LC-84。
18. 正式化 LC-853。
19. 安全归档 NC Gas Station。
20. 保留全部 NC 原始资料。
21. 创建第一轮建议新增的六道题。
22. 独立进行第二轮题库审核。
23. 必要时新增最多三道高价值题。
24. 按最终学习顺序调整编号。
25. 创建根目录 README。
26. 创建五个 Level 1 README。
27. 创建 Pattern Recognition Guide。
28. 创建 Stack vs Deque Comparison。
29. 创建 Strict vs Non-strict Cheat Sheet。
30. 创建 Contribution Counting Cheat Sheet。
31. 创建 Amortized Analysis 笔记。
32. 结合原始问题文档生成 FAQ。
33. 创建 P0/P1/P2 Roadmap。
34. 对新增代码执行语法检查。
35. 测试重复值和边界条件。
36. 验证旧文件 SHA-256。
37. 检查原始学习附件完整性。
38. 检查 README 相对链接。
39. 验证目录编号连续。
40. 只清理确认已空的旧目录。
41. 运行最终 tree。
42. 检查最终 Git 状态。
43. 输出详细验收报告。

最终报告必须包含：

- 完整最终 tree
- 五个 Level 1
- 所有 Level 2 Pattern
- 原有十道题的迁移结果
- LC-84 / LC-853 正式化结果
- NC Gas Station 跨专题归档
- 第一轮六道新增题目
- 第二轮自主新增题目
- 未新增候选及原因
- P0 / P1 / P2 数量
- 6–8 道最核心学习路线
- 原始问题文档处理结果
- Stack / Deque 比较规则检查
- Duplicate Tie Breaking 测试
- 原始文件 SHA-256 校验
- 跨专题索引
- Git 变更摘要
- 未完成或失败事项

如果某个操作存在文件损坏、
越界写入或覆盖用户资料的风险：

保留相关原文件，
明确报告原因，
继续完成其他安全任务。

不要只输出重构规划。

请直接开始完整的
Monotonic Stack & Monotonic Deque 专题重构。
PROMPT
)"
