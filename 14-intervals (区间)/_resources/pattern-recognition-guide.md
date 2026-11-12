# Interval Pattern Recognition Guide（区间题型识别指南）

> 读完题干，按顺序问这几个问题。**这些规则不互斥** ——
> 一道题经常同时命中多条（例如 LC-0253 = Q7 + Q8，LC-1851 = Q10 + Heap）。

---

## 决策树

### Q1：需要把所有重叠区间**合并**起来吗？
→ **Sort + Merge**（模板 1）。按 **start 升序**排，维护 `cur_end = max(cur_end, end)`。
📍 [LC-0056 Merge Intervals](<../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>)

### Q2：往一个**已排序、互不重叠**的列表里**插入一个**新区间？
→ **Insert Interval 三段式**（模板 2）：左边原样 → 合并相交的 → 右边原样。
**输入已排序 ⟹ O(n)，不要再排序。**
📍 [LC-0057 Insert Interval](<../01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>)
🔁 反向操作（**减**一个区间）→ [LC-1272 Remove Interval](<../01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/02 - LC-1272 - Remove Interval>)

### Q3：求**两个有序区间序列的交集**？
→ **Two Pointers**（模板 3）。`left=max(s)`、`right=min(e)`，**弹掉 end 更小的那个**。O(m+n)。
📍 [LC-0986 Interval List Intersections](<../02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>)
➕ 再加一个长度约束 → [LC-1229 Meeting Scheduler](<../02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/02 - LC-1229 - Meeting Scheduler>)
🔀 推广到 k 个序列 → [LC-0759 Employee Free Time](<../02 - 双指针区间交集与多路合并/02 - 多人时间表与公共空闲区间/01 - LC-0759 - Employee Free Time>)

### Q4：要**最大化**互不冲突的区间数量？
→ **End-time Greedy**（模板 4）。按 **end 升序**排，`start >= last_end` 就取。
📍 [LC-0435 Non-overlapping Intervals](<../03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/02 - LC-0435 - Non-overlapping Intervals>)

### Q5：要用**尽可能少的点**扎破/覆盖所有区间？
→ 同样是 **End-time Greedy**，把点放在**当前区间的 end** 上。
**答案 = Q4 的最大兼容区间数**（同一个贪心的两种计数方式）。
📍 [LC-0452 Minimum Number of Arrows](<../03 - 不重叠区间与贪心调度/02 - 最少覆盖点与区间射击/01 - LC-0452 - Minimum Number of Arrows to Burst Balloons>)
⚠️ **不要**用「每次挑能扎最多气球的点」—— 最大覆盖贪心对集合覆盖**不最优**。

### Q6：只问**所有会议能不能塞进一间房**？
→ **Conflict Detection**：按 start 排序，相邻检查 `prev_end > cur_start` 就冲突。O(n log n)。
📍 [LC-0252 Meeting Rooms](<../03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/01 - LC-0252 - Meeting Rooms>)

### Q7：要**最少房间数** / **最大并发数** / **最少分组数**？
→ **Max Overlap**。三种等价做法：**Min Heap**（模板 5）、**Sweep Line**（模板 6）、**差分数组**（模板 7）。
📍 [LC-0253 Meeting Rooms II](<../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>)（半开区间）
📍 [LC-2406 Divide Intervals Into Min Groups](<../04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>)（**闭区间**，不等号差一个 `=`）

### Q8：涉及**大量开始/结束事件**，要沿坐标轴扫？
→ **Sweep Line**（模板 6）。`(pos, ±1)` 排序后扫；**tie-break 决定端点语义**。
📍 [LC-2021 Brightest Position on Street](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/02 - LC-2021 - Brightest Position on Street>)

### Q9：要**累计多个区间对坐标的影响**（区间加）？
→ **Difference Array + 前缀和**（模板 7）。`diff[l] += v`，半开在 `end` 减、闭区间在 `right+1` 减。
📍 [LC-1094 Car Pooling](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>)（要**峰值**）
📍 [LC-1109 Corporate Flight Bookings](<../04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/03 - LC-1109 - Corporate Flight Bookings>)（要**整条数组**）

### Q10：有**多个查询点**，每个要「最小的覆盖它的区间」？
→ **Offline Sorting + Min Heap**（模板 8）。查询按坐标排序，区间按 start 排序，
堆按长度排序 + **懒删除**过期区间。
📍 [LC-1851 Minimum Interval to Include Each Query](<../05 - 离线区间查询与动态预订/01 - 最短覆盖区间的离线查询/01 - LC-1851 - Minimum Interval to Include Each Query>)

### Q11：要**动态新增**区间并在冲突时**拒绝**？
→ **Calendar Design**（模板 9）。在线维护已接受区间；拒绝**不能污染状态**。
📍 [LC-0729 My Calendar I](<../05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>)（上限 1）
📍 [LC-0731 My Calendar II](<../05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/02 - LC-0731 - My Calendar II>)（上限 2）

### Q12：**端点允许相等吗？**
→ **先核对 Closed / Half-open Semantics**，再写不等号。
📍 [Endpoint Semantics Cheat Sheet](<./endpoint-semantics-cheat-sheet.md>)
这一条**每道题都要问**，而且应该**第一个**问。

### 补充 Q13：要判断「谁被谁包含」/ 删掉冗余区间？
→ 排序键是 **(start 升序, end 降序)**，扫描维护 `max_end`。
📍 [LC-1288 Remove Covered Intervals](<../01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/01 - LC-1288 - Remove Covered Intervals>)

### 补充 Q14：输入是**连续整数**而不是区间，要输出区间？
→ **连续段扫描**（不是真正的区间算法，但常和区间题一起考）。
📍 [LC-0228 Summary Ranges](<../01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/01 - LC-0228 - Summary Ranges>)（输出**存在的**段）
📍 [LC-0163 Missing Ranges](<../01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/02 - LC-0163 - Missing Ranges>)（输出**缺失的**段）
⚠️ **这两道不是同一题**：228 要「有什么」，163 要「缺什么」，而且 163 有 `lower`/`upper` 两个哨兵边界。

---

## 三秒速判表

| 题干关键词 | 模板 |
|---|---|
| merge / overlapping / union | Sort + Merge |
| insert / add one interval | Insert Interval 三段式 |
| intersection / both available / common | Two Pointers |
| maximum number of non-overlapping / minimum removals | End-time Greedy |
| minimum number of arrows / points / taps | End-time Greedy（最少点覆盖） |
| can attend all meetings | Conflict Detection |
| minimum rooms / minimum groups / maximum concurrent | Max Overlap（Heap / Sweep / 差分） |
| capacity / seats / passengers / brightness | Difference Array |
| for each query / smallest interval containing | Offline Query + Min Heap |
| book / calendar / double booking | Dynamic Booking |
| remove covered / redundant | (start ↑, end ↓) + max_end |
| summary ranges / missing ranges | 连续段扫描 |

---

## 排序键速查（选错就全错）

| 想要 | 排序键 |
|---|---|
| 并集 / 最大并发 | **start 升序** |
| 最大兼容数 / 最少覆盖点 | **end 升序** |
| 判断包含关系 | **start 升序，end 降序** |
| 事件扫描（半开语义） | `(pos, delta)` —— `-1` 先 |
| 事件扫描（闭区间语义） | `(pos, -delta)` —— `+1` 先 |
| 离线查询 | 查询按坐标升序，区间按 start 升序 |
