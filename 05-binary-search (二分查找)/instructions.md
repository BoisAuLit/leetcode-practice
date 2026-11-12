
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/05-binary-search (二分查找)' && claude "$(cat <<'PROMPT'
请直接执行当前 Binary Search（二分查找）LeetCode 学习目录的全面重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请建立一套高质量、覆盖核心面试题型、教学顺序清晰、能够长期复习，并且尽可能减少记忆负担的 Binary Search 学习体系。

你必须实际执行目录重构、现有文件迁移、新题目生成、文档编写和最终验证，而不是只输出计划。

==================================================
一、最重要的学习目标
==================================================

我希望真正掌握 Binary Search 的少量核心不变量，而不是机械记住几十个不同模板。

重点学习：

1. Exact Binary Search（精确查找）
2. Lower Bound（第一个 >= target 的位置）
3. Upper Bound（第一个 > target 的位置）
4. First True / Last True（单调谓词边界）
5. Structural Binary Search（特殊结构上的二分）
6. Binary Search on Answer（二分答案）
7. Feasibility Check（可行性判断）
8. Binary Search Partition（二分分区）

必须特别解释：

- 为什么可以排除一半搜索空间？
- 当前搜索区间的不变量是什么？
- low/high 代表什么？
- 为什么选择当前 mid？
- 为什么边界更新是安全的？
- 如何防止死循环？
- 如何处理重复元素与边界不存在？
- 什么情况下根本不能使用 Binary Search？

所有同级目录按学习优先级排序。

综合标准：

A. 面试代表性
B. 算法迁移价值
C. 教学基础性
D. 逻辑依赖关系
E. 记忆成本
F. 难度递进

不按照题号机械排序。

不要因为某题带 Binary Search 标签就自动收录。

==================================================
二、目录层级与命名规范
==================================================

采用：

Level 1：Binary Search 算法家族
Level 2：具体 Pattern
Level 3：具体 LeetCode 题目
Level 4：仅在确实必要时使用

所有同级正式学习文件夹必须使用：

01 - ...
02 - ...
03 - ...

Level 3 格式：

01 - LC-XXXX - Official Problem Title
02 - LC-YYYY - Official Problem Title

每个 Level 2 内的 Level 3 编号独立从 01 开始。

不要创建无教学价值的深层嵌套。

题目文件夹应尽可能包含：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

所有已有额外资料必须保留。

资源文件夹使用 _resources。
NC 原始题目使用 _neetcode 归档。

==================================================
三、Level 1 -> Level 3 目标结构
==================================================

第一轮采用以下 6 个 Level 1 分类。

--------------------------------------------------
LEVEL 1
01 - 基础查找与边界二分 (Basic and Boundary Search)
--------------------------------------------------

核心：

Exact Search
Lower Bound
Upper Bound
Monotonic Predicate
Half-open Search Interval

Level 2：
01 - 标准精确查找

Level 3：

01 - LC-0704 - Binary Search

教学重点：

最基础的二分查找。
使用 lo、hi、mid。
寻找 target 是否存在。

理解：

- 搜索区间如何逐渐缩小
- nums[mid] < target 时为什么可以丢弃左半部分
- nums[mid] > target 时为什么可以丢弃右半部分
- 为什么 O(log n)

--------------------------------------------------

Level 2：
02 - Lower Bound 与 Upper Bound

Level 3：

01 - LC-0035 - Search Insert Position
02 - LC-0034 - Find First and Last Position of Element in Sorted Array
03 - LC-0278 - First Bad Version

教学重点：

LC-35：
Lower Bound。
寻找第一个大于等于 target 的位置。

LC-34：
通过 Lower Bound / Upper Bound 找到 target 的左右边界。

LC-278：
First True Predicate。
从 False -> True 的单调布尔序列中寻找第一个 True。

必须解释：

bisect_left 和 bisect_right 的区别。

Lower Bound：
first index with nums[i] >= target。

Upper Bound：
first index with nums[i] > target。

必须展示二者的 Python 实现和对应循环不变量。

