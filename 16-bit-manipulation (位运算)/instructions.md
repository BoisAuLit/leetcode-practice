
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/16-bit-manipulation (位运算)' && claude "$(cat <<'PROMPT'
请直接执行当前 Bit Manipulation（位运算）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 算法面试和 Online Assessment（OA）。

请将此目录建设为一套：
- 高面试价值
- 高算法迁移性
- 学习结构清晰
- 核心技巧少而精
- 尽可能降低机械记忆负担
- 能够长期复习
- 有完整文件保护和验收机制

的 Bit Manipulation 学习体系。

这是实际文件系统重构任务，不是规划任务。

请执行目录重构、文件迁移、NC 正式化、新题生成、README 编写、独立审核及完整性验证。

==================================================
一、最重要的学习原则
==================================================

我不希望花大量时间记忆低迁移性的位运算技巧。

相比 Graph、DP、Binary Search 等专题，
Bit Manipulation 的学习范围应该明显收窄。

主要掌握：

1. Binary Representation（二进制表示）
2. Bitwise AND（按位与）
3. Bitwise OR（按位或）
4. Bitwise XOR（按位异或）
5. Left Shift（左移）
6. Right Shift（右移）
7. Bit Mask（位掩码）
8. Popcount（二进制 1 的数量）
9. Lowest Set Bit（最低有效置位）
10. XOR Cancellation（异或抵消）
11. Carry Propagation（进位传播）
12. Common Binary Prefix（公共二进制前缀）
13. Two's Complement（二进制补码）
14. Bitwise OR / AND Aggregation（位聚合）

其他高级技巧以了解为主。

尤其不要把：

- Bitmask DP
- Binary Trie
- Gray Code
- 特殊位编码
- 复杂 XOR 最大化
- 罕见数学位技巧

全部自动列入核心必刷路线。

对于确实具有重要迁移价值的内容，
可以通过跨专题链接学习。

==================================================
二、Level 1 -> Level N 目录规则
==================================================

优先采用：

Level 1：算法家族
Level 2：具体 Bit Pattern
Level 3：LeetCode 题目

确有必要时可以增加 Level 4。

同级正式学习目录统一使用：

01 - ...
02 - ...
03 - ...

排序依据：

1. 基础知识依赖
2. 面试代表性
3. 算法迁移价值
4. 正确性不变量的复用价值
5. 学习难度
6. 记忆成本

不能按 LeetCode 编号机械排序。

Level 3 目录格式：

01 - LC-0191 - Number of 1 Bits
02 - LC-0231 - Power of Two

每个 Level 2 下独立从 01 开始编号。

以下目录不参与算法编号：

_resources
_neetcode
_original_sources
_alternative_solutions
_conflicts
_audit

一个题目在当前专题中只保留一个正式学习位置。

==================================================
三、推荐的 5 个 Level 1
==================================================

第一轮建议：

01 - 二进制基础、位计数与位反转
02 - XOR 不变量与二进制算术
03 - Bitwise Subarray 与位聚合
04 - 二进制分解与原地编码
05 - 跨专题与低优先级存档

以下是完整的第一轮 17 道题目。

如果第二轮审核发现更合理的分类，
可以适当调整 Level 2。

但不得为了低优先级题目创建大量碎片化目录。

==================================================
LEVEL 1
01 - 二进制基础、位计数与位反转
==================================================

核心：

Binary Representation
Bit Mask
Popcount
Bit DP
Fixed-width Bits

--------------------------------------------------
Level 2：
01 - Popcount 与最低有效置位

题目顺序：

LC-0191 - Number of 1 Bits
LC-0231 - Power of Two
LC-0338 - Counting Bits

教学重点：

LC-191：

当前只有：
NC - Number of 1 Bits

需要正式化为 LC-0191。

核心方法之一：

n = n & (n - 1)

每次操作清除最右侧的一个 1。

必须解释：

为什么：

n & (n-1)

可以清除最低有效的 1？

为什么循环次数等于原数字中的 1 的数量？

还可以介绍：

n.bit_count()

但要强调 Python 内建函数
与面试中理解位操作原理的区别。

LC-231：

判断正整数是否为 2 的整数次幂。

核心条件：

n > 0 and (n & (n-1)) == 0

必须解释：

2 的整数次幂在二进制中恰好只有一个 1。

为什么必须单独检查 n > 0？

为什么 0 不符合条件？

LC-338：

计算从 0 到 n 的每个整数的 Popcount。

经典 DP：

dp[i] = dp[i >> 1] + (i & 1)

因为：
i >> 1 相当于去掉最低位。

