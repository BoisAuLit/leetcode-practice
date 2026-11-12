
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/15-math-geometry (数学、几何)' && claude "$(cat <<'PROMPT'
请直接执行当前 Math & Geometry（数学、几何）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请将这个目录建设成一套：

- 高面试价值
- 高算法迁移性
- 清晰的多级目录
- 学习顺序合理
- 尽可能减少机械记忆
- 具备必要的正确性证明
- 适合长期复习

的 Math & Geometry 学习体系。

这是一项实际文件系统重构任务，而不是规划任务。

请实际执行：
文件审计、目录重构、原文件迁移、NC 正式化、新题生成、README 编写、第二轮独立审核以及最终验收。

==================================================
一、核心学习目标
==================================================

Math & Geometry 并不是一个只有单一模板的算法类别。

我希望将它归纳成少量可迁移的 Pattern：

1. Matrix Traversal（矩阵遍历）
2. Boundary Simulation（边界模拟）
3. Direction Vectors（方向向量）
4. Coordinate Transformation（坐标变换）
5. In-place Matrix Modification（原地矩阵修改）
6. Simultaneous State Update（同步状态更新）
7. Digit Processing（数位处理）
8. Carry Propagation（进位传播）
9. Integer Parsing（整数解析）
10. Fast Exponentiation（快速幂）
11. Bounding Box（最小外接矩形）
12. Rectangle Intersection（矩形交集）
13. Coordinate Hashing（坐标哈希）
14. Geometric Counting（几何计数）

特别要求：

这个专题不要盲目扩充纯数学题。

对于需要记忆特殊数学定理、
冷门数论公式或竞赛技巧的题目，
应谨慎评估学习收益。

我更希望掌握：

- 如何安全处理矩阵边界
- 如何定义遍历方向
- 如何进行原地修改
- 如何正确处理数位和进位
- 如何避免整数溢出
- 如何使用平方快速幂
- 如何将几何问题转化成坐标计算或 Hash Map 计数

不要把每道题视为完全独立的算法。

==================================================
二、Level 1 -> Level N 规则
==================================================

优先采用：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：LeetCode 题目

有必要时允许 Level 4。

但不要为了某一道简单题
制造无意义的分类层级。

所有同级正式学习目录使用：

01 - ...
02 - ...
03 - ...

排序综合考虑：

1. 学习依赖关系
2. 面试代表性
3. 算法迁移价值
4. 代码与不变量的复用性
5. 难度递进
6. 学习与记忆成本

不要按照 LeetCode 题号机械排序。

Level 3 命名示例：

01 - LC-0054 - Spiral Matrix
02 - LC-0059 - Spiral Matrix II

每个 Level 2 下的题目独立编号。

资源目录：

_resources
_neetcode
_original_sources
_alternative_solutions
_conflicts
_audit
utils

不参与算法分类编号。

==================================================
三、第一轮 Level 1 分类
==================================================

建议建立以下四个 Level 1：

01 - 矩阵遍历与方向模拟 (Matrix Traversal)
02 - 矩阵变换与状态模拟 (Matrix Transformation)
03 - 整数运算与数位处理 (Arithmetic)
04 - 坐标几何与空间计数 (Geometry)

以下是完整的第一轮题目结构。

==================================================
LEVEL 1
01 - 矩阵遍历与方向模拟
==================================================

核心：

Boundary Traversal
Spiral Traversal
Direction Simulation
Diagonal Traversal
Coordinate Validation

--------------------------------------------------
Level 2：
01 - 螺旋遍历、生成与填充

题目顺序：

LC-0054 - Spiral Matrix
LC-0059 - Spiral Matrix II
LC-2326 - Spiral Matrix IV

教学重点：

LC-54：

给定二维矩阵，
按照顺时针螺旋顺序返回元素。

推荐维护四个边界：

top
bottom
left
right

每轮依次遍历：

1. 上边界，从左到右
2. 右边界，从上到下
3. 下边界，从右到左
4. 左边界，从下到上

必须解释：

- 为什么遍历完一条边就要收缩边界
- 为什么有些方向遍历前需要检查边界
- 为什么单行或单列容易发生重复访问
- 为什么每个有效格子只能访问一次
- 如何处理非正方形矩阵

LC-59：

给定 n，生成一个 n*n 矩阵，
按照螺旋顺序填入 1..n*n。

核心与 LC-54 相同：

Spiral Boundary Traversal。

只是：
LC-54 是 Read。
LC-59 是 Write。

不需要记忆两套独立的螺旋算法。

LC-2326：

将 Linked List 中的元素
按照螺旋顺序填入 m*n 矩阵。

未填充的格子保持 -1。

