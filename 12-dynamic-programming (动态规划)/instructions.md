
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/12-dynamic-programming (动态规划)' && claude "$(cat <<'PROMPT'
请直接执行当前 Dynamic Programming（动态规划）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试和 Online Assessment（OA）。

请将当前目录整理为一个：

- 高面试价值
- 核心算法模式清晰
- 学习顺序循序渐进
- 尽可能减少记忆负担
- 状态定义和转移容易理解
- 方便长期复习
- 能够持续扩充

的 Dynamic Programming 学习体系。

这是实际的文件系统重构任务，不是规划任务。

请直接完成文件迁移、重命名、题目生成、README 编写、独立审核及完整性验证。

==================================================
一、最重要的学习原则
==================================================

Dynamic Programming 最重要的不是背诵代码。

我希望真正掌握：

1. State Definition（状态定义）
2. State Transition（状态转移）
3. Base Case（初始状态）
4. State Dependency（状态依赖）
5. Evaluation Order（计算顺序）
6. Top-down Memoization（自顶向下记忆化）
7. Bottom-up Tabulation（自底向上递推）
8. Space Optimization（空间压缩）
9. State Machine DP（状态机动态规划）
10. Counting vs Optimization（计数与最优化）

每种 Pattern 必须回答：

Q1. dp[i] / dp[i][j] 表示什么？
Q2. 最后一步决策是什么？
Q3. 当前状态依赖哪些更小的状态？
Q4. 为什么状态转移覆盖所有合法选择？
Q5. 为什么不会重复计数？
Q6. 初始状态为什么这样设置？
Q7. 为什么这个遍历顺序正确？
Q8. 能否进行空间压缩？
Q9. 空间压缩后是否覆盖了仍需要的旧状态？
Q10. 该题是否真的需要 DP，还是有更简单的算法？

不要把每一道 DP 题都当成新的算法记忆。

优先寻找同一类状态设计及转移方程。

==================================================
二、多层级目录及编号规则
==================================================

优先采用：

Level 1：DP 算法家族
Level 2：具体 DP Pattern
Level 3：LeetCode 题目

如确有教学需要，可以增加 Level 4。

但不要创建大量只有一道题、
又没有独立教学意义的分类。

所有同级正式学习文件夹使用连续编号：

01 - ...
02 - ...
03 - ...

编号必须综合考虑：

1. 学习依赖关系
2. 算法的代表性
3. FAANG / Big Tech 面试价值
4. 题型迁移价值
5. 难度递进
6. 减少机械记忆的效果

不能按 LC 题号机械排序。

Level 3 的命名格式：

01 - LC-0070 - Climbing Stairs
02 - LC-0746 - Min Cost Climbing Stairs

每个 Level 2 内重新从 01 编号。

_resources、_neetcode、_conflicts、_audit
属于非学习分类目录，不参与编号。

==================================================
三、最终 Level 1 分类
==================================================

建议使用以下 10 个 Level 1：

01 - 一维线性 DP 与相邻约束
02 - Kadane 与连续子数组 DP
03 - 背包 DP
04 - 子序列 DP
05 - 字符串分割与双序列 DP
06 - 网格路径与空间 DP
07 - 股票与状态机 DP
08 - 区间 DP 与博弈
09 - 计数 DP 与多维状态
10 - 概率 DP 与特殊进阶

以下列出第一轮完整的 68 道题目。

所有题目都必须归入恰好一个 Primary Learning Location。

不同算法解法可以作为 Alternative Solution，
但不能随意丢掉原有文件。

==================================================
LEVEL 1
01 - 一维线性 DP 与相邻约束
==================================================

核心：

Linear Recurrence
Rolling State
Include / Exclude
Non-adjacent Selection
Minimum Cost

--------------------------------------------------
Level 2：
01 - Fibonacci 型线性递推

题目顺序：

LC-0509 - Fibonacci Number
LC-0070 - Climbing Stairs
LC-0746 - Min Cost Climbing Stairs

教学重点：

509：
理解最基础的递推关系：

dp[i] = dp[i-1] + dp[i-2]

70：
将爬楼梯方案数转化成 Fibonacci 型递推。

746：
最小代价问题。

状态表示和初始值与 LC-70 不同，
不能直接复制同一个 Base Case。

这组题用于掌握：

- DP 状态定义
- 初始化
- Rolling Variables
- O(1) 空间优化

--------------------------------------------------
Level 2：
02 - 相邻位置不能同时选择

题目顺序：

LC-0198 - House Robber
LC-0213 - House Robber II
LC-0740 - Delete and Earn

教学重点：

198：
最典型的 Include / Exclude DP。

dp[i] = max(dp[i-1], dp[i-2] + nums[i])

必须根据所采用的下标定义写出正确递推。

213：
环形 House Robber。

分别考虑：
- 不包含最后一个房屋
- 不包含第一个房屋

复用 LC-198。

必须处理只有一个房屋的情况。

740：
先聚合相同数值的收益，
然后通过相邻数值不能同时选择的性质，
转化成类似 House Robber 的问题。

三题共享相邻冲突的结构，
不应当记忆三套独立算法。

--------------------------------------------------
Level 2：
03 - 一维决策与最低成本

题目顺序：

LC-0983 - Minimum Cost For Tickets
LC-0343 - Integer Break

教学重点：

983：
在当前位置选择不同长度的车票。

状态表示可以是：
从第 i 个旅行日开始的最小费用，
或者到某个日期的最小费用。

必须解释为什么跳转到下一个未覆盖日期。

343：
将整数拆分为至少两个正整数，
最大化乘积。

