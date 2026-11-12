# 06 · Linked List（链表）

> 链表题几乎没有「算法」，全是**指针操作的组合**。
> 掌握 6 个基础动作（Dummy、反转、快慢、固定间距、拆分重接、哈希映射），
> 剩下的题都是它们的拼装。**不要把每种拼装当成一道新算法去背。**

本专题共 **32 道题** + 1 条跨专题索引，7 个 Level 1。

## 一、知识地图

| Level 1 | 主题 | 题数 | README |
|---|---|---|---|
| 01 | 基础指针、Dummy Node 与反转 | 7 | [→](<01 - 基础指针、Dummy Node 与反转/README.md>) |
| 02 | 双指针、固定间距与链表中点 | 7 | [→](<02 - 双指针、固定间距与链表中点/README.md>) |
| 03 | Floyd 环检测与隐式函数图 | 4 | [→](<03 - Floyd 环检测与隐式函数图/README.md>) |
| 04 | 链表归并与排序 | 3 | [→](<04 - 链表归并与排序/README.md>) |
| 05 | 链表分区、重排与分段操作 | 5 | [→](<05 - 链表分区、重排与分段操作/README.md>) |
| 06 | 复杂指针与链表数据结构设计 | 3 + 1 索引 | [→](<06 - 复杂指针与链表数据结构设计/README.md>) |
| 07 | 低优先级与跨专题存档 | 5 | [→](<07 - 低优先级与跨专题存档/README.md>) |

```
01 - 基础指针、Dummy Node 与反转/
  01 - 链表反转与局部节点交换/  01 LC-0206  02 LC-0092←新  03 LC-0024←新
  02 - Dummy Node 与链表删除/   01 LC-0203  02 LC-0083←新  03 LC-0082←新
  03 - 链表逐位计算与进位/      01 LC-0002  02 LC-0445←新₂
02 - 双指针、固定间距与链表中点/
  01 - 寻找中点与固定指针间距/  01 LC-0876  02 LC-0019  03 LC-2095
  02 - 双指针换头与长度对齐/    01 LC-0160
  03 - 中点、反转与双端重组/    01 LC-0234  02 LC-0143  03 LC-2130
03 - Floyd 环检测与隐式函数图/
  01 - 链表环检测与环入口/      01 LC-0141  02 LC-0142
  02 - 隐式函数图与环检测/      01 LC-0202  02 LC-0457   （LC-0287 跨专题索引）
04 - 链表归并与排序/
  01 - 两条有序链表归并/        01 LC-0021
  02 - K 条有序链表归并/        01 LC-0023
  03 - 链表归并排序/            01 LC-0148
05 - 链表分区、重排与分段操作/
  01 - 稳定分区与交错重排/      01 LC-0086←新  02 LC-0328
  02 - K 个节点为一组的反转/    01 LC-0025
  03 - 链表旋转与分段拆分/      01 LC-0061  02 LC-0725←新₂
06 - 复杂指针与链表数据结构设计/
  01 - 基础链表设计/            01 LC-0707
  02 - LRU Cache 与双向链表/    → 跨专题索引（LC-0146 实体目录在 17-design）
  03 - Random Pointer 与深拷贝/ 01 LC-0138
  04 - 多级双向链表展开/        01 LC-0430←新（含 _original_sources/ 原始代码）
07 - 低优先级与跨专题存档/
  01 - 其他链表设计与特殊结构/  01 LC-0353  02 LC-0708  03 LC-1721
  02 - 跨专题结构与状态循环/    01 LC-0109  02 LC-0957
_resources/  docs/  doubly-linked-list/  templates/  utils/（ListNode 工具类）
```

---

## 二、6 个基础动作（所有题都是它们的组合）

**① Dummy Node（哑节点）—— 什么时候必须用**
> **只要头节点可能被删除或替换，就用 dummy。**

| 题 | 需要 dummy 吗 | 为什么 |
|---|---|---|
| LC-0083 | 不需要 | 头节点永远是它那组的第一个，一定保留 |
| LC-0082 | **需要** | `1->1->2` 的头会被删掉 |
| LC-0019 | **需要** | 可能删的就是头节点 |
| LC-0024 / 0025 / 0092 | **需要** | 头节点会被换走 |
| LC-0086 / 0328 | **需要**（两个） | 两条子链各要一个 |

**② In-place Reversal（原地反转）**
```python
prev, curr = None, head
while curr:
    nxt = curr.next      # 必须先存，再改 curr.next
    curr.next = prev
    prev, curr = curr, nxt
return prev
```
不变量：`prev` 是已反转部分的头，`curr` 是待处理部分的首节点。O(n)/O(1)。
复用：206 → 092（局部）→ 025（分组）→ 234/143/2130（反转后半段）。

