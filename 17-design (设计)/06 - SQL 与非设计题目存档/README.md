# Level 1 · 06 — SQL 与非设计题目存档（SQL & Non-design Archive）

> **本层的目的：保留原有学习成果，同时明确标出「这不是算法设计题」。**
> 放在这里**不代表题目没价值** —— 只代表它**不该占用设计题的复习预算**。

---

## 为什么要有这一层

`17-design` 原来的 `randomized (随机化)` 目录下躺着一道 **SQL 题**
（LC-0580 Count Student Number in Departments）——
它既不属于「随机化」，也不属于「数据结构设计」。

**不处理它有两个坏处**：
1. 它会出现在设计题的复习队列里，稀释真正重要的那十来道题
2. 它挂在一个完全错误的分类下，将来找不到

**所以单独开一层存档**，并在这里说清它真正属于哪里。

---

## Level 2 · 01 — SQL Aggregation 与 Database Query

### [LC-0580 Count Student Number in Departments](<./01 - SQL Aggregation 与 Database Query/01 - LC-0580 - Count Student Number in Departments>)

**⚠️ 这是一道 SQL 题，和数据结构设计无关。**

**题意**：给 `Student` 和 `Department` 两张表，
统计**每个系**的学生人数（**包括没有学生的系**），按人数降序、系名升序排列。

**核心考点：`LEFT JOIN` 而不是 `INNER JOIN`**

```sql
SELECT d.dept_name, COUNT(s.student_id) AS student_number
FROM   department d
LEFT JOIN student s ON d.dept_id = s.dept_id      -- ! LEFT JOIN 保留没有学生的系
GROUP BY d.dept_id, d.dept_name
ORDER BY student_number DESC, d.dept_name ASC;
```

**三个必须想清的点**：

1. **为什么必须 `LEFT JOIN`？**
   题目要求「**包括没有学生的系**」。
   `INNER JOIN` 只保留两边都匹配的行 ⟹ 空系会**整行消失**。
   `LEFT JOIN` 保留左表（department）的全部行，右表没匹配的填 `NULL`。

2. **为什么 `COUNT(s.student_id)` 而不是 `COUNT(*)`？**
   这是全题唯一的坑。
   - `COUNT(*)` 数的是**行数** —— 空系 LEFT JOIN 后仍有 1 行（右侧全 NULL）
     ⟹ 会得到 **1** 而不是 0 ❌
   - `COUNT(列名)` **跳过 NULL** ⟹ 空系得到 **0** ✅

3. **为什么 `GROUP BY` 要带上 `dept_name`？**
   严格 SQL 模式（`ONLY_FULL_GROUP_BY`）要求
   `SELECT` 里的非聚合列必须出现在 `GROUP BY` 里。
   只写 `GROUP BY d.dept_id` 在 MySQL 的宽松模式下能跑，但不可移植。

**它真正属于哪里**：SQL / Database 专题。
若将来建立该专题，应整体迁出。

**优先级 P2（存档）** —— **不要把它当设计题练**。

---

## Level 2 · 02 — 跨专题索引

很多经典「设计题」的**主归属在别的专题**，因为
**解开它们需要的那个关键洞察属于那个领域**，而不是「数据结构设计」本身。

按指令要求：**已有完整主归属 ⟹ 建立跨专题相对路径索引，避免无意义的重复生成。**