不要将“最后一个等于 target”与 Upper Bound 的返回索引混淆。

--------------------------------------------------

Level 2：
03 - 二维有序结构与未知边界

Level 3：

01 - LC-0074 - Search a 2D Matrix
02 - LC-0702 - Search in a Sorted Array of Unknown Size

教学重点：

LC-74：
将二维矩阵逻辑上展开为有序的一维数组。

mid 对应：

row = mid // cols
col = mid % cols

整体达到 O(log(m*n))。

必须说明这种展开要求矩阵满足题目给定的跨行有序条件。

LC-702：
Exponential Search。
先倍增寻找搜索上界，然后在该区间内二分。

注意：
LC-702 属于 Premium。
保留原有文件。

--------------------------------------------------

Level 2：
04 - 整数范围与单调数学谓词

Level 3：

01 - LC-0069 - Sqrt(x)
02 - LC-0367 - Valid Perfect Square
03 - LC-0374 - Guess Number Higher or Lower

教学重点：

LC-69：
寻找满足 mid*mid <= x 的最大整数。

LC-367：
判断是否存在整数平方恰好等于 num。

LC-374：
根据 Guess API 的反馈排除一半候选。

注意：

LC-69 与 LC-367 的思想高度相似。
不能将它们当成两个必须单独记忆的算法模板。

这组题主要用于巩固基本边界与整数计算。
并非所有题目都需要标记 P0。

==================================================
LEVEL 1
02 - 旋转数组、峰值与结构性二分 (Structural Search)
==================================================

核心：

Rotated Sorted Array
Locally Ordered Half
Peak Search
Parity Invariant
Indexed Monotonic Function

Level 2：
01 - Rotated Sorted Array

Level 3：

01 - LC-0153 - Find Minimum in Rotated Sorted Array
02 - LC-0033 - Search in Rotated Sorted Array

教学重点：

LC-153：
与右边界比较。
利用旋转数组结构寻找最小值。

LC-33：
判断左半边或右半边哪部分有序。
再判断 target 是否处于该有序区间。

必须解释：

为什么至少有一侧保持有序？
为什么可以排除另一侧？

注意本组题目默认符合题目给定的无重复元素条件。

对于允许重复元素的 Rotated Array 变体，
不能无条件套用相同证明。

--------------------------------------------------

Level 2：
02 - Peak 与奇偶结构

Level 3：

01 - LC-0162 - Find Peak Element
02 - LC-0540 - Single Element in a Sorted Array

教学重点：

LC-162：
比较 nums[mid] 和 nums[mid+1]。
根据坡度方向寻找 Peak。

必须解释：

为什么可以朝更高的一侧搜索？
不要求整个数组全局有序。

LC-540：
元素成对出现，只有一个元素只出现一次。
利用配对位置和下标奇偶关系做 Binary Search。

必须解释：
为什么目标元素出现前后，成对元素的下标规律会改变。

--------------------------------------------------

Level 2：
03 - 索引单调状态与连续窗口起点

Level 3：

01 - LC-1539 - Kth Missing Positive Number
02 - LC-0658 - Find K Closest Elements

教学重点：

LC-1539：
定义：

missing(i) = arr[i] - (i+1)

该函数在有序、互异正整数数组上单调不减。

二分寻找缺失数量首次达到 k 的边界。

注意：
它主要是对索引及缺失数量的关系进行二分。
不是典型的对任意答案进行成本模拟的 Binary Search on Answer。

LC-658：
可以对连续长度为 k 的候选窗口起点做二分。

比较：

x - arr[mid]
arr[mid+k] - x

理解为什么可以排除不优的窗口起点。

该题也有其他正确解法。
本专题优先提供能清晰体现二分边界思想的解法。

==================================================
LEVEL 1
03 - 二分答案与可行性判断 (Binary Search on Answer)
==================================================

这是本专题最重要的进阶知识家族。

必须明确区分：

Minimum Feasible Answer
Maximum Feasible Answer

核心：

将 Optimization Problem（优化问题）
转换成 Decision Problem（判定问题）。

定义：

feasible(x) -> bool