**③ Fast / Slow（快慢指针）—— 找中点**
```python
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
# 偶数长度时 slow 停在「第二个中点」
```
想停在**第一个**中点：循环条件改成 `while fast.next and fast.next.next`。
**这两种停法要分清**：143 Reorder 要前半段短一点，148 Sort 要能切成两半。

**④ Fixed-gap（固定间距）—— 倒数第 n 个**
```python
fast = dummy
for _ in range(n): fast = fast.next
slow = dummy
while fast.next:
    slow, fast = slow.next, fast.next
slow.next = slow.next.next    # slow 恰好停在待删节点的前驱
```

**⑤ 拆分 + 重接（两条子链各带 tail）**
```python
d1 = t1 = ListNode(); d2 = t2 = ListNode()
for node in 原链:
    if 条件: t1.next = node; t1 = node
    else:    t2.next = node; t2 = node
t2.next = None          # ★ 必须切断，否则成环
t1.next = d2.next
```
复用：086、328、725。**忘记 `t2.next = None` 是这类题的头号 bug。**

**⑥ Hash Map + 链表**
`key -> node` 让「按 key 定位」变成 O(1)；链表负责维护顺序。
复用：146（LRU）、138（深拷贝）。

| 动作 | 时间 | 空间 |
|---|---|---|
| 遍历 / Dummy / 删除 | O(n) | O(1) |
| 反转（整条 / 局部 / 分组） | O(n) | O(1) |
| 快慢指针找中点 / 环检测 | O(n) | O(1) |
| 归并两条有序链 | O(m+n) | O(1) |
| 归并 k 条（堆） | O(N log k) | O(k) |
| 链表归并排序 | O(n log n) | **O(log n) 递归栈** |
| LRU get/put | 平均 O(1) | O(capacity) |

---

## 三、一题多模式（不要当成新算法）

| 题 | = 哪几个基础动作的组合 |
|---|---|
| LC-0234 Palindrome | 找中点 ③ + 反转后半 ② + 双端比较 |
| LC-0143 Reorder List | 找中点 ③ + 反转后半 ② + 交替拼接 |
| LC-2130 Max Twin Sum | 找中点 ③ + 反转后半 ② + 配对扫描 |
| LC-0148 Sort List | 找中点 ③ + 切断 ⑤ + 递归 + 归并（LC-0021） |
| LC-0025 k-Group | LC-0024（k=2）的推广 = 反转 ② + 分段接线 ⑤ |
| LC-0146 LRU | Hash Map ⑥ + 双向链表 + 哨兵 |

**02/03 那三道题共用同一个「找中点 → 反转后半 → 处理两半」的骨架，
写熟一道，另外两道只是最后一步不同。**

---

## 四、P0 / P1 / P2

**P0（核心必练，11 道）**
LC-0206、LC-0021、LC-0002、LC-0019、LC-0876、LC-0141、LC-0142、
LC-0143、LC-0234、LC-0023、LC-0138、LC-0025（LC-0146 见 17-design）

**P1（重要变体，11 道）**
LC-0092、LC-0024、LC-0082、LC-0203、LC-0160、LC-0148、LC-0086、
LC-0328、LC-0061、LC-0202、LC-0707、LC-0430、LC-0445、LC-2130

**P2（低优先级 / 存档，8 道）**
LC-0083、LC-2095、LC-0457、LC-0725、LC-0353、LC-0708、LC-1721、LC-0109、LC-0957

### 推荐学习顺序
```
阶段 A 指针基本功   206 → 203 → 083 → 082 → 002
阶段 B 局部重排     092 → 024 → 025
阶段 C 双指针       876 → 019 → 160 → 2095
阶段 D 中点+反转    234 → 143 → 2130
阶段 E 环检测       141 → 142 → 202 →（287 跨专题）→ 457
阶段 F 归并         021 → 023 → 148
阶段 G 分区重排     086 → 328 → 061 → 725
阶段 H 设计         707 → 138 → 146（在 17-design）→ 430
阶段 I 存档         445、353、708、1721、109、957
```

---

## 五、跨专题索引

| LC | 本专题的角色 | 实体目录 |
|---|---|---|
| LC-0287 Find the Duplicate Number | Level 1 `03/02` 的隐式函数图代表题 | [01-arrays-hashing](<../01-arrays-hashing (数组、哈希表)/04 - Array Index Mapping 与 In-place Marking/04 - LC-0287 - Find the Duplicate Number>)（那里的 ⭐ 解法就是 Floyd） |
| LC-0109 Sorted List → BST | Level 1 `07`，主归属是树的构造 | 本专题保留，[07-trees](<../07-trees (树)/>) 可交叉参考 |
| LC-0234 / 0143 | 也用到双指针 | 主归属本专题（核心是链表指针操作，不是数组双指针） |
| LC-0023 Merge k Sorted Lists | 也用到堆 | 主归属本专题，[09-heap](<../09-heap (堆)/>) 可交叉参考 |

