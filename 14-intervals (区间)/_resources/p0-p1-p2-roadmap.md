# Intervals P0 / P1 / P2 学习路线

> P0 / P1 / P2 是**教学优先级**（学习依赖 + 模板覆盖面），
> **不代表任何公司的实际出题频次** —— 本文件不编造频次数据。

---

## P0 — 核心七题（必须闭着眼睛写出来）

这七道覆盖了 Intervals 的**全部核心模板**。练完就有了处理绝大多数区间题的基础。

| # | 题 | 模板 | 一句话必须记住 |
|---|---|---|---|
| 1 | [LC-0056 Merge Intervals](<../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>) | Sort + Merge | **start 升序**，`cur_end = max(cur_end, end)` |
| 2 | [LC-0057 Insert Interval](<../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>) | 三段式 | 输入已排序 ⟹ **O(n)，不要排序** |
| 3 | [LC-0986 Interval List Intersections](<../02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>) | Two Pointers | `left <= right`（闭区间，`[2,2]` 算交集） |
| 4 | [LC-0252 Meeting Rooms](<../03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/01 - LC-0252 - Meeting Rooms>) | Conflict Detection | `prev_end > cur_start` 才算冲突 |
| 5 | [LC-0253 Meeting Rooms II](<../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>) | Min Heap / Sweep | 答案 = **最大并发数** |
| 6 | [LC-0435 Non-overlapping Intervals](<../03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/02 - LC-0435 - Non-overlapping Intervals>) | End-time Greedy | **end 升序**（start 升序是错的） |
| 7 | [LC-1851 Min Interval to Include Each Query](<../05 - 离线区间查询与动态预订/01 - 最短覆盖区间的离线查询/01 - LC-1851 - Minimum Interval to Include Each Query>) | Offline + Heap | 堆顶要**先懒删除过期区间**才有效 |

**P0 建议顺序**：56 → 57 → 986 → 252 → 435 → 253 → 1851
（先学合并，再学插入，再学双指针，然后从「能否」到「最多」到「最少房间」，最后上离线查询 + 堆。）

---

## P1 — 标准面试路线（P0 + 这五题）

| # | 题 | 模板 | 为什么值得练 |
|---|---|---|---|
| 8 | [LC-0452 Minimum Arrows](<../03 - 不重叠区间与贪心调度/02 - 最少覆盖点与区间射击/01 - LC-0452 - Minimum Number of Arrows to Burst Balloons>) | End-time Greedy | 和 435 是同一贪心的两种计数，必须看穿 |
| 9 | [LC-1288 Remove Covered Intervals](<../01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/01 - LC-1288 - Remove Covered Intervals>) | (start ↑, end ↓) | 唯一需要 **end 降序** tie-break 的题 |
| 10 | [LC-1094 Car Pooling](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>) | Difference Array | 差分数组的入门题，跨专题复用极广 |
| 11 | [LC-0729 My Calendar I](<../05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>) | Dynamic Booking | 唯一的**在线**区间题 + 半开语义 |
| 12 | [LC-0759 Employee Free Time](<../02 - 双指针区间交集与多路合并/02 - 多人时间表与公共空闲区间/01 - LC-0759 - Employee Free Time>) | K-way Merge | 「空闲的交集 = 忙碌并集的 Gap」这个反转 |

**P0 + P1 = 12 道**，这是标准面试覆盖面。

---

## P1+ — 第二轮审核新增的四道（每道都填了一个真实缺口）

| # | 题 | 填的缺口 | 挂在哪 |
|---|---|---|---|
| 13 | [LC-1229 Meeting Scheduler](<../02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/02 - LC-1229 - Meeting Scheduler>) | 交集 **+ 长度约束**；且题目**不保证输入有序** | 986 之后 |
| 14 | [LC-1272 Remove Interval](<../01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/02 - LC-1272 - Remove Interval>) | **区间差集（减法）**，专题原本只有加法 | 1288 之后 |
| 15 | [LC-2406 Divide Intervals Into Min Groups](<../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>) | **闭区间版的 253** —— 端点语义的最佳对照题 | 253 之后 |
| 16 | [LC-1109 Corporate Flight Bookings](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/03 - LC-1109 - Corporate Flight Bookings>) | 差分数组要**整条前缀和数组**（1094 只要峰值）+ 1-based 下标陷阱 | 1094 之后 |
| 17 | [LC-0731 My Calendar II](<../05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/02 - LC-0731 - My Calendar II>) | 在线重叠上限从 1 推广到 k | 729 之后 |

