
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/10-backtracking (回溯)' && claude "$(cat <<'PROMPT'
请直接执行当前 Backtracking（回溯）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请建立一套：
- 高面试价值
- 高算法迁移性
- 清晰的多级知识分类
- 循序渐进的学习顺序
- 尽可能低的记忆成本
- 可长期复习和扩充

的 Backtracking 学习体系。

这是实际的文件系统重构任务，不是单纯的规划任务。

请完成旧题迁移、NC 题目正式化、新题生成、分类编号、学习文档编写、独立审核和最终验收。

==================================================
一、最重要的学习目标
==================================================

我希望将 Backtracking 归纳为少量可复用的 DFS 模式。

核心框架：

1. Choose（选择）
2. Explore / DFS（递归探索）
3. Undo（撤销选择）

但不能简单认为所有回溯题只有这一套代码。

必须区分以下核心问题：

1. Subsets：是否选择当前元素？
2. Combinations：如何避免重复顺序？
3. Permutations：如何安排元素顺序？
4. Combination Sum：元素能否重复使用？
5. Duplicate Handling：如何避免重复答案？
6. String Generation：每个位置有哪些合法选择？
7. String Partitioning：切割点在哪里？
8. Grid Search：哪些相邻格子可以访问？
9. Constraint Satisfaction：哪些选择违反约束？
10. Pruning：哪些分支能够提前排除？
11. Symmetry Breaking：如何避免等价搜索状态？

重点解释：

- DFS 的参数代表什么？
- start_index 与 used 有什么区别？
- path 保存什么？
- 什么时候将 path 加入结果？
- 为什么必须复制 path？
- 什么时候执行 pop / restore？
- 为什么可以安全剪枝？
- 如何避免重复答案？
- 哪些题可以提前返回 True？
- 哪些题必须枚举全部解？

我不希望机械记忆大量独立代码。

希望通过这些问题掌握少量核心算法不变量。

==================================================
二、目录层级与编号规则
==================================================

优先采用：

Level 1：算法家族
Level 2：具体 Backtracking Pattern
Level 3：具体 LeetCode 题目

确实需要时可以创建 Level 4。

但不要为了增加层级而创建无意义的文件夹。

所有同级正式学习目录都必须使用连续编号：

01 - ...
02 - ...
03 - ...

编号应综合反映：

1. 学习依赖关系
2. 面试代表性
3. 算法迁移性
4. 教学价值
5. 难度递进
6. 记忆成本

不能按照 LeetCode 题号机械排序。

Level 3 格式：

01 - LC-0078 - Subsets
02 - LC-0090 - Subsets II

每个 Level 2 内部独立从 01 编号。

_neetcode、_resources、_conflicts
等来源或资源目录不参与算法分类编号。

==================================================
三、第一轮目标目录结构
==================================================

建议建立 4 个 Level 1。

请优先遵守以下结构。

独立审核后可以调整，但任何调整都需要明确的教学理由。

--------------------------------------------------
LEVEL 1
01 - 子集、组合与目标和 (Subsets and Combinations)
--------------------------------------------------

核心：

Include / Exclude
Start Index
Combination Enumeration
Target Sum
Duplicate Skipping

Level 2：
01 - 子集枚举与重复元素去重

Level 3：

01 - LC-0078 - Subsets
02 - LC-0090 - Subsets II

教学重点：

LC-78：

最基础的回溯枚举。

必须理解两种等价思路：

A. Include / Exclude（选或不选）
B. For-loop Enumeration（从 start 开始选择）

核心状态：

start
path
result

必须解释：

- 为什么每个元素只使用一次
- 为什么不需要 used 数组
- 为什么每个 DFS 状态可以形成一个子集
- 为什么需要 result.append(path.copy())
- 为什么时间复杂度与 2^n 有关

LC-90：

输入允许重复数字。

先排序，然后进行同层去重。

典型规则：

if i > start and nums[i] == nums[i-1]:
    continue

必须解释：

为什么 i > start 表示当前递归层的重复选择？

