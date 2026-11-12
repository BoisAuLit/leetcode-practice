# 17-Design 重构验收报告（Post-migration Report）

**执行日期**：2026-11-11
**执行范围**：所有写入**严格限制**在 `17-design (设计)/` 内部；
仓库其余部分只做**只读**扫描。
**Git**：未执行 `git add` / `git commit` / `git push`；未执行任何破坏性命令；
未使用 `rm -rf`。

---

## 一、总览

| 指标 | 重构前 | 重构后 |
|---|---|---|
| 实体题目数 | 10 | **17** |
| 本专题条目数 | 10 | **18**（17 实体 + 1 跨专题索引） |
| 目录结构 | 扁平五类（`cache` / `general` / `hash-structures` / `randomized` / `rate-and-counter`） | **Level 1 → Level 2 → Level 3** 三级 |
| Level 1 数 | — | **6** |
| Level 2 数 | — | **14** |
| 原始文件 | 42 | **42 全部保留，SHA-256 全部一致** |
| README | 0 | **根 1 + Level 1 六个 + 跨专题索引 1 + _resources 两份** |
| 基线测试 | 10 通过 / 0 失败 | **17 通过 / 0 失败** |

**最终目录树**

```
17-design (设计)/
├── README.md                              ← 根 README（知识地图 / 六套路 / 跨专题索引 / 审核结果）
├── instructions.md                        ← 用户的指令文件（原样保留）
├── _audit/
│   ├── pre-migration-manifest.json
│   ├── migration-map.json
│   └── post-migration-report.md           ← 本文件
├── _resources/
│   ├── design-checklist.md                ← 开场五步 + 六套路 + 边界清单 + Stateful API 测试法
│   └── pattern-recognition-guide.md       ← Q1–Q14 决策树
├── 01 - Hash Structures 与稀疏数据设计/     README.md
│   ├── 01 - HashSet 与 HashMap 基础实现/
│   │   ├── 01 - LC-0705 - Design HashSet/
│   │   └── 02 - LC-0706 - Design HashMap/
│   └── 02 - Sparse Representation 与高效内积/
│       └── 01 - LC-1570 - Dot Product of Two Sparse Vectors/
├── 02 - Cache 与 O(1) 淘汰策略/             README.md
│   ├── 01 - LRU Cache/
│   │   └── 01 - LC-0146 - LRU Cache/
│   └── 02 - LFU Cache 与频率桶/
│       └── 01 - LC-0460 - LFU Cache/                    ★ 第一轮新增
├── 03 - Randomized Data Structures/         README.md
│   └── 01 - O(1) 插入、删除与均匀随机访问/
│       ├── 01 - LC-0380 - … (学习索引 · 实体在 01-arrays-hashing)/   README.md only
│       └── 02 - LC-0381 - … Duplicates allowed/         ★ 第二轮新增
├── 04 - 时间窗口、计数器与限流/              README.md
│   ├── 01 - Recent Calls 与流式时间窗口/
│   │   ├── 01 - LC-0933 - Number of Recent Calls/
│   │   └── 02 - LC-0362 - Design Hit Counter/
│   └── 02 - 消息去重与时间限流/
│       ├── 01 - LC-0359 - Logger Rate Limiter/
│       └── 02 - LC-1797 - Design Authentication Manager/ ★ 第二轮新增
├── 05 - 有状态 API、缓冲区与模拟/            README.md
│   ├── 01 - Buffered Reader 与跨调用状态/
│   │   ├── 01 - LC-0157 - Read N Characters Given Read4/
│   │   └── 02 - LC-0158 - … Call Multiple Times/         ★ 第一轮新增
│   ├── 02 - 棋盘状态与历史导航/
│   │   ├── 01 - LC-0348 - Design Tic-Tac-Toe/
│   │   └── 02 - LC-1472 - Design Browser History/        ★ 第一轮新增
│   ├── 03 - 多对象状态与增量平均值/
│   │   └── 01 - LC-1396 - Design Underground System/     ★ 第一轮新增
│   └── 04 - 版本快照与历史访问/
│       └── 01 - LC-1146 - Snapshot Array/                ★ 第二轮新增
└── 06 - SQL 与非设计题目存档/                README.md
    └── 01 - SQL Aggregation 与 Database Query/
        └── 01 - LC-0580 - Count Student Number in Departments/
```

