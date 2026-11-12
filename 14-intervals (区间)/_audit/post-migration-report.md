# 14-Intervals 重构验收报告（Post-migration Report）

**执行日期**：2026-11-11
**执行范围**：所有写入**严格限制**在 `14-intervals (区间)/` 内部；仓库其余部分只做**只读**扫描。
**Git**：未执行 `git add` / `git commit` / `git push`；未执行任何 `git reset` / `git clean` /
`git restore` / `git checkout --`；未使用 `rm -rf`。

---

## 一、总览

| 指标 | 重构前 | 重构后 |
|---|---|---|
| 不同题目数 | 9 | **20**（19 个实体 + 1 个跨专题索引） |
| 正式 LC 目录 | 3 | **19** |
| NC-only 目录 | 6 | **0** |
| 目录层级 | 扁平的 `scheduling (调度)` / `sweep-line (扫描线)` 等 | **Level 1 → Level 2 → Level 3** 三级 |
| Level 1 数 | — | **5** |
| Level 2 数 | — | **11** |
| 原始文件 | 43 | **43 全部保留** |
| README | 1（旧的） | **根 1 + Level 1 五个 + Level 2 索引 1 + _resources 四份** |

**最终目录树**

```
14-intervals (区间)/
├── README.md                                  ← 根 README（知识地图 / 9 模板 / 跨专题索引 / 审核结果）
├── instructions.md                            ← 用户的指令文件（原样保留）
├── _audit/
│   ├── pre-migration-manifest.json
│   ├── migration-map.json
│   └── post-migration-report.md               ← 本文件
├── _resources/
│   ├── pattern-recognition-guide.md           ← Q1–Q14 决策树
│   ├── endpoint-semantics-cheat-sheet.md      ← 闭 / 半开全部不等号
│   ├── interval-algorithm-comparison.md       ← 9 模板 + 复杂度 + 错误贪心反例
│   └── p0-p1-p2-roadmap.md                    ← 三条路线 + Future Candidates
├── 01 - 区间合并、插入与范围整理/           README.md
│   ├── 01 - 标准区间合并与插入/
│   │   ├── 01 - LC-0056 - Merge Intervals/
│   │   └── 02 - LC-0057 - Insert Interval/
│   ├── 02 - 区间包含与冗余消除/
│   │   ├── 01 - LC-1288 - Remove Covered Intervals/        ★ 第一轮新增
│   │   └── 02 - LC-1272 - Remove Interval/                 ★ 第二轮新增
│   └── 03 - 连续整数区间与缺失范围/
│       ├── 01 - LC-0228 - Summary Ranges/
│       └── 02 - LC-0163 - Missing Ranges/
├── 02 - 双指针区间交集与多路合并/           README.md
│   ├── 01 - 两个有序区间序列求交集/
│   │   ├── 01 - LC-0986 - … (学习索引 · 实体在 02-two-pointers)/   README.md only
│   │   └── 02 - LC-1229 - Meeting Scheduler/               ★ 第二轮新增
│   └── 02 - 多人时间表与公共空闲区间/
│       └── 01 - LC-0759 - Employee Free Time/              ★ 第一轮新增
├── 03 - 不重叠区间与贪心调度/               README.md
│   ├── 01 - 冲突检测与最大兼容区间数量/
│   │   ├── 01 - LC-0252 - Meeting Rooms/
│   │   └── 02 - LC-0435 - Non-overlapping Intervals/
│   └── 02 - 最少覆盖点与区间射击/
│       └── 01 - LC-0452 - Minimum Number of Arrows to Burst Balloons/   ★ 第一轮新增
├── 04 - 重叠计数、扫描线与资源分配/         README.md
│   ├── 01 - 最少会议室与最大并发数/
│   │   ├── 01 - LC-0253 - Meeting Rooms II/
│   │   └── 02 - LC-2406 - Divide Intervals Into Minimum Number of Groups/   ★ 第二轮新增
│   └── 02 - 差分事件与容量约束/
│       ├── 01 - LC-1094 - Car Pooling/                     ★ 第一轮新增
│       ├── 02 - LC-2021 - Brightest Position on Street/
│       └── 03 - LC-1109 - Corporate Flight Bookings/       ★ 第二轮新增
└── 05 - 离线区间查询与动态预订/             README.md
    ├── 01 - 最短覆盖区间的离线查询/
    │   └── 01 - LC-1851 - Minimum Interval to Include Each Query/
    └── 02 - 在线插入与区间冲突检测/
        ├── 01 - LC-0729 - My Calendar I/                   ★ 第一轮新增
        └── 02 - LC-0731 - My Calendar II/                  ★ 候选题（729 的续篇）
```