核心仍然是螺旋填充。

额外需要维护：

curr = head

必须正确处理：
- 链表比矩阵容量短
- 链表为空
- 矩阵单行或单列
- 不重复填充格子
- 链表节点已经使用完毕时停止读取

这道题与 Linked List 专题存在交叉关系。

当前目录存在：

utils/ListNode.py

必须检查其引用并完整保留。

本题标记 P2，
重点只是对 LC-54 / 59 的技巧迁移。

--------------------------------------------------
Level 2：
02 - 对角线与动态方向遍历

题目顺序：

LC-0498 - Diagonal Traverse
LC-0885 - Spiral Matrix III

教学重点：

LC-498：

按照对角线顺序遍历矩阵。

需要根据当前位置决定：

向右上方移动
或者
向左下方移动。

可以利用：

row + col

表示元素所在的对角线编号。

但应根据正确的边界规则更新坐标。

必须解释：

- 为什么同一对角线 row+col 相等
- 为什么需要交替改变方向
- 如何处理碰到上边界、下边界、左边界、右边界
- 为什么单行和单列需要边界验证

LC-885：

从指定起点出发，
按照逐渐扩大的矩形螺旋路径移动。

与 LC-54 不同：

LC-54：
在有限矩阵内部逐层收缩边界。

LC-885：
从起点向外扩展，允许路径暂时超出矩阵。

只有当坐标位于：

0 <= row < rows
0 <= col < cols

时才记录位置。

必须持续移动，
直到输出恰好 rows*cols 个合法坐标。

重点解释：

为什么可以在矩阵之外继续移动？

如何设计步长序列和四个移动方向？

为什么最终应当只记录合法坐标？

本题标记 P2。

不要要求把 LC-885 的特殊螺旋步长
作为所有 Matrix 题的核心模板背诵。

==================================================
LEVEL 1
02 - 矩阵变换与状态模拟
==================================================

核心：

Transpose
Rotate
In-place Marking
Simultaneous Update
Grid Simulation
Gravity Simulation

--------------------------------------------------
Level 2：
01 - 转置与矩阵旋转

题目顺序：

LC-0867 - Transpose Matrix
LC-0048 - Rotate Image

教学重点：

LC-867：

Transpose Matrix。

对于原矩阵中的：

matrix[r][c]

新矩阵对应：

result[c][r]

必须解释：

m*n 矩阵转置后，
新矩阵尺寸为 n*m。

对于一般矩形矩阵，
通常需要创建新矩阵。

LC-48：

将 n*n 矩阵顺时针旋转 90 度。

要求原地修改。

推荐核心方法：

1. Transpose
2. Reverse Each Row

必须解释：

为什么先转置再反转每一行，
等价于顺时针旋转 90 度？

通过坐标映射证明：

(r,c) -> (c,n-1-r)

还可以简单介绍：
Four-way Layer Rotation。

但是只需要选择一套最清晰的标准实现。

不要求背诵两种复杂写法。

特别强调：

LC-867 不要求原地完成矩形矩阵转置。

LC-48 要求原地旋转正方形矩阵。

不能将两者的空间复杂度混淆。

--------------------------------------------------
Level 2：
02 - 原地标记与同步状态更新

题目顺序：

LC-0073 - Set Matrix Zeroes
LC-0289 - Game of Life

教学重点：

LC-73：

这是本次最重要的新增 Matrix 题目。

如果原矩阵某个位置为 0，
需要将其整行和整列设置成 0。

关键难点：

不能在第一次发现 0 时，
就立即清零整行和整列。

否则新产生的 0
会错误地影响其他行和列。

必须区分：

Original State
Final State

推荐两种解法：

A. Row Set + Column Set

容易理解，额外空间 O(m+n)。

B. First Row / First Column Markers

使用第一行和第一列存储标记，
实现 O(1) 额外空间。

必须解释：

- 为什么需要两阶段处理
- 为什么第一行和第一列有特殊性
- 如何处理 matrix[0][0]
- 为什么通常需要额外记录 first_col_zero
- 为什么写入顺序影响正确性
- 如何避免污染尚未读取的原始标记

LC-289：

Game of Life。

每个格子的下一状态
取决于它周围 8 个格子的原始状态。

必须同时更新全部细胞。

不能按扫描顺序直接覆盖旧状态，
否则后面的格子将读到错误的新值。

可以使用：

A. 新矩阵存储下一轮状态

或者：

B. In-place State Encoding

例如使用不同的临时状态标记：
原来活、后来死；
原来死、后来活。

也可以使用 Bit Encoding，
通过最低位表示旧状态，
另一位表示新状态。

必须解释：

