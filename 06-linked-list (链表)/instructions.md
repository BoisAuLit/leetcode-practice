
cd '/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice/06-linked-list (链表)' && claude "$(cat <<'PROMPT'
请直接执行当前 Linked List（链表）LeetCode 学习目录的系统性重构。

我的目标是准备 Silicon Valley FAANG / Big Tech Software Engineer、AI Engineer 的算法面试和 Online Assessment（OA）。

请将当前目录建设为一套：
- 高面试价值
- 高算法迁移性
- 知识结构清晰
- 循序渐进
- 尽量减少机械记忆
- 可以长期复习和不断扩展

的 Linked List 学习体系。

你必须实际完成目录整理、新题生成、README 编写和完整性检查，而不是只提供计划。

==================================================
一、核心学习目标
==================================================

我不想记忆几十套独立的链表算法。

我希望理解少量核心 Pointer Manipulation Patterns，
并且通过不同题目熟练掌握这些模式。

重点包括：

1. Dummy Node（哑节点）
2. Iterative Reversal（迭代反转）
3. Local Pointer Rewiring（局部指针重连）
4. Fast/Slow Pointers（快慢指针）
5. Fixed-gap Pointers（固定间距指针）
6. Floyd Cycle Detection（环检测）
7. Head Switching（换头对齐）
8. Merge Two Sorted Lists（双路合并）
9. Merge K Sorted Lists（多路合并）
10. Linked List Merge Sort（链表归并排序）
11. Partition / Reorder（分区与重排）
12. Doubly Linked List（双向链表）
13. Hash Map + Linked List（哈希表与链表组合）
14. Random Pointer Cloning（随机指针深拷贝）
15. Linked List Design（链表数据结构设计）

特别强调：

同一道题可能使用多个 Pattern。

例如：

LC-143 Reorder List：

Find Middle
+ Reverse Second Half
+ Merge Alternately

应该按照主要教学目标归类，同时在 README 中注明它复用了哪些基础技巧。

不要将每种技巧的组合都视为一套独立算法。

==================================================
二、Level 1 -> Level N 文件夹规则
==================================================

本次推荐使用：

Level 1：算法家族
Level 2：具体 Pattern
Level 3：具体 LeetCode 题目

只有确实需要进一步细分时才使用 Level 4。

不追求层级越深越好。

所有同级目录使用连续编号：

01 - ...
02 - ...
03 - ...

编号代表：

1. 学习依赖关系
2. 面试重要程度
3. 核心算法的代表性
4. 难度递进
5. Pattern 的迁移价值

绝不按照 LeetCode 题号机械排序。

Level 3 命名格式：

01 - LC-0206 - Reverse Linked List
02 - LC-0092 - Reverse Linked List II

每个 Level 2 内部独立从 01 开始编号。

已有 NC 版本归档到对应 LC 题目目录的 _neetcode/。

_resources、utils、_neetcode 等资源或代码辅助目录不参与算法层级编号。

==================================================
三、正式 Level 1 / Level 2 / Level 3 结构
==================================================

以下是第一轮推荐的完整目标结构。

原则上建立 7 个 Level 1。

--------------------------------------------------
LEVEL 1
01 - 基础指针、Dummy Node 与反转
--------------------------------------------------

核心：

Linked List Traversal
Dummy Head
Pointer Rewiring
In-place Reversal

Level 2：
01 - 链表反转与局部节点交换

Level 3：

01 - LC-0206 - Reverse Linked List
02 - LC-0092 - Reverse Linked List II
03 - LC-0024 - Swap Nodes in Pairs

教学重点：

LC-206：
最经典的链表反转。

重点掌握：

prev
curr
next_node

不变量：
prev 指向已经完成反转的链表头，
curr 指向尚未处理部分的首节点。

每一步必须先保存 curr.next，
再修改 curr.next。

理解为什么 O(n) 时间、O(1) 额外空间。

LC-92：
局部区间反转。

重点掌握：
- 定位反转区间前一个节点
- 保存区间尾部的后继
- 反转局部链表
- 重新连接前后两部分

可以使用 Dummy Node 简化头节点变化。

LC-24：
相邻两个节点交换。

必须真正交换节点连接关系，
不能仅仅交换节点的 val。

解释每一次交换中的：
- prev
- first
- second
- next_pair

与 LC-206 对照，理解局部 Rewiring。