i & 1 是当前最低位是否为 1。

也可以使用：

dp[i] = dp[i & (i-1)] + 1

对于 i > 0。

必须解释两种递推为什么正确。

重点：

这不是一套独立复杂的 DP 算法。

它是基础位操作在 DP 中的自然应用。

请将 LC-191、231、338 放在一起学习。

--------------------------------------------------
Level 2：
02 - 固定宽度位读取与反转

题目顺序：

LC-0190 - Reverse Bits

教学重点：

LeetCode 190 使用固定 32-bit 表示。

推荐使用：

- Right Shift
- AND 1
- Left Shift
- OR

逐位读取并构造反转后的结果。

必须解释：

为什么需要恰好处理 32 位？

为什么前导零在固定宽度位反转中不能忽略？

为什么不能只把整数转成普通二进制字符串，
再忽略位宽？

必须说明：

Python int 没有固定 32-bit 宽度。

但该题的输入输出遵守固定宽度语义。

原有 note.md 必须完整保留。

==================================================
LEVEL 1
02 - XOR 不变量与二进制算术
==================================================

核心：

XOR Cancellation
Index-Value Pairing
Carry Propagation
Bitwise Arithmetic
Common Binary Prefix

--------------------------------------------------
Level 2：
01 - XOR 抵消与缺失元素

题目顺序：

LC-0136 - Single Number
LC-0268 - Missing Number

教学重点：

LC-136：

输入中除一个元素外，
其他元素都出现两次。

关键性质：

a ^ a = 0
a ^ 0 = a

以及 XOR 满足交换律和结合律。

因此可以对所有元素执行 XOR。

必须解释：

为什么重复元素会抵消？

为什么不需要 Hash Map？

为什么 XOR 适用于本题的出现次数约束？

不能错误地声称：
只要数组存在重复元素，
就可以直接 XOR 得到唯一元素。

LC-268：

数字来自 0..n，
其中缺少一个数字。

可以对：

0..n 的全部数字
以及
nums 中的全部数字

进行 XOR。

重复出现的数字会抵消，
剩下缺失数字。

也可以使用数学求和公式。

必须对比：

XOR 方案
与
Arithmetic Sum 方案。

解释：
为什么本题用 XOR 是合理的，
但不代表它永远比求和法更好？

LC-268 的 note.md 必须完整保留。

--------------------------------------------------
Level 2：
02 - XOR 与 AND 形成二进制加法

题目顺序：

LC-0371 - Sum of Two Integers

教学重点：

这是本次新增的重要核心题。

要求：
不使用 + 或 - 实现两个整数相加。

最重要的观察：

a ^ b

表示不考虑 Carry 的逐位加法结果。

(a & b) << 1

表示需要传递到下一位的 Carry。

重复将：

sum_without_carry
carry

重新进行相加，
直到 Carry 为 0。

必须解释：

为什么 XOR 对应无进位加法？

为什么 AND 可以找到需要产生进位的位置？

为什么 Carry 要左移一位？

为什么这一过程最终可以结束？

特别重要：

Python 的整数具有任意精度，
负数的按位表示可视为无限符号扩展。

因此如果直接对负数执行未经限制的：

a ^ b
(a & b) << 1

并不断迭代，
某些情况下可能无法结束。

正确实现必须处理固定宽度补码。

建议使用：

MASK = 0xFFFFFFFF
MAX_INT = 0x7FFFFFFF

在循环中通过 MASK 限制结果宽度。

最终正确转换回 Python 的有符号整数。

必须实际测试：

(1,2)
(2,3)
(-1,1)
(-2,3)
(-5,-7)
(0,0)

以及更多符合题目约束的边界输入。

不允许给出在负数输入下无限循环的代码。

--------------------------------------------------
Level 2：
03 - Range AND 与共同高位前缀

题目顺序：

LC-0201 - Bitwise AND of Numbers Range

教学重点：

给定两个非负整数：

left
right

计算闭区间 [left,right]
内所有整数的 Bitwise AND。

核心观察：

对于左右端点二进制表示不同的低位，
区间内的某些整数会使这些位变成 0。

最终能保留的是：

left 和 right 的公共高位二进制前缀。

经典方法：

while left < right:
    left >>= 1
    right >>= 1
    shifts += 1

最后将公共前缀左移回来。

必须解释：

- 为什么可以同时右移两个端点
- 为什么公共高位是答案的关键
- 为什么不同的低位最终会被 AND 清零
- 为什么使用 left < right
- 结果如何通过左移恢复到原位

特别注意：