为什么可以在一个整数中暂存新旧信息？

如何保证邻居计数使用的仍是旧状态？

为什么需要第二遍统一应用新状态？

这两题的共同模式：

Read Original State
-> Record Updates
-> Apply Updates

重点理解 Simultaneous Update，
而不是背诵特殊数字标记。

--------------------------------------------------
Level 2：
03 - 多轮矩阵消除与重力模拟

题目顺序：

LC-0723 - Candy Crush

教学重点：

这是复杂 Matrix Simulation。

每轮：

1. 找到所有应该消除的连续元素。
2. 同时标记所有待消除元素。
3. 完成消除。
4. 让剩余元素按照重力下落。
5. 重复直到状态稳定。

必须解释：

为什么不能扫描到一组三连消
就立即触发重力？

为什么应该先确定本轮所有消除对象？

为什么消除后需要从每列底部向上处理？

如何使用 Write Pointer
将非零元素向下压缩？

为什么必须正确处理：
- Horizontal Matches
- Vertical Matches
- Overlapping Matches
- Multiple Rounds
- Stable Board

如果使用负数暂存消除标记，
必须解释这种方法依赖的输入值约束。

本题标记 P2。

不要求记忆额外的复杂矩阵模拟框架，
重点是理解多阶段状态更新。

==================================================
LEVEL 1
03 - 整数运算与数位处理
==================================================

核心：

Digit Processing
Carry Propagation
Integer Parsing
Overflow
Long Multiplication
Fast Exponentiation

--------------------------------------------------
Level 2：
01 - 数位进位与整数反转

题目顺序：

LC-0066 - Plus One
LC-0007 - Reverse Integer

教学重点：

LC-66：

给定十进制数字数组，
表示一个非负整数。

需要加一。

从最后一位开始处理。

如果 digit < 9：
加一并直接返回。

如果 digit == 9：
变成 0，向前传播 Carry。

如果所有数字都是 9：
需要增加新的最高位。

必须解释：

为什么加一只可能影响末尾的连续 9？

为什么不需要先把所有数字转换成整数？

LC-7：

将一个有符号整数的十进制数位反转。

推荐使用整数运算：

digit extraction
integer truncation
result accumulation

必须特别处理负数。

Python 的 // 对负数执行向下取整，
不等价于某些语言中的向零截断。

因此不能直接照搬正数拆位逻辑处理负数。

可以先保存符号，
对绝对值处理数位。

还需要检查 32-bit Signed Integer Range：

[-2^31, 2^31-1]

如果反转后的整数超出范围，
返回 0。

必须解释：

为什么 Python 整数不会自动出现 32-bit Overflow，
但题目的输出限制仍然需要人工判断？

不要把 LC-7 与 LC-66 当成完全不同的数位算法。

两者共享 Digit Processing，
但一个主要关注 Carry，
另一个关注位序与 Overflow。

--------------------------------------------------
Level 2：
02 - 字符串解析与大整数乘法

题目顺序：

LC-0008 - String to Integer (atoi)
LC-0043 - Multiply Strings

教学重点：

LC-8：

将字符串解析成 32-bit Signed Integer。

需要正确处理：

- Leading Whitespace
- Optional Sign
- Digit Sequence
- 第一个非数字字符
- 无有效数字
- 32-bit Range Clamping

必须解释：

为什么应当按照有限的解析阶段处理输入？

为什么不能简单地直接使用 int(s)？

为什么遇到数字序列之后的非法字符
需要停止，而不是跳过？

LC-43：

两个非负整数以字符串表示。

要求计算乘积，
不能直接将整个字符串转换成大整数再相乘。

推荐模拟竖式乘法：

Grade-school Multiplication。

使用长度：

m+n

的结果数组。

对于：
num1[i]
num2[j]

将乘积累加到对应的数位位置。

必须解释：

为什么使用 i+j 和 i+j+1
对应乘法结果中的相邻位置？

为什么需要正确处理 Carry？

为什么最终结果最多需要 m+n 位？

如何去除多余的前导零？

为什么输入中有 "0" 时
必须返回正确的零表示？

目标复杂度：

O(m*n) 时间。

不要错误地将 Python 内建任意精度乘法
当成符合题意的标准解法。

--------------------------------------------------
Level 2：
03 - Fast Exponentiation 平方快速幂

题目顺序：

LC-0050 - Pow(x, n)

教学重点：

这是本次最重要的新增数值算法题之一。

Exponentiation by Squaring
（平方快速幂）。

核心观察：

对于偶数 n：

x^n = (x*x)^(n/2)

对于奇数 n：

x^n = x * x^(n-1)

因此可以不断将指数减半。

