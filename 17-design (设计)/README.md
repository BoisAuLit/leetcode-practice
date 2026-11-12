# 17 - Design（设计题）

> **一句话**：设计题没有算法可背，它只考三个问题 ——
> **① 两次调用之间我必须记住什么？② 哪个操作必须最快？③ 边界语义是什么？**
> 答对这三问，代码只是搬运。

**26 道题 · 6 个 Level 1 · 15 个 Level 2**

---

## 一、知识地图

```
Level 1 · 01  Hash Structures 与稀疏数据设计        ← 地基：把字典拆开看
                ├─ 01 HashSet 与 HashMap 基础实现    LC-0705  LC-0706
                └─ 02 Sparse Representation 与高效内积 LC-1570

Level 1 · 02  Cache 与 O(1) 淘汰策略                ← 链表管顺序 + 字典管定位
                ├─ 01 LRU Cache                      LC-0146
                └─ 02 LFU Cache 与频率桶             LC-0460★

Level 1 · 03  Randomized Data Structures            ← 数组管随机 + 字典管定位
                └─ 01 O(1) 插入、删除与均匀随机访问   LC-0380↗ LC-0381★

Level 1 · 04  时间窗口、计数器与限流                 ← 难点全在不等号
                ├─ 01 Recent Calls 与流式时间窗口     LC-0933  LC-0362
                └─ 02 消息去重与时间限流              LC-0359  LC-1797★

Level 1 · 05  有状态 API、缓冲区与模拟               ← 「我必须记住什么」
                ├─ 01 Buffered Reader 与跨调用状态    LC-0157  LC-0158★
                ├─ 02 棋盘状态与历史导航              LC-0348  LC-1472★
                ├─ 03 多对象状态与增量平均值          LC-1396★
                └─ 04 版本快照与历史访问              LC-1146★

Level 1 · 06  SQL 与非设计题目存档                   ← 保留成果，标清归属
                ├─ 01 SQL Aggregation 与 Database Query  LC-0580
                └─ 02 跨专题索引（9 道题的主归属在别处）
```

★ = 本次新增 · ↗️ = 实体在其他专题，只放学习索引

---

## 二、六个 Level 1

| Level 1 | 核心冲突 | 解法 |
|---|---|---|
| [**01** Hash Structures 与稀疏数据](<./01 - Hash Structures 与稀疏数据设计>) | 随机访问 vs 碰撞处理 | 数组（桶）+ 链表（链地址法） |
| [**02** Cache 与 O(1) 淘汰](<./02 - Cache 与 O(1) 淘汰策略>) | O(1) 查找 vs O(1) 顺序调整 | **双向链表 + 字典**（LFU 再加频率桶） |
| [**03** Randomized Data Structures](<./03 - Randomized Data Structures>) | O(1) 删除 vs 均匀随机 | **紧凑数组 + 字典 + swap-with-last** |
| [**04** 时间窗口、计数器与限流](<./04 - 时间窗口、计数器与限流>) | 状态随时间自动失效 | **懒清理**（前提：时间单调不减） |
| [**05** 有状态 API、缓冲区与模拟](<./05 - 有状态 API、缓冲区与模拟>) | 跨调用保留什么 | 看题 —— **这是设计题的母问题** |
| [**06** SQL 与非设计题目存档](<./06 - SQL 与非设计题目存档>) | — | 归档 + 跨专题索引 |

**依赖顺序**：01 是地基（理解「O(1) 平均」）→ 02 / 03 / 04 / 05 相对独立 → 06 是归档。

---

## 三、全部题目（含真实相对路径）