--------------------------------------------------

Level 2：
02 - Dummy Node 与链表删除

Level 3：

01 - LC-0203 - Remove Linked List Elements
02 - LC-0083 - Remove Duplicates from Sorted List
03 - LC-0082 - Remove Duplicates from Sorted List II

教学重点：

LC-203：
Dummy Head + Deletion。
使用 prev.next 跳过待删除节点。

LC-83：
有序链表去重，但每个重复值保留一个。

LC-82：
有序链表去重，所有出现重复的值都必须彻底删除。

重点解释：

LC-83 与 LC-82 的删除语义不同。

特别注意 LC-82：
连续重复值可能出现在链表头部。
Dummy Node 可以避免复杂的特殊情况。

LC-83 是基础训练，标记 P2。
LC-82 更有区分度，标记 P1。

--------------------------------------------------

Level 2：
03 - 链表逐位计算与进位

Level 3：

01 - LC-0002 - Add Two Numbers

教学重点：

逐个节点处理数字。
维护 carry。
使用 Dummy Node 构建结果链表。

理解：

digit = total % 10
carry = total // 10

注意两个链表长度不同，以及最后仍有 carry 的情况。

这是一道高价值的链表模拟题。

==================================================
LEVEL 1
02 - 双指针、固定间距与链表中点
==================================================

核心：

Fast/Slow Pointers
Fixed Distance
Head Switching
Middle + Reversal

--------------------------------------------------

Level 2：
01 - 寻找中点与固定指针间距

Level 3：

01 - LC-0876 - Middle of the Linked List
02 - LC-0019 - Remove Nth Node From End of List
03 - LC-2095 - Delete the Middle Node of a Linked List

教学重点：

LC-876：
slow 每次一步。
fast 每次两步。

理解：
- 奇数长度
- 偶数长度
- 何时返回第二个中间节点

LC-19：
两个指针相距 n 个节点。
当 fast 到达末尾，slow 定位删除位置附近。

推荐使用 Dummy Node。

必须解释：
- 为什么需要 n 的固定间距
- 单节点删除
- 删除头节点
- n 等于链表长度

LC-2095：
先定位中点，再删除。

属于中点技巧的延伸，
标记 P2，不需要额外记忆新模板。

--------------------------------------------------

Level 2：
02 - 双指针换头与长度对齐

Level 3：

01 - LC-0160 - Intersection of Two Linked Lists

教学重点：

Pointer Switching（指针换头）。

两个指针分别从 headA、headB 出发。

到达末尾时切换到另一条链表的头部。

利用：
lengthA + lengthB
和
lengthB + lengthA

消除长度差异。

必须解释：

- 为什么两个指针最终能够相遇
- 没有交点时为什么都会到达 None
- 比较的是 Node Identity，不是 Node Value

特别说明：

此题虽然使用两个指针，
但不是典型的 fast/slow 速度不同的算法。

不要把它和 Floyd Cycle Detection 混为一谈。

--------------------------------------------------

Level 2：
03 - 中点、反转与双端重组

Level 3：

01 - LC-0234 - Palindrome Linked List
02 - LC-0143 - Reorder List
03 - LC-2130 - Maximum Twin Sum of a Linked List

教学重点：

共同模式：

1. Find Middle
2. Reverse Second Half
3. Process Both Halves

LC-234：
从两端向中间比较。
链表不支持随机访问，
因此通过反转后半段实现双端比较。

说明是否需要恢复原链表，以及恢复操作的额外成本。

LC-143：
找到中点。
断开并反转后半段。
将两个链表交替拼接。

重点防止：
- 节点丢失
- 形成意外的环
- 奇数长度的尾节点连接错误

LC-2130：
前后对应节点形成 Twin Pair。
寻找最大 Twin Sum。

可以复用：
Find Middle + Reverse + Pairwise Scan。

这三道题不需要记忆三套完全不同的基础算法。

==================================================
LEVEL 1
03 - Floyd 环检测与隐式函数图
==================================================

核心：

Floyd's Tortoise and Hare
Cycle Detection
Cycle Entry
Functional Graph

--------------------------------------------------

Level 2：
01 - 链表环检测与环入口

Level 3：

01 - LC-0141 - Linked List Cycle
02 - LC-0142 - Linked List Cycle II

教学重点：

LC-141：
slow 走一步，fast 走两步。
有环时两个指针必定相遇。