AND 不等于 OR。

不能把 Range AND 的 Common Prefix 思想
直接当成所有 Range Bitwise Operations 的通用公式。

==================================================
LEVEL 1
03 - Bitwise Subarray 与位聚合
==================================================

核心：

Subarray OR
Distinct Aggregated States
Last Set Bit Position
Maximum AND
Bitwise Monotonicity

这个 Level 1 是 P1/P2 扩展。

不应该取代基础 XOR 和 Popcount 学习。

--------------------------------------------------
Level 2：
01 - 子数组 OR 状态与按位贡献

题目顺序：

LC-0898 - Bitwise ORs of Subarrays
LC-2411 - Smallest Subarrays With Maximum Bitwise OR

教学重点：

LC-898：

给定非负整数数组，
统计所有非空连续子数组能够产生多少种
不同的 Bitwise OR 结果。

重要观察：

从左到右扫描时，
维护所有以当前位置结尾的子数组 OR 值集合。

设：

previous = 以 i-1 结尾的所有不同 OR 值

则：

current = {nums[i]}
          union
          {value | nums[i] for value in previous}

为什么只需要上一位置的 OR 值集合？

为什么不同子数组可能产生相同 OR 值？

为什么位的数量受到整数位宽约束？

解释：

对于固定起点、非负整数，
不断扩展右端点时，
Bitwise OR 只能增加置位，
不能清除已经为 1 的位。

因此不同 OR 状态数量受到位宽限制。

可以给出基于位宽 W 的复杂度分析，
不要直接声称对任意无限精度整数
都有固定的 O(n) 时间。

LC-2411：

对于每个起点 i，
找到最短的非空连续子数组，
使其 OR 等于从 i 开始所能得到的最大 OR。

可以从右向左扫描。

维护每个 Bit 最近一次出现 1 的位置。

对于当前 i，
为了取得该后缀的全部可取得置位，
需要扩展到这些 Bit 所要求的最远位置。

必须解释：

为什么维护每一位的最近出现位置就足够？

为什么最短长度由这些位置中的最远者决定？

为什么可以从右向左维护状态？

为什么这与普通 Sliding Window
并不是完全相同的模板？

这两题主要用于理解：

Bitwise Aggregation
+ Limited State Changes。

不要额外为每一道 OR 题记忆复杂数据结构。

--------------------------------------------------
Level 2：
02 - 最大 Bitwise AND 与连续区间

题目顺序：

LC-2419 - Longest Subarray With Maximum Bitwise AND

教学重点：

本题具有一个非常重要的简化观察：

在题目所有元素均为正整数的约束下，
任何非空子数组的 Bitwise AND
不可能超过该子数组中的任何一个元素。

因此所有子数组能取得的最大 AND 值
等于：

max(nums)

要使一个长度大于 1 的子数组
仍保持 AND == max(nums)，
其所有元素都必须等于该最大值。

问题因此转化为：

寻找数组中最长的连续 max(nums) 区间。

不需要复杂的 Bitwise DP。

必须给出简短证明。

同时解释：
为什么这道题看起来是位运算题，
最终却可以使用普通线性扫描？

标记 P2。

不能为了保持位运算标签
而强行使用复杂的 Bitmask 算法。

==================================================
LEVEL 1
04 - 二进制分解与原地编码
==================================================

核心：

Binary Decomposition
Powers of Two
Prefix Sum
In-place Encoding
Original/New State Packing

--------------------------------------------------
Level 2：
01 - Powers of Two 与范围乘积

题目顺序：

LC-2438 - Range Product Queries of Powers

教学重点：

将正整数 n 表示为若干个
互不重复的 2 的整数次幂之和。

例如：

n = 13

二进制：

1101

对应：

1 + 4 + 8

题目需要回答这些幂构成的数组中，
一段连续区间的乘积。

重要观察：

2^a * 2^b = 2^(a+b)

因此可以提取每个置位对应的指数：

[0,2,3]

然后对指数建立 Prefix Sum。

区间乘积对应：

2^(sum_of_exponents_in_range)

再根据题目要求执行 Modular Exponentiation。

必须解释：

为什么可以用指数求和替代直接求大整数乘积？

为什么普通的模乘积前缀和
不能不经说明就直接使用整数除法求区间乘积？

为什么此题更适合归为：

Binary Decomposition + Prefix Sum

而不是 Bitwise Subarray？

特别保护原始 PDF 图解。

标记 P2。

--------------------------------------------------
Level 2：
02 - In-place 编码与旧状态保护

题目顺序：