| # | 题 | 优先级 | 核心技巧 | 路径 |
|---|---|---|---|---|
| 1 | LC-0705 Design HashSet | P1 | Separate Chaining | [→](<./01 - Hash Structures 与稀疏数据设计/01 - HashSet 与 HashMap 基础实现/01 - LC-0705 - Design HashSet>) |
| 2 | LC-0706 Design HashMap | P1 | Separate Chaining | [→](<./01 - Hash Structures 与稀疏数据设计/01 - HashSet 与 HashMap 基础实现/02 - LC-0706 - Design HashMap>) |
| 3 | LC-1570 Dot Product of Two Sparse Vectors | **P0** | 只存非零 + 双指针 | [→](<./01 - Hash Structures 与稀疏数据设计/02 - Sparse Representation 与高效内积/01 - LC-1570 - Dot Product of Two Sparse Vectors>) |
| 4 | LC-0146 LRU Cache | **P0** | 双向链表 + 字典 | [→](<./02 - Cache 与 O(1) 淘汰策略/01 - LRU Cache/01 - LC-0146 - LRU Cache>) |
| 5 | LC-0460 LFU Cache ★ | P1 | **频率桶 + min_freq** | [→](<./02 - Cache 与 O(1) 淘汰策略/02 - LFU Cache 与频率桶/01 - LC-0460 - LFU Cache>) |
| 6 | LC-0380 Insert Delete GetRandom O(1) ↗️ | **P0** | swap-with-last | [→](<./03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) |
| 7 | LC-0381 … Duplicates allowed ★ | P1 | 下标**集合** + 顺序陷阱 | [→](<./03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/02 - LC-0381 - Insert Delete GetRandom O(1) - Duplicates allowed>) |
| 8 | LC-0933 Number of Recent Calls | **P0** | 队列 + 懒弹出 | [→](<./04 - 时间窗口、计数器与限流/01 - Recent Calls 与流式时间窗口/01 - LC-0933 - Number of Recent Calls>) |
| 9 | LC-0362 Design Hit Counter | P1 | 环形数组 | [→](<./04 - 时间窗口、计数器与限流/01 - Recent Calls 与流式时间窗口/02 - LC-0362 - Design Hit Counter>) |
| 10 | LC-0359 Logger Rate Limiter | P1 | `key -> 上次时刻` | [→](<./04 - 时间窗口、计数器与限流/02 - 消息去重与时间限流/01 - LC-0359 - Logger Rate Limiter>) |
| 11 | LC-1797 Design Authentication Manager ★ | P1 | **过期时刻 + 懒清理** | [→](<./04 - 时间窗口、计数器与限流/02 - 消息去重与时间限流/02 - LC-1797 - Design Authentication Manager>) |
| 12 | LC-0157 Read N Characters Given Read4 | P2 | 单次缓冲读取 | [→](<./05 - 有状态 API、缓冲区与模拟/01 - Buffered Reader 与跨调用状态/01 - LC-0157 - Read N Characters Given Read4>) |
| 13 | LC-0158 read4 II - Call Multiple Times ★ | P1 | **跨调用持久缓冲区** | [→](<./05 - 有状态 API、缓冲区与模拟/01 - Buffered Reader 与跨调用状态/02 - LC-0158 - Read N Characters Given read4 II - Call Multiple Times>) |
| 14 | LC-0348 Design Tic-Tac-Toe | P1 | **增量行列计数** | [→](<./05 - 有状态 API、缓冲区与模拟/02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>) |
| 15 | LC-1472 Design Browser History ★ | P1 | 游标 + **逻辑删除** | [→](<./05 - 有状态 API、缓冲区与模拟/02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>) |
| 16 | LC-1396 Design Underground System ★ | P1 | **增量聚合** | [→](<./05 - 有状态 API、缓冲区与模拟/03 - 多对象状态与增量平均值/01 - LC-1396 - Design Underground System>) |
| 17 | LC-1146 Snapshot Array ★ | P1 | **版本链 + 二分** | [→](<./05 - 有状态 API、缓冲区与模拟/04 - 版本快照与历史访问/01 - LC-1146 - Snapshot Array>) |
| 18 | LC-0580 Count Student Number in Departments | P2（存档） | **SQL，非设计题** | [→](<./06 - SQL 与非设计题目存档/01 - SQL Aggregation 与 Database Query/01 - LC-0580 - Count Student Number in Departments>) |

**实体文件夹 17 个 + 跨专题学习索引 1 个（LC-0380）= 18 个条目。**
另有 9 道经典设计题的主归属在其他专题，见**第八节跨专题索引**。

---

## 四、P0 / P1 / P2

| 等级 | 数量 | 题 |
|---|---|---|
| **P0**（核心，必须熟练） | **4** | 1570, 0146, 0380↗️, 0933 |
| **P1**（标准面试覆盖面） | **11** | 0705, 0706, 0460, 0381, 0362, 0359, 1797, 0158, 0348, 1472, 1396, 1146 |
| **P2**（存档与补充） | **2** | 0157, 0580 |

> P0/P1/P2 是**教学优先级**（模式覆盖面 + 学习依赖），
> **不代表任何公司的实际出题频次** —— 本仓库不编造频次数据。

---

## 五、六个反复出现的套路

### ① 两个结构组合（一个管顺序/随机，一个管定位）

**字典几乎总是那个「管定位」的角色。**

| 题 | 管顺序 / 随机 | 管定位 |
|---|---|---|
| LC-0146 LRU | **双向链表** | `key -> node` |
| LC-0460 LFU | **频率桶**（桶内有序） | `key -> val` + `key -> freq` |
| LC-0380 / 0381 | **紧凑数组** | `val -> 下标(集合)` |