| 题 | 实体位置 | Primary Pattern | 为什么不在 Design |
|---|---|---|---|
| **LC-0155** Min Stack | [`04-stack-queue`](<../../04-stack-queue (栈、队列)/04 - Stack 与 Queue 数据结构设计 (Design)/01 - 带额外状态的 Stack/01 - LC-0155 - Min Stack>) | 带额外状态的 Stack | 辅助栈是 Stack 专题的核心内容 |
| **LC-0622** Design Circular Queue | [`04-stack-queue`](<../../04-stack-queue (栈、队列)/04 - Stack 与 Queue 数据结构设计 (Design)/02 - FIFO 队列与循环结构/02 - LC-0622 - Design Circular Queue>) | 环形缓冲 | 环形下标是 Queue 的内容 |
| **LC-0981** Time Based Key-Value Store | [`05-binary-search`](<../../05-binary-search (二分查找)/04 - 二分查找与数据结构设计 (Binary Search Design)/01 - 按时间戳检索历史版本/01 - LC-0981 - Time Based Key-Value Store>) | **Binary Search** | 考点是二分找版本 |
| **LC-0208** Implement Trie | [`08-tries`](<../../08-tries (字典树、前缀树)/01 - Trie 基础结构与前缀匹配/01 - Trie 基础操作与最短前缀/01 - LC-0208 - Implement Trie (Prefix Tree)>) | **Trie** | 考点是 Trie 本身 |
| **LC-0295** Find Median from Data Stream | [`09-heap`](<../../09-heap (堆)/03 - Two Heaps 与动态中位数/01 - 动态中位数与双堆平衡/01 - LC-0295 - Find Median from Data Stream>) | **Two Heaps** | 考点是双堆平衡 |
| **LC-0355** Design Twitter | [`09-heap`](<../../09-heap (堆)/06 - Heap + Hash Map 数据结构设计/01 - 社交信息流与多路合并/01 - LC-0355 - Design Twitter>) | **k 路合并** | 考点是堆合并 |
| **LC-3408** Design Task Manager | [`09-heap`](<../../09-heap (堆)/06 - Heap + Hash Map 数据结构设计/02 - 动态优先级与 Lazy Deletion/01 - LC-3408 - Design Task Manager>) | **动态优先级 + 懒删除** | 考点是堆 |
| **LC-0729** My Calendar I | [`14-intervals`](<../../14-intervals (区间)/05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>) | **区间重叠判定** | 考点是半开区间的不等号 |
| **LC-0380** Insert Delete GetRandom | [`01-arrays-hashing`](<../../01-arrays-hashing (数组、哈希表)/01 - Hash Set 与 Hash Map 基础/08 - LC-0380 - Insert Delete GetRandom O(1)>) | **Array + Hash Map** | 见 [Level 1 · 03 的学习索引](<../03 - Randomized Data Structures/01 - O(1) 插入、删除与均匀随机访问/01 - LC-0380 - Insert Delete GetRandom O(1) (学习索引 · 实体在 01-arrays-hashing)>) |

> **「这是不是设计题」不取决于 API 的形状，
> 而取决于「解开它需要的那个关键洞察属于哪个领域」。**
>
> 所有带 `class XxxDesign:` 和若干方法的题**看起来**都像设计题，
> 但 LC-0295 的难点是**双堆**，LC-0981 的难点是**二分**，
> LC-0729 的难点是**区间语义** —— 这些是别的专题的核心内容。

**本专题真正的设计题**，考的是：
**「两次调用之间记住什么」+「哪个操作要最快」+「两个数据结构怎么配合」**。

---

## 核心不变量（本层的「不变量」是分类标准本身）

> 一道题属于这一层，当且仅当
> **①它根本不是算法设计题**（LC-0580 是 SQL），
> 或**②它在别的专题有更合适的主归属**（上面那张表）。

---

## 代表题目与优先级

| # | 题 | 优先级 | 为什么在这一层 |
|---|---|---|---|
| 1 | [LC-0580 Count Student Number in Departments](<./01 - SQL Aggregation 与 Database Query/01 - LC-0580 - Count Student Number in Departments>) | P2（存档） | **SQL 题，不是设计题** |
| 2–10 | 上表的 9 道跨专题题 | 各专题的 P0/P1 | 主归属在别处 ⟹ **只建索引** |

跨专题索引**不建实体文件夹**（除了 LC-0380 —— 它是
[Level 1 · 03](<../03 - Randomized Data Structures>) 的奠基题，
那里需要它参与 Level 3 编号），因为
**一道题在仓库里只能有一个实体文件夹**，否则 `review_due.py` 会重复叫号。

---

## 典型反例（针对 LC-0580）

| 错误做法 | 结果 |
|---|---|
| 用 `INNER JOIN` | **没有学生的系整行消失** ❌ |
| 用 `COUNT(*)` | 空系被数成 **1** 而不是 0 ❌ |
| `GROUP BY` 只写 `dept_id`，`SELECT` 里有 `dept_name` | 严格 SQL 模式下报错 ⚠️ |
| 忘记 `ORDER BY ... DESC, ... ASC` | 顺序不符合题目要求 ❌ |
| 把它当成设计题来练 | 浪费设计题的复习预算 ⚠️ |

---

## 容易混淆的 Pattern

### 「有 class 和方法」≠「是设计题」

| 题 | 看起来像 | 真正的考点 |
|---|---|---|
| LC-0295 Find Median from Data Stream | 设计题 | **双堆平衡** |
| LC-0981 Time Based KV Store | 设计题 | **二分找版本** |
| LC-0729 My Calendar I | 设计题 | **半开区间的不等号** |
| LC-0208 Implement Trie | 设计题 | **Trie 结构** |
| LC-0580 Count Student Number | — | **SQL 的 LEFT JOIN + COUNT(列)** |

**判断标准**：把 API 的壳去掉，剩下的那个难点属于哪个专题？

---

## 相关资料

- [设计题通用清单 · 第六节](<../_resources/design-checklist.md>) — 跨专题设计题的完整列表
- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>)