可以使用 DP，也存在数学贪心方案。

本专题优先解释 DP 转移，
但不能说 DP 是唯一可行解法。

==================================================
LEVEL 1
02 - Kadane 与连续子数组 DP
==================================================

核心：

Best Subarray Ending Here
Maximum Product
Sign Tracking
Circular Subarray
Gain Transformation

--------------------------------------------------
Level 2：
01 - 最大连续子数组和及其变体

题目顺序：

LC-0053 - Maximum Subarray
LC-0918 - Maximum Sum Circular Subarray
LC-3434 - Maximum Frequency After Subarray Operation

教学重点：

53：
Kadane's Algorithm。

核心状态：
以当前元素结尾的最大连续子数组和。

dp[i] = max(nums[i], dp[i-1] + nums[i])

918：
Circular Subarray。

最大环形区间和可以由：

total_sum - minimum_subarray_sum

得到，但必须单独处理全负数情况，
避免错误地选择空区间。

3434：
把修改某个区间带来的频率变化
转化成正负贡献数组上的最大子数组和。

必须说明它为什么能够归约到 Kadane。

这是特殊应用，建议 P2。

--------------------------------------------------
Level 2：
02 - 连续乘积与符号状态

题目顺序：

LC-0152 - Maximum Product Subarray
LC-1567 - Maximum Length of Subarray With Positive Product

教学重点：

152：
维护：

max_product_ending_here
min_product_ending_here

因为负数会使最大值和最小值交换角色。

特别解释：
为什么只维护最大乘积不够？

1567：
维护以当前位置结尾的：
- 正乘积子数组的最大长度
- 负乘积子数组的最大长度

必须正确处理：
- 0
- 正数
- 负数

两题都与符号状态有关，
但一个求乘积数值，另一个求最长长度。

==================================================
LEVEL 1
03 - 背包 DP
==================================================

这是非常重要的核心专题。

必须严格区分：

0/1 Knapsack
Unbounded Knapsack
Subset Sum
Count Combinations
Count Permutations
Multi-capacity Knapsack

--------------------------------------------------
Level 2：
01 - 0/1 背包与可达性

题目顺序：

LC-0416 - Partition Equal Subset Sum
LC-1049 - Last Stone Weight II

教学重点：

416：
将数组分成和相等的两个子集。

目标：
是否存在子集和等于 total_sum // 2。

0/1 Knapsack Boolean DP。

1049：
将原问题转化成两个集合的总重量差最小。

设两个集合的和分别为 A 和 B。

最小化：

abs(A-B)

由于 A+B=total_sum，
可转化为寻找不超过 total_sum//2
且尽可能大的子集和。

重点理解：
Optimization Problem -> Subset Sum。

--------------------------------------------------
Level 2：
02 - 0/1 背包计数

题目顺序：

LC-0494 - Target Sum
LC-2787 - Ways to Express an Integer as Sum of Powers

教学重点：

494：
求正负号分配的方案数量。

可以转换为 0/1 Knapsack Counting。

必须正确处理：
- target 为负数
- 不可能的目标范围
- 奇偶性不匹配
- 输入元素为 0 时的方案计数

2787：
每个正整数的 x 次幂最多选择一次。

因此可归为 0/1 Knapsack Counting。

注意 Modulo。

2787 标记 P2，
主要用于复习 0/1 计数转移。

--------------------------------------------------
Level 2：
03 - 二维容量约束背包

题目顺序：

LC-0474 - Ones and Zeroes

教学重点：

每个字符串消耗两种资源：
- 0 的数量
- 1 的数量

定义：

dp[zeros_capacity][ones_capacity]

表示在资源容量限制下，
最多能选择多少个字符串。

每个字符串最多选择一次。

因此在原地一维对象处理的二维 DP 表中，
两个容量维度都应正确倒序遍历。

必须解释：
为什么不能错误地改为正序，
从而重复使用同一个字符串？

这是从一维 0/1 Knapsack
过渡到多资源 Knapsack 的代表题。

--------------------------------------------------
Level 2：
04 - 完全背包最少数量

题目顺序：

LC-0322 - Coin Change

教学重点：

每种硬币可以无限使用。

目标：
组成 amount 的最少硬币数量。

必须区分：
minimization DP
与 counting DP。

无解时返回 -1。

正确处理：
dp[0] = 0
以及不可达状态。

--------------------------------------------------
Level 2：
05 - 完全背包的组合与排列计数

题目顺序：

LC-0518 - Coin Change II
LC-0377 - Combination Sum IV

教学重点：

518：
统计硬币组合的数量。

不同顺序不算不同方案。

经典遍历：

for coin in coins:
    for amount in ...:
        ...

377：
统计有序组合（Sequence）的数量。

不同顺序算不同方案。

经典遍历：

for amount in ...:
    for num in nums:
        ...

必须通过具体例子解释：

1+2
和
2+1

在 518 中视为同一个组合，
在 377 中视为不同的有序序列。

这是背包计数最重要的区别之一。

同时必须说明：
循环顺序的意义取决于 DP 状态和转移。
不能脱离具体实现，把任意代码的循环顺序
机械地理解为“组合”或“排列”。

==================================================
LEVEL 1
04 - 子序列 DP
==================================================

核心：

Longest Increasing Subsequence
Predecessor State
Count Optimal Solutions
Sorting + Subsequence
Modular State

--------------------------------------------------
Level 2：
01 - LIS 长度与方案计数

题目顺序：

LC-0300 - Longest Increasing Subsequence
LC-0673 - Number of Longest Increasing Subsequence
LC-0368 - Largest Divisible Subset