### ② swap-with-last（O(n) 删除 → O(1)）

```python
arr[i] = arr[-1]; arr.pop()          # ! 数组保持紧凑 ⟹ 随机访问仍均匀
```
**代价**：顺序被打乱。📍 LC-0380、LC-0381

### ③ 逻辑删除 / 有效长度（不真删，只标记不可达）

```python
self.last = self.cur                 # ! O(1)，而 del arr[cur+1:] 是 O(n)
```
📍 LC-1472

### ④ 懒清理（Lazy Cleanup）

**正确性前提**：时间/版本**单调不减** ⟹ 过期的**永远不会复活**。
📍 LC-1797、LC-0933、LC-0362

### ⑤ 增量聚合（Incremental Aggregation）

```python
self.sum += x; self.count += 1       # ! 更新时 O(1)
avg = self.sum / self.count          # ! 查询时 O(1)
```
✅ 和、计数、平均值、最大/最小值
❌ **中位数、分位数**（要有序结构 ⟹ 双堆，见 `09-heap`）
📍 LC-1396、LC-0348

### ⑥ 懒删除堆（Lazy Deletion Heap）

**不变量**：只保证**清理后的堆顶**有效，堆里仍可能躺着垃圾。
📍 LC-1797 解法 3、`14-intervals` LC-1851、`09-heap` LC-0480

---

## 六、「成本往哪边挪」—— 本专题的中心问题

| 情形 | 策略 | 题 |
|---|---|---|
| **查询频繁、更新稀少** | 把工作挪到**更新**时 | LC-1396（增量 sum/count）、LC-0348（增量行列计数） |
| **更新频繁、查询稀少** | 把工作挪到**查询**时（懒清理） | LC-1797、LC-0362 |
| **两者都频繁** | 用**两个数据结构**组合 | LC-0146、LC-0460、LC-0380 |
| **某个操作太贵** | 把成本挪到别的操作 | **LC-1146**（`snap` O(1)，代价是 `get` O(log k)） |

> **LC-1396 和 LC-1146 是两个相反方向的同一思想：**
> 一个把成本挪到更新时（查询变 O(1)），
> 一个把成本挪到查询时（更新变 O(1)）。
> **选哪个取决于哪个操作更频繁。**

---

## 七、复杂度用词必须精确

| 说法 | 含义 | 本专题的例子 |
|---|---|---|
| **最坏 O(1)** | 任何单次调用都是常数 | **LC-0380 的 `getRandom`**（纯数组访问）；双向链表插删 |
| **平均 O(1)** | 哈希表的期望；最坏可能退化 | 所有用 `dict` / `set` 定位的操作 |
| **均摊 O(1)** | n 次总共 O(n)，单次可能更贵 | **LC-0933 的 `ping`**；LC-1472 双栈版的 `visit` |
| **O(log n)** | 有序结构 / 二分 / 堆 | **LC-1146 的 `get`**；懒删除堆 |

**不要把所有操作一律写成 O(1)：**
- LC-1797 懒清理版的 `countUnexpiredTokens` 是 **O(n)**
- LC-1146 的 `get` 是 **O(log k)**
- LC-1472 双栈版的 `back(steps)` 是 **O(steps)**（游标版才是 O(1)）
- LC-0362 的 `getHits` 是 **O(300)**（= O(1)，但常数不小）

---

## 八、跨专题索引

很多经典「设计题」的**主归属在别的专题** ——
因为**解开它们需要的那个关键洞察属于那个领域**。
按指令：**已有完整主归属 ⟹ 建立跨专题引用，避免无意义的重复生成，不修改其他专题。**