---

## 二、六个 Level 1 与 14 个 Level 2

| Level 1 | Level 2 | Pattern | 题数 |
|---|---|---|---|
| 01 Hash Structures 与稀疏数据设计 | 01 HashSet 与 HashMap 基础实现 | Separate Chaining | 2 |
| | 02 Sparse Representation 与高效内积 | Sparse Representation + 双指针 | 1 |
| 02 Cache 与 O(1) 淘汰策略 | 01 LRU Cache | 双向链表 + Hash Map | 1 |
| | 02 LFU Cache 与频率桶 | Frequency Buckets + min_freq | 1 |
| 03 Randomized Data Structures | 01 O(1) 插入、删除与均匀随机访问 | Array + Hash Map + swap-with-last | 2（1 索引） |
| 04 时间窗口、计数器与限流 | 01 Recent Calls 与流式时间窗口 | Sliding Time Window / 环形数组 | 2 |
| | 02 消息去重与时间限流 | Rate Limiting / Expiration Semantics | 2 |
| 05 有状态 API、缓冲区与模拟 | 01 Buffered Reader 与跨调用状态 | Persistent State Across Calls | 2 |
| | 02 棋盘状态与历史导航 | 增量计数 / Array Cursor | 2 |
| | 03 多对象状态与增量平均值 | Incremental Aggregation | 1 |
| | 04 版本快照与历史访问 | Versioned Array + Binary Search | 1 |
| 06 SQL 与非设计题目存档 | 01 SQL Aggregation 与 Database Query | （非设计题） | 1 |
| | 02 跨专题索引 | （README 表格，无文件夹） | 8 条引用 |

**Level 1 分布**：01→3、02→2、03→2、04→4、05→6、06→1，合计 **18**。

---

## 三、原有 10 道题的迁移情况（零丢失）

| 原路径 | 新路径 |
|---|---|
| `hash-structures/LC-0705 - Design HashSet` | `01/01/01` |
| `hash-structures/LC-0706 - Design HashMap` | `01/01/02` |
| `hash-structures/LC-1570 - Dot Product of Two Sparse Vectors` | `01/02/01` |
| `cache/LC-0146 - LRU Cache` | `02/01/01` |
| `rate-and-counter/LC-0933 - Number of Recent Calls` | `04/01/01` |
| `rate-and-counter/LC-0362 - Design Hit Counter` | `04/01/02` |
| `rate-and-counter/LC-0359 - Logger Rate Limiter` | `04/02/01` |
| `general/LC-0157 - Read N Characters Given Read4` | `05/01/01` |
| `general/LC-0348 - Design Tic-Tac-Toe` | `05/02/01` |
| **`randomized/LC-0580 - Count Student Number in Departments`** | **`06/01/01`** |

旧目录 `hash-structures`、`cache`、`rate-and-counter`、`general`、`randomized`
确认**已全部迁移且为空**后才清理（只删除了残留的 `.DS_Store`）。

### 一个分类错误被顺手修正

**LC-0580 原本躺在 `randomized (随机化)/` 下** —— 它是一道 **SQL 题**，
既不属于「随机化」也不属于「数据结构设计」。
本次把它移到新建的 **Level 1 · 06「SQL 与非设计题目存档」**，
并在该层 README 中说明它真正的归属是 SQL / Database 专题。
**原文件一个字节没改。**

**本专题没有 NC-only 题目**（指令第三节所述的 NC - LRU Cache 已在早先的
跨专题去重中处理为 LC-0146，实体就在本专题）。

---

## 四、第一轮建议新增的五道题