LC-1920 - Build Array from Permutation
LC-1470 - Shuffle the Array

教学重点：

LC-1920：

基础要求：

ans[i] = nums[nums[i]]

最简单、最清晰的做法是创建新数组。

它的主要教学价值是：

Double Indexing。

如果讨论 O(1) 额外空间 Follow-up，
可以利用元素取值范围，
将 Old Value 和 New Value 同时编码在原数组里。

例如使用适当的 Base：

encoded = old_value + base * new_value

必须解释：

为什么 base 要严格大于原始值的最大可能值？

为什么可以通过：

encoded % base

恢复 Old Value？

为什么可以通过：

encoded // base

得到 New Value？

特别注意：

当 nums[i] 已经被编码时，
不能直接将其当作未修改的原始下标。

所有嵌套索引必须正确提取 Old Value。

LC-1470：

交错排列数组的前后两部分。

基础方案可以使用 O(n) 新数组。

如果使用特殊的 In-place Encoding，
必须依赖题目明确的元素值边界。

不能无条件假设任意 Python 整数
都能在固定宽度存储中安全进行 Bit Packing。

本题不强制记忆 In-place Trick。

两题重点理解：

怎样在原地修改时保留旧信息？

这与 Matrix / Simultaneous Update 专题有关系。

标记 P2。

==================================================
LEVEL 1
05 - 跨专题与低优先级存档
==================================================

目的：

保留原有学习成果，
但明确区分真正的位运算核心算法
与非典型、低迁移性的题目。

--------------------------------------------------
Level 2：
01 - Popcount + Sorting

题目顺序：

LC-1356 - Sort Integers by The Number of 1 Bits

教学重点：

按：

(popcount(x), x)

进行排序。

优先使用：

int.bit_count()

或复用 LC-191 的 Popcount。

本题真正的操作是：
Custom Sorting Key。

不需要额外背一套 Bit Manipulation 算法。

标记 P2。

--------------------------------------------------
Level 2：
02 - 特殊二进制贪心与有符号幂分解

题目顺序：

LC-2571 - Minimum Operations to Reduce an Integer to 0

教学重点：

每次可以给整数加上或减去一个 2 的幂。

目标是用最少操作将其变成 0。

该题涉及：

Binary Representation
Greedy
Signed Powers of Two
Carry Propagation

可以讨论：

连续的 1 如何通过进位
转化为更少数量的加减操作。

例如：

0111

既可以分别消除三个置位，
也可以通过：

1000 - 0001

的思想减少操作。

必须解释：

为什么简单地数 Popcount
不一定等于最少操作数？

为什么有时先加上一个 2 的幂
反而能减少总操作次数？

需要通过正确性证明或可靠的状态推导
确认贪心规则。

这是特殊位运算贪心题，
标记 P2。

必须保留原有 PDF 和 PNG 图解。

不要求长期背诵特殊实现。

--------------------------------------------------
Level 2：
03 - 非位运算题目与 Shell 文本处理

题目顺序：

LC-0194 - Transpose File

特别重要：

LC-194 的官方题目是：

Transpose File。

它是 Shell / Bash 文本处理题。

不是 Bit Manipulation。

主要目标是对文本文件进行行列转置。

必须：

1. 读取现有 metadata.json。
2. 检查 problem.pdf。
3. 检查 solution.py 实际内容。
4. 确认目录是否真的对应 LC-194。
5. 保留所有原始文件。
6. 在本 Level 2 做低优先级存档。
7. 在 README 中明确标记：
   Primary Topic = Shell / Text Processing。

如果 solution.py 实际对应另一道题，
不能未经验证就简单重命名或替换。

如果仓库已有独立 Shell / Bash 专题，
只建立跨专题相对路径索引。

本次不得修改其他专题。

此题不计入 Bit Manipulation 核心必刷路线，
但仍计入当前专题保留的原始题目总数。

==================================================
四、NC-only 题正式化
==================================================

当前只有一个 NC-only 来源：

NC - Number of 1 Bits

对应：

LC-0191 - Number of 1 Bits

请实际读取：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

确认题目身份。

确认后：

1. 创建正式 LC-0191 Level 3 目录。
2. 使用原有工作流生成正式 LC 文件。
3. 将 NC 原始资料完整放入 _neetcode/。
4. 保留 NC 原有 solution.py。
5. 保留 NC metadata.json。
6. 保留 NC 的两个 PDF。
7. 保留额外的：
   asset-n-and-n-minus-1.md
8. 不得把 NC metadata 冒充为官方 LC metadata。
9. 不得覆盖已有解法。