推荐提供 Iterative Binary Exponentiation。

例如：

result = 1
base = x
exponent = abs(n)

当指数当前最低位为 1 时，
将当前 base 乘进 result。

每轮：

base *= base
exponent //= 2

必须解释：

为什么处理指数二进制位，
相当于将 x^n 分解成若干平方项的乘积？

为什么只需要 O(log |n|) 次循环？

如何处理负指数？

为什么 n < 0 时需要计算倒数？

如何处理：
- n == 0
- n == 1
- n < 0
- x == 1
- x == -1
- 极端整数指数
- 浮点数误差

本题不仅用于 LeetCode，
其思想还迁移到：
- Modular Exponentiation
- Binary Lifting
- Matrix Exponentiation

但本次不需要展开学习所有这些进阶算法。

重点掌握 Fast Power 的一个清晰可靠模板。

==================================================
LEVEL 1
04 - 坐标几何与空间计数
==================================================

核心：

Coordinate Bounding
Rectangle Intersection
Hash Map Frequency
Geometric Constraints
Axis-aligned Shapes

--------------------------------------------------
Level 2：
01 - Bounding Box 与矩形交集

题目顺序：

LC-3195 - Find the Minimum Area to Cover All Ones I
LC-0223 - Rectangle Area

教学重点：

LC-3195：

在二进制矩阵中，
找到能够覆盖全部 1 的最小轴对齐矩形。

维护：

min_row
max_row
min_col
max_col

遇到每个 1 时更新边界。

最终矩形面积：

(max_row-min_row+1)
*
(max_col-min_col+1)

必须解释：

为什么最小矩形由所有 1 的
最小和最大行列坐标决定？

为什么这里需要 +1？

注意根据题目真实输入约束处理特殊情况。

LC-223：

给定两个 Axis-aligned Rectangles
（坐标轴对齐矩形），计算并集总面积。

核心：

Area(A union B)
=
Area(A) + Area(B) - Area(A intersection B)

矩形交集宽度：

max(
    0,
    min(ax2,bx2) - max(ax1,bx1)
)

矩形交集高度：

max(
    0,
    min(ay2,by2) - max(ay1,by1)
)

Intersection Area：

width * height

必须解释：

- 为什么需要减去重叠面积
- 为什么不重叠时宽度或高度为 0
- 为什么两个矩形只在边界相接时交集面积为 0
- 如何处理负坐标
- 为什么这里没有 LC-3195 中的 +1

重点比较：

LC-3195：
离散矩阵格子数量。

LC-223：
平面连续坐标中的几何面积。

二者虽然都使用矩形，
但面积计算中的端点语义不同。

--------------------------------------------------
Level 2：
02 - 坐标 Hash Map 与正方形计数

题目顺序：

LC-2013 - Detect Squares

当前只有：

NC - Detect Squares

请验证后正式化为 LC-2013。

教学重点：

维护：

point_counts[(x,y)]

或者等价的二维频率映射。

实现：

add(point)
count(point)

count 查询时：

给定一个查询点，
寻找与它一起形成 Axis-aligned Square
的三个已添加顶点。

重点解释：

- 为什么正方形必须四边平行于坐标轴
- 为什么可以枚举对角顶点
- 为什么正方形需要宽高绝对值相等
- 为什么零边长不构成合法正方形
- 如何根据另外两个角的坐标计算数量
- 为什么必须使用 Frequency Map，而不是 Set

例如三个需要被使用的点，
其出现次数分别为：

a
b
c

则它们能够形成的组合数量贡献是：

a*b*c

必须解释重复点如何影响计数。

本题不要求计算浮点距离或平方根。

重点是：

Geometry -> Coordinate Constraints -> Hash Map Counting。

这是一道非常值得保留的经典 Geometry + Design 题。

==================================================
四、NC-only 正式化
==================================================

当前只有一个 NC-only 题目：

NC - Detect Squares

正式编号：

LC-2013 - Detect Squares

请首先检查：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
note.md

验证题面与实际代码确实对应 LC-2013。

确认后：

1. 创建正式 LC-2013 Level 3 目录。
2. 使用原有题目生成工作流补齐标准 LC 文件。
3. 将 NC 原始文件全部归档到：
   _neetcode/
4. 保留原有 NC solution.py。
5. 保留原有 note.md。
6. 保留原有 metadata 和 PDF。
7. 不得把 NC metadata 直接冒充官方 LC metadata。

本专题中没有其他已知的 NC / LC 同题双来源。

如果实际审计发现更多重复来源，
应当按照文件内容核实后再合并。

==================================================
五、第一轮新增的五道题
==================================================

明确建议新增：