教学重点：

300：
必须理解两个版本：

A. O(n^2) DP
B. O(n log n) Greedy + Binary Search

对于 O(n^2)：

dp[i] = 以 i 结尾的 LIS 长度。

对于 O(n log n)：

tails[len-1] 表示当前已发现的
长度为 len 的递增子序列中，
尽可能小的结尾值。

必须说明：
tails 不一定本身就是某条真实的 LIS。

不要错误地把 tails 直接解释成原始答案序列。

673：
在 LIS 长度 DP 基础上，
额外维护每个状态的方案数量。

使用：
length[i]
count[i]

必须正确合并具有相同最优长度的方案数量。

368：
先排序，
再利用整除关系构建可扩展的子序列。

保存 Parent / Predecessor 信息，
用于恢复实际答案。

不能只返回最大长度。

--------------------------------------------------
Level 2：
02 - 特殊状态与字符串链

题目顺序：

LC-1048 - Longest String Chain
LC-3201 - Find the Maximum Length of Valid Subsequence I
LC-3202 - Find the Maximum Length of Valid Subsequence II

教学重点：

1048：
先按字符串长度排序。
通过删除一个字符查找前驱字符串。

可以使用 Hash Map + DP。

3201 / 3202：
根据题目中的模运算关系定义 DP 状态。

必须解释：
为什么普通 LIS 模板不适用？

为什么需要保存与余数或状态有关的信息？

这两道题标记 P2，
不必作为经典 LIS 的核心模板背诵。

==================================================
LEVEL 1
05 - 字符串分割与双序列 DP
==================================================

核心：

String Segmentation
Decode Counting
LCS
Edit Distance
Distinct Subsequences
Regex Matching

--------------------------------------------------
Level 2：
01 - 单字符串分割与解码

题目顺序：

LC-0091 - Decode Ways
LC-0139 - Word Break
LC-3291 - Minimum Number of Valid Strings to Form Target I

教学重点：

91：
根据当前位置和前一位置字符，
判断是否可以形成合法编码。

重点处理：
- 0
- 两位数 10..26
- 不合法的前导零

139：
定义：

dp[i] = 前 i 个字符是否可以被字典分割。

尝试合法的最后一个单词。

3291：
Trie + DP。

通过 Trie 快速寻找从某位置开始
可以匹配的合法前缀。

本题已存在于 Trie 专题，
保留当前 DP 版本原始资料。

建立跨专题引用。

--------------------------------------------------
Level 2：
02 - LCS 与连续公共片段

题目顺序：

LC-1143 - Longest Common Subsequence
LC-0718 - Maximum Length of Repeated Subarray

教学重点：

1143：
Longest Common Subsequence。

允许不连续，但必须保持原始顺序。

标准二维 DP：

如果字符相同：
dp[i][j] = dp[i-1][j-1] + 1

否则：
dp[i][j] = max(dp[i-1][j], dp[i][j-1])

718：
Longest Common Contiguous Subarray。

要求连续。

如果当前位置的两个元素不同，
以这两个位置结尾的公共连续长度为 0。

必须解释：
Subsequence 与 Subarray / Substring
在连续性约束上的本质区别。

--------------------------------------------------
Level 2：
03 - Distinct Subsequences 计数

题目顺序：

LC-0115 - Distinct Subsequences

教学重点：

统计源字符串中有多少种不同的位置选取方式，
能够形成目标字符串。

必须明确：

这不是在找最长公共子序列。

而是 Counting DP。

匹配字符时存在：
- 使用当前字符
- 跳过当前字符

两种选择。

必须正确设置空目标字符串的 Base Case。

--------------------------------------------------
Level 2：
04 - Edit Distance 与双字符串状态

题目顺序：

LC-0072 - Edit Distance
LC-0097 - Interleaving String
LC-0010 - Regular Expression Matching

教学重点：

72：
编辑距离。

操作：
insert
delete
replace

dp[i][j] 表示将第一个字符串的前 i 个字符
转换成第二个字符串的前 j 个字符
所需的最少操作数。

97：
判断 s3 是否可以由 s1、s2
保持各自内部顺序地交错组成。

dp[i][j] 表示使用 s1 前 i 个字符
和 s2 前 j 个字符是否可组成
s3 的前 i+j 个字符。

10：
Regular Expression Matching。

支持：
'.'
'*'

必须解释：
'*' 表示前一个模式元素出现零次或多次，
并不是普通 Shell Wildcard 的任意字符串匹配语义。

本题属于复杂二维 DP，
标记 P1 进阶。

--------------------------------------------------
Level 2：
05 - 跨专题字符串 DP

题目顺序：

LC-0032 - Longest Valid Parentheses

教学重点：

本题已经在 Stack 专题出现。

当前 DP 版本必须完整保留。

可以定义：
dp[i] = 以位置 i 结尾的最长有效括号长度。

必须解释：
为什么只有当前字符为 ')' 时
才可能以当前位置结尾形成非空有效括号串？

在 README 对比 Stack 解法与 DP 解法。

标记为跨专题 P1/P2。

==================================================
LEVEL 1
06 - 网格路径与空间 DP
==================================================

核心：

Grid DP
Number of Paths
Minimum Path Cost
Bottom-up Triangle
Square State

--------------------------------------------------
Level 2：
01 - 网格路径计数

题目顺序：

LC-0062 - Unique Paths
LC-0063 - Unique Paths II

教学重点：

62：
从左边和上边累加路径数量。

63：
增加障碍约束。

必须解释：
为什么障碍位置的路径数是 0？