**LC-0287 为什么不在这里建实体目录**：它已经在 arrays-hashing 有完整资料
（含 Floyd 解法、负数标记解法、二分解法三种），一道题只能有一个实体文件夹，
否则复习队列会重复。它的 Primary Pattern 其实就是本章的「隐式函数图 + Floyd」。

---

## 六、NC / LC 重复题处理结果

原目录下有 3 个 NeetCode 版本和对应的 LeetCode 版本并存：

| NC 目录 | 对应 LC | 处理 |
|---|---|---|
| `NC - Merge K Sorted Linked Lists` | LC-0023 | NC 实现并入 LC 的 `Solution_NC`，NC 目录删除 |
| `NC - Copy Linked List with Random Pointer` | LC-0138 | 同上 |
| `NC - Merge Two Sorted Linked Lists` | LC-0021 | 同上 |

**按仓库现行规则「LC / NC 重复时只保留 LeetCode 版」**，没有建 `_neetcode/` 子目录。
三个 NC 版本的算法各有特点，**代码一字未改地并入了对应 LC 的 solution.py**，
所以删除目录没有丢失任何学习成果：

- NC-0023：堆里直接放**原节点** `(val, id(node), node)` 并重连；
  已有的 LC 版是取值**新建节点** + index 当 tie-breaker。两种都对，思路不同。
- NC-0138：`defaultdict(lambda: Node(0))` **一趟**同时接好 next 和 random；
  已有 LC 版是经典的两趟映射法。
- NC-0021：同一思路，收尾用 `node.next = list1 or list2` 更简洁。

三个 NC 目录的 `practice` 迁移前都是空的，**没有复习记录损失**。
删除使用 macOS 的 `trash`（可从废纸篓恢复），**没有用 `rm -rf`**。

---

## 七、第二轮独立审核结果

**自主新增 2 道**（上限 5，没有凑数）：

| 题 | Pattern | 为什么值得加 | 与已有题的区别 |
|---|---|---|---|
| LC-0445 Add Two Numbers II | **链表 + 栈** | LC-0002 是低位在前，遍历方向和进位方向一致；445 把顺序反过来，**进位方向与遍历方向相反**，逼出「需要逆序访问但不能反转 ⟹ 用栈」这个通用技巧。结果用**头插**构造，也是新东西 | 002 边走边加 + 尾插；445 栈 + 头插 |
| LC-0725 Split Linked List in Parts | **精确切断 + 边界算术** | 把「切断链表」这个动作单独拎出来练（`divmod` 算段长 + 先存 next 再断开）。这个动作在 148、025 里都用到，但那里被包在递归/反转里看不清 | 086/328 是按条件分两组；725 是按长度精确切 k 段 |

**审核过、决定不加（Future Candidates）**

| 题 | 理由 |
|---|---|
| LC-1472 Design Browser History | 双向链表设计，但和 LC-0146 + LC-0707 的技能点高度重合 |
| LC-0382 Linked List Random Node | 核心是 Reservoir Sampling（蓄水池抽样），是概率算法，不是链表指针题 |
| LC-0460 LFU Cache | Hard，需要「频次桶 + 每桶一个 DLL」双层结构，记忆成本远高于收益；先吃透 146 |
| LC-0432 All O`one Data Structure | 同上，更偏数据结构工程题 |
| LC-0147 Insertion Sort List | O(n²)，被 LC-0148 完全覆盖 |

---

## 八、原有资料与安全

- `docs/`、`doubly-linked-list/` 的 3 个 PDF、Floyd 模板、`utils/ListNode.py`
  全部搬到 [`_resources/`](<_resources>)，**内容未改**。
  已确认**没有任何 solution.py 依赖 `utils/ListNode.py`**（每个文件都自带 ListNode 定义），
  所以搬迁不会破坏任何运行环境。
- LC-0430 的原始代码 `02 - Flatten ML Doubly Linked List.py` 保留在正式题目目录下的
  `_original_sources/`，并作为 `Solution_1` 一字未改地并入新的 solution.py。
- **修复了 3 个原本跑不起来的文件**（LC-0023 / LC-0025 / LC-0328）：
  它们底部的示例代码调用 `ListNode.from_list` / `print_list_node`，
  但各自的 ListNode 类没有定义这两个方法，导致 `AttributeError`。
  已把 `_resources/utils/ListNode.py` 里的同名方法补进去，**没有改动任何解法代码**。
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`。

完整校验见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