然后根据单调性寻找正确边界。

--------------------------------------------------

Level 2：
01 - 最小可行速度、时间与资源

Level 3：

01 - LC-0875 - Koko Eating Bananas
02 - LC-1011 - Capacity To Ship Packages Within D Days
03 - LC-1482 - Minimum Number of Days to Make m Bouquets
04 - LC-1283 - Find the Smallest Divisor Given a Threshold

教学重点：

LC-875：
二分最小吃香蕉速度。

可行性：
给定速度 x，能否在 h 小时内完成？

注意整数向上取整：
(pile + x - 1) // x

LC-1011：
二分最小运输容量。

给定 capacity，
通过 Greedy Simulation 计算所需天数。

合理下界：
max(weights)

合理上界：
sum(weights)

LC-1482：
二分最小制作天数。

给定 day，
判断能否制作 m 束、每束 k 朵相邻花。

必须检查：
m*k > len(bloomDay) 时无解。

LC-1283：
二分最小除数。
使用向上取整计算结果总和。

重点讲解：
为什么速度、容量、天数、除数都可以抽象成“第一个可行答案”。

--------------------------------------------------

Level 2：
02 - Minimize Maximum 与贪心可行性

Level 3：

01 - LC-0410 - Split Array Largest Sum
02 - LC-2616 - Minimize the Maximum Difference of Pairs

教学重点：

LC-410：
Minimize Maximum Subarray Sum。

给定最大允许子数组和 x，
通过 Greedy 判断能否拆分成不超过 k 组。

解释：
- 为什么按顺序贪心分组可行
- 为什么可行性随 x 单调变化
- 为什么最小可行 x 就是答案

题目的非负整数约束对这个贪心判断很重要。

LC-2616：
先排序。
给定最大允许差值 x，
贪心选择相邻且不重叠的有效配对。

判断能否构造至少 p 对。

必须解释：
为什么排序后可以贪心。
为什么不需要尝试所有配对组合。

两题共享 Binary Search on Answer，
但 Feasibility Check 的 Greedy 逻辑不同。

--------------------------------------------------

Level 2：
03 - Maximize Minimum

Level 3：

01 - LC-1552 - Magnetic Force Between Two Balls

教学重点：

与最小可行答案相反：

本题最大化最小距离。

给定距离 d，
判断能否放置 m 个球，
使任意相邻选中位置的距离至少为 d。

需要排序并使用 Greedy Placement。

这是典型的：

True True True False False

二分寻找 Last True。

必须解释：

Minimum Feasible 和 Maximum Feasible
的谓词单调方向不同。

不能混淆两者的边界更新方式。

==================================================
LEVEL 1
04 - 二分查找与数据结构设计 (Binary Search Design)
==================================================

Level 2：
01 - 按时间戳检索历史版本

Level 3：

01 - LC-0981 - Time Based Key-Value Store

教学重点：

Hash Map + Sorted Timestamps + Binary Search。

每个 key 维护有序的：
(timestamp, value)

get(key, timestamp)：

寻找 timestamp 不超过查询值的最近记录。

对应：
Upper Bound - 1

必须解释：

- 为什么使用二分而不是线性扫描
- 如何处理不存在的 key
- 如何处理不存在的历史时间
- 时间戳升序插入的题目约束
- Python bisect 的正确使用方式

此题是二分查找与数据结构设计结合的经典案例。

==================================================
LEVEL 1
05 - 双有序数组与分区二分 (Binary Search Partition)
==================================================

Level 2：
01 - 两个有序数组的正确分区

Level 3：

01 - LC-0004 - Median of Two Sorted Arrays

本题当前只有：
NC - Median of Two Sorted Arrays

请确认题目对应关系后升级整理。

教学重点：

Binary Search on Partition。

在较短数组上二分分区位置。

使用：

leftA
rightA
leftB
rightB

正确分区需要满足：

leftA <= rightB
leftB <= rightA

然后根据奇数或偶数长度计算 Median。

必须解释：