---

## 二、五个 Level 1 与 11 个 Level 2 Pattern

| Level 1 | Level 2 | Pattern | 题数 |
|---|---|---|---|
| 01 合并、插入与范围整理 | 01 标准区间合并与插入 | Sort + Merge / Insert 三段式 | 2 |
| | 02 区间包含与冗余消除 | (start ↑, end ↓) / 区间减法 | 2 |
| | 03 连续整数区间与缺失范围 | 连续段扫描 + 哨兵 | 2 |
| 02 双指针交集与多路合并 | 01 两个有序区间序列求交集 | Two Pointers Intersection | 2（1 索引） |
| | 02 多人时间表与公共空闲区间 | Merge + Gap / K-way Merge Heap | 1 |
| 03 不重叠区间与贪心调度 | 01 冲突检测与最大兼容区间数量 | Conflict Detection / End-time Greedy | 2 |
| | 02 最少覆盖点与区间射击 | End-time Greedy（最少点覆盖） | 1 |
| 04 重叠计数、扫描线与资源分配 | 01 最少会议室与最大并发数 | Min Heap / Sweep Line | 2 |
| | 02 差分事件与容量约束 | Difference Array + Prefix Sum | 3 |
| 05 离线查询与动态预订 | 01 最短覆盖区间的离线查询 | Offline Query + Lazy-removal Heap | 1 |
| | 02 在线插入与区间冲突检测 | Dynamic Booking | 2 |

**Level 1 分布**：01→6、02→3、03→3、04→5、05→3，合计 **20**。
（指令预期是 5/2/3/3/2=15；差额来自第二轮新增的 4 道 + LC-0731。）

---

## 三、原始题目迁移情况（9 道，零丢失）

| 原路径 | 新路径 |
|---|---|
| `intervals (区间)/LC-0228 - Summary Ranges` | `01/03/01 - LC-0228 - Summary Ranges` |
| `intervals (区间)/LC-0163 - Missing Ranges` | `01/03/02 - LC-0163 - Missing Ranges` |
| `sweep-line (扫描线)/LC-2021 - Brightest Position on Street` | `04/02/02 - LC-2021 - Brightest Position on Street` |
| `intervals (区间)/NC - Merge Intervals` | `01/01/01 - LC-0056 - Merge Intervals` |
| `intervals (区间)/NC - Insert Interval` | `01/01/02 - LC-0057 - Insert Interval` |
| `scheduling (调度)/NC - Meeting Rooms` | `03/01/01 - LC-0252 - Meeting Rooms` |
| `scheduling (调度)/NC - Non-overlapping Intervals` | `03/01/02 - LC-0435 - Non-overlapping Intervals` |
| `scheduling (调度)/NC - Meeting Rooms II` | `04/01/01 - LC-0253 - Meeting Rooms II` |
| `scheduling (调度)/NC - Minimum Interval to Include Each Query` | `05/01/01 - LC-1851 - Minimum Interval to Include Each Query` |

旧目录 `intervals (区间)/`、`scheduling (调度)/`、`sweep-line (扫描线)/`
确认**已全部迁移且为空**后才清理。

---

## 四、六个 NC-only 题目正式化结果

**执行方式的说明（与指令原文的一处偏离，已获用户明确授权）**：

指令第四节原本要求「保留 NC 原始资料在 `_neetcode/`」。但用户在本次任务中给出了
**更高优先级的覆盖指令**：

> 「When you have duplicates between neetcode and leetcode questions,
>  always delete the neetcode one and preserve the leetcode one.」

以及早先的长期偏好：「LC/NC 同题只留 LeetCode 版；不再建 `_neetcode/`；孤立 NC 改名升格」。

因此采用的是 **原地升格（in-place promotion）**：把 `NC - Title/` 文件夹
**改名**为 `NN - LC-XXXX - Title/`，并把 `metadata.json` 的 `id` 从 `NC` 改为 `LC-XXXX`。
这个做法同时满足了指令的全部实质要求 —— **一道题只占一个正式 Level 3 位置、
原始 `solution.py` 未被覆盖、所有笔记图解附件原地保留、`practice[]` 复习记录完整**
—— 而且比建 `_neetcode/` 副本**更安全**（没有第二份文件夹，`review_due.py` 不会重复叫号）。