为什么同一递归分支中仍然允许选取多个相同数值？

为什么不能简单地使用全局去重集合代替所有逻辑？

重点：
同层去重，不是全局禁止使用重复数字。

--------------------------------------------------

Level 2：
02 - 固定数量的组合选取

Level 3：

01 - LC-0077 - Combinations

教学重点：

从 1..n 中选择 k 个不同元素。

核心：

start
path
k

必须解释：

为什么不考虑选择顺序？

为什么下一轮只能从 i+1 开始？

什么时候 path 长度达到 k？

如何使用剩余候选数量进行安全剪枝？

它是 Subsets 模板增加固定长度约束的典型应用。

--------------------------------------------------

Level 2：
03 - 目标和与元素复用限制

Level 3：

01 - LC-0039 - Combination Sum
02 - LC-0040 - Combination Sum II
03 - LC-0216 - Combination Sum III

教学重点：

这三道题必须放在一起对比。

LC-39：

每个候选数字可以重复使用。

核心转移：

dfs(i, remaining - candidates[i])

因为同一个数字还可以再次使用。

LC-40：

每个输入位置最多使用一次。
输入允许重复数值。
最终不能输出重复组合。

通常先排序。

递归使用：

dfs(i+1, remaining - candidates[i])

再结合同层去重：

if i > start and candidates[i] == candidates[i-1]:
    continue

LC-216：

从 1..9 中选择恰好 k 个不同数字。
数字总和必须为 n。

结合：
- 固定数量
- 固定目标和
- 不重复使用
- 搜索范围限制

必须提供清晰的对比：

LC-39：允许重复使用同一个候选值
LC-40：每个输入位置最多使用一次，且需要去重
LC-216：候选值固定为 1..9，恰好选择 k 个

强调：
这三道题主要复用同一个组合搜索框架。

不要记忆三套完全无关的代码。

==================================================
LEVEL 1
02 - 排列与重复元素去重 (Permutations)
==================================================

核心：

Order Matters
Used Array
Visited State
Duplicate Handling

Level 2：
01 - 全排列与重复元素

Level 3：

01 - LC-0046 - Permutations
02 - LC-0047 - Permutations II

教学重点：

LC-46：

Permutation（排列）。

给定互不相同的元素，
列举全部不同顺序。

核心状态：

path
used

每层可以考虑所有尚未使用的元素。

必须解释：

- 为什么需要 used
- 为什么不能直接使用组合题的 start_index
- 为什么排列与组合的数量不同
- 为什么完成一个长度为 n 的 path 后才加入结果
- 为什么需要撤销 used 状态

LC-47：

允许重复数字。

先排序。

典型条件：

if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
    continue

必须解释：

为什么重复元素通常需要按固定顺序参与搜索？

为什么条件中要使用 not used[i-1]？

这个条件与 LC-90 的：

i > start

在不变量上有什么区别？

特别重要：

Subsets II 和 Permutations II
虽然都需要处理重复元素，
但去重状态并不完全相同。

不要错误地给两个题使用同一份去重判断。

==================================================
LEVEL 1
03 - 字符串构造与分割 (String Backtracking)
==================================================

核心：

Character Choices
Valid Prefix
String Partitioning
Constraint Pruning

Level 2：
01 - 逐位置字符串生成与前缀约束

Level 3：

01 - LC-0017 - Letter Combinations of a Phone Number
02 - LC-0022 - Generate Parentheses

教学重点：

LC-17：

每个数字映射到若干字符。

递归状态：

digit_index
path

每一层选择一个合法字母。

必须处理：
- 空输入
- 每个数字可能对应不同数量的字母
- 路径长度与 digits 长度的关系

这是一道很好的基础多分支 DFS 题。

LC-22：

生成合法括号字符串。

必须维护：

open_count
close_count

重要约束：

open_count <= n
close_count <= open_count

必须解释：

为什么不能先生成全部 2^(2n)
个括号字符串，再逐一判断？

为什么通过前缀合法性就能提前剪枝？

为什么 close_count 不能超过 open_count？