| 题 | 结果 | 位置 |
|---|---|---|
| **LC-0380** Insert Delete GetRandom O(1) | ⚠️ **未新建实体** —— 仓库已有 ⟹ 跨专题索引 | `01-arrays-hashing/01/08` |
| **LC-0460** LFU Cache | ✅ 新建，3 实现 + 3000 组随机对拍 | `02/02/01` |
| **LC-0158** read4 II - Call Multiple Times | ✅ 新建（**Premium，无 PDF**），3 实现 + 3000 组对拍 | `05/01/02` |
| **LC-1396** Design Underground System | ✅ 新建，3 实现 + 2000 组随机对拍 | `05/03/01` |
| **LC-1472** Design Browser History | ✅ 新建，3 实现 + 3000 组随机对拍 | `05/02/02` |

**仓库只读查重结果**（指令第四节要求检查的所有专题）：

| 题 | 检查结果 | 处理 |
|---|---|---|
| LC-0380 | **已在** `01-arrays-hashing/01/08` | **只建索引**（规则：已有完整主归属） |
| LC-0460 | 仓库**无** | 本专题新建 |
| LC-0158 | 仓库**无** | 本专题新建 |
| LC-1396 | 仓库**无** | 本专题新建 |
| LC-1472 | 仓库**无** | 本专题新建 |

还顺带核查了第二轮候选的全部 15 道题（见第五节）。
**没有修改其他专题的任何文件。**

---

## 五、第二轮独立审核

**自主新增 3 道（上限 3，用满）**：

| 题 | 填补缺口 | 通过的条件 |
|---|---|---|
| **LC-0381** Insert Delete GetRandom - Duplicates | Level 1 · 03 原本**没有任何实体题**（LC-0380 只能建索引） | 1–7 ✅ |
| **LC-1797** Design Authentication Manager | **Expiration Semantics**（审核清单第 13 项）原本只被 LC-0359 部分覆盖 | 1–7 ✅ |
| **LC-1146** Snapshot Array | **Versioned Array / Snapshot** 原本完全没有 | 1–7 ✅ |

**条件 5（不与现有题高度重复）的详细说明**：
- **LC-0381 vs LC-0380**：`val -> int` 变成 `val -> set`，
  `remove` 的不变量和三步顺序完全不同（见第八节的真实 bug）。
- **LC-1797 vs LC-0359**：0359 是「**每 key 限流**」（判时间差），
  1797 是「**每 token 过期 + 可续期**」（判过期时刻），且不等号方向相反。
- **LC-1146 vs LC-0981**：0981 的考点是**二分找版本**（所以在 `05-binary-search`），
  1146 的考点是「**怎么设计存储让 `snap` 变 O(1)**」——
  二分只是手段，不是考点。两题的版本号来源（传入 vs 自增）和粒度
  （每次 set vs 每次 snap）也不同。

**未新增的候选及原因**（指令第五节点名的全部候选）：

| 题 | 违反条件 | 原因 | 已在哪 |
|---|---|---|---|
| LC-0155 Min Stack | **3** | Stack 的辅助状态是 Stack 专题的内容 | `04-stack-queue` |
| LC-0622 Design Circular Queue | **3** | 环形缓冲属于 Queue | `04-stack-queue` |
| LC-0641 Design Circular Deque | **5** | LC-0622 的 deque 变体，高度重复 | — |
| LC-0981 Time Based KV Store | **3** | 考点是二分 | `05-binary-search` |
| LC-0208 Implement Trie | **3** | 考点是 Trie | `08-tries` |
| LC-0295 Find Median from Data Stream | **3** | 考点是双堆 | `09-heap` |
| LC-0355 Design Twitter | **3** | 考点是 k 路合并 | `09-heap` |
| LC-3408 Design Task Manager | **3** | 考点是动态优先级 + 懒删除 | `09-heap` |
| LC-0729 My Calendar I | **3** | 考点是区间重叠判定 | `14-intervals` |
| LC-1381 Design a Stack With Increment | **3** | Stack 设计属于 `04-stack-queue` | — |
| LC-0432 All O(1) Data Structure | **6** | 指令明确「高级复杂结构设计，不应直接加入核心 P0」 | — |

判断标准（指令第五节 1–7）：
1 面试代表性 · 2 填补重要缺口 · 3 没有更合适的现成归属 · 4 独立可迁移知识 ·
5 不与现有题高度重复 · 6 学习成本合理 · 7 能解释清 API / 状态 / 复杂度。