- 为什么两个数组的分区大小存在确定关系
- 为什么只需二分较短数组
- 为什么可以根据边界比较移动分区
- 如何处理空数组
- 如何处理奇偶总长度
- 如何处理 +/- infinity 哨兵
- 为什么时间复杂度 O(log(min(m,n)))

此题属于 Hard。

标记为 P1 进阶重点，
不要求在最初学习阶段强行背诵。

==================================================
LEVEL 1
06 - 低优先级与跨专题存档 (Archive)
==================================================

该分类不属于核心必刷路线。

用于保留已有学习成果以及特殊、低迁移性题目。

--------------------------------------------------

Level 2：
01 - BST 性质与最近值

Level 3：

01 - LC-0270 - Closest Binary Search Tree Value

说明：

本题利用 Binary Search Tree 的有序性质进行搜索。

它并不是标准的有序数组 Binary Search 模板。

更适合在 BST 专题复习。

保留当前原始解法、PDF 和所有资料。
在 README 中建立跨专题引用。

--------------------------------------------------

Level 2：
02 - 非典型二分标签题

Level 3：

01 - LC-3346 - Maximum Frequency of an Element After Performing Operations I

说明：

此题可以使用 Sorting、Sliding Window、
Prefix Sum / Difference Array 等技巧。

不要因为 LeetCode 存在 Binary Search 标签，
就将其强行讲成典型 Binary Search on Answer。

标记 P2。

完整保留其现有代码、PDF 和附件。

--------------------------------------------------

Level 2：
03 - 特殊数学约束与二分答案

Level 3：

01 - LC-3733 - Minimum Time to Complete All Deliveries

说明：

这是实际的 Binary Search on Answer 应用。

但可行性检查涉及：
- 周期性不可用时间
- 两个配送主体的独立限制
- 不能同时执行配送
- 容斥或 LCM 相关计数

比 Koko / Shipping Capacity 更特殊。

建议 P2，保留进阶学习资料。

不要将它视为普通基础二分题。

==================================================
四、明确新增题目与文件生成
==================================================

第一轮明确建议新增的 7 道不同题目：

LC-0074 - Search a 2D Matrix
LC-1011 - Capacity To Ship Packages Within D Days
LC-1482 - Minimum Number of Days to Make m Bouquets
LC-0410 - Split Array Largest Sum
LC-1283 - Find the Smallest Divisor Given a Threshold
LC-1552 - Magnetic Force Between Two Balls
LC-0658 - Find K Closest Elements

另外：

NC - Median of Two Sorted Arrays

需要整理为正式 LC-0004。

对于每一道新增题：

1. 先检查当前目录。
2. 再检查全仓库是否存在。
3. 如果已有当前专题版本，保留原有文件。
4. 如果其他专题已有同题，判断主归属并优先建立交叉索引。
5. 如本专题确实需要实体题目且当前不存在，调用已有 LeetCode 生成工具。
6. 不能无意义生成重复版本。

应生成：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据 LeetCode 编号生成这些文件的能力。

请复用原有生成工作流。

现有题目缺少标准文件时，也应尝试补齐。

严禁覆盖用户原来的 solution.py、note.md 或其他学习资料。

==================================================
五、NC / LC 重复题目整理
==================================================

当前已有：

NC - Koko Eating Bananas
LC-0875 - Koko Eating Bananas

NC - Time Based Key-Value Store
LC-0981 - Time Based Key-Value Store

NC - Find Minimum in Rotated Sorted Array
LC-0153 - Find Minimum in Rotated Sorted Array

NC - Search in Rotated Sorted Array
LC-0033 - Search in Rotated Sorted Array

以及：

NC - Median of Two Sorted Arrays

请检查实际题面和代码。

对于前四组：

1. 保留正式 LC 目录。
2. 将 NC 版本全部文件放入对应 LC 题目的 _neetcode/ 子目录。
3. 保留两套 solution.py 和 PDF。
4. 不覆盖已有代码。
5. 若两个版本算法不同，在 README 中简要注明差异。
6. 同一道题只占据一个正式 Level 3 位置。

对于 Median：