这代表：
Constrained String Generation。

--------------------------------------------------

Level 2：
02 - 字符串分割与合法片段判断

Level 3：

01 - LC-0131 - Palindrome Partitioning
02 - LC-0093 - Restore IP Addresses

教学重点：

LC-131：

将字符串分割成多个连续子串，
要求每段都是 Palindrome。

核心状态：

start
path

尝试不同的结束位置 end。

如果 s[start:end] 不是回文，
不能选择这个片段。

必须解释：

- 为什么不是排列字符
- 为什么字符的原始顺序不能改变
- 为什么每次选择的是一个连续区间
- 如何检查回文
- 如何使用 Palindrome DP Table 进行可选优化

优先使用容易理解的标准 Backtracking。

LC-93：

将字符串分成恰好四个合法 IPv4 数字段。

必须满足：

- 恰好四段
- 每段 1 到 3 个字符
- 数值在 0..255
- 不允许不合法的前导零
- 所有字符必须被使用

重要剪枝：

如果剩余字符数量
小于剩余段数，
或者大于剩余段数的三倍，
可以立即返回。

必须解释：
为什么这些剪枝条件是必要条件，
且不会错过合法答案。

将 LC-93 与 LC-131 对比：

它们共享 String Partitioning 框架，
但片段合法性判断不同。

==================================================
LEVEL 1
04 - 网格搜索与约束满足 (Constraint Search)
==================================================

核心：

Grid DFS
Visited / Restore
Constraint Sets
Symmetry Pruning
Bucket Assignment

Level 2：
01 - 网格路径与访问状态

Level 3：

01 - LC-0079 - Word Search

教学重点：

Grid DFS + Backtracking。

从网格中的某个位置开始，
沿上下左右搜索 word。

必须解释：

- DFS 状态 (row, col, index)
- 当前字符必须匹配目标字符
- 同一条路径不能重复使用同一个格子
- 什么时候标记 visited
- 什么时候恢复 visited
- 为什么需要回溯而不是永久标记已访问
- 如何提前停止搜索

可以使用原地字符标记，
也可以使用 visited Set。

如使用原地修改：
必须保证失败分支撤销状态。
成功提前返回时也不应留下不符合函数约定的输入副作用。

与 LC-212 Word Search II 对比：

LC-79：寻找一个固定单词。
LC-212：Trie + DFS 同时寻找多个单词。

LC-212 可能已存在于 Trie 专题。

本次只建立跨专题引用，
不复制其完整题目资料。

--------------------------------------------------

Level 2：
02 - N-Queens 与棋盘冲突检查

Level 3：

01 - LC-0051 - N-Queens
02 - LC-0052 - N-Queens II

教学重点：

N-Queens：

在 n*n 棋盘放置 n 个皇后，
保证不存在互相攻击。

按行进行 DFS。

每一行放置一个皇后。

维护：

cols
diag1
diag2

对角线标识可采用：

row - col
row + col

必须解释：

为什么皇后是否冲突
可以通过列、主对角线和副对角线判断？

为什么一行只放一个皇后，
就不必额外保存行冲突？

LC-51：
返回所有合法棋盘。

LC-52：
返回合法棋盘总数。

注意：

LC-51 与 LC-52 是两道不同的题目。
虽然共享相同的搜索树，
但不能将它们作为 NC/LC 重复题合并。

LC-51 已有 NC 来源。
LC-52 已有正式 LC 来源。

二者都必须保留。

重点说明：
当只需要计数时，可以避免构造完整棋盘结果。

--------------------------------------------------

Level 2：
03 - 等和分桶与对称性剪枝

Level 3：

01 - LC-0698 - Partition to K Equal Sum Subsets

教学重点：

判断能否将数组划分为 k 个非空子集，
且各子集和相同。

首先检查：

total_sum % k == 0

目标桶容量：

target = total_sum // k

可以使用 Bucket Assignment Backtracking。

每个数字只能放入一个桶。

推荐将数字从大到小排列，
以便较早发现容量冲突。

必须解释：