LC-0073 - Set Matrix Zeroes
LC-0050 - Pow(x, n)
LC-0289 - Game of Life
LC-0007 - Reverse Integer
LC-0223 - Rectangle Area

请首先检查：

1. 当前专题是否已有。
2. 整个仓库其他专题是否已有。
3. 是否属于正确的算法主归属。
4. 是否具备合法可靠的题面来源。

如果确实缺失，
调用仓库现有的 LeetCode 题目生成能力：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据 LeetCode 编号
创建这些标准资料的能力。

请复用已有工作流。

不能：

- 覆盖旧 solution.py
- 生成空白 PDF
- 伪造 metadata
- 使用错误题目的题面
- 删除用户的注释
- 删除原始图片和笔记

如果生成失败：
保留已有成果，
记录失败原因，
继续其他安全任务。

==================================================
六、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 第一轮推荐。

请再独立审核一次，
判断是否遗漏重要的 Math & Geometry Pattern。

参考：

- NeetCode 150
- NeetCode 250
- Blind 75
- Grind 75 / Grind 169
- LeetCode Top Interview 150
- 其他可靠的算法面试题单

如果网络访问可用，
请核对题号、官方题名、约束与主流算法。

不要编造 FAANG 内部出题频次。

必须检查：

1. Spiral Traversal
2. Matrix Boundary Simulation
3. Diagonal Traversal
4. Direction Vectors
5. Transpose / Rotation
6. In-place Matrix Marking
7. Simultaneous Updates
8. Grid Gravity Simulation
9. Digit Extraction
10. Carry Propagation
11. String-to-Integer Parsing
12. Grade-school Multiplication
13. Fast Exponentiation
14. Bounding Box
15. Rectangle Intersection
16. Coordinate Hashing
17. Counting Axis-aligned Squares

额外审核候选：

LC-0202 - Happy Number
LC-0013 - Roman to Integer
LC-0012 - Integer to Roman
LC-0067 - Add Binary
LC-0204 - Count Primes
LC-0149 - Max Points on a Line
LC-0939 - Minimum Area Rectangle
LC-0836 - Rectangle Overlap
LC-1572 - Matrix Diagonal Sum
LC-1861 - Rotating the Box
LC-0006 - Zigzag Conversion

特别注意：

LC-202：
已有 Linked List / Floyd Cycle Detection 资料。
优先建立跨专题索引，
不重复生成。

LC-13 / LC-12：
字符串和数值转换，
有一定基础价值，
但通常不需要专门记忆复杂算法。

LC-67：
与 LC-66 具有 Carry Propagation 关联。

LC-204：
Sieve of Eratosthenes。
属于独立数学算法，
但不要因此自动扩充完整数论专题。

LC-149：
Slope Normalization + GCD。
有独立几何价值，
但实现细节和边界处理较多。

可作为 P2 候选。

LC-939：
Axis-aligned Rectangle + Coordinate Hashing。
与 LC-2013 有较多共同思想。

是否新增取决于它是否提供额外教学收益。

LC-836：
矩形交集判定，
与 LC-223 的面积交集公式有重合。

LC-1572：
比较简单，可能不值得单独记忆。

LC-1861：
Rotation + Gravity Simulation，
与 LC-48、723 有明显联系。

LC-6：
Zigzag Conversion。
与二维轨迹模拟相关，
但未必值得单独建立核心 Pattern。

允许第二轮最多自主新增 3 道题。

新增必须满足：

A. 确实填补某个重要知识缺口。
B. 有较高的面试代表性。
C. 能够迁移到其他题目。
D. 不是现有题的简单重复。
E. 学习成本合理。
F. 没有其他专题更合适的主归属。

如果无高价值遗漏，
完全可以不新增。

不允许因为 Math & Geometry 范围广泛，
就引入大量低迁移性的竞赛数学题。

特别不要为了追求所谓完整性，
自动新增以下复杂专题：

- Computational Geometry 全家族
- Convex Hull
- FFT / NTT
- Advanced Number Theory
- 高级组合数学
- 复杂矩阵快速幂
- 特殊数论定理

如果确实值得了解，
可以在 Future Candidates 中简要记录，
不必立刻变成正式题目。

==================================================
七、跨专题检查
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0202 -> Linked List / Floyd
LC-0007 -> Bit Manipulation / Arithmetic
LC-0069 -> Binary Search
LC-0050 -> Math / Fast Power
LC-0073 -> Matrix
LC-0289 -> Matrix Simulation
LC-2013 -> Geometry / Hash Map
LC-2326 -> Linked List
LC-3195 -> Matrix Bounding Box
LC-149 -> Geometry / Hashing

原则：

1. 当前 Math & Geometry 已有原始资料，
   必须完整保留。