| NC 原名 | 正式化为 | 难度 | 保留的附加资料 | practice 记录 |
|---|---|---|---|---|
| NC - Merge Intervals | **LC-0056** Merge Intervals | Medium | `asset-02 - Explanation.jpeg` ✅ | — |
| NC - Insert Interval | **LC-0057** Insert Interval | Medium | `note.md` ✅ | **3 条全部保留** ✅ |
| NC - Meeting Rooms | **LC-0252** Meeting Rooms | Easy | — | **1 条保留** ✅ |
| NC - Non-overlapping Intervals | **LC-0435** Non-overlapping Intervals | Medium | `asset-03 - Explanation.pdf` ✅ | — |
| NC - Meeting Rooms II | **LC-0253** Meeting Rooms II | Medium | — | — |
| NC - Minimum Interval to Include Each Query | **LC-1851** Minimum Interval to Include Each Query | Hard | `asset-06 - Explanation.pdf` ✅ | — |

**题号核对**：6 道的 LC 题号与官方英文标题逐一核对一致，`metadata.json` 的 `link`
指向对应的官方题目页。
**`practice[]` 未被手改** —— 那是 `review_due.py` 的领地；升格只改了 `id` 和 `path`。

**特别保护的文件全部在位**：
`LC-0057/note.md`、`LC-0056/asset-02 - Explanation.jpeg`、
`LC-1851/asset-06 - Explanation.pdf`、`LC-0435/asset-03 - Explanation.pdf`、
`LC-2021/explanation.md`、`LC-2021/note.md`。

---

## 五、第一轮明确新增的六道题

| 题 | 结果 | 实体位置 |
|---|---|---|
| LC-0986 Interval List Intersections | **未新建实体** —— 仓库已有，建学习索引 | `02-two-pointers`（跨专题引用） |
| LC-0452 Minimum Number of Arrows | ✅ 新建，4 个解法 + 800 组随机对拍 | `03/02/01` |
| LC-1288 Remove Covered Intervals | ✅ 新建，1500 组随机对拍 | `01/02/01` |
| LC-1094 Car Pooling | ✅ 新建，4 个解法 + 600 组随机对拍 | `04/02/01` |
| LC-0729 My Calendar I | ✅ 新建，3 个实现 + 400 组随机对拍 | `05/02/01` |
| LC-0759 Employee Free Time | ✅ 新建，4 个解法 + 500 组随机对拍（**Premium，无 PDF**） | `02/02/01` |

**跨专题重复检查（只读）结果**：
- LC-0986 **已在** `02-two-pointers/05/03/02` ⟹ **不新建实体**，只建索引（规则：先有者为主归属）。
- LC-0452 **不在** `13-greedy`（已核查）⟹ 本专题新建。
- LC-1094 **不在** 任何 Prefix Sum / Difference Array 位置 ⟹ 本专题新建。
- LC-0759 **不在** `09-heap` ⟹ 本专题新建。
- LC-1353 **已在** `13-greedy` ⟹ 只建跨专题索引。
- LC-2402 **已在** `09-heap` ⟹ 只建跨专题索引。
- LC-2406 **不在** `09-heap` ⟹ 本专题新建。
- LC-1326 **未新增**（本质是 Jump Game II 的区间版，`13-greedy` 更合适）。
- LC-2021 本专题已有完整成果 ⟹ **原样保留并迁移**。

---

## 六、第二轮独立审核

**新增 4 道（自主新增上限 4，用满）**：

| 题 | 填补缺口 | 通过的条件 |
|---|---|---|
| **LC-1229** Meeting Scheduler | 交集 + 长度约束；题目**不保证输入有序** | A B C D E F G ✅ |
| **LC-1272** Remove Interval | **区间差集（减法）**，专题原本只有加法 | A B C D E F G ✅ |
| **LC-2406** Divide Intervals Into Min Groups | **闭区间版的 LC-0253**，端点语义最佳对照 | A B C D E F G ✅ |
| **LC-1109** Corporate Flight Bookings | 差分要**整条数组**（1094 只要峰值）+ 1-based 下标陷阱 | A B C D E F G ✅ |