- 为什么桶容量超过 target 时可以剪枝
- 为什么相同桶状态可以进行对称性剪枝
- 为什么给两个空桶分别放置同一个数
  可能产生等价搜索分支
- 如何保证所有元素恰好使用一次
- 为什么该问题在最坏情况下具有指数复杂度

可以比较 Used Mask + Memoization 的进阶方法，
但不强制要求再背一套 Bitmask DP。

请把本题当成学习
Constraint Backtracking + Symmetry Breaking
的代表题。

--------------------------------------------------

Level 2：
04 - Sudoku 与多约束回溯

Level 3：

01 - LC-0037 - Sudoku Solver

教学重点：

Sudoku Solver 属于较复杂的约束满足搜索。

必须维护：

rows
cols
boxes

或者与之等价的约束状态。

对每个空格尝试数字 1..9。

只有数字同时满足：
- 行约束
- 列约束
- 3x3 宫格约束

才能继续 DFS。

必须解释：

- 如何定位 box
- 如何记录已经使用的数字
- 如何撤销失败的尝试
- 如何区分搜索失败与找到完整答案
- 找到完整解后为什么应停止搜索
- 如何避免错误地撤销成功路径中的填充值

如果实现中使用最少候选优先
（Minimum Remaining Values），
可以作为进阶剪枝说明。

但优先提供清晰可靠的标准解法。

LC-37 属于 P2 进阶，
不应该因为它是 Hard 就强制列为最重要必刷。

==================================================
四、原有 NC 题目正式化
==================================================

当前存在 15 个题目来源文件夹。

其中 5 个已有正式 LC 版本：

LC-0037 - Sudoku Solver
LC-0052 - N-Queens II
LC-0047 - Permutations II
LC-0077 - Combinations
LC-0216 - Combination Sum III

另外 10 个为 NC-only：

NC - N-Queens
NC - Word Search
NC - Permutations
NC - Generate Parentheses
NC - Letter Combinations of a Phone Number
NC - Palindrome Partitioning
NC - Combination Sum
NC - Combination Sum II
NC - Subsets
NC - Subsets II

对应 LC 编号：

NC - N-Queens -> LC-0051
NC - Word Search -> LC-0079
NC - Permutations -> LC-0046
NC - Generate Parentheses -> LC-0022
NC - Letter Combinations of a Phone Number -> LC-0017
NC - Palindrome Partitioning -> LC-0131
NC - Combination Sum -> LC-0039
NC - Combination Sum II -> LC-0040
NC - Subsets -> LC-0078
NC - Subsets II -> LC-0090

请逐一检查题面和 solution.py 是否对应。

确认对应后：

1. 创建正式 LC Level 3 目录。
2. 使用现有题目生成工作流补齐 LC 标准文件。
3. 在正式 LC 目录下创建 _neetcode/。
4. 将 NC 原始文件完整迁入 _neetcode/。
5. 保留所有 NC solution.py。
6. 保留 NC metadata.json 和 PDF。
7. 保留所有图片与笔记。
8. 不得将 NC metadata 直接冒充为 LC metadata。
9. 不得覆盖任何原有代码或注释。

特别注意：

当前：
NC - Permutations/

存在：
solution.py
solution_retry.py

两份代码都必须保留。

当前：
NC - N-Queens/

存在：
asset-10 - Explnanation.jpg

必须保留。

当前：
NC - Palindrome Partitioning/

存在：
asset-08 - explanation.jpeg

必须保留。

当前：
NC - Combination Sum/
NC - Combination Sum II/
NC - Subsets/

均有图片资料，必须全部保留。

当前：
LC-0037 - Sudoku Solver/

存在 note.md。

必须保留。

特别强调：

LC-0051 N-Queens
和
LC-0052 N-Queens II

不能合并成一题。

LC-0039、LC-0040、LC-0216
也不能合并成一题。

它们属于相同算法家族，但题目约束不同。

==================================================
五、明确新增的题目
==================================================

第一轮需要新增的不同题目：