如何正确初始化第一行和第一列？

--------------------------------------------------
Level 2：
02 - 网格路径最小代价

题目顺序：

LC-0064 - Minimum Path Sum
LC-0120 - Triangle
LC-0931 - Minimum Falling Path Sum

教学重点：

64：
从上方或左方转移最小路径和。

120：
Triangle DP。

可以从底部向上递推，
每个节点选择下一行两个相邻位置的较小结果。

展示 O(n) 额外空间优化。

931：
向下一行的左下、正下、右下移动。

必须处理边界列。

这三道题体现：
相同的 Minimum Path DP 思想，
但允许的前驱/后继集合不同。

--------------------------------------------------
Level 2：
03 - 最大正方形与二维结构状态

题目顺序：

LC-0221 - Maximal Square

教学重点：

dp[i][j] 表示以当前格子为右下角，
由 1 组成的最大正方形边长。

典型转移：

1 + min(top, left, top_left)

必须解释：
为什么三个相邻方向中任意一个太小，
都会限制当前正方形的边长？

注意最后答案是面积：
max_side * max_side。

==================================================
LEVEL 1
07 - 股票与状态机 DP
==================================================

核心：

Hold / Cash State
Buy / Sell Transition
Cooldown
Transaction Fee
At Most K Transactions

--------------------------------------------------
Level 2：
01 - 单次与无限次交易

题目顺序：

LC-0121 - Best Time to Buy and Sell Stock
LC-0122 - Best Time to Buy and Sell Stock II

教学重点：

121：
单次交易。

标准 O(n) Running Minimum 解法
通常比通用状态机更简单。

保留原有代码，
不能强迫将所有股票题改写成 DP。

122：
允许多次交易，但同一时间最多持有一股。

可以使用两状态 DP：

hold
cash

也可以使用简单 Greedy，
累加所有正的相邻价格差。

必须解释两种解法的关系。

--------------------------------------------------
Level 2：
02 - 冷却期与交易费用

题目顺序：

LC-0309 - Best Time to Buy and Sell Stock with Cooldown
LC-0714 - Best Time to Buy and Sell Stock with Transaction Fee

教学重点：

309：
卖出后存在 Cooldown。

必须定义足够区分：
- 持有股票
- 可自由买入
- 冷却期

的状态或等价转移。

714：
每次交易产生 Fee。

明确交易费在哪一步扣除，
不能在买入和卖出时重复扣费。

--------------------------------------------------
Level 2：
03 - 交易次数限制

题目顺序：

LC-0123 - Best Time to Buy and Sell Stock III
LC-0188 - Best Time to Buy and Sell Stock IV

教学重点：

123：
最多两次交易。

可以维护：
buy1
sell1
buy2
sell2

或者通用交易次数状态机。

188：
最多 k 次交易。

必须解释：
为什么需要交易次数维度？

什么叫做“一笔完整交易”？

买入与卖出中的哪一步计数？
具体实现必须保持一致。

为什么 k 足够大时，
问题可简化为无限次交易？

目标：
先理解 LC-123，
再推导 LC-188。

不要机械背诵两套完全不同的算法。

==================================================
LEVEL 1
08 - 区间 DP 与博弈
==================================================

核心：

Interval DP
Choice of Last Operation
Two-player Optimal Play
Palindrome Interval DP

--------------------------------------------------
Level 2：
01 - 区间博弈与分数差

题目顺序：

LC-0486 - Predict the Winner

教学重点：

两名玩家都采用最优策略。

定义：

dp[l][r] = 当前玩家在区间 [l,r]
能够获得的最大净分差。

解释：
为什么选择左端或右端后，
需要减去对手在剩余区间能够获得的分差？

必须说明：
Minimax 和 Interval DP 的关系。

--------------------------------------------------
Level 2：
02 - 最后一步决策型区间 DP

题目顺序：

LC-0312 - Burst Balloons

教学重点：

这是重要的 Interval DP 代表题。

常见错误：
直接选择当前最先戳破的气球，
会导致邻居动态变化，难以定义状态。

正确思路：
枚举区间内最后一个被戳破的气球。

使用区间 DP：

dp[l][r]

表示在指定边界条件下，
完成某个区间内部气球操作的最大收益。

必须明确区间开闭约定。

例如使用开区间 (l,r)：

dp[l][r] =
max(
    dp[l][k] + dp[k][r]
    + nums[l]*nums[k]*nums[r]
)

其中 l < k < r，
nums 两端添加适当的虚拟边界值。

必须解释：
为什么把 k 设为最后戳破，
其左右边界在最终操作时是确定的？

--------------------------------------------------
Level 2：
03 - Palindrome Interval DP

题目顺序：

LC-0647 - Palindromic Substrings
LC-0516 - Longest Palindromic Subsequence

教学重点：

647：
统计回文 Substrings。

必须连续。

可以使用二维区间 DP，
也可以使用 Center Expansion。

要明确说明：
Center Expansion 往往实现更简单、
额外空间也更少。

不要强迫以 DP 作为唯一推荐解法。

516：
最长回文 Subsequence。

不要求连续，但必须保留相对顺序。

定义：

dp[l][r] =
s[l:r+1] 的最长回文子序列长度。

若两端相等：
可利用内部区间的最优结果加 2。

否则：
考虑跳过左端或右端。

必须处理长度为 1、长度为 2 的区间。

重点对比：

647：Substring，要求连续。
516：Subsequence，不要求连续。

本组可以和 LC-1143 的 LCS
建立跨 Pattern 联系。

==================================================
LEVEL 1
09 - 计数 DP 与多维状态
==================================================

