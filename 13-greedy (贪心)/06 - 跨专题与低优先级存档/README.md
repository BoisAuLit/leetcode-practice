# Level 1 · 06 跨专题与低优先级存档

## 用途
保留已有学习成果，但不把「主归属在别处」或「其实不是贪心」的题放进主线。
本章全部 **P2**。

## 01 - Graph Search 而非标准 Greedy（LC-1306 Jump Game III）

**它不是贪心。**

| | LC-0055 / LC-0045 | LC-1306 本题 |
|---|---|---|
| 跳跃方向 | **只能向前** | **可以向左也可以向右** |
| 能贪心吗 | **能**（维护最远可达） | **不能** |
| 解法 | 线性扫描 | **BFS / DFS + visited** |

**为什么不能贪心**：可以往回跳 ⟹ 可达关系不再单调
⟹ 「最远可达」这个量失去意义，必须真正搜索整张图。

它本质上是**隐式图上的可达性搜索**，和
[11-graphs 的状态图 BFS](<../../11-graphs (图论)/01-graph-modeling (阶段 0 · 建图、隐式图、状态图)/state-graph-bfs (状态图 BFS：一个状态就是一个点)>)
是同一类问题（点 = 下标，边 = `i ± arr[i]`）。

**放在这里是为了提醒**：Jump Game 系列到了 III 就**换算法了**，
不要看到「Jump Game」就去套 reach。

## 02 - String Segmentation 与 Jump Game 迁移

### LC-3292 Minimum Number of Valid Strings to Form Target II（P2）
LC-3291 的加强版（n 更大），需要 **Z-function / 后缀自动机**级别的工具
来快速算「从每个位置出发最长能匹配多长」，然后套「区间覆盖 ⟹ 跳跃」的贪心。

**它和 LC-0045 的联系很漂亮**：
算出每个位置的 `reach[i]`（从 i 出发最远能覆盖到哪）之后，
**就是 LC-1024 Video Stitching / LC-0045 Jump Game II**。
难点全在「怎么快速算 reach」这个字符串匹配部分，贪心部分是现成的。

### LC-3291 → **跨专题索引**
实体目录在 [08-tries](<../../08-tries (字典树、前缀树)/04 - Trie + DP 与字符串划分/01 - Trie 加速字符串划分/01 - LC-3291 - Minimum Number of Valid Strings to Form Target I>)
（那份有 note.md、讲解图和 4 条复习记录）。
本专题 Cluster 里的那份已归档为下面 `03` 里的「变体 · …」。

## 03 - 题号冲突与非 Greedy 归档

### LC-2651 Calculate Delayed Arrival Time（P2）
一行取模：`(arrivalTime + delayedTime) % 24`。
**完全不是贪心**，纯粹是个取模练习。放这里只是为了保留资料。

### 两个「变体 · …」归档目录

| 目录 | 为什么在这里 |
|---|---|
| `变体 · LC-0045 - Jump Game II (Cluster 版，含 DP 与记忆化)` | LC-0045 的正式位置是 `01/02/01`。这份的三种解法（贪心 / 记忆化 / DP）已全部并入正式位置；目录名刻意改成「变体 · …」，不再匹配 `LC-xxxx - ` 前缀 ⟹ **不进复习队列**，但文件一个没删 |
| `变体 · LC-3291 - Min Number Valid Str Form Target I (正式目录在 12-DP)` | 同理，LC-3291 的正式位置在 08-tries |

> **「变体 · 」这个前缀的作用**：让 `review_due.py` 的复习队列里一道题只出现一次，
> 同时完整保留另一份实现、PDF 和笔记。全仓库统一用这个约定
>（11-graphs 的六组同题多算法也是这么处理的）。

## 为什么这几道不进主线

| 题 | 原因 |
|---|---|
| LC-1306 | **不是贪心**，是图上的可达性搜索 |
| LC-3292 | 贪心部分是现成的，难点在字符串匹配（Z-function），学习成本高 |
| LC-2651 | 一行取模，不构成任何 Pattern |
| 两个变体目录 | 重复题号，正式位置在别处 |

## 保留承诺
本目录下所有 `solution.py`、`metadata.json`、PDF、笔记
在本次重构中都**完整保留**。唯一的改动是：
Cluster 版 LC-0045 里那行 `curr_end, curr_far = 0`（会 ValueError）改成了
`curr_end = curr_far = 0`，并加了注释说明。