如果生成工具无法得到正确题面，
可以保留已正式编号的目录和 NC 来源，
但不能伪造标准文件。

==================================================
五、第一轮明确新增两道题
==================================================

第一轮只新增：

LC-0371 - Sum of Two Integers
LC-0201 - Bitwise AND of Numbers Range

新增前：

1. 检查当前 Bit Manipulation 专题。
2. 只读检查整个仓库。
3. 核对官方题号和英文题名。
4. 检查是否已有完整题目资料。
5. 判断是否存在合理的跨专题主归属。

如果本专题确实缺失，
使用仓库原有的 LeetCode 生成工具创建：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备通过 LC 编号生成题目文件的能力，
直接复用现有工具即可。

禁止：

- 创建空白 PDF
- 伪造题目 metadata
- 覆盖原有 solution.py
- 删除任何原有附件
- 修改其他专题

如果生成工具失败，
记录失败原因并继续安全的后续步骤。

==================================================
六、Claude Code 第二轮独立审核
==================================================

上述分类和题目由 ChatGPT 第一轮筛选。

你必须独立进行第二轮审核。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
可靠的经典 Bit Manipulation 学习资料

如果网络可用：
核对题号、题名、约束、典型算法。

不能编造 FAANG 真实面试出现频率。

重点审核：

1. XOR Cancellation
2. Popcount
3. Power of Two
4. Lowest Set Bit
5. Clear Lowest Set Bit
6. Read / Set / Clear / Toggle Bit
7. Fixed-width Reverse Bits
8. Counting Bits DP
9. Missing Number XOR
10. Binary Addition with Carry
11. Two's Complement
12. Range Bitwise AND
13. Bitwise OR Aggregation
14. Bitwise AND Aggregation
15. Binary Decomposition
16. Bitmask State Representation
17. Binary Trie Cross-reference

额外候选：

LC-0461 - Hamming Distance
LC-2220 - Minimum Bit Flips to Convert Number
LC-0260 - Single Number III
LC-0137 - Single Number II
LC-1318 - Minimum Flips to Make a OR b Equal to c
LC-0318 - Maximum Product of Word Lengths
LC-0078 - Subsets
LC-0421 - Maximum XOR of Two Numbers in an Array

这些只是候选，不要求全部新增。

必须判断：

LC-461、2220：
基本都是 XOR + Popcount。

与 LC-136、191 的技巧高度重复。

不一定需要新增。

LC-260：
XOR 抵消 + Lowest Set Bit 分组。

如果认为具有独立的经典面试价值，
可以作为 P1 候选。

LC-137：
可以使用逐位计数 mod 3，
或者更复杂的有限状态位运算。

不要为了学习它而机械记忆难懂的位状态公式。

LC-1318：
逐位 Truth Table。
可以训练 OR 约束，
但不一定需要单独记忆。

LC-318：
Bit Mask 表示字符集合。
可以作为跨专题应用候选。

LC-78：
已经在 Backtracking 专题中存在。
可以介绍 Bitmask Enumeration，
但不必重复生成题目。

LC-421：
可能已经在 Trie 专题。
它属于 Binary Trie + XOR。
如已存在，仅建立跨专题索引。

本次第二轮最多新增 2 道。

新增条件：

A. 有明确的经典面试价值。
B. 具有独立可迁移的 Pattern。
C. 现有题目确实没有覆盖该知识。
D. 不是已有题目的简单重复训练。
E. 学习成本相对合理。
F. 不会将 Bit Manipulation 扩张为大规模竞赛题库。

如果找不到真正重要的遗漏，
允许不新增任何题。

另外：

不要主动扩充以下低优先级专题：

- Gray Code 全套变体
- Advanced Bitmask DP
- SOS DP
- XOR Basis / Linear Basis
- 大量罕见位运算数学公式
- 高阶 Binary Trie 查询

除非某项明显符合当前面试目标，
否则记录在 Future Candidates 即可。

==================================================
七、Python 位操作的正确性要求
==================================================

这一部分非常重要。

必须在 README 中建立：

Python Bit Manipulation Pitfalls。

至少解释：

1. Python int 是任意精度整数。
2. Python 负整数的按位操作具有符号扩展语义。
3. ~x 与固定宽度 Bitwise NOT 的区别。
4. >> 对负数的算术右移行为。
5. 为什么 LC-371 需要固定宽度 MASK。
6. 为什么 LC-190 必须处理固定的 32 位。
7. 为什么位运算中的负数不能不加检查地套用正数模板。
8. 为什么表达式应使用合适的括号避免优先级误读。
9. 为什么 1 << k 对应 2 的 k 次幂。
10. 为什么 Bitwise OR 和 Logical OR 不同。