- 创建正式 LC-0004 目录。
- 原 NC 文件完整迁入 _neetcode/。
- 补齐标准 LC 文件。
- 不丢失原来的实现或注释。

==================================================
六、现有理论资料与代码模板
==================================================

当前目录存在：

00-Theory/

其中包含：
- bisect_left+bisect_right.png
- claude_code_理论.pdf
- claude_code_图解.png

以及：

templates/

包含多个 Binary Search Python 模板、PDF
和至少一个 Symbolic Link（符号链接）。

请统一整理到：

_resources/
  00-Theory/
  templates/

必须完整保留全部文件。

特别注意：

templates 下存在指向其他 Greedy 目录的 .py 符号链接。

请：

1. 使用 lstat / readlink 检查符号链接。
2. 不跟随符号链接修改外部目标。
3. 不复制或修改外部目标文件内容。
4. 不在本次重构中自动修复指向外部的链接。
5. 如果链接已经失效，保留原链接并在报告中说明。
6. 迁移符号链接对象本身时，不允许解引用。
7. 不允许因移动模板目录而修改 Greedy 专题文件。

对于模板：

保留全部现有版本。

可以在 README 中建立一个统一的模板索引，
但不得删除或覆盖原来的 Template 1 / 2 / 3。

==================================================
七、Claude Code 第二轮独立审核
==================================================

以上清单是 ChatGPT 第一轮筛选的结果。

你还必须独立检查是否存在重要遗漏。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
可靠的 Binary Search 面试学习资料

如果具备网络能力，可核对官方题号、名称、
约束、题目难度与代表性。

不要编造 FAANG 企业内部出题频次。

重点审核：

1. Exact Search
2. Lower Bound / Upper Bound
3. First True / Last True
4. Rotated Array
5. Peak Search
6. Parity-based Search
7. Search Unknown Size
8. Search in Matrix
9. Binary Search on Answer
10. Minimum Feasible
11. Maximum Feasible
12. Greedy Feasibility Check
13. Binary Search Partition
14. Timestamp Lookup
15. Index-based Monotonic Function
16. Binary Search Combined With Sorting

重点考虑以下候选：

LC-1760 - Minimum Limit of Balls in a Bag
LC-0852 - Peak Index in a Mountain Array
LC-0081 - Search in Rotated Sorted Array II
LC-0154 - Find Minimum in Rotated Sorted Array II
LC-0378 - Kth Smallest Element in a Sorted Matrix
LC-1870 - Minimum Speed to Arrive on Time
LC-0275 - H-Index II

这些题目不要求全部新增。

尤其注意：

- LC-852 与 LC-162 具有明显重复性。
- LC-81 / 154 主要用于研究重复元素导致的边界退化。
- LC-1760 与 Koko / Divisor 的二分答案模式有重合。
- LC-378 可以使用其他算法，必须说明对应的二分方案及适用约束。

是否新增取决于它们是否真正填补了教学缺口。

独立新增建议最多 5 道。

每道新增题必须说明：

1. 对应哪个重要 Pattern？
2. 为什么面试中值得练习？
3. 与已有题目的区别是什么？
4. 为什么不是无意义重复？
5. 推荐放在哪个 Level 1 / Level 2？
6. P0 / P1 / P2 优先级？

如果发现有必要的新 Pattern：
允许新增 Level 1 或 Level 2。

但不能为了一道偏门题无限扩张分类数量。

如果独立审核没有发现值得新增的题，
可以不新增。

==================================================
八、跨专题去重原则
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

- LC-270 是否位于 BST 专题
- LC-2616 是否位于 Greedy 专题
- LC-3346 是否位于 Sliding Window 专题
- LC-4 是否已有其他版本
- 其他候选题是否已存在

本次只能修改当前 Binary Search 目录。

不得移动、覆盖、重命名或删除其他专题的文件。

如果其他专题中已经有题目：

- 优先确定最合适的主归属
- 通过 README 使用相对路径建立跨专题索引
- 不重复生成无价值的题目副本
- 不删除当前目录已有学习成果
- 不修改外部目录