LC-142：
找到相遇点后，
再使用一个从 head 出发的指针，
两个指针都每次走一步，
最终找到环入口。

必须提供：

- 环长与速度差解释
- 为什么会相遇
- 为什么第二阶段能找到环入口
- 没有环时的正确终止条件

重点说明：

Floyd Cycle Detection 与 Floyd-Warshall
是完全不同的算法。

--------------------------------------------------

Level 2：
02 - 隐式函数图与环检测

Level 3：

01 - LC-0202 - Happy Number
02 - LC-0287 - Find the Duplicate Number
03 - LC-0457 - Circular Array Loop

教学重点：

LC-202：
将每个整数视为状态。
下一个状态由数位平方和函数决定。

反复应用确定性函数会形成状态转移序列。

可以使用 Floyd 检测循环。

LC-287：
将数组视为函数图：

next(i) = nums[i]

在题目约束下使用 Floyd 找到环入口，
对应重复数字。

注意：
不能修改原数组。
正确实现应符合 O(n) 时间、O(1) 额外空间。

本题也可能存在于 Arrays & Hashing 专题。
保留当前完整题目资料，
并建立跨专题索引。

LC-457：
Circular Array Loop。
属于环检测的复杂应用。

必须正确处理：
- 方向一致
- 环长度大于 1
- 下标取模
- 正负移动
- 自环排除

标记 P2。

不要要求我为 LC-457 额外记忆一套特殊模板。

==================================================
LEVEL 1
04 - 链表归并与排序
==================================================

核心：

Merge Two Lists
Merge K Lists
Min-Heap
Divide and Conquer
Merge Sort

--------------------------------------------------

Level 2：
01 - 两条有序链表归并

Level 3：

01 - LC-0021 - Merge Two Sorted Lists

教学重点：

Dummy Node + Tail Pointer。

每次比较两个链表的当前节点，
将较小节点连接到结果链表尾部。

最后连接剩余部分。

这是 Linked List 的核心基础题。

必须熟练理解：

tail.next = selected_node
tail = tail.next

--------------------------------------------------

Level 2：
02 - K 条有序链表归并

Level 3：

01 - LC-0023 - Merge k Sorted Lists

教学重点：

优先提供 Min-Heap 版本。

理解：
- Heap 存储每条链表的当前头节点
- 每次弹出最小节点
- 将弹出节点的 next 加入 Heap
- 维护结果链表的尾部

目标复杂度：

O(N log k)

N 是所有链表的节点总数。

Python 实现中：
如果 ListNode 不支持比较，
Heap Tuple 需要合适的 Tie-breaker，
不能在权重相同时错误地比较 ListNode 对象。

还要简要说明：
Divide and Conquer 两两归并也可达到
O(N log k)。

但不要求同时背诵多种实现。

--------------------------------------------------

Level 2：
03 - 链表归并排序

Level 3：

01 - LC-0148 - Sort List

教学重点：

Merge Sort（归并排序）。

1. 使用 Fast/Slow 找到中点。
2. 切断链表。
3. 分别排序左右两半。
4. 使用 LC-21 的归并思想合并。

必须解释递归终止条件。

注意复杂度：

时间 O(n log n)。

递归版本通常需要 O(log n) 调用栈空间，
不能直接声称它满足严格 O(1) 额外空间。

若需要 O(1) 辅助空间，可介绍迭代 Bottom-up Merge Sort。

但不要要求为面试初级阶段额外背诵两套排序代码。

==================================================
LEVEL 1
05 - 链表分区、重排与分段操作
==================================================

核心：

Stable Partition
Pointer Rewiring
Group Reversal
Rotation

--------------------------------------------------

Level 2：
01 - 稳定分区与交错重排

Level 3：

01 - LC-0086 - Partition List
02 - LC-0328 - Odd Even Linked List

教学重点：

LC-86：
建立两条链表。

small_dummy
large_dummy

将小于 x 和大于等于 x 的节点分别连接。

最后拼接两条链表。

必须保持两组内部原始顺序。

LC-328：
将奇数位置和偶数位置节点分别串联。
最后连接两个分组。

注意：
Odd / Even 指的是节点位置，
不是节点值的奇偶性。

两题都体现：
拆分链表 -> 分别维护 Tail -> 最后连接。

--------------------------------------------------