2. 当前目录没有、
   其他专题已经有相同题目的，
   优先使用 README 跨专题引用。
3. 不无意义地复制 PDF。
4. 不修改其他专题。
5. 同一道题可以通过多个算法理解，
   但必须标记清楚 Primary Pattern。
6. 不以 LeetCode 标签作为唯一分类依据。

README 中记录：

Primary Pattern
Secondary Pattern
Recommended Algorithm
Cross-topic Reference

尤其：

LC-202 已存在于 Floyd Cycle Detection。

虽然它也是 NeetCode Math & Geometry 的经典题，
本次不需要再次生成。

==================================================
八、现有资料与 utils 保护
==================================================

当前存在：

utils/
  ListNode.py

必须首先检查：
- 哪些 solution.py 导入了它
- 是否存在相对路径依赖
- 是否有其他脚本调用
- 是否存在符号链接

如果移动可能破坏依赖，
保持 utils/ 原位置不变。

如果需要整理理论资源：

优先建立：

_resources/
  docs/
  diagrams/
  templates/

但只有实际存在的资源才需要创建目录。

不能制造大量空目录。

特别保护：

LC-0066：
note.md

LC-0048：
note.md

LC-0054：
note.md

LC-0498：
asset-0498 - Diagonal Traverse.drawio

NC - Detect Squares：
note.md

以及全部：

metadata.json
problem.pdf
problem_dark.pdf
solution.py
所有原始图解
所有自定义附件

不允许为了重新生成漂亮的题目 PDF，
而覆盖原来的 problem.pdf。

==================================================
九、文件安全与 Git 保护
==================================================

当前 Git 仓库存在大量未提交修改
以及未跟踪文件。

这些都是已有学习成果。

执行前必须：

1. pwd
2. tree
3. git status --short
4. 递归扫描本专题全部文件
5. 建立原始文件相对路径清单
6. 为普通文件记录 SHA-256
7. 记录文件大小
8. 检查 Symbolic Links
9. 检查原有 Python import
10. 检查 Markdown 相对链接
11. 验证题目身份
12. 建立完整迁移映射

推荐创建：

_audit/
  pre-migration-manifest.json
  migration-map.json
  post-migration-report.md

审计文件必须放在本专题内部。

严格禁止：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖
删除未跟踪文件
覆盖 solution.py
覆盖 note.md
删除 Draw.io
删除 PDF 或图片
修改其他算法专题

不要自动：

git add
git commit
git push

全部写入范围必须限制在：

15-math-geometry (数学、几何)

内部。

可以只读扫描整个仓库。

如果题目生成工具需要修改外部配置、
其他算法目录或公共仓库文件，
先寻找只在本专题输出的方法。

无法安全限制时，
跳过该生成步骤并说明原因。

对于目标路径冲突：

- 不同内容必须全部保留。
- 相同内容需要保留来源记录。
- 可以使用 _conflicts/。
- 不得静默覆盖。
- 不得删除来源资料。

如果原目录已迁移完成，
只有确认完全为空后，
才允许删除空目录。

确保流程尽可能 Idempotent（幂等）。

重复执行不能：
- 重复添加编号
- 重复创建题目
- 重复归档 NC
- 覆盖代码
- 遗失学习资料

==================================================
十、README 学习文档
==================================================

必须创建：

A. Math & Geometry 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 建立必要的短 README
D. Math & Geometry Pattern Recognition Guide
E. Matrix Operations Cheat Sheet
F. Arithmetic & Geometry Cheat Sheet
G. P0 / P1 / P2 Core Roadmap

根 README 包含：

1. Math & Geometry 知识地图
2. 四个 Level 1 分类
3. 每个 Level 2 的教学目标
4. 所有题目及真实相对路径
5. P0 / P1 / P2
6. Matrix Traversal 模板
7. Matrix Rotation 模板
8. In-place Marking 模板
9. Simultaneous Update 模板
10. Digit Processing 模板
11. Fast Exponentiation 模板
12. Coordinate Geometry 基础公式
13. Cross-topic References
14. 第二轮审核结果
15. 最终推荐学习顺序

每个 Pattern 讲解：

1. 1–3 个决定性观察
2. 状态或坐标的含义
3. 核心不变量
4. 边界条件
5. 简短正确性证明
6. Python 参考模板
7. 时间复杂度
8. 空间复杂度
9. 代表题目
10. 常见错误和反例

对于数学几何题，
不要把公式直接写出来而不解释其来源。

必须说明：

为什么该公式成立？

什么时候不能使用？

哪些边界条件会使公式失效？

==================================================
十一、核心模板
==================================================