不要通过符号链接访问外部文件并写入。

==================================================
九、Git 与现有文件安全
==================================================

当前仓库存在大量未提交修改和未跟踪文件。

这点非常重要。

开始执行前：

1. pwd
2. tree
3. git status --short
4. 递归列出全部文件和符号链接
5. 记录原始文件相对路径
6. 记录普通文件 SHA-256
7. 记录符号链接目标字符串
8. 建立旧路径到新路径的迁移映射
9. 检查目标路径冲突
10. 检查是否存在未提交修改

严格禁止：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖原有 solution.py
修改其他算法目录

本次不自动：

git add
git commit
git push

优先使用安全的文件系统移动操作。
不要使用会改动 Git 暂存区的方式进行无必要的迁移。

如果发生同名冲突：

- 相同内容可以按可追溯规则归档
- 不同内容必须分别保留
- 使用 _conflicts/ 保存冲突版本
- 在最终报告中说明

不允许在没有验证的情况下丢弃文件。

旧目录只有确认完全迁移且为空后，
才允许删除空目录。

确保操作尽可能 Idempotent（幂等）。

重复执行不得创建重复题目或破坏原有文件。

==================================================
十、生成高质量 README 学习文档
==================================================

必须创建：

A. 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 创建必要的简短 README.md

根目录 README：

1. Binary Search 知识地图
2. 六大算法家族的教学目标
3. 所有题目的推荐学习顺序
4. P0 / P1 / P2 分类
5. 核心 Python 模板
6. 关键不变量
7. 标准复杂度
8. 二分答案的适用条件
9. 与其他算法的边界
10. 跨专题索引
11. 新增题目及理由
12. 独立审核的补充结果

必须重点解释：

【模板一】
Exact Binary Search

目标：
查找数组中是否存在 target。

【模板二】
Lower Bound / First True

目标：
找到第一个满足单调条件的位置。

【模板三】
Last True / Maximum Feasible

目标：
找到最后一个满足单调条件的位置。

【模板四】
Binary Search on Answer

目标：
在答案范围中搜索满足 feasible(x) 的边界。

优先使用少量统一模板。

必须讲清楚：

- [lo, hi] 与 [lo, hi) 两种区间约定
- 两种约定的循环不变量
- mid 的取整方式
- 何时使用 lo = mid + 1
- 何时使用 hi = mid
- 为什么 Last True 需要避免边界停滞
- 如何处理无解情况
- 如何确定搜索上下界
- O(log R) 与 O(n log R) 的区别

特别说明：

Binary Search 并不要求原数组一定有序，
它真正依赖的是足以安全缩小搜索空间的结构、
单调性或特定不变量。

但是不能泛化为：
所有优化问题都能 Binary Search。

必须先验证 Feasibility Predicate 的单调性。

==================================================
十一、理论讲解与中英文风格
==================================================

采用：

中文主导 + 英文技术术语。

首次出现专业术语时使用：

English（中文解释）

例如：

Binary Search（⼆分查找）
Lower Bound（下界）
Upper Bound（上界）
Monotonic Predicate（单调谓词）
Feasibility Check（可行性判断）
Search Invariant（搜索不变量）
Binary Search on Answer（二分答案）

每个 Pattern 采用以下讲解结构：

1. 1–3 个决定性观察
2. 核心不变量
3. 搜索区间的含义
4. 简短正确性证明
5. 可复用 Python 模板
6. 时间与空间复杂度
7. 代表题目
8. 常见错误与反例

不要使用空泛或冗长的理论描述。

要尽可能让我看到不同题目背后的共同模式。

==================================================
十二、P0 / P1 / P2 优先级
==================================================

P0 = 核心必练
P1 = 重要拓展
P2 = 低优先级、重复或进阶专题

优先将以下题目设为 P0：

LC-0704 - Binary Search
LC-0035 - Search Insert Position
LC-0034 - Find First and Last Position of Element in Sorted Array
LC-0074 - Search a 2D Matrix
LC-0153 - Find Minimum in Rotated Sorted Array
LC-0033 - Search in Rotated Sorted Array
LC-0162 - Find Peak Element
LC-0875 - Koko Eating Bananas
LC-1011 - Capacity To Ship Packages Within D Days
LC-1482 - Minimum Number of Days to Make m Bouquets
LC-0981 - Time Based Key-Value Store