Level 2：
02 - K 个节点为一组的反转

Level 3：

01 - LC-0025 - Reverse Nodes in k-Group

教学重点：

这是 LC-206 和 LC-92 的高级组合。

1. 确认剩余节点数量不少于 k。
2. 保存当前分组边界。
3. 反转 k 个节点。
4. 连接上一组与下一组。
5. 处理不足 k 个的尾部。

重点学习：

group_prev
kth
group_next
prev
curr

必须说明每个变量的作用。

理解正确性后再学习代码。

不要靠机械记忆复杂指针赋值顺序来解题。

--------------------------------------------------

Level 2：
03 - 链表旋转与环形连接

Level 3：

01 - LC-0061 - Rotate List

教学重点：

计算链表长度。
使用 k % n 处理循环旋转。
临时形成环，再找到新的尾节点并断开。

这不是普通 Floyd Cycle Detection。

关键是利用链表长度定位新头和新尾。

==================================================
LEVEL 1
06 - 复杂指针与链表数据结构设计
==================================================

核心：

Singly Linked List Design
Doubly Linked List
Hash Map + DLL
Random Pointer
Multilevel Linked List

--------------------------------------------------

Level 2：
01 - 基础链表设计

Level 3：

01 - LC-0707 - Design Linked List

教学重点：

实现：

get
addAtHead
addAtTail
addAtIndex
deleteAtIndex

理解：
- Head
- Tail
- Size
- Sentinel Node
- 指针边界
- 空链表操作

可以使用单链表完成。
也可以对比双链表实现。

优先选易于理解的标准版本。

--------------------------------------------------

Level 2：
02 - LRU Cache 与双向链表

Level 3：

01 - LC-0146 - LRU Cache

当前已有：

NC - LRU Cache

必须核对对应关系，
建立正式 LC-0146 目录，
并将 NC 原始文件完整保留在 _neetcode/。

教学重点：

Hash Map + Doubly Linked List。

Hash Map：
key -> node

Doubly Linked List：
维护 Recently Used Order。

必须理解：
- get 时如何移动节点
- put 时如何插入或更新
- 如何淘汰 Least Recently Used 节点
- 为什么需要 prev 和 next
- 为什么使用 Head / Tail Sentinels
- 为什么每次操作平均 O(1)

这是整个链表专题最重要的数据结构设计题之一。

优先提供清晰、易复述的 Python 实现。

不要只给 OrderedDict 的简化版本。
可以在笔记中将 OrderedDict 作为对照。

--------------------------------------------------

Level 2：
03 - Random Pointer 与深拷贝

Level 3：

01 - LC-0138 - Copy List with Random Pointer

教学重点：

节点有：
next
random

Deep Copy 不能让新链表的指针指向原节点。

优先提供：

Hash Map:
original_node -> copied_node

完成两阶段 Deep Copy。

同时可以简要解释：
Interleaving Nodes 的 O(1) 额外空间方法。

不要求同时背诵两套代码。

重点理解 Node Identity 与 Node Value 的区别。

--------------------------------------------------

Level 2：
04 - 多级双向链表展开

Level 3：

01 - LC-0430 - Flatten a Multilevel Doubly Linked List

当前已有独立代码：

doubly-linked-list/
02 - Flatten ML Doubly Linked List.py

这是重要的既有学习成果。

请先检查这份代码是否确实对应 LC-430。

如果符合：
- 建立正式 LC-0430 题目目录。
- 保留原始代码文件。
- 使用现有生成工具补齐标准文件。
- 可以参考旧代码编写正式 solution.py，
  但不能覆盖或丢弃原始代码。

教学重点：

Doubly Linked List + Nested Structure。

涉及：
prev
next
child

可以使用 DFS / Stack。

必须保证：
- 前后指针正确连接
- child 指针被清空
- 原始后续节点不会丢失
- 多层嵌套顺序正确

标记 P1。

==================================================
LEVEL 1
07 - 低优先级与跨专题存档
==================================================

这个分类保留原有学习资料，
但不要求将每道题都作为核心面试题反复练习。

--------------------------------------------------

Level 2：
01 - 其他链表设计与特殊结构

Level 3：

01 - LC-0353 - Design Snake Game
02 - LC-0708 - Insert into a Sorted Circular Linked List
03 - LC-1721 - Swapping Nodes in a Linked List

说明：