LC-0093 - Restore IP Addresses
LC-0698 - Partition to K Equal Sum Subsets

先扫描本专题和整个仓库。

如果已经存在：
复用现有资料或建立合理的跨专题引用。

如果本专题真正缺失：
使用已有 LeetCode 题目生成能力创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据 LC 题号生成全部标准文件的能力。

请直接使用现有工作流。

不要重新设计题目下载或 PDF 生成系统。

对于原有 NC-only 题，
也应补齐正式 LC 标准文件。

禁止：

- 覆盖已有 solution.py
- 生成空白 PDF
- 伪造 metadata
- 使用错误题号对应的题目内容
- 用新生成代码替换原有学习笔记

如果生成失败：
保留成功内容并在最终报告中说明。

==================================================
六、Claude Code 第二轮独立审核
==================================================

ChatGPT 已完成第一轮题库筛选。

你需要进行独立的第二轮审核。

目标：
发现真正重要、具有教学意义、
且当前题库尚未覆盖的 Backtracking Pattern。

参考：

- NeetCode 150
- NeetCode 250
- Blind 75
- Grind 75 / Grind 169
- LeetCode Top Interview 150
- 其他可靠的经典 Backtracking 面试题单

如果具备网络访问，
请验证题号、题名、约束、难度和主流算法。

不要编造 FAANG 内部真实出题频次。

重点审核：

1. Include / Exclude Subsets
2. For-loop Subsets
3. Fixed-size Combinations
4. Combination Sum with Reuse
5. Combination Sum without Reuse
6. Same-level Duplicate Skipping
7. Permutations with Used Array
8. Permutations with Duplicates
9. String Generation
10. Prefix Validity Pruning
11. String Partitioning
12. Palindrome Partitioning
13. Grid DFS + Visited
14. Constraint Sets
15. N-Queens
16. Sudoku
17. Bucket Assignment
18. Symmetry Breaking
19. Branch Pruning
20. Early Termination
21. Backtracking vs Memoization / DP

额外审核候选：

LC-0491 - Non-decreasing Subsequences
LC-0784 - Letter Case Permutation
LC-0473 - Matchsticks to Square
LC-0140 - Word Break II
LC-1593 - Split a String Into the Max Number of Unique Substrings
LC-0526 - Beautiful Arrangement
LC-0980 - Unique Paths III
LC-0494 - Target Sum

这些只是候选，不要求全部新增。

特别判断：

LC-491：
无序输入中的同层去重，
与 LC-90 的排序去重有区别。

LC-784：
相对简单，可能与 LC-17 高度重复。

LC-473：
与 LC-698 的桶分配思路高度相似。

LC-140：
Backtracking + Memoization / DP，
可能更适合 DP 专题。

LC-1593：
需要维护已选择字符串的 Set，
属于字符串唯一性约束。

LC-526：
可能使用 Backtracking 或 Bitmask DP。

LC-980：
可以用于学习访问状态恢复与路径覆盖约束，
但可能也已有 Graph / Grid 专题。

LC-494：
通常属于 DP / Target Sum，
不应因存在回溯暴力解法就强行归入核心题库。

对于每道候选，
都需要评估：

A. 是否真的填补现有知识缺口？
B. 是否属于经典面试题型？
C. 是否具有独立且可迁移的 Pattern？
D. 与现有题目相比是否存在明显重复？
E. 是否值得增加学习和记忆成本？
F. 是否已有其他专题作为主要归属？

允许自主新增最多 4 道真正有价值的题。

如果发现超过 4 道候选：
只新增最重要的 4 道，
其余列入 README 的 Future Candidates。

如果没有值得增加的题，可以不新增。

允许在确有需要时增加 Level 1、Level 2 或 Level 4。

但不能为了单道低频题制造新的算法家族。

==================================================
七、跨专题检查与避免重复
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0022：
可能被 Stack 专题索引。

LC-0079：
可能出现在 Graph / Grid 专题。

LC-0212：
应主要位于 Trie + DFS 专题。

LC-0698：
可能出现在 DP / Bitmask 专题。