以下可优先考虑 P1：

LC-0278
LC-0540
LC-1539
LC-0702
LC-0069
LC-1283
LC-0410
LC-2616
LC-1552
LC-0658
LC-0004

以下建议 P2：

LC-0367
LC-0374
LC-0270
LC-3346
LC-3733

这些优先级反映当前学习价值，
不是声称所有公司都有确定的出题排名。

允许根据独立审核结果调整，
但必须解释原因。

README 中分别输出：

P0：最小核心必练路线
P0 + P1：标准面试准备路线
P2：扩展与存档路线

尤其注意：

LC-4 虽然是重要的经典 Hard 题，
但学习门槛较高，应放在标准边界和二分答案
掌握之后再练习。

==================================================
十三、题目数量与完整性验收
==================================================

根据当前 tree 的初步清单：

现有题目来源目录约 24 个。

其中至少有 4 组 NC / LC 重复：
875、981、153、33。

去重后约 20 道不同题目，
其中 Median 目前只有 NC 来源。

第一轮新增 7 道不同题目。

因此第一轮预计：

27 道不同题目。

预期 Level 1 分布：

01：9 道
02：6 道
03：7 道
04：1 道
05：1 道
06：3 道

总计 27 道。

LC-4 的正式目录创建不应重复计算为新题。

如果第二轮独立审核新增了题目，
最终数量可合理增加。

如果跨专题去重使用索引代替实体目录，
实体文件夹数量可以少于预计值。

绝不能为了满足数字创建假文件。

必须检查：

1. 所有原始文件均有新位置。
2. 所有文件内容与迁移前一致，除非明确授权生成新内容。
3. 原有笔记和代码无丢失。
4. Symbolic Link 没有被意外解引用或修改外部目标。
5. 题目编号和官方名称正确。
6. NC / LC 重复资料完整归档。
7. Level 1 / Level 2 / Level 3 编号连续。
8. 没有重复正式题目目录。
9. 新题标准文件齐全。
10. README 路径真实存在。
11. 不存在非预期的旧目录残留。
12. 当前专题之外的文件没有被修改。
13. Git 原有未提交内容没有被覆盖。

==================================================
十四、执行顺序
==================================================

请实际执行：

1. 审计当前目录及文件。
2. 记录 Git 状态。
3. 记录原始文件哈希与符号链接信息。
4. 检查跨专题重复题目。
5. 验证原有题目和算法分类。
6. 建立目标目录和迁移映射。
7. 创建 6 个 Level 1 分类。
8. 创建对应 Level 2。
9. 安全迁移并编号现有 Level 3。
10. 整理 NC / LC 重复来源。
11. 安全迁移理论资料与模板。
12. 检查并保护 Symbolic Links。
13. 创建第一轮新增的 7 道题目。
14. 将 NC Median 正式整理成 LC-0004。
15. 进行第二轮独立题库审核。
16. 补充少量确实有价值的遗漏题目。
17. 调整最终编号和学习顺序。
18. 创建根目录及各 Level 1 README。
19. 验证所有文件完整性。
20. 校验迁移前后哈希与符号链接。
21. 清理安全确认的空目录。
22. 运行 tree 展示最终结果。
23. 检查 Git 状态。
24. 输出最终验收报告。

最终报告至少包含：

- 完整最终 tree
- Level 1 / Level 2 结构
- 原始题目的迁移清单
- 新增题目清单
- NC / LC 合并情况
- 理论与模板资料整理结果
- Symbolic Link 检查结果
- 第二轮独立推荐结果
- P0 / P1 / P2 统计
- 原文件完整性验证
- Git 变更摘要
- 所有失败或未完成任务
- 最终推荐学习顺序

不要只给我目录设计或修改方案。

请在所有安全约束内直接执行完整重构。
PROMPT
)"