LC-353：
更偏向 Queue / Deque + Hash Set + Simulation。
不属于链表的核心指针操作题。

LC-708：
特殊循环有序链表插入。
涉及跨越最大值与最小值的边界。

LC-1721：
标准题意允许交换节点的值，
不要求真正重新连接两个节点。

不要把它误教成必须进行复杂 Pointer Rewiring。

以上保留原文件，标记 P2。

--------------------------------------------------

Level 2：
02 - 跨专题结构与状态循环

Level 3：

01 - LC-0109 - Convert Sorted List to Binary Search Tree
02 - LC-0957 - Prison Cells After N Days

说明：

LC-109：
Linked List + Binary Tree + Divide and Conquer。
与 Tree Construction 专题有很强关联。

LC-957：
Finite-state Cycle Detection / State Simulation。

它可能使用 Hash Map 检测重复状态，
也可以讨论 Floyd Cycle Detection 的适用性。

但是它不是普通链表环检测题。
不要强行套用 LC-141 的代码。

这两题标记 P2。
保留已有解法及所有资料。

==================================================
四、明确建议新增的题目
==================================================

第一轮新增 6 道不同题目：

LC-0092 - Reverse Linked List II
LC-0024 - Swap Nodes in Pairs
LC-0086 - Partition List
LC-0082 - Remove Duplicates from Sorted List II
LC-0083 - Remove Duplicates from Sorted List
LC-0430 - Flatten a Multilevel Doubly Linked List

其中：

LC-430 已经有独立 Python 代码，
但尚未建立完整的 LeetCode 题目目录。

另外：

NC - LRU Cache
需要升级整理为正式 LC-0146 目录。

LC-146 已经有 NC 学习资料，
所以不算全新的独立题目。

对于每一道题：

1. 先检查本专题。
2. 再检查整个仓库。
3. 验证 LeetCode 题号和英文题名。
4. 如本专题已有正式版本，复用原文件。
5. 如其他专题已有，优先评估跨专题引用。
6. 如确实缺失，使用现有题目生成工具创建。

标准文件：

metadata.json
problem.pdf
problem_dark.pdf
solution.py

你已经具备根据 LeetCode 题号生成完整题目文件的能力，
直接复用即可。

禁止创建空 PDF 或伪造 metadata。

已有 solution.py 和自定义附件不得被覆盖。

==================================================
五、NC / LC 重复题目处理
==================================================

当前存在以下 NeetCode 题目：

NC - LRU Cache
NC - Merge K Sorted Linked Lists
NC - Add Two Numbers
NC - Copy Linked List with Random Pointer
NC - Merge Two Sorted Linked Lists
NC - Remove Nth Node From End of List
NC - Reverse Linked List
NC - Reverse Nodes in K-Group

对应：

LC-0146
LC-0023
LC-0002
LC-0138
LC-0021
LC-0019
LC-0206
LC-0025

请逐一检查题面与代码是否真正对应。

确认对应后：

1. 使用标准 LC Level 3 目录。
2. 原 NC 文件全部归档到 _neetcode/。
3. 不覆盖已有 LC solution.py。
4. 不覆盖 NC solution.py。
5. 保留两套 PDF 和 metadata。
6. 保留所有旧笔记、图片、注释。
7. 如果解法不同，在 README 中简要对比。
8. 同一道题只占据一个正式 Level 3 位置。

对于 LC-146：
当前只有 NC 来源，先生成正确的正式 LC 文件，
不能直接把 NC metadata 冒充为 LeetCode 官方 metadata。

==================================================
六、Claude Code 第二轮独立审核
==================================================

以上是 ChatGPT 的第一轮推荐。

你必须独立审核整个 Linked List 学习体系，
确认是否仍缺少高价值面试题和重要 Pattern。

参考：

NeetCode 150
NeetCode 250
Blind 75
Grind 75 / Grind 169
LeetCode Top Interview 150
其他可靠的经典算法面试题单

如果有网络访问，请核对题号、题名、难度、
题目约束和主流解法。

不要编造 FAANG 内部实际出题频率。

重点审核是否覆盖：