必须解释：

& 与 and 的区别。
| 与 or 的区别。
^ 与幂运算的区别。

Python 中：

^ 是 XOR，
不是乘方。

乘方运算是：

**

还要介绍：

bit_count()
bit_length()
bin()

但要说明：
内建函数属于语言工具，
理解底层位操作仍然有价值。

==================================================
八、位操作 Cheat Sheet
==================================================

建立一个简洁的：

Bit Operations Cheat Sheet。

至少包含：

读取第 k 位：

(n >> k) & 1

将第 k 位设为 1：

n | (1 << k)

将第 k 位清零：

n & ~(1 << k)

翻转第 k 位：

n ^ (1 << k)

提取最低有效置位：

n & -n

清除最低有效置位：

n & (n-1)

判断正整数是否为 2 的幂：

n > 0 and (n & (n-1)) == 0

XOR 抵消：

x ^ x = 0

统计置位：

n.bit_count()

位移：

n << k
n >> k

必须注明适用前提。

对于需要固定 W 位的场景，
必须解释 Mask 的作用。

不要把所有公式作为孤立的魔法口诀。

每个核心公式应有：

- 一句直观解释
- 一个二进制示例
- 一个典型 LeetCode 题号

==================================================
九、跨专题检查
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0078：
Backtracking / Subsets。

LC-0421：
Trie / Binary Trie。

LC-0202：
Linked List / Floyd Cycle Detection。

LC-0007：
Math & Geometry / Reverse Integer。

LC-0050：
Math & Geometry / Fast Exponentiation。

LC-1920：
Arrays / In-place Encoding。

LC-1470：
Arrays / Simulation。

LC-0243? 不要凭猜测创建题号。

LC-194：
Shell / Text Processing。

规则：

当前 Bit Manipulation 目录已有原始资料的题目，
必须保留全部文件。

如果其他专题已有同题：
建立相对路径引用。

不要修改其他专题。

不要重复生成无意义的 PDF。

README 要写清楚：

Primary Pattern
Secondary Pattern
Recommended Algorithm
Cross-topic Reference

不要因为一个题目具有 Bit Manipulation 标签，
就将它强行列为核心位运算面试题。

==================================================
十、原有资料和 Git 安全
==================================================

当前 Git 仓库存在大量未提交修改、
未跟踪文件和用户自己编写的学习笔记。

必须严格保护全部现有资料。

开始前：

1. pwd
2. tree
3. git status --short
4. 递归扫描全部原始文件
5. 记录相对路径
6. 记录普通文件大小与 SHA-256
7. 检查 Symbolic Links
8. 检查现有代码与题号关系
9. 检查 Markdown 相对路径
10. 设计完整迁移映射

建议在本专题内部建立：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

全部审计文件必须写在当前目录内部。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖 solution.py
丢弃 note.md
删除自定义 PDF
删除 PNG/JPEG
修改其他算法专题

不要自动：

git add
git commit
git push

允许只读检查整个仓库，
但实际写入必须限制在：

16-bit-manipulation (位运算)

内部。

如果题目生成工具会修改其他目录或公共配置，
先寻找将输出限制到当前专题的安全方式。

无法限制时，
不要执行不安全的生成步骤，
并在最终报告中说明原因。

如果出现文件路径冲突：

- 内容不同的版本全部保留。
- 不覆盖原有文件。
- 必要时存入 _conflicts/。
- 在报告中记录两个来源及最终路径。

如果移动某个 Symbolic Link，
不得通过该链接修改外部目标。

保证尽可能 Idempotent（幂等）：

重复运行不能：
- 叠加编号
- 重复生成题目
- 重复归档 NC
- 覆盖原文件
- 丢失资料

==================================================
十一、特别保护的文件
==================================================

当前原始目录存在：

summary.jpg

必须完整保留。

可安全移动至：

_resources/
  diagrams/
    summary.jpg

但不得修改文件内容。

LC-0190：
note.md

LC-0268：
note.md

LC-0338：
note.md

NC - Number of 1 Bits：
asset-n-and-n-minus-1.md

LC-2571：
PDF 和 PNG 图解。

LC-0898：
原有 PDF。

LC-2411：
两份 PDF。

LC-2419：
原有 PDF。

LC-2438：
原有 PDF。

LC-194：
所有标准文件及原始 solution.py。

以及所有其他：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
自定义附件

这些文件都必须保留。

不得因重新分类而重新生成并覆盖旧 PDF。