参考：NeetCode 150/250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Design 分区。**未编造任何公司的实际出题频次。**

---

## 六、P0 / P1 / P2 数量

| 等级 | 数量 | 题 |
|---|---|---|
| **P0** | **4** | 1570, 0146, 0380↗️, 0933 |
| **P1** | **12** | 0705, 0706, 0460, 0381, 0362, 0359, 1797, 0158, 0348, 1472, 1396, 1146 |
| **P2** | **2** | 0157, 0580 |

合计 18。**没有把所有题都标 P0。**

---

## 七、题面生成情况

| 题 | metadata.json | solution.py | problem.pdf | problem_dark.pdf |
|---|---|---|---|---|
| LC-0460 | ✅ | ✅ | ✅ | ✅ |
| LC-1472 | ✅ | ✅ | ✅ | ✅ |
| LC-1396 | ✅ | ✅ | ✅ | ✅ |
| LC-0381 | ✅ | ✅ | ✅ | ✅ |
| LC-1797 | ✅ | ✅ | ✅ | ✅ |
| LC-1146 | ✅ | ✅ | ✅ | ✅ |
| **LC-0158** | ✅ | ✅ | ❌ **Premium** | ❌ **Premium** |

**LC-0158 是 LeetCode Premium 题目**，题面在登录墙后，本仓库无法合法抓取。
按指令严格遵守：
- ❌ 未创建空白 PDF
- ❌ 未伪造 metadata
- ❌ 未用其他题目的内容替代
- ✅ `metadata.json` 正常生成（`id` / `path` / `difficulty` / `link` 真实）
- ✅ `solution.py` 的题意描述为**公开通行表述**，实现与证明自撰
- ✅ 在根 README、Level 1 · 05 README 和本报告中**明确标注**

**另有 4 道 Premium 题 PDF 完整**（LC-1570、LC-0362、LC-0359、LC-0157、LC-0348）
—— 题面在早先入库时已抓到，本次**完整保留，未覆盖**。

**学习索引文件夹**（LC-0380）**故意只有 `README.md`**：
没有 `metadata.json` ⟹ `review_due.py:154` 要求同时满足
「有 `metadata.json`」且「文件夹名匹配 `PROBLEM_DIR_RE`」才入复习队列
⟹ **不会重复叫号**。

---

## 八、边界测试结果

每道新题的 `__main__` 都跑了官方样例 + 逐项边界 + **随机操作序列对拍 + 独立真值**：

| 题 | 关键边界断言 | 对拍 |
|---|---|---|
| LC-0460 | `capacity=0`、`capacity=1`、**put 已存在的 key 不淘汰**、freq 平局取最旧 | 3000 组 ✅（3 实现） |
| LC-0158 | `n=0`、文件比 n 短、**n 不是 4 的倍数**、空文件、读完后继续读 | 3000 组 ✅（2 实现 + **顺序切片真值**） |
| LC-1396 | 同一乘客多次乘车、**方向相反是两条线路**、起点==终点、耗时为 0 | 2000 组 ✅（3 实现） |
| LC-1472 | `back(100)` 在首页、**visit 后 forward 停原地**、`back(0)`、反复 visit 同 url | 3000 组 ✅（3 实现 + **朴素真值**） |
| LC-0381 | **插入重复返回 False**、删到一个不剩、**val == arr[-1]**、全部相同 | 3000 组 ✅（3 实现）+ **40000 次加权随机分布验证** |
| LC-1797 | **`expiry == now` 算死**、renew 不存在/已过期的 token、`ttl=1` | 3000 组 ✅（3 实现 + **定义真值**） |
| LC-1146 | 从未 set 的位置→0、**同周期多次 set 只留最后**、snap 之间无 set | 3000 组 ✅（3 实现）+ **空间收益验证** |

### 被随机对拍抓出的一个真实 bug（LC-0381）

我最初给 `Solution_1` 写的是「**add 再 discard**」的顺序：
```python
self.idx[last].add(i)
self.idx[val].discard(i)          # ← 当 val == last 时，这两行作用在同一个 set
```
**官方样例和手写的全部边界用例都通过了**，但随机序列
`insert(5); insert(5); remove(5); remove(5)` 触发了它：
第二次 `remove` 返回 `False`（应为 `True`）。