核心：

Counting DP
State Machine Counting
Sequence Transition
Multi-dimensional State
Scheduling State

--------------------------------------------------
Level 2：
01 - 线性计数与铺砖

题目顺序：

LC-0276 - Paint Fence
LC-0790 - Domino and Tromino Tiling

教学重点：

276：
不能有超过两个连续相同颜色。

通过“最后两个是否相同”等状态计数。

790：
Domino / Tromino 铺砖。

需要处理完整覆盖和部分覆盖状态，
或推导等价压缩递推式。

标记 P1/P2。

--------------------------------------------------
Level 2：
02 - 骰子与受限序列计数

题目顺序：

LC-1155 - Number of Dice Rolls With Target Sum
LC-0935 - Knight Dialer
LC-1220 - Count Vowels Permutation

教学重点：

1155：
dp[dice_count][sum]

表示使用指定数量骰子得到某个和的方案数。

935：
根据电话键盘上的骑士移动规则，
统计长度为 n 的数字序列数量。

1220：
根据元音之间允许的转移关系，
统计长度为 n 的字符串数量。

重点学习：
Count Paths in a State Transition Graph。

这些题本质上是有限状态之间的计数转移。

不需要为每个题分别记忆完全不同的算法。

--------------------------------------------------
Level 2：
03 - Paint House 与相邻状态限制

题目顺序：

LC-0256 - Paint House
LC-0265 - Paint House II
LC-1473 - Paint House III

教学重点：

256：
相邻房屋颜色不同。
维护每个房屋使用各颜色的最小成本。

265：
颜色数量扩展到 k。

解释：
如何利用最小值和次小值
避免每次遍历全部其他颜色。

1473：
需要考虑：
- 当前位置
- 颜色
- 已形成的 Neighborhood 数量

这是高维状态 DP。

标记 P2 进阶。

--------------------------------------------------
Level 2：
04 - 多维决策与任务划分

题目顺序：

LC-1770 - Maximum Score from Performing Multiplication Operations
LC-1335 - Minimum Difficulty of a Job Schedule

教学重点：

1770：
每一步只能从数组左端或右端选择。

可以使用：
操作次数 + 已从左端选取数量
作为 DP 状态。

1335：
将工作按顺序分配给指定天数。

状态考虑：
- 已处理任务
- 已使用天数

并枚举最后一天的任务分割点。

必须解释为什么任务顺序不能改变。

这两题是多维状态练习，
但不应成为一维 DP 初学者的必背题。

--------------------------------------------------
Level 2：
05 - 特殊输入压缩与计数 DP

题目顺序：

LC-3333 - Find the Original Typed String II

教学重点：

先将连续相同字符压缩为 Run Lengths。

再根据可能的原始字符串长度，
使用受限计数 DP。

需要处理：
- 连续字符块
- 至少 k 个字符的约束
- 组合数量
- 模运算
- Prefix Sum 优化

标记 P2。

不要为了这道特殊题
额外扩充大量低频计数技巧。

==================================================
LEVEL 1
10 - 概率 DP 与特殊进阶
==================================================

核心：

Probability Transitions
Probability Mass
Expected Value vs Probability
State Aggregation

Level 2：
01 - 离散概率转移

题目顺序：

LC-0688 - Knight Probability in Chessboard
LC-0799 - Champagne Tower

教学重点：

688：
每一步根据合法位置和移动概率转移。

799：
当前杯子超过容量的部分，
向下一层两个杯子平均流动。

注意：
它们分别属于随机概率转移
和确定性容量分配模拟。

不能将两者错误地描述为完全相同的概率模型。

--------------------------------------------------
Level 2：
02 - 停止过程与概率窗口优化

题目顺序：

LC-0837 - New 21 Game
LC-0808 - Soup Servings

教学重点：

837：
Probability DP + Sliding Window Optimization。

必须区分：
游戏仍可以继续的状态，
与达到停止阈值后的终止状态。

808：
递归概率状态与 Memoization。

注意题目中的概率停止条件、
规模缩放及大输入近似截断的正确性前提。

这两题标记 P2。

不需要作为主要 FAANG DP 模板长期背诵。

==================================================
四、NC-only 题目正式化
==================================================

当前有 12 道只有 NC 来源：

NC - Burst Balloons
NC - Maximum Product Subarray
NC - Partition Equal Subset Sum
NC - Climbing Stairs
NC - House Robber
NC - House Robber II
NC - Min Cost Climbing Stairs
NC - Decode Ways
NC - Longest Increasing Subsequence
NC - Distinct Subsequences
NC - Edit Distance
NC - Longest Common Subsequence

分别对应：

LC-0312 - Burst Balloons
LC-0152 - Maximum Product Subarray
LC-0416 - Partition Equal Subset Sum
LC-0070 - Climbing Stairs
LC-0198 - House Robber
LC-0213 - House Robber II
LC-0746 - Min Cost Climbing Stairs
LC-0091 - Decode Ways
LC-0300 - Longest Increasing Subsequence
LC-0115 - Distinct Subsequences
LC-0072 - Edit Distance
LC-1143 - Longest Common Subsequence

必须逐一核对题目内容。

确认对应后：

1. 创建正式 LC Level 3 目录。
2. 将原始 NC 目录全部迁入 _neetcode/。
3. 保留所有 NC 原始 solution.py。
4. 保留 NC metadata、PDF、图片和注释。
5. 使用仓库已有工具补齐 LC 正式题目文件。
6. 不得以新代码覆盖原有解法。

特别保护：