LC-0140：
可能位于 Dynamic Programming。

LC-0494：
通常主要位于 DP 专题。

LC-0980：
可能位于 Graph / DFS 专题。

处理原则：

1. 当前 Backtracking 目录已有完整题目资料的，
   必须保留已有学习成果。
2. 当前没有、但其他专题已经有的，
   优先考虑建立相对路径索引。
3. 不修改其他专题的文件。
4. 不重复生成不必要的 PDF 和代码。
5. 在 README 标注 Primary Pattern 和 Secondary Pattern。
6. 不将所有可以使用 DFS 的题都归入 Backtracking。

特别区分：

Tree DFS：
通常是沿既定结构遍历和汇总信息。

Graph DFS：
通常需要处理图的访问关系。

Backtracking：
需要枚举候选决策，
并在探索结束后恢复决策状态。

Memoized DFS / DP：
重用等价子问题的计算结果。

这些算法可以重合，
但不能被错误地当成完全一样的概念。

==================================================
八、Git 安全与原始文件保护
==================================================

当前 Git 仓库存在大量未提交修改和未跟踪文件。

必须严格保护所有现有学习资料。

执行前：

1. 运行 pwd。
2. 检查当前 tree。
3. 运行 git status --short。
4. 扫描全部文件和子目录。
5. 建立原始文件相对路径清单。
6. 为普通文件记录大小和 SHA-256。
7. 检查 Symbolic Links。
8. 检查所有 Python 文件和额外附件。
9. 建立旧路径到新路径的迁移映射。
10. 检查可能的重名冲突。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖原有 solution.py
丢弃 solution_retry.py
覆盖原有笔记
删除图片或 PDF

不要自动：

git add
git commit
git push

只允许在当前：

10-backtracking (回溯)

目录内部新增、移动或重命名文件，
以及安全清理已确认空置的目录。

允许只读扫描其他专题。

如果题目生成工具会写入其他专题或公共仓库配置，
先寻找能限制输出范围的方式。

不能安全限制时，
跳过该生成步骤并报告原因。

对于文件名冲突：

- 不同内容必须保留两个版本。
- 使用 _conflicts/ 或来源子目录。
- 不允许静默覆盖。
- 在最终报告中列出处理方式。

迁移后必须验证：

原有普通文件的 SHA-256 不变。
原有符号链接的目标字符串不变。
所有原始学习资料都可以追溯到新路径。

尽量保证幂等性：

重复执行不会产生：
- 重复题目
- 重复 NC 来源
- 重复编号前缀
- 文件覆盖
- 内容丢失

==================================================
九、README 与学习文档
==================================================

必须创建：

A. Backtracking 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 创建必要的简短 README.md

根目录 README 包含：

1. Backtracking 知识地图。
2. 所有 Level 1 / Level 2 分类。
3. 所有题目及真实相对路径。
4. 推荐学习顺序。
5. P0 / P1 / P2 优先级。
6. 核心 Backtracking Python 模板。
7. 去重条件对照。
8. 剪枝策略对照。
9. 时间与空间复杂度。
10. 跨专题引用。
11. 新增题目的教学价值。
12. 第二轮审核结果。

最重要的是生成：

Backtracking Pattern Recognition Guide。

例如：

Q1：
是否需要输出所有子集？
-> Subsets。

Q2：
是否从候选集合中选出若干元素，
而顺序无关？
-> Combinations。

Q3：
是否需要输出所有可能的顺序？
-> Permutations。

Q4：
同一个候选元素是否允许重复使用？
-> 决定递归时使用 i 还是 i+1。

Q5：
输入是否包含重复元素？
-> Duplicate Skipping。

Q6：
是否逐字符生成满足约束的字符串？
-> String Generation。

Q7：
是否将原字符串切割成连续片段？
-> String Partitioning。

Q8：
是否沿网格邻接关系搜索？
-> Grid DFS + Backtracking。

Q9：
是否需要满足列、对角线、宫格等约束？
-> Constraint Satisfaction。