**根因**：`val == last` 时 `idx[val]` 和 `idx[last]` 是**同一个 set**，
`add(i)` 之后 `discard(i)` 净效果是「`i` 不在集合里」——
但位置 `i` 上**确实还放着一个 `val`**。

**修正**为唯一正确的三步顺序：
```python
i = self.idx[val].pop()                      # ① 先摘掉 i
self.idx[last].add(i)                        # ② 再记到 last 名下
self.idx[last].discard(len(self.arr) - 1)    # ③ 清掉原末尾下标
```
两种顺序的逐步对比表已写进该题 docstring 的「坑 ②」。

> **这正是指令第 21 项「Stateful API Sequence Testing」的价值**：
> **单个方法对 ≠ 操作序列对。** 本专题每道新题都做了序列级别的随机对拍。

### 另外两处已修正的文档问题

1. **LC-1472 的 Level 1 README 模板里有一行写坏了**
   （`return self.history[max(0, self.cur - steps) or 0]`，`or 0` 是错的）
   ⟹ 已改为与 `solution.py` 一致的两行写法。
2. **LC-0158 的「丢弃多读字符会怎样」不是理论担忧** ——
   该题保留了 `Solution_3_BROKEN` 并实际跑出
   `['a', 'e', '', '']`（正确是 `['a','b','c','d']`），
   证明 LC-0157 的解法用在 LC-0158 上会**永久丢失 b, c, d**。

---

## 九、原始文件与 SHA-256 验证结果

```
[1] 原始文件 42 个 → 内容仍在的 42，丢失 0        ✅
[2] 相对链接 122 条，死链 0                       ✅
[3] solution.py 运行 17 通过 / 0 失败             ✅（迁移前 10 通过 / 0 失败）
[4] 题目文件夹 17 个，Level 1/2/3 编号连续        ✅
```

- **SHA-256**：重构前记录全部 42 个文件的哈希；重构后逐一比对，
  **42/42 内容完全一致**（`metadata.json` 作为可变文件单独处理 ——
  只有 `path` 按设计变更，`practice[]` 未手改）。
- **符号链接**：本专题内**未发现**符号链接。
- **文件名冲突**：无。
- **未跟踪文件**：未删除任何一个（只删了几个 `.DS_Store` 以便 `rmdir` 空目录）。
- **原有 `solution.py` 覆盖**：**零次**。
- **原有 PDF / 附件覆盖**：**零次**。

---

## 十、Git 变更摘要

- **未执行** `git add` / `git commit` / `git push`（按指令要求）。
- **未执行** 任何破坏性命令（`git reset` / `git clean` / `git restore` / `rm -rf`）。
- 文件夹移动用 `mv`（这些文件是 untracked）。
- 变更性质：
  - **新增**：7 道题的文件夹 + 10 份 README/文档 + `_audit/` 三份
  - **移动**：10 个原有题目文件夹
  - **修改**：10 个 `metadata.json` 的 `path` 字段（`practice[]` 未动）
  - **删除**：几个 `.DS_Store`
- 写入范围：**全部在 `17-design (设计)/` 内部**。
  唯一例外是 `tools/intake.py` 自动更新的仓库级 `progress.md` —— 该工具的既有行为。

---

## 十一、失败或未完成的任务

| 项 | 状态 | 说明 |
|---|---|---|
| LC-0158 的 PDF | ⚠️ **受限，已记录** | LeetCode Premium 登录墙，按指令不伪造 |
| 其余全部验收项 | ✅ **通过** | 见第九节 |

**没有其他失败或未完成项。**

---

## 十二、幂等性

重复执行本次重构**不会**叠加编号、重复生成题目、覆盖原文件或丢失资料
（`intake.py` 不加 `--force` 就跳过已存在的文件；所有操作都是 `mv` / 新建）。

---

## 十三、建议的学习顺序

见根 [README.md](<../README.md>) 第十节。

最短路线 4 道：`1570 → 0146 → 0380 → 0933`