NC - Maximum Product Subarray：
asset-09 - Kadane 的精髓.pdf
asset-09 - Kadane Algorithm.pdf

NC - Longest Increasing Subsequence：
原有 PDF 和 JPEG 图解。

NC - Distinct Subsequences：
原有 JPEG 图解。

NC - Edit Distance：
note.md。

NC - Longest Common Subsequence：
asset-Explanation.png。

这些文件都是重要学习成果，
必须完整保留。

==================================================
五、第一轮明确新增的 8 道题
==================================================

本次明确建议新增：

LC-0120 - Triangle
LC-0122 - Best Time to Buy and Sell Stock II
LC-0123 - Best Time to Buy and Sell Stock III
LC-0474 - Ones and Zeroes
LC-1049 - Last Stone Weight II
LC-0516 - Longest Palindromic Subsequence
LC-0673 - Number of Longest Increasing Subsequence
LC-0647 - Palindromic Substrings

先检查当前专题和整个仓库。

如果当前目录中已经存在正式版本，
应直接复用。

如果其他专题中已经有完整题目，
评估是否使用跨专题索引即可。

对于真正缺失的题目，
使用已有 LeetCode 题目生成工作流创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备按题号生成题目文件的能力。

请直接复用，不要重新设计生成工具。

不允许：
- 生成空白 PDF
- 伪造 metadata
- 覆盖原有 solution.py
- 把别的题目的内容放入新题目录
- 删除已存在的学习附件

如果某道题生成失败，
记录原因并继续处理其他安全任务。

==================================================
六、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 第一轮推荐。

你必须进行第二轮独立审核。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可靠的 DP 题单

如果具备网络访问，可以核对题号、
英文题名、约束和主流解法。

不要编造 FAANG 实际出题频次。

重点检查：

1. Fibonacci DP
2. House Robber
3. Kadane
4. Maximum Product
5. 0/1 Knapsack
6. Unbounded Knapsack
7. Subset Sum
8. Combination Counting
9. Permutation Counting
10. Two-capacity Knapsack
11. LIS
12. LCS
13. Edit Distance
14. Distinct Subsequences
15. Word Break
16. Decode Ways
17. Grid DP
18. Interval DP
19. Palindrome DP
20. Stock State Machine
21. Tree DP Cross-reference
22. DAG DP Cross-reference
23. Counting State Machines
24. Memoized DFS
25. Space Optimization

请审核额外候选：

LC-0005 - Longest Palindromic Substring
LC-0044 - Wildcard Matching
LC-0154? 不要凭编号猜测题目，必须核对。
LC-0157? 同样不要凭编号猜测。
LC-0174 - Dungeon Game
LC-0354 - Russian Doll Envelopes
LC-1547 - Minimum Cost to Cut a Stick
LC-0879 - Profitable Schemes
LC-0337 - House Robber III

正确题号与名称必须核对。

其中：

LC-5：
常见的 Center Expansion 方案可能更简单。
不要因为可使用 DP 就强制增加核心 DP 题。

LC-44：
Wildcard Matching 与 LC-10 的 Regex Matching
具有不同匹配规则。

LC-354：
Sorting + LIS。
属于 LIS 的高迁移价值应用。

LC-1547：
典型 Interval DP，
但与 LC-312 有明显联系。

LC-174：
Reverse Grid DP，
需要正确维护最低生命值约束。

LC-879：
复杂计数背包，
学习成本较高。

LC-337：
Tree DP 代表题，
如果已经在 Trees 专题存在，
优先建立跨专题索引。

第二轮独立新增最多 5 道。

新增需要满足：

A. 高面试代表性。
B. 可迁移的独立 Pattern。
C. 能弥补真实知识缺口。
D. 不属于已有题的低价值重复。
E. 与学习阶段匹配。
F. 不会引入过度记忆负担。

如发现超过 5 道值得学习的题目，
仅新增最重要的 5 道，
其余写入 Future Candidates。

如果没有明显遗漏，
可以不新增。

不要为了题库数量而盲目扩张。

==================================================
七、DP 正确性和遍历顺序
==================================================

README 必须重点讲清楚：

【0/1 Knapsack】

每个物品最多选择一次。

进行原地容量压缩时，
通常需要倒序遍历容量。

原因：
防止同一个物品在当前轮中重复使用。

【Unbounded Knapsack】

每个物品可以无限次选择。

在适当的一维 DP 定义下，
可以正序遍历容量，
允许当前物品重复使用。

【Counting Combinations】

不同顺序不计为不同结果。

经典 Coin Change II：
物品外层，容量内层。

【Counting Ordered Sequences】

不同顺序算不同结果。

经典 Combination Sum IV：
目标容量外层，候选数字内层。

必须提供可运行的 Python 示例，
用小数据验证结果数量。

注意以上是针对相应经典状态定义的规律，
不是任何 DP 中循环顺序的普适法则。

==================================================
八、Top-down 与 Bottom-up
==================================================

每个核心 DP 家族的 README
都需要说明：

Top-down Memoization：
从目标问题向子问题递归，
对子问题结果缓存。

Bottom-up Tabulation：
按照依赖顺序依次计算状态。

必须解释：

- 什么时候递归更自然？
- 什么时候迭代更节省栈空间？
- 什么时候状态可以空间压缩？
- 为什么不能随意改变计算顺序？
- 为什么某些 DP 可以只保存上一行？
- 为什么某些 DP 需要保留同一行的旧值？

尤其要避免：

看到二维 DP 就强行压缩为一维，
却没有证明依赖关系仍然正确。