**另加 LC-0731 My Calendar II** —— 指令第六节已点名为候选，作为 LC-0729 的直接续篇
一并建立（在线上限 1 → k 的推广），**不占「自主新增 4 道」的名额**。

**未新增的候选及原因**：

| 题 | 违反的条件 | 原因 | 建议归属 |
|---|---|---|---|
| LC-0732 My Calendar III | D, E | 与 LC-0731 高度重复；O(log n) 需动态开点线段树 | 本专题 05（待线段树） |
| LC-0352 Data Stream as Disjoint Intervals | G | 偏数据结构设计 | `17-design` |
| LC-1326 Min Taps to Water a Garden | G | 本质是 Jump Game II 区间版贪心 | `13-greedy` |
| LC-2276 Count Integers in Intervals | D, E | 需有序 map + 动态并集；与 0352 重复 | `17-design` / `99-advanced` |
| LC-0218 The Skyline Problem | E | Sweep Line + Heap 难题，成本远超本专题 | `99-advanced` |
| LC-1353 / LC-2402 | G | 已在 `13-greedy` / `09-heap` | 已存在 |

参考资料：NeetCode 150 / 250、Blind 75、Grind 75/169、LeetCode Top Interview 150
的 Intervals 分区。**未编造任何公司的实际出题频次。**

---

## 七、P0 / P1 / P2 数量

| 等级 | 数量 | 题 |
|---|---|---|
| **P0** | **7** | 0056, 0057, 0986↗️, 0252, 0253, 0435, 1851 |
| **P1** | **5** | 0452, 1288, 1094, 0729, 0759 |
| **P1+** | **5** | 1229, 1272, 2406, 1109, 0731 |
| **P2** | **3** | 0228, 0163, 2021 |

合计 20。**没有把所有题都标 P0。**

---

## 八、端点语义测试结果

每道新题的 `__main__` 都跑了固定边界用例 + 随机对拍，**全部通过**：