Q10：
是否有多个相互等价的桶或状态？
-> Symmetry Breaking。

Q11：
是否存在反复出现的等价子问题？
-> 考虑 Memoization / DP。

==================================================
十、核心 Python 模板
==================================================

README 至少提供以下概念模板：

Template 1：
Subsets - Include / Exclude

Template 2：
Combinations - For Loop + start_index

Template 3：
Permutations - used Array

Template 4：
Duplicate Skipping - Sorted Candidates

Template 5：
Combination Sum - Reuse / No Reuse

Template 6：
String Partitioning - start / end

Template 7：
Grid DFS - Mark / Explore / Restore

Template 8：
Constraint Backtracking - Choose / Validate / Undo

不需要把这八种模式写成八套完全独立的完整算法。

应该先展示共同框架：

def dfs(state):
    if terminal_condition:
        record_or_return()
        return

    for choice in valid_choices(state):
        apply(choice)
        dfs(next_state)
        undo(choice)

然后逐项说明：
各类题目为什么改变 DFS 参数、
候选选择范围和终止条件。

模板必须包含正确的不变量及适用前提。

特别建立一份去重对比：

Subsets II：
使用排序后同层去重。

Permutations II：
使用排序 + used 判断重复数值的选择顺序。

Combination Sum II：
使用排序 + start_index + 同层去重。

必须用具体例子证明这些规则为什么不同。

还要特别区分：

剪枝（Pruning）：
提前排除无法产生答案的分支。

去重（Deduplication）：
避免生成相同的结果。

记忆化（Memoization）：
避免反复求解相同子问题。

不能把三者混为一谈。

==================================================
十一、正确性与复杂度要求
==================================================

必须解释：

1. 为什么 Subsets 具有 2^n 个可能子集。
2. 为什么 Permutations 的结果数量可能达到 n!。
3. 为什么 Combination Sum 的复杂度还与 target、
   正数候选限制以及搜索深度有关。
4. 为什么回溯空间分析要区分递归栈、
   路径状态和输出结果。
5. 为什么输出所有解时不能忽略输出本身的成本。
6. 为什么剪枝通常改善实际运行时间，
   但不一定改变最坏情况下的指数复杂度。
7. 为什么 Backtracking 不一定需要 visited。
8. 为什么 Grid DFS 需要恢复访问状态。
9. 为什么全局 visited 与当前路径 visited 语义不同。
10. 为什么返回一个布尔值与收集全部路径
    会影响搜索的提前终止方式。

不能无条件将所有回溯题的复杂度写成：

O(2^n)

必须根据搜索树和输出规模分析。

==================================================
十二、文档语言风格
==================================================

使用中文主导 + 英文专业术语。

例如：

Backtracking（回溯）
Decision Tree（决策树）
Search State（搜索状态）
Loop Invariant（循环不变量）
Pruning（剪枝）
Duplicate Skipping（重复元素去重）
Symmetry Breaking（对称性剪枝）
Constraint Satisfaction（约束满足）
String Partitioning（字符串分割）

每种 Pattern 采用：

1. 1–3 个决定性观察
2. DFS 状态定义
3. 候选选择范围
4. 递归不变量
5. Base Case
6. 简短正确性证明
7. Python 模板
8. 时间与空间复杂度
9. 典型题目
10. 常见错误

避免冗长和重复。

希望我今后打开 README，
能立即回忆起这个 Pattern 的核心思想。

==================================================
十三、P0 / P1 / P2 优先级
==================================================

P0：
经典核心题目与最重要的算法模式。

P1：
重要变体、独立剪枝技巧和进阶应用。

P2：
低优先级或复杂特殊约束。

建议 P0：

LC-0078 - Subsets
LC-0077 - Combinations
LC-0039 - Combination Sum
LC-0046 - Permutations
LC-0090 - Subsets II
LC-0040 - Combination Sum II
LC-0017 - Letter Combinations of a Phone Number
LC-0022 - Generate Parentheses
LC-0131 - Palindrome Partitioning
LC-0079 - Word Search
LC-0051 - N-Queens