| 题 | 实体位置 | Primary Pattern | Secondary Pattern | Recommended Algorithm |
|---|---|---|---|---|
| **LC-0380** Insert Delete GetRandom | [`01-arrays-hashing`](<../01-arrays-hashing (数组、哈希表)/01 - Hash Set 与 Hash Map 基础/08 - LC-0380 - Insert Delete GetRandom O(1)>) | **Array + Hash Map** | Randomized O(1)、swap-with-last | 紧凑数组 + `val->下标` |
| **LC-0155** Min Stack | [`04-stack-queue`](<../04-stack-queue (栈、队列)/04 - Stack 与 Queue 数据结构设计 (Design)/01 - 带额外状态的 Stack/01 - LC-0155 - Min Stack>) | **带额外状态的 Stack** | Design | 辅助栈 / 存差值 |
| **LC-0622** Design Circular Queue | [`04-stack-queue`](<../04-stack-queue (栈、队列)/04 - Stack 与 Queue 数据结构设计 (Design)/02 - FIFO 队列与循环结构/02 - LC-0622 - Design Circular Queue>) | **环形缓冲** | Design | 定长数组 + 两个指针 |
| **LC-0981** Time Based Key-Value Store | [`05-binary-search`](<../05-binary-search (二分查找)/04 - 二分查找与数据结构设计 (Binary Search Design)/01 - 按时间戳检索历史版本/01 - LC-0981 - Time Based Key-Value Store>) | **Binary Search** | 版本链 | `key -> [(ts, val)]` + 二分 |
| **LC-0208** Implement Trie | [`08-tries`](<../08-tries (字典树、前缀树)/01 - Trie 基础结构与前缀匹配/01 - Trie 基础操作与最短前缀/01 - LC-0208 - Implement Trie (Prefix Tree)>) | **Trie** | Design | 26 叉树 / 字典树 |
| **LC-0295** Find Median from Data Stream | [`09-heap`](<../09-heap (堆)/03 - Two Heaps 与动态中位数/01 - 动态中位数与双堆平衡/01 - LC-0295 - Find Median from Data Stream>) | **Two Heaps** | Design | 大顶堆 + 小顶堆平衡 |
| **LC-0355** Design Twitter | [`09-heap`](<../09-heap (堆)/06 - Heap + Hash Map 数据结构设计/01 - 社交信息流与多路合并/01 - LC-0355 - Design Twitter>) | **k 路合并** | Hash Map | 堆合并各关注者的推文 |
| **LC-3408** Design Task Manager | [`09-heap`](<../09-heap (堆)/06 - Heap + Hash Map 数据结构设计/02 - 动态优先级与 Lazy Deletion/01 - LC-3408 - Design Task Manager>) | **动态优先级 + 懒删除** | Hash Map | 堆 + 真相表校验 |
| **LC-0729** My Calendar I | [`14-intervals`](<../14-intervals (区间)/05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>) | **区间重叠判定** | Design | `s1 < e2 and s2 < e1` |

**跨专题规则**（本次执行遵循）：
1. 本专题已有原始资料 ⟹ **完整保留**。
2. 其他专题已有 ⟹ **只建 README 引用**，不重复生成、不复制 PDF。
3. **不修改其他专题的任何文件。**
4. 一道题只能有一个实体文件夹（否则 `review_due.py` 重复叫号）。
5. **Primary Pattern 必须标清**。

> **「这是不是设计题」不取决于 API 的形状，
> 而取决于「解开它需要的那个关键洞察属于哪个领域」。**

---

## 九、第二轮独立审核结果

**第一轮（指令给定）建议新增 5 道**：LC-0380、LC-0460、LC-0158、LC-1396、LC-1472。
其中 **LC-0380 仓库里已有**（在 `01-arrays-hashing`）⟹ 按规则改为**跨专题索引**，
**实际新建 4 道**。

**第二轮自主新增 3 道**（上限 3，用满）：

| 题 | 填补的缺口（条件 2） | 独立可迁移知识（条件 4） | 为什么不重复（条件 5） |
|---|---|---|---|
| **LC-0381** Insert Delete GetRandom - Duplicates | Level 1 · 03 原本**没有任何实体题** | 下标**集合** + 三步顺序陷阱 | LC-0380 的 `val->int` 变成 `val->set`，`remove` 的不变量完全不同 |
| **LC-1797** Design Authentication Manager | **Expiration Semantics**（审核清单第 13 项）原本只被 LC-0359 部分覆盖 | 「存过期时刻而非生成时刻」+ 懒清理的三种实现 | LC-0359 是**每 key 限流**，本题是**每 token 过期 + 可续期** |
| **LC-1146** Snapshot Array | **Versioned Array / Snapshot** 原本完全没有 | 「把成本从 `snap` 挪到 `get`」的反向思维 | 与 LC-0981 的区别见下 |

**LC-1146 vs LC-0981（条件 5 的详细说明）**：

| | LC-0981（在 `05-binary-search`） | **LC-1146** |
|---|---|---|
| 版本号 | 调用方**传入**的 timestamp | 系统**自增**的 snap_id |
| 版本粒度 | 每次 `set` 一个版本 | **一次 `snap()` 才切一个版本** |
| 考点 | **二分找版本** | **怎么设计存储让 `snap` 变 O(1)** |

**二分只是 LC-1146 的手段，不是考点** —— 所以它归在 Design。

**未新增的候选及原因**：