README 应包含以下核心 Python 模板索引：

Template 1：
Matrix Spiral Boundary Traversal

Template 2：
Matrix Transpose + Reverse

Template 3：
In-place Matrix Marking

Template 4：
Simultaneous State Update

Template 5：
Digit Processing + Carry

Template 6：
Integer Parsing + Bounds

Template 7：
Grade-school String Multiplication

Template 8：
Exponentiation by Squaring

Template 9：
Rectangle Intersection

Template 10：
Coordinate Hash Map Counting

注意：

这十个模板不意味着需要记忆十套复杂算法。

应该说明：

LC-54 / 59 / 2326：
共享 Spiral Boundary。

LC-867 / 48：
共享 Coordinate Transformation。

LC-73 / 289 / 723：
共享 Original State 与 Update State 的分离思想，
但各自的更新机制不同。

LC-66 / 7 / 8 / 43：
共享 Digit Processing 基础，
但输出目标不同。

LC-3195 / 223：
共享矩形坐标分析，
但前者是离散格子计数，
后者是连续平面面积。

==================================================
十二、Pattern Recognition Guide
==================================================

请创建清晰简洁的判断指南。

Q1：
是否按指定顺序访问二维矩阵？
-> Matrix Traversal。

Q2：
是否顺时针一圈圈处理矩阵？
-> Spiral Boundary。

Q3：
是否需要改变矩阵元素的坐标？
-> Matrix Transformation。

Q4：
是否需要原地修改整个行或列？
-> In-place Marking。

Q5：
下一轮状态是否只能依赖旧状态？
-> Simultaneous State Update。

Q6：
是否需要模拟重力、消除、重新填充？
-> Multi-phase Matrix Simulation。

Q7：
是否需要逐位处理整数？
-> Digit Processing。

Q8：
是否需要模拟加法或乘法的进位？
-> Carry Propagation。

Q9：
是否需要计算很大的整数指数？
-> Fast Exponentiation。

Q10：
是否需要覆盖所有有效点的最小矩形？
-> Bounding Box。

Q11：
是否需要两个矩形的面积并集？
-> Rectangle Intersection + Inclusion-Exclusion。

Q12：
是否需要统计重复坐标组成的图形数量？
-> Coordinate Frequency Map。

必须说明：

这些是帮助识别问题的提示，
不是绝对互斥的分类。

==================================================
十三、边界测试与正确性
==================================================

本专题非常依赖边界条件。

对于新增题目，
必须设计并执行针对性的测试。

矩阵类至少考虑：

1. 单行
2. 单列
3. 1x1
4. 非正方形
5. 全部元素相同
6. 边界发生变化
7. 多次更新后的状态一致性
8. 符合题目约束的空输入情况

数值类至少考虑：

1. 0
2. 正数
3. 负数
4. Carry
5. Leading Zeros
6. 32-bit 边界
7. 负指数
8. 非常大的指数

几何类至少考虑：

1. 负坐标
2. 共享边界
3. 没有交集
4. 完全包含
5. 重复坐标
6. 零宽度或零高度
7. 无效正方形边长
8. 大量重复点的计数

具体测试必须遵守题目的输入约束。

不要为了测试而假设题目支持不存在的输入类型。

==================================================
十四、P0 / P1 / P2 优先级
==================================================

P0：
必须熟练掌握的核心代表题。

建议：

LC-0054 - Spiral Matrix
LC-0048 - Rotate Image
LC-0073 - Set Matrix Zeroes
LC-0066 - Plus One
LC-0050 - Pow(x, n)
LC-2013 - Detect Squares

P1：

LC-0059 - Spiral Matrix II
LC-0498 - Diagonal Traverse
LC-0867 - Transpose Matrix
LC-0008 - String to Integer (atoi)
LC-0007 - Reverse Integer
LC-0043 - Multiply Strings
LC-0289 - Game of Life
LC-0223 - Rectangle Area

P2：

LC-0885 - Spiral Matrix III
LC-2326 - Spiral Matrix IV
LC-0723 - Candy Crush
LC-3195 - Find the Minimum Area to Cover All Ones I

优先级仅表示当前学习路线中的价值。

不是声称某家公司有固定的面试出题概率。

允许第二轮独立审核调整，
但必须说明理由。

不要将所有题目都列为 P0。

根 README 必须包含：

A. P0 最小核心必练路线
B. P0 + P1 标准面试准备路线
C. P2 可选练习与存档

==================================================
十五、数量及完整性验收
==================================================

根据当前 tree：

原始目录数量：
18

原始文件数量：
58

原始不同题目：
13

其中：

12 道正式 LC 来源
1 道 NC-only