==================================================
九、跨专题去重与引用
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0032 -> Stack
LC-0121 -> Arrays / Greedy
LC-3291 -> Trie
LC-0337 -> Trees
LC-0329 -> Graph DAG DP
LC-0279 -> Graph BFS 或 DP
LC-0494 -> Backtracking Cross-reference
LC-0300 -> Binary Search / LIS
LC-0647 -> Two Pointers / Palindrome
LC-0104? 不是 DP 主线，不需要新增。

如果本专题已有题目，
必须保留原有完整资料。

如果其他专题已有同题，
可以建立相对路径索引。

不得修改其他专题文件。

对于交叉题，
README 应标注：

Primary Pattern
Secondary Pattern
Recommended Algorithm
Alternative Algorithm

不要因为有多种解法就重复下载大量 PDF。

==================================================
十、现有学习成果与 Git 安全
==================================================

当前 Git 仓库存在大量未提交修改和未跟踪文件。

必须严格保护。

操作前：

1. pwd
2. tree
3. git status --short
4. 扫描当前 DP 目录所有文件
5. 记录原始文件相对路径
6. 记录原始普通文件 SHA-256
7. 检查 Symbolic Links
8. 记录原始题目编号
9. 记录 Markdown / Python 依赖引用
10. 制作完整迁移映射

特别保留：

LC-2787：
原有 PDF 图解。

LC-3434：
原有 PDF 图解。

LC-1770：
原有 JPEG。

LC-808：
原有 PDF 和 JPEG。

LC-837：
原有 Draw.io。

LC-188：
原有 JPEG。

LC-309：
asset-03 - TODO.md。

LC-3333：
原有 PDF。

LC-3202：
原有 PDF。

LC-0010：
原有 PNG 和 PDF。

以及全部：
metadata.json
problem.pdf
problem_dark.pdf
solution.py
note.md
自定义图片
自定义文档

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖已有代码
删除未跟踪文件
覆盖原始笔记
删除原始学习资料

不要自动：

git add
git commit
git push

只允许写入当前：

12-dynamic-programming (动态规划)

内部。

允许只读检查整个仓库。

如存在目标路径冲突：

- 不同内容必须保留全部版本。
- 相同内容可可追溯地整理。
- 必要时使用 _conflicts/。
- 不能静默覆盖任意原文件。

尽可能保证 Idempotence（幂等性）。

重复运行不能：
- 叠加编号
- 重复创建题目
- 重复 NC 归档
- 覆盖原始解法
- 丢失资料

==================================================
十一、README 学习文档
==================================================

必须创建：

A. 根目录 README.md。
B. 每个 Level 1 的 README.md。
C. 重要 Level 2 的短 README。
D. DP Pattern Recognition Guide。
E. DP State Transition Cheat Sheet。
F. DP Interview Roadmap。

根目录 README 包含：

1. Dynamic Programming 知识地图。
2. 十大 Level 1 分类。
3. 每个 Pattern 的核心不变量。
4. 所有题目及其真实相对路径。
5. P0 / P1 / P2。
6. Top-down 与 Bottom-up。
7. 0/1 和 Unbounded Knapsack。
8. LIS 与 LCS。
9. Subsequence 与 Substring。
10. Interval DP。
11. Counting DP。
12. Stock State Machine。
13. Tree DP / DAG DP 跨专题索引。
14. 空间压缩规律。
15. 第二轮审核结果。
16. 最终学习顺序。

每个 Level 1 README 应包含：

1. 1–3 个决定性观察。
2. State Definition。
3. Transition Equation。
4. Base Case。
5. Evaluation Order。
6. 简短正确性证明。
7. Python 核心模板。
8. 时间复杂度。
9. 空间复杂度。
10. 代表题目。
11. 容易混淆的相邻 Pattern。
12. 常见错误与反例。

说明复杂度时，
必须包含状态数量和每个状态的转移成本。

不能机械认为：

一维 DP = O(n)
二维 DP = O(n^2)

例如：
某个二维状态可能有第三层转移枚举。

==================================================
十二、中文主导的技术笔记风格
==================================================

采用：

中文主导 + 英文专业术语。

首次出现使用：

English（中文解释）

例如：

Dynamic Programming（动态规划）
Optimal Substructure（最优子结构）
Overlapping Subproblems（重叠子问题）
State Transition（状态转移）
Top-down Memoization（自顶向下记忆化）
Bottom-up Tabulation（自底向上递推）
0/1 Knapsack（0/1 背包）
Unbounded Knapsack（完全背包）
Longest Increasing Subsequence（最长递增子序列）
Interval DP（区间动态规划）
State Machine DP（状态机动态规划）

理论讲解先给：

1. 状态表示什么？
2. 核心转移公式是什么？
3. 为什么正确？

再用具体例子验证。

不要写空泛的长篇解释。

不要为了教学而生成几十套几乎相同的模板。

==================================================
十三、P0 P1 P2 优先级
==================================================

P0：
必须熟练理解的经典 DP 核心题。

建议 P0：

LC-0070 - Climbing Stairs
LC-0746 - Min Cost Climbing Stairs
LC-0198 - House Robber
LC-0053 - Maximum Subarray
LC-0152 - Maximum Product Subarray
LC-0416 - Partition Equal Subset Sum
LC-0322 - Coin Change
LC-0518 - Coin Change II
LC-0300 - Longest Increasing Subsequence
LC-0091 - Decode Ways
LC-0139 - Word Break
LC-1143 - Longest Common Subsequence
LC-0072 - Edit Distance
LC-0062 - Unique Paths
LC-0064 - Minimum Path Sum
LC-0120 - Triangle
LC-0221 - Maximal Square