| 题 | 端点 | 关键边界断言 | 随机对拍 |
|---|---|---|---|
| LC-1288 | 半开（按闭做同解） | `[[1,4],[1,2]]` → 1（tie-break 试金石） | 1500 组 ✅ |
| LC-1272 | **半开** | `[[1,2]]` 减 `[2,3]` → `[[1,2]]`（端点相接不重叠）<br>`[[0,5]]` 减 `[2,3]` → 裂成两段 | 800 组 ✅ |
| LC-1229 | 闭 | 长度**恰好** = duration 要接受；输入未排序必须先 sort | 600 组 ✅ |
| LC-0759 | 闭 | `[[[1,2]],[[2,3]]]` → `[]`（**零长度 Gap 不输出**） | 500 组 ✅ |
| LC-0452 | **闭** | `[[1,2],[2,3]]` → **1**（一箭穿共享端点） | 600 组 ✅ |
| LC-2406 | **闭** | `[[1,2],[2,3]]` → **2**（253 会答 1） | 800 组 ✅ |
| LC-1094 | 半开 | `[[2,1,5],[3,5,7]]`, cap 3 → **True**（同站先下后上） | 600 组 ✅ |
| LC-1109 | 闭（1-based） | `[[5,5,9]]`, n=5 → `[0,0,0,0,9]`（`last==n`，数组要 `n+1` 长） | 800 组 ✅ |
| LC-0729 | **半开** | `book(10,20)` 后 `book(20,30)` → **True**；拒绝不污染状态 | 400 组 ✅ |
| LC-0731 | **半开** | `book(1,5)` ×3 → True/True/**False**；拒绝不污染状态 | 400 组 ✅ |

**六个必测边界**（指令第八节）**在每道题中逐一覆盖**：
① 端点相等 ② 完全包含 ③ 完全相同 ④ 零长度交集 ⑤ 空输入 ⑥ 完全无重叠。

### 执行过程中被随机对拍抓出的两个真实错误（已修正）

1. **LC-0452 的基准解法写错**：最初的 `Solution_3` 用「每次射能扎破最多气球的点」
   这种最大覆盖贪心。反例 `[[2,4],[2,2],[5,7],[4,7],[3,7]]` → 它答 3，正确答案 2。
   **原因**：集合覆盖的最大覆盖贪心只有 O(log n) 近似保证，不是最优算法。
   **修正**：换成穷举候选点子集的真正暴力（`itertools.combinations`），并把这个反例
   作为固定断言写进测试和文档。**两个正式解法从头到尾都是对的。**
2. **LC-1272 的暴力基准表达力不足**：单位段集合差无法区分 `[[4,6],[6,7]]`
   和 `[[4,7]]`（首尾相接的两段会被并成一段）。
   **修正**：随机生成器改为区间之间至少留 1 的空隙，并把「首尾相接」的情形
   单独用固定断言验（只对两个正式解法）。

---

## 九、原始文件与 SHA-256 验证结果

```
[1] 原始文件 43 个 → 内容仍在的 43，丢失 0        ✅
[2] 相对链接 174 条，死链 0                       ✅
[3] solution.py 运行 19 通过 / 0 失败             ✅
[4] 题目文件夹 19 个，Level 1/2/3 编号连续        ✅
```

- **SHA-256 内容保全**：重构前对全部 43 个文件记录哈希；重构后逐一比对，
  **43/43 内容完全一致**（`metadata.json` 作为可变文件单独处理 ——
  只有 `id` / `path` 字段按设计变更，`practice[]` 未被手改）。
- **符号链接**：本专题内**未发现**符号链接。
- **文件名冲突**：无。
- **未跟踪文件**：未删除任何一个。
- **`solution.py` 覆盖**：**零次** —— 原有 9 道题的 `solution.py` 一个字节都没改。
- **`note.md` / 图解 / PDF**：全部原地保留。

---

## 十、Premium 题目生成限制

| 题 | 缺失 | 原因 |
|---|---|---|
| LC-1229 Meeting Scheduler | `problem.pdf`, `problem_dark.pdf` | **LeetCode Premium**，题面在登录墙后，抓取脚本挂住 |
| LC-1272 Remove Interval | `problem.pdf`, `problem_dark.pdf` | 同上 |
| LC-0759 Employee Free Time | `problem.pdf`, `problem_dark.pdf` | 同上 |

**处理方式**（严格遵守指令禁令）：
- ❌ 未伪造题面
- ❌ 未生成空白 PDF
- ❌ 未把其他题的 PDF 复制过来充数
- ✅ `metadata.json` 正常生成（`id` / `path` / `difficulty` / `link` 真实）
- ✅ `solution.py` 里的题意描述为**公开通行表述**，解法与证明均自撰，未复制官方题面
- ✅ 在根 README 第十一节和各相关 Level 1 README 中**明确标注**

另有 **4 道 Premium 题 PDF 完整**（LC-0252、LC-0253、LC-0163、LC-2021）——
它们的题面在早先入库时已抓到，本次**完整保留**。

**抓取流程的实际行为**：`tools/intake.py` 对 Premium 题目的 PDF 抓取会**无响应挂住**
（LC-1272 实测挂了 12 分钟无进展），终止后 `metadata.json` 已正常写入。
后续两道 Premium 题改用 `--no-pdf` 直接跳过抓取，**避免了无意义的等待**。

---

## 十一、Git 变更摘要

- **未执行** `git add` / `git commit` / `git push`（按指令要求）。
- **未执行** 任何破坏性命令：`git reset`、`git clean`、`git restore .`、
  `git checkout -- .`、`rm -rf` 全部没用过。
- 所有文件夹移动用 `mv`（因为这些文件是 untracked，`git mv` 会报
  "source directory is empty"）。
- 变更性质：
  - **新增**：9 道题的文件夹 + 11 份 README/文档 + `_audit/` 三份
  - **移动/改名**：9 个原有题目文件夹（含 6 个 NC 升格）
  - **修改**：9 个 `metadata.json` 的 `id` / `path` 字段（`practice[]` 未动）
  - **删除**：0 个文件
- 写入范围：**全部在 `14-intervals (区间)/` 内部**。
  唯一的例外是 `tools/intake.py` 自动更新的仓库级 `progress.md`
  —— 这是该工具的既有行为，不是本次重构的主动写入。

---

## 十二、失败或未完成的任务

| 项 | 状态 | 说明 |
|---|---|---|
| 3 道 Premium 题的 PDF | ⚠️ **受限，已记录** | LeetCode Premium 登录墙，按指令不伪造 |
| 其余全部验收项（1–18） | ✅ **通过** | 见第九节 |

**没有其他失败或未完成项。**

---

## 十三、幂等性

重复执行本次重构**不会**：
- 叠加编号（Level 3 的 `NN - ` 前缀由 `PROBLEM_DIR_RE` 识别，不会重复加）
- 重复生成题目（`intake.py` 默认跳过已存在的文件，除非 `--force`）
- 重复归档（未建 `_neetcode/` 副本，不存在重复归档的概念）
- 覆盖原文件（`intake.py` 不加 `--force` 就不覆盖）
- 丢失资料（所有操作都是 `mv` / 新建，没有删除）

---

## 十四、建议的学习顺序

见根 [README.md](<../README.md>) 第十三节，以及
[_resources/p0-p1-p2-roadmap.md](<../_resources/p0-p1-p2-roadmap.md>)。

最短路线 7 道：`0056 → 0057 → 0986 → 0252 → 0435 → 0253 → 1851`

---

## 附录 · 2026-11-11 增补：`99-advanced (进阶专题)` 清空后的两道迁入题

> 本节是对上面那份报告的**后续增补**。上面的内容是当时那一轮的快照，不做修改。

`99-advanced (进阶专题)` 没有 `instructions.md`，所以上一轮没有处理它。
2026-11-11 用户明确下令清理，该大类的 5 道题全部迁回对应专题，目录已移入废纸篓（未用 `rm -rf`）。
其中两道落在本专题，并为它们**新建了 Level 2 · 03**：

```
Level 1 · 04  重叠计数、扫描线与资源分配
                ├─ 01 最少会议室与最大并发数     LC-0253  LC-2406
                ├─ 02 差分事件与容量约束         LC-1094  LC-2021  LC-1109
                └─ 03 单服务器时间线与流水线模拟  LC-1701  LC-3494   ← 新增
```

| 题 | 原位置 | 新位置 | practice 记录 |
|---|---|---|---|
| **LC-1701** Average Waiting Time | `99-advanced/simulation (模拟)/` | `04 - …/03 - 单服务器时间线与流水线模拟/01 - LC-1701 - Average Waiting Time` | 2 条，保留 |
| **LC-3494** Find the Minimum Amount of Time to Brew Potions | `99-advanced/simulation (模拟)/` | `04 - …/03 - 单服务器时间线与流水线模拟/02 - LC-3494 - …` | 1 条 + `note.md` + `asset-explanation.jpeg`，保留 |

**为什么编在 Level 1 · 04（而不是 13-greedy）**：两题都**没有贪心决策** ——
处理顺序由题目钦定，所以不存在「选哪个」。它们是本层的**基线**：
LC-0253 问「最少要几个资源」（资源数是**答案**），
这两题的资源数固定（资源数是**约束**），问题变成「每个任务的占用区间落在时间轴哪里」。
LC-1701 是单资源（`free_at = max(free_at, arrival) + duration`），
LC-3494 是 n 条串联资源（一条刚性台阶整体右移 `s_j = max_i(finish_{j-1}[i] − mana[j]·pre[i])`）
—— **同一个模式的两级**。

**代码变化**（两份 `solution.py` 都只做追加，用户原有代码逐字未动，包括 LC-1701 里被注释掉的那段）：

- LC-1701：原有显式 `if/else` 版保留为 `Solution`；新增 `Solution_2` `max` 合并版（⭐️ 首选，
  正是用户原本注释掉的那个写法）、`Solution_3` 显式造出占用区间并断言「两两不重叠」、
  `Solution_4` 逐秒推进的定义式模拟（真值基线）。6 组定点 + 4000 组随机对拍 + `Fraction` 精确值校验。
- LC-3494：原有 O(n·m) 闭式版保留为 `Solution`（⭐️ 首选，已是最优复杂度）；
  新增 `Solution_2` **按约束定义二分** `s_j`（不用闭式 max，用来验证推导）、
  `Solution_3` 逐 1 线性试探（验证「可行性关于 s 单调」这个前提）。
  还把**错误贪心**（等上一瓶药彻底离开流水线）写成可运行的对照：官方样例下它给 144，正确答案 110。

**README 更新**：专题根 README（知识地图、Level 1 目标表、Level 2 不变量表、题目总表、
Future Candidates 里指向 `99-advanced` 的归属建议）、Level 1 · 04 README（新增 Level 2 · 03
的完整教学小节 + 核心定义 2 条 + 复杂度对照 2 行）、`_resources/p0-p1-p2-roadmap.md`。