==================================================
十二、README 学习文档
==================================================

必须创建：

A. Bit Manipulation 根目录 README.md
B. 每个 Level 1 的 README.md
C. 复杂 Level 2 的必要短 README
D. Bit Operations Cheat Sheet
E. Python Bitwise Pitfalls
F. Bit Pattern Recognition Guide
G. P0 / P1 / P2 Roadmap
H. 第二轮审核记录

根 README 至少包含：

1. Bit Manipulation 知识地图。
2. 五个 Level 1 分类。
3. 所有 Level 2 / Level 3。
4. 每道题的真实相对路径。
5. P0 / P1 / P2。
6. 重要位运算操作和公式。
7. XOR Cancellation。
8. Popcount。
9. Bit DP。
10. Binary Addition。
11. Common Prefix。
12. Bitwise Subarray。
13. Python 固定宽度问题。
14. 跨专题索引。
15. 不建议长期记忆的特殊技巧。
16. 最终推荐刷题路线。

每个 Level 1 README：

1. 1–3 个决定性观察。
2. Core Invariant（核心不变量）。
3. 为什么使用该位操作。
4. 简短正确性证明。
5. Python 核心模板。
6. 时间与空间复杂度。
7. 代表题目。
8. 典型反例。
9. 容易混淆的 Pattern。

语言要求：

中文主导 + 英文专业术语。

例如：

Bitwise XOR（按位异或）
Bit Mask（位掩码）
Popcount（二进制置位数量）
Two's Complement（二进制补码）
Carry Propagation（进位传播）
Common Binary Prefix（公共二进制前缀）
Fixed-width Integer（固定宽度整数）
Binary Decomposition（二进制分解）

不要写冗长、重复、空泛的讲解。

对于每个核心公式，
先解释为什么正确，
再举一个短二进制例子。

==================================================
十三、核心 Python 模板
==================================================

请至少建立以下模板索引：

Template 1：
Read / Set / Clear / Toggle Bits

Template 2：
Popcount - Clear Lowest Set Bit

Template 3：
XOR Cancellation

Template 4：
Counting Bits DP

Template 5：
Fixed-width Bit Reversal

Template 6：
Binary Addition Using XOR and Carry

Template 7：
Common Prefix for Range AND

Template 8：
Bitwise OR States of Subarrays

Template 9：
Last-set-bit Position Tracking

这些模板只是知识模式。

不代表都需要背诵复杂代码。

应特别解释：

LC-191 / 231 / 338：
共享最低位与 Popcount 技巧。

LC-136 / 268：
共享 XOR Cancellation。

LC-371：
在 XOR 基础上增加 Carry。

LC-201：
关注范围内公共高位。

LC-898 / 2411：
都利用 OR 不会清除已经置位的 Bit，
但维护的状态不同。

LC-2438：
位分解后转为 Prefix Sum。

==================================================
十四、P0 / P1 / P2
==================================================

P0：
核心必练。

建议：

LC-0136 - Single Number
LC-0191 - Number of 1 Bits
LC-0231 - Power of Two
LC-0338 - Counting Bits
LC-0268 - Missing Number
LC-0190 - Reverse Bits
LC-0371 - Sum of Two Integers

P1：
重要变体。

建议：

LC-0201 - Bitwise AND of Numbers Range
LC-0898 - Bitwise ORs of Subarrays
LC-2411 - Smallest Subarrays With Maximum Bitwise OR

P2：
低优先级、特殊技巧或跨专题存档。

建议：

LC-2419 - Longest Subarray With Maximum Bitwise AND
LC-2438 - Range Product Queries of Powers
LC-1920 - Build Array from Permutation
LC-1470 - Shuffle the Array
LC-1356 - Sort Integers by The Number of 1 Bits
LC-2571 - Minimum Operations to Reduce an Integer to 0
LC-0194 - Transpose File

注意：

LC-194 不是 Bit Manipulation，
必须明确标注非本专题算法。

优先级允许第二轮适当调整，
但必须说明具体理由。

不要把所有 Medium 题都提升到 P0。

P0 是学习优先级，
不是任何公司的精确出题概率。

==================================================
十五、数量及完整性验收
==================================================

当前 tree：

19 个目录。
72 个文件。

其中：

15 个题目来源目录。

14 个 LC 编号来源。
1 个 NC-only 来源。

NC-only：
Number of 1 Bits -> LC-191。

当前不同题目：
15 道。

第一轮新增：
LC-371
LC-201

共 2 道。

如果全部成功：

第一轮目标：
17 道不同题目。

预计 Level 1 分布：