P1：

LC-0213
LC-0740
LC-0983
LC-0918
LC-1049
LC-0494
LC-0474
LC-0377
LC-0673
LC-0368
LC-0115
LC-0097
LC-0010
LC-0718
LC-0122
LC-0123
LC-0309
LC-0714
LC-0188
LC-0312
LC-0516
LC-0647
LC-1155
LC-0256
LC-0265
LC-0931

其他根据面试价值标记 P1 或 P2。

尤其以下倾向 P2：

LC-3434
LC-2787
LC-3201
LC-3202
LC-3333
LC-1473
LC-0837
LC-0808

P0 / P1 / P2 允许根据第二轮审核调整。

但必须给出具体理由。

不要因 Hard 难度自动提升优先级。

不要假设所有被 LeetCode 标记为 DP 的题
都需要使用 DP。

README 必须分别输出：

P0：核心必练。
P0 + P1：标准面试准备。
P2：进阶与低优先级存档。

==================================================
十四、数量与完整性检查
==================================================

已核对当前原始 tree：

原有不同题目：
60 道。

其中：
48 个正式 LC 目录。
12 个 NC-only 目录。

没有现有 LC/NC 双来源同题目录需要合并，
但 NC-only 需要正式化。

第一轮新增：
8 道。

因此第一轮目标：
68 道不同题目。

第一轮预计 Level 1 题目数：

01：8
02：5
03：8
04：6
05：10
06：6
07：6
08：4
09：11
10：4

总计：68。

第二轮如果确实有高价值遗漏题目，
数量可以适当增加。

如果某些新增题已有其他专题主归属，
并通过索引代替实体目录，
实体数量可以有所不同。

严禁为了凑数字创建空文件。

必须验证：

1. 原有 60 道题都有明确归属。
2. 原始文件全部保留。
3. 12 道 NC-only 正式化正确。
4. 8 道推荐新题得到处理。
5. 所有题号与正式英文题名正确。
6. 同一道题没有两个正式主目录。
7. Level 1 编号连续。
8. Level 2 编号连续。
9. Level 3 编号连续。
10. 新题 metadata、PDF、Python 完整。
11. 所有自定义附件保留。
12. 原始文件 SHA-256 一致。
13. README 相对路径真实存在。
14. 跨专题索引可用。
15. 当前 DP 专题外没有发生写入。
16. Git 原有未提交修改未被覆盖。

==================================================
十五、最终学习路线
==================================================

在根 README 中额外生成：

DP Core Roadmap。

推荐阶段：

阶段 A：
Fibonacci
-> Climbing Stairs
-> House Robber

阶段 B：
Kadane
-> Maximum Product

阶段 C：
0/1 Knapsack
-> Unbounded Knapsack
-> Counting Knapsack

阶段 D：
LIS
-> LCS
-> Edit Distance

阶段 E：
Word Break
-> Decode Ways
-> String Segmentation

阶段 F：
Grid DP
-> Triangle
-> Maximal Square

阶段 G：
Stock State Machine
-> Transaction Constraints

阶段 H：
Interval DP
-> Tree DP / DAG DP Cross-references

阶段 I：
Multidimensional Counting
-> Probability DP

阶段 I 的许多题属于选修进阶。

不要把所有 68 道题都列为必刷。

另外，请生成一条：

20–25 道题的最小核心 DP 面试路线。

这条路线需要覆盖主要状态定义、
转移方式和常见优化模式。

不能仅挑选二十多道相似的一维递推题。

==================================================
十六、实际执行流程
==================================================

请直接执行：

1. 扫描完整当前 DP 目录。
2. 检查 Git 状态。
3. 建立所有原始文件的 Manifest。
4. 计算 SHA-256。
5. 识别 NC-only 题目。
6. 检查代码内容与题号是否匹配。
7. 只读检查跨专题重复。
8. 建立最终分类与迁移映射。
9. 创建 10 个 Level 1。
10. 创建对应 Level 2。
11. 安全迁移现有题目。
12. 将 12 个 NC-only 题正式化。
13. 保留所有原有 NC 解法。
14. 为所有 Level 3 重新编号。
15. 创建推荐新增的 8 道题目。
16. 补齐原有缺失的必要文件。
17. 进行第二轮独立题库审核。
18. 如有必要新增最多 5 道题目。
19. 根据新增情况调整排序。
20. 生成根目录 README。
21. 生成 Level 1 README。
22. 创建 DP Pattern Recognition Guide。
23. 创建 DP State Transition Cheat Sheet。
24. 创建 20–25 题核心学习路线。
25. 检查核心代码语法。
26. 对新增解法运行适当测试。
27. 验证旧文件哈希。
28. 检查所有 README 链接。
29. 检查编号连续性。
30. 清理确认已空的旧目录。
31. 运行最终 tree。
32. 检查最终 Git 状态。
33. 输出完整验收报告。

最终报告必须包含：

- 最终完整 tree
- 10 个 Level 1
- 所有 Level 2 分类
- 原始 60 道题的迁移结果
- 12 个 NC-only 的正式化结果
- 第一轮新增的 8 道题
- 第二轮自主新增题目
- 未新增候选及理由
- P0 / P1 / P2 统计
- 20–25 道核心 DP 推荐路线
- 原始文件校验结果
- Git 变更摘要
- 失败或未完成项目

如果某个操作不安全，
保留原始文件并报告，
继续完成其他可以安全执行的工作。

不要仅仅生成目录规划。

请直接执行整个 Dynamic Programming 专题重构。
PROMPT
)"