NC-only：
Detect Squares -> LC-2013

本次明确新增：
5 道。

若全部成功：

第一轮预计不同题目：
18 道。

Level 1 分布：

01：5 道
02：5 道
03：5 道
04：3 道

合计：
18 道。

第二轮独立审核：
最多自主新增 3 道。

如果其他专题已有完整题目，
并通过跨专题索引替代新建实体目录，
最终实体目录数可以少于 18。

不能为了凑题目数量而制造虚假文件。

必须验证：

1. 原始 13 道题都有明确的新归属。
2. 原始 58 个文件全部可追溯。
3. NC-Detect Squares 正式化正确。
4. 新增题号与官方题名一致。
5. Level 1 编号连续。
6. Level 2 编号连续。
7. Level 3 编号连续。
8. 原始 solution.py 全部保留。
9. 原始 PDF 全部保留。
10. 原始 note.md 全部保留。
11. LC-498 Draw.io 完整保留。
12. utils/ListNode.py 不被破坏。
13. 全部新题标准文件完整，
    或者明确记录生成失败。
14. README 相对链接有效。
15. 原始文件 SHA-256 校验成功。
16. 当前专题之外没有发生写入。
17. Git 原有未提交修改未被覆盖。
18. 第二轮审核结果得到记录。

如果无法完成某项验证，
必须在最终报告中明确说明。

==================================================
十六、最小核心学习路线
==================================================

请生成：

Math & Geometry Core Roadmap。

建议阶段：

阶段 A：
矩阵遍历

LC-54 -> LC-59 -> LC-498

阶段 B：
矩阵变换

LC-867 -> LC-48 -> LC-73

阶段 C：
数位与进位

LC-66 -> LC-7 -> LC-8 -> LC-43

阶段 D：
Fast Exponentiation

LC-50

阶段 E：
坐标几何

LC-3195 -> LC-223 -> LC-2013

阶段 F：
矩阵模拟进阶

LC-289 -> LC-723 -> LC-885 -> LC-2326

阶段 F 的多数题属于选修。

另外输出：

6–8 道最核心 Math & Geometry 面试题，
作为最高优先级复习路线。

优先覆盖不同算法不变量，
而不是挑选大量相似的矩阵模拟题。

==================================================
十七、实际执行流程
==================================================

请直接执行：

1. 检查当前目录。
2. 扫描完整 tree。
3. 检查 Git 状态。
4. 记录原始文件 Manifest。
5. 计算所有原始文件 SHA-256。
6. 检查 Symbolic Links。
7. 检查 utils/ListNode.py 引用。
8. 核对原始 13 道题的题号和代码。
9. 检查 NC Detect Squares。
10. 只读扫描全仓库跨专题重复。
11. 建立最终迁移映射。
12. 创建 4 个 Level 1。
13. 创建对应 Level 2。
14. 安全迁移原始题目。
15. 为所有 Level 3 重新编号。
16. 将 NC Detect Squares 正式化。
17. 保留完整 NC 原始资料。
18. 新增五道推荐题中真正缺失的题。
19. 进行第二轮独立审核。
20. 必要时新增最多三道重要题目。
21. 根据审核结果调整排序与编号。
22. 安全整理理论资源。
23. 创建根目录 README。
24. 创建每个 Level 1 README。
25. 创建 Pattern Recognition Guide。
26. 创建 Matrix Operations Cheat Sheet。
27. 创建 Arithmetic & Geometry Cheat Sheet。
28. 创建 P0 / P1 / P2 Roadmap。
29. 对新增 Python 代码进行语法检查。
30. 运行适当的边界测试。
31. 对比原始文件与迁移后的 SHA-256。
32. 检查 README 相对链接。
33. 检查所有目录编号。
34. 安全清理已经确认为空的旧目录。
35. 运行最终 tree。
36. 再次检查 Git 状态。
37. 输出完整验收报告。

最终报告必须包含：

- 完整最终 tree
- 4 个 Level 1 分类
- 所有 Level 2 Pattern
- 原有 13 道题目的迁移清单
- NC Detect Squares 正式化结果
- 第一轮新增的五道题
- Claude Code 第二轮自主新增的题
- 未新增候选及原因
- P0 / P1 / P2 数量
- 6–8 道核心面试学习路线
- 跨专题索引
- 原始文件哈希检查
- utils/ListNode.py 检查
- 新题边界测试结果
- Git 变更摘要
- 失败或未完成项目

如果某个局部操作存在数据损失风险，
保持原始文件不变并报告，
继续完成其他安全任务。

不要仅仅给出目录规划。

请在上述安全约束下直接执行
Math & Geometry 专题的完整重构。
PROMPT
)"