01：4 道
02：4 道
03：3 道
04：3 道
05：3 道

合计：
17 道。

其中 LC-194 为非位运算存档题，
但仍计入需要保留的不同题目总数。

如果第二轮独立新增，
最多增加 2 道。

不能为了达到数量而制造虚假文件。

最终必须验证：

1. 15 道原始题都有新归属。
2. 72 个原始文件全部可追溯。
3. NC-191 正式化成功或明确报告限制。
4. LC-194 被正确标记为 Shell 题。
5. LC-2438 被正确标记为 Binary Decomposition。
6. 所有旧 solution.py 都被保留。
7. 原有 note.md 完整。
8. 原有 PDF、PNG、summary.jpg 完整。
9. Level 1 编号连续。
10. Level 2 编号连续。
11. Level 3 编号连续。
12. 新题内容与 LC ID 一致。
13. README 相对路径真实有效。
14. 旧文件 SHA-256 验证通过。
15. Python 负数 Bitwise 测试正确。
16. 当前专题外没有文件被修改。
17. Git 未提交内容未被覆盖。
18. 第二轮审核结果记录完整。

如果某项检查无法完成，
在最终报告中说明，
不能未经检查就声称成功。

==================================================
十六、最小核心复习路线
==================================================

请生成：

Bit Manipulation Core Roadmap。

推荐：

阶段 A：
Binary Basics

LC-191 -> LC-231 -> LC-338

阶段 B：
XOR Cancellation

LC-136 -> LC-268

阶段 C：
Fixed-width Bits 与 Carry

LC-190 -> LC-371

阶段 D：
Range Bitwise Operation

LC-201

阶段 E：
Bitwise Subarray

LC-898 -> LC-2411

阶段 F：
特殊技巧与存档

LC-2419
LC-2438
LC-1920
LC-1470
LC-1356
LC-2571

阶段 F 非必修。

LC-194 只保留在 Shell 存档，
不加入位运算刷题路线。

另输出：

5–7 道最核心 Bit Manipulation 面试题。

必须覆盖不同的基础位操作，
不能只是选择大量重复 Popcount 题。

==================================================
十七、实际执行流程
==================================================

请实际执行：

1. pwd。
2. 扫描完整 tree。
3. 检查 Git 状态。
4. 记录原始文件 Manifest。
5. 计算所有文件 SHA-256。
6. 检查 Symbolic Links。
7. 核对全部 15 道原始题目。
8. 特别核查 LC-194 的真实题目类型。
9. 核查 LC-2438 的实际解法。
10. 核查 NC-191。
11. 只读检查整个仓库的跨专题重复。
12. 设计 5 个 Level 1。
13. 设计所有 Level 2。
14. 建立完整迁移映射。
15. 安全迁移旧题。
16. 为 Level 3 重新编号。
17. 正式化 LC-191。
18. 保留完整 NC 原始资料。
19. 新增 LC-371。
20. 新增 LC-201。
21. 独立进行第二轮题库审核。
22. 必要时新增最多 2 道高价值题。
23. 根据审核结果调整排序。
24. 安全整理 summary.jpg。
25. 创建根目录 README。
26. 创建所有 Level 1 README。
27. 创建 Bit Operations Cheat Sheet。
28. 创建 Python Bitwise Pitfalls。
29. 创建 Pattern Recognition Guide。
30. 创建 P0 / P1 / P2 Roadmap。
31. 对新增 Python 代码执行语法检查。
32. 对负数和固定宽度进行专项测试。
33. 验证全部原始文件哈希。
34. 检查所有 README 相对链接。
35. 检查全部目录编号。
36. 仅清理确认已空的旧目录。
37. 运行最终 tree。
38. 再次检查 Git 状态。
39. 输出完整验收报告。

最终报告包括：

- 最终完整 tree
- 5 个 Level 1
- 所有 Level 2 Pattern
- 原始 15 道题目的迁移清单
- LC-191 正式化结果
- LC-194 分类修正
- LC-2438 分类修正
- 第一轮新增 2 道题
- Claude Code 第二轮自主新增题
- 未新增候选及理由
- P0 / P1 / P2 统计
- 最小核心复习路线
- 原始文件 SHA-256 验证
- Python 负数与固定宽度测试
- 跨专题引用
- Git 变更摘要
- 失败或未完成项目

如果某项操作存在文件损失风险，
保持原始文件不变并报告，
继续完成其他安全步骤。

不要仅仅输出目录规划。

请直接在以上安全约束下完成
Bit Manipulation 专题的完整重构。
PROMPT
)"