1. Reverse Entire List
2. Reverse Sublist
3. Reverse K-group
4. Swap Adjacent Nodes
5. Dummy Node
6. Delete Node
7. Fixed-gap Two Pointers
8. Find Middle
9. Fast/Slow Cycle Detection
10. Find Cycle Entrance
11. Functional Graph
12. Intersection via Head Switching
13. Merge Two Sorted Lists
14. Merge K Sorted Lists
15. Linked List Merge Sort
16. Reorder List
17. Palindrome Linked List
18. Stable Partition
19. Random Pointer Deep Copy
20. Doubly Linked List
21. LRU Cache
22. Linked List Design
23. Cyclic Linked List
24. Carry Propagation

额外审核候选：

LC-0445 - Add Two Numbers II
LC-0725 - Split Linked List in Parts
LC-0382 - Linked List Random Node
LC-1472 - Design Browser History
LC-0432 - All O`one Data Structure
LC-0460 - LFU Cache

这些只是候选，不要求全部新增。

特别注意：

LC-445 涉及 Stack / Reverse 的迁移。
LC-382 涉及 Reservoir Sampling。
LC-460 涉及更加复杂的数据结构设计。

这些题目不一定适合当前核心链表必刷路线。

只有同时满足以下条件，才允许自主新增：

A. 具有明确的面试代表性。
B. 具有独立的教学价值。
C. 弥补现有知识体系缺口。
D. 不只是现有题目的重复训练。
E. 能清楚说明新增后的收益。
F. 不明显增加不必要的记忆负担。

第二轮建议最多新增 5 道。

若确有超过 5 道值得学习，
请新增最重要的 5 道，
其余放入 README 的 Future Candidates。

如果没有真正重要的遗漏，
可以不新增任何题目。

允许在确有必要时增加 Level 1、Level 2 或 Level 4，
但必须有清晰的教学依据。

==================================================
七、资源、模板与代码保护
==================================================

当前存在：

docs/
  00 - Linked List Problems Summary.pdf

doubly-linked-list/
  00 - Double Linked List Insertion.pdf
  01 - Linked List VS array.pdf
  02 - Flatten ML Doubly Linked List.py

Floyd's Cycle Detection Algorithm/
  template_hasCycle_&_cycleStart.py

utils/
  ListNode.py

请妥善处理这些非题目资料。

建议：

_resources/
  docs/
  doubly-linked-list/
  templates/

其中：

- PDF 理论资料移动到 _resources。
- Floyd 模板移动到 _resources/templates。
- LC-430 原始代码保留在正式题目内部的
  _original_sources/ 或其他明确的来源目录。

对于 utils/ListNode.py：

先检查现有 solution.py 是否有导入依赖。

如果移动会破坏相对路径或运行环境，
允许保留当前根目录 utils/ 不变。

不要为了目录外观强行移动基础工具代码。

不允许修改其他专题的 ListNode 定义。

原有理论资料和模板绝不能丢失。

==================================================
八、完整文件保护与 Git 安全
==================================================

当前 Git 工作区包含大量未提交修改和未跟踪文件。

操作必须非常谨慎。

执行前必须：

1. pwd
2. tree
3. git status --short
4. 扫描全部已有文件
5. 记录所有原始文件相对路径
6. 为普通文件记录 SHA-256
7. 检查是否存在符号链接
8. 检查旧目录到新目录的迁移映射
9. 检查重名冲突
10. 确认所有待移动的题目内容

特别注意：

LC-0142 当前可能缺少标准 PDF，
但存在 problem.jpg。

必须保留 problem.jpg，
再补齐缺少的标准文件。

LC-0160：
保留现有 PDF 和 PNG 附件。

LC-0025：
保留额外讲解 PDF。

LC-0138：
保留额外讲解 PDF。

LC-0206：
保留 Reverse Linked List 的讲解 PDF。

LC-0328：
保留图片和 note.md。

LC-0202：
保留 note.md。

LC-0457：
保留 asset-explanation.jpg。

其他所有非标准附件同样必须完整保留。

严禁：

git reset
git clean
git restore .
git checkout -- .
rm -rf
强制覆盖文件
删除未跟踪文件
覆盖已有 solution.py
覆盖原有笔记
删除原始学习资料

不要自动：

git add
git commit
git push

只允许在当前：

06-linked-list (链表)

目录内进行写入、移动和删除空目录。

可以只读扫描整个仓库，
用于发现跨专题重复题目。

如果目标文件已存在：

- 内容相同：安全归档并记录来源。
- 内容不同：两个版本全部保留。
- 使用 _conflicts/ 保存必要的冲突文件。
- 在最终报告中说明。

优先使用安全的文件系统 rename。
避免改动 Git 暂存区。

确保重构过程尽量满足 Idempotence（幂等性）：
重复执行不会导致文件重复、编号叠加或内容丢失。

==================================================
九、建立高质量 README 学习体系
==================================================

必须创建：

A. 根目录 README.md
B. 每个 Level 1 的 README.md
C. 对复杂 Level 2 创建必要的短 README.md

根目录 README 包含：

1. Linked List 完整知识地图
2. 所有 Level 1 / Level 2 分类
3. 所有题目的学习顺序
4. P0 / P1 / P2 优先级
5. 核心指针操作模板
6. 每种 Pattern 的 Loop Invariant
7. 时间和空间复杂度
8. 常见边界情况
9. 跨专题索引
10. 第二轮独立审核结果
11. 新增题目的理由
12. 不需要额外记忆的重复题目

特别为以下核心模式提供 Python 模板：

Template 1:
Dummy Node + Delete / Insert

Template 2:
Reverse Linked List

Template 3:
Fast/Slow Pointers

Template 4:
Fixed-gap Two Pointers

Template 5:
Floyd Cycle Detection

Template 6:
Merge Two Sorted Lists

Template 7:
Merge K Sorted Lists

Template 8:
Reverse Sublist / K-group

Template 9:
Doubly Linked List + Hash Map

注意：

这些是知识模式，不代表必须记住九套互不相关的代码。

重点解释模板之间如何复用。

每个 Level 1 README：

- Pattern 定义
- 1–3 个决定性观察
- Pointer Invariant（指针不变量）
- 为什么指针可以安全移动
- 简短正确性证明
- 代表代码模板
- 典型题目
- 常见错误
- Pattern Recognition 提示

特别讲清楚：

1. 修改 curr.next 前，什么时候必须先保存 next？
2. Dummy Node 如何统一删除头节点的情况？
3. 什么时候需要断开链表，防止形成环？
4. Fast/Slow 和 Fixed-gap 的本质区别是什么？
5. 为什么两个指针换头后能够消除长度差？
6. 为什么 Floyd 可以检测隐式函数图的环？
7. 为什么 Min-Heap 能完成 K 路合并？
8. 为什么 LRU 需要 Hash Map + Doubly Linked List？
9. 什么时候修改 Node.val 与修改 Node.next 的区别会影响正确性？

语言要求：

中文主导 + 英文专业术语。

例如：

Dummy Node（哑节点）
Pointer Rewiring（指针重连）
Fast/Slow Pointers（快慢指针）
Cycle Entry（环入口）
Deep Copy（深拷贝）
Amortized Complexity（摊还复杂度）

避免冗长、重复、空泛的理论描述。

==================================================
十、P0 / P1 / P2 优先级
==================================================

P0：核心必练。
P1：重要补充与变体。
P2：低优先级、重复训练或跨专题。

以下优先标记 P0：

LC-0206 - Reverse Linked List
LC-0092 - Reverse Linked List II
LC-0021 - Merge Two Sorted Lists
LC-0019 - Remove Nth Node From End of List
LC-0876 - Middle of the Linked List
LC-0141 - Linked List Cycle
LC-0142 - Linked List Cycle II
LC-0143 - Reorder List
LC-0234 - Palindrome Linked List
LC-0002 - Add Two Numbers
LC-0138 - Copy List with Random Pointer
LC-0023 - Merge k Sorted Lists
LC-0025 - Reverse Nodes in k-Group
LC-0146 - LRU Cache

以下可优先考虑 P1：

LC-0024
LC-0082
LC-0086
LC-0160
LC-0287
LC-0328
LC-0148
LC-0707
LC-0430
LC-0202
LC-0061
LC-2130

以下建议 P2：

LC-0083
LC-2095
LC-1721
LC-0109
LC-0457
LC-0957
LC-0353
LC-0708

允许根据独立审核结果调整，但必须解释理由。

不要把所有题目都标记 P0。

README 必须包含：

1. P0 核心必练路线
2. P0 + P1 标准面试路线
3. P2 进阶与存档路线

同时区分：

- 必须理解的核心 Pattern
- 值得独立完成的代表题
- 只需复用已有模板的练习题
- 不值得长期单独背诵的特殊技巧

==================================================
十一、跨专题去重
==================================================

允许只读扫描整个 leetcode-practice 仓库。

重点检查：

LC-0287：
可能已存在于 Arrays & Hashing。

LC-0141、LC-0142、LC-0019：
可能已被 Two Pointers 专题索引。

LC-0957：
可能存在于 Simulation / Cycle Detection。

LC-0109：
可能存在于 Trees。

LC-0353：
可能存在于 Queue / Design。

以及本次新增候选。

规则：

如果本专题已有完整原始题目：
必须保留原始资料，不因外部重复而删除。

如果本专题没有该题，
但其他专题已有：
优先通过 README 建立相对路径引用。

不得修改其他专题的文件。

对于同一道题：
清楚标注 Primary Pattern 和 Secondary Patterns。

目标是减少重复记忆，而不是强行保证仓库中每个题号只出现一次。

==================================================
十二、数量与完整性验收
==================================================

根据当前 tree 初步统计：

原有题目来源文件夹约 36 个。

其中有 7 组已有 LC / NC 双版本，
另有 NC - LRU Cache 只有 NC 来源。

统一题目身份后：
当前约有 29 道不同题目。

第一轮新增不同题目：
6 道。

目标约为：
35 道不同题目。

其中：
LC-146 属于已有 NC 题的正式化整理，
不能重复计算为一门新题。

LC-430 虽然已有独立 Python 代码，
但尚未具有正式 LeetCode 题目目录。

第一轮预期的 Level 1 分布：

01：7 道
02：7 道
03：5 道
04：3 道
05：4 道
06：4 道
07：5 道

合计：35 道。

以实际审计结果为准。

如果第二轮增加了题目，
最终数量可以增加。

如果发现跨专题题只需要索引，
实体题目文件夹数可以适当减少。

绝不能为了凑齐 35 道题而生成假文件。

必须验证：

- 所有旧题都迁移到正确位置。
- 所有旧文件都被完整保留。
- NC 原始版本没有丢失。
- LC-142 缺失文件得到检查和补齐。
- LC-430 旧脚本被完整保留。
- utils/ListNode.py 不受破坏。
- 所有新题的 metadata 正确。
- 所有新题的 PDF 正确。
- 所有新题 solution.py 对应题号。
- Level 1 编号连续。
- Level 2 编号连续。
- Level 3 编号连续。
- 所有 README 路径真实有效。
- 不存在不必要的重复题目文件夹。
- 旧文件的 SHA-256 校验通过。
- 当前专题外的文件没有被修改。
- Git 中未提交内容没有被覆盖。

==================================================
十三、实际执行顺序
==================================================

请按以下步骤实际执行：

1. pwd
2. 扫描 tree
3. 检查 Git 状态
4. 建立原始文件及 SHA-256 清单
5. 检查跨专题重复题
6. 核对现有题目编号与解法
7. 设计最终迁移映射
8. 建立 7 个 Level 1
9. 建立对应 Level 2
10. 安全迁移已有题目
11. 整理 NC / LC 重复版本
12. 为所有 Level 3 重新编号
13. 正式整理 LC-146
14. 正式整理 LC-430
15. 新增明确推荐的缺失题目
16. 补齐已有题目缺失的标准文件
17. 进行 Claude Code 第二轮独立审核
18. 新增少量真正必要的题目
19. 根据新增结果调整排序与编号
20. 安全整理理论资料与模板
21. 生成根目录与各 Level 1 README
22. 检查所有文件及引用完整性
23. 对比迁移前后的文件哈希
24. 检查目录编号连续性
25. 清理确认已空的遗留目录
26. 运行最终 tree
27. 再次检查 Git 状态
28. 输出完整验收报告

最终报告必须包含：

- 完整最终 tree
- Level 1 / Level 2 分类及学习目标
- 所有旧题目的迁移结果
- ChatGPT 第一轮推荐的新增题
- Claude Code 第二轮自主新增的题
- 未新增但值得考虑的候选题
- NC / LC 版本归档结果
- LC-146 正式化结果
- LC-430 旧代码迁移结果
- 跨专题索引
- P0 / P1 / P2 数量
- 原始文件保留和哈希验证结果
- Git 变更摘要
- 失败或未完成步骤
- 最终推荐复习顺序

请不要只输出目录重构方案。

请在上述安全限制内直接执行完整任务。
PROMPT
)"