| 题 | 违反条件 | 原因 |
|---|---|---|
| LC-0155 Min Stack | **3** | 已在 `04-stack-queue`（Stack 是主归属） |
| LC-0622 Design Circular Queue | **3** | 已在 `04-stack-queue` |
| LC-0641 Design Circular Deque | **5** | 是 LC-0622 的 deque 变体，高度重复 |
| LC-0981 Time Based KV Store | **3** | 已在 `05-binary-search`（二分是考点） |
| LC-0208 / LC-0295 / LC-0355 / LC-3408 / LC-0729 | **3** | 分别已在 `08-tries` / `09-heap` ×3 / `14-intervals` |
| LC-1381 Design a Stack With Increment | **3** | Stack 设计属于 `04-stack-queue`（懒传播是个好技巧，但归属不对） |
| LC-0432 All O(1) Data Structure | **6** | 指令明确「属于高级复杂结构设计，不应直接加入核心 P0」；学习成本过高 |

判断标准（指令第五节 1–7）：
1 面试代表性 · 2 填补重要缺口 · 3 没有更合适的现成归属 · 4 独立可迁移 ·
5 不与现有题高度重复 · 6 学习成本合理 · 7 能解释清 API / 状态 / 复杂度。

参考：NeetCode 150/250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Design 分区。**未编造任何公司的实际出题频次。**

---

## 十、最终推荐刷题路线

```
【第一遍 · 4 道】核心模式（P0）
  1570 → 0146 → 0380 → 0933

【第二遍 · 15 道】标准面试覆盖面（P0 + P1）
  0705 → 0706 → 1570
       → 0146 → 0460
       → 0380 → 0381
       → 0933 → 0362 → 0359 → 1797
       → 0158 → 0348 → 1472 → 1396 → 1146

【第三遍 · 18 道】按 Level 1 顺序
  L1 → 0705 0706 1570
  L2 → 0146 0460
  L3 → 0380 0381
  L4 → 0933 0362 0359 1797
  L5 → 0157 0158 0348 1472 1396 1146
  L6 → 0580（SQL，存档）
```

**配对练习**（一次打穿各自的坑）：

| 配对 | 对照的是什么 |
|---|---|
| `0146` → `0460` | **一个维度**（时间） vs **两个维度**（频率 + 时间） |
| `0380` → `0381` | `val -> int` vs **`val -> set`**（三步顺序陷阱） |
| `0157` → `0158` | 调用**一次**（可丢残留） vs 调用**多次**（**必须留**） |
| `0359` → `1797` | `>= 窗口` **允许** vs `> now` **才算活**（不等号相反） |
| `0933` → `0362` | 队列（空间按事件数） vs **环形数组**（空间 O(窗口)） |
| `1396` → `1146` | 成本挪到**更新**时 vs 成本挪到**查询**时 |
| `1472` → `0381` | **逻辑删除**（保序） vs **swap-with-last**（不保序） |

---

## 十一、通用边界清单（每道设计题都过一遍）

| # | 边界 | 本专题的例子 |
|---|---|---|
| 1 | **容量 / 长度为 0** | LC-0460 不特判 ⟹ 空桶 `popitem` 崩溃 |
| 2 | **容量为 1** | 每次插入都触发淘汰 |
| 3 | **操作不存在的 key** | 返回哨兵值，且**不改变任何状态** |
| 4 | **put 已存在的 key** | 是**更新**不是插入 ⟹ **不能触发淘汰** |
| 5 | **删到一个都不剩** | LC-0381：**必须删 key** |
| 6 | **恰好在边界时刻** | LC-1797：`expiry == now` 算**死** |
| 7 | **失败操作的幂等性** | LC-1797 的 `renew`、LC-0359 被拒绝时不更新 |
| 8 | **状态清理** | LC-1396 `checkOut` 后必须删在途记录 |
| 9 | **Stateful API 序列** | 单个方法对 ≠ 序列对 ⟹ **必须随机序列对拍** |

> **LC-0381 的下标集合顺序 bug 就是随机对拍抓出来的** ——
> 官方样例和手写边界用例**全部通过**，只有随机序列能触发
> 「要删的值恰好等于末尾元素的值」这个组合。
> 详见 [设计题通用清单 · 第四节](<./_resources/design-checklist.md>)。

---

## 相关资料

| 文档 | 内容 |
|---|---|
| [设计题通用清单](<./_resources/design-checklist.md>) | 开场五步 + 六个套路 + 边界清单 + **Stateful API 怎么测** + 复杂度用词 |
| [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>) | Q1–Q14 决策树 + 三秒速判表 + 读题三问 |
| [_audit/post-migration-report.md](<./_audit/post-migration-report.md>) | 迁移映射、SHA-256 校验、跨专题去重、Premium 限制 |