建议 P1：

LC-0047 - Permutations II
LC-0216 - Combination Sum III
LC-0093 - Restore IP Addresses
LC-0698 - Partition to K Equal Sum Subsets

建议 P2：

LC-0052 - N-Queens II
LC-0037 - Sudoku Solver

允许根据第二轮独立审核进行适当调整。

但必须解释调整理由。

P0 不代表某家公司有精确的高出题频率，
而是代表最值得优先掌握的经典 Pattern。

README 需要分别提供：

1. P0 核心学习路线
2. P0 + P1 标准面试准备路线
3. P2 进阶与存档路线

不要把所有题目都列为 P0。

==================================================
十四、数量与完整性验收
==================================================

根据当前 tree：

现有题目来源文件夹：
15 个。

已有正式 LC 来源：
5 个。

只有 NC 来源：
10 个。

当前对应不同题目：
15 道。

NC 题正式化：
只是目录整理，不是增加不同题目。

第一轮明确新增：
LC-0093
LC-0698

如果全部成功：

最终预计：
17 道不同题目。

Level 1 分布：

01：6 道
02：2 道
03：4 道
04：5 道

共 17 道。

如果第二轮独立审核新增，
数量允许合理增加。

不得为了凑齐数字创建虚假题目文件。

最终必须验证：

1. 所有旧文件都保留。
2. 所有 NC 来源完整归档。
3. 所有 LC 题号与题名正确。
4. Level 1 编号连续。
5. Level 2 编号连续。
6. Level 3 编号连续。
7. 不存在同题重复主目录。
8. LC-51 与 LC-52 未被错误合并。
9. 所有原始图片保留。
10. LC-37 的 note.md 保留。
11. NC Permutations 的 solution_retry.py 保留。
12. 所有新题标准文件完整。
13. README 引用路径真实存在。
14. 所有旧文件哈希验证通过。
15. 当前专题外没有发生写入或删除。
16. 原有 Git 未提交变更没有被覆盖。

如无法完整验证，
在报告中明确说明未通过的项目。

==================================================
十五、执行步骤
==================================================

请实际执行：

1. 检查当前目录和 Git 状态。
2. 建立原始文件及 SHA-256 清单。
3. 检查所有 Python 代码和自定义附件。
4. 检查当前 NC / LC 对应关系。
5. 只读检查仓库中的跨专题重复。
6. 建立目标目录结构与迁移映射。
7. 创建 4 个 Level 1。
8. 创建对应的 Level 2。
9. 安全迁移全部已有题目。
10. 将 10 个 NC-only 题正式化为 LC。
11. 保留原 NC 来源文件。
12. 为所有 Level 3 正确编号。
13. 创建 LC-93。
14. 创建 LC-698。
15. 补齐旧题确实缺失的标准文件。
16. 独立审核是否遗漏重要 Pattern。
17. 如有必要，自主补充最多 4 道新题。
18. 根据新增题重新调整排序和编号。
19. 创建根目录 README。
20. 创建每个 Level 1 README。
21. 创建 Pattern Recognition Guide。
22. 检查新解法与题目分类的一致性。
23. 对可运行的代码进行语法及适当的样例检查。
24. 验证全部旧文件内容与哈希。
25. 检查跨专题引用。
26. 安全清理已确认空置的遗留目录。
27. 运行最终 tree。
28. 检查最终 Git 状态。
29. 输出完整验收报告。

最终报告必须包含：

- 完整最终 tree
- Level 1 / Level 2 分类
- 原有题目迁移结果
- 10 个 NC-only 题正式化结果
- ChatGPT 推荐新增的 2 道题
- Claude Code 独立新增的题
- 未新增但值得了解的候选
- P0 / P1 / P2 统计
- 旧文件与哈希验证
- 跨专题索引
- Git 变更摘要
- 失败或未完成事项
- 最终推荐刷题顺序

不要只输出目录规划。

请在上述安全限制内直接完成 Backtracking 专题的完整重构。
PROMPT
)"