> 第二轮**自主新增上限是 4 道**：1229、1272、2406、1109。
> LC-0731 原本就在候选名单里（指令第六节点名了它），
> 作为 LC-0729 的直接续篇一起建了，不占「自主新增」的 4 个名额。

---

## P2 — 存档与补充

| # | 题 | 为什么是 P2 |
|---|---|---|
| 18 | [LC-0228 Summary Ranges](<../01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/01 - LC-0228 - Summary Ranges>) | 不是真正的区间算法，是连续段扫描 |
| 19 | [LC-0163 Missing Ranges](<../01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/02 - LC-0163 - Missing Ranges>) | 同上；哨兵边界是唯一难点 |
| 20 | [LC-2021 Brightest Position on Street](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/02 - LC-2021 - Brightest Position on Street>) | 差分数组的变体，1094 练过之后就是送分题 |

---

## 三条路线

```
【最短路线 · 7 道】只求把模板学完
  56 → 57 → 986 → 252 → 435 → 253 → 1851

【标准面试路线 · 12 道】P0 + P1
  56 → 57 → 986 → 252 → 435 → 452 → 1288 → 253 → 1094 → 1851 → 729 → 759

【完整路线 · 20 道】按 Level 1 顺序刷，端点语义对照最完整
  Level 1 → 56 → 57 → 1288 → 1272 → 228 → 163
  Level 2 → 986 → 1229 → 759
  Level 3 → 252 → 435 → 452
  Level 4 → 253 → 2406 → 1094 → 1109 → 2021
  Level 5 → 1851 → 729 → 731
```

**配对练习建议**（把端点语义的坑一次打穿）：
- `253` 紧跟 `2406` —— 半开 vs 闭，同一算法
- `435` 紧跟 `452` —— 同一贪心，两种计数
- `57` 紧跟 `1272` —— 区间的加法 vs 减法
- `1094` 紧跟 `1109` —— 差分要峰值 vs 要整条数组
- `729` 紧跟 `731` —— 上限 1 vs 上限 2
- `228` 紧跟 `163` —— 有什么 vs 缺什么

---

## Future Candidates（本次**未**新增，附原因）

| 题 | 不新增的原因 | 将来放哪 |
|---|---|---|
| **LC-0732 My Calendar III** | 和 LC-0731 高度重复（违反条件 D）；真要 O(log n) 得上动态开点线段树，记忆成本超出本专题 | 本专题 Level 1 · 05，等线段树学完 |
| **LC-0352 Data Stream as Disjoint Intervals** | 更偏**数据结构设计**（违反条件 G）；`17-design` 是更合适的主归属 | `17-design` |
| **LC-1326 Min Taps to Open to Water a Garden** | 本质是 **Jump Game II 的区间版贪心**（违反条件 G）；`13-greedy` 已有 LC-0045 的完整教学 | `13-greedy` |
| **LC-2276 Count Integers in Intervals** | 需要有序 map + 动态并集维护，记忆成本偏高（违反条件 E），且和 LC-0352 重复 | `17-design`（`99-advanced` 已于 2026-11-11 清空） |
| **LC-0218 The Skyline Problem** | Sweep Line + Heap 的难题，学习成本远超本专题其他题（违反条件 E）；适合单独专题 | 将来**单独建专题** |
| LC-1353 Maximum Number of Events That Can Be Attended | **已在 `13-greedy`**（Heap + Greedy Scheduling 是它的主归属） | 已存在，见跨专题索引 |
| LC-2402 Meeting Rooms III | **已在 `09-heap`**（两个堆的调度，Heap 是主归属） | 已存在，见跨专题索引 |

**判断标准**（指令第六节的 A–G）：
A 填补 Pattern 缺口 · B 面试代表性 · C 可迁移性 · D 不与现有题高度重复 ·
E 记忆成本合理 · F 能说明正确性不变量 · G 没有其他专题更合适的主归属。
