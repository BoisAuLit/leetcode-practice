# 14 - Intervals（区间）

> **一句话**：区间题只有两步 —— **先确定端点语义，再确定排序键**。
> 这两步定了，代码就只剩五行；这两步错了，再漂亮的代码都是错的。

**22 道题 · 5 个 Level 1 · 10 个核心模板**

---

## 一、完整知识地图

```
Level 1 · 01  区间合并、插入与范围整理      ← 地基：把区间整理成「排好序、互不相交」
                ├─ 01 标准区间合并与插入        LC-0056  LC-0057
                ├─ 02 区间包含与冗余消除        LC-1288  LC-1272
                └─ 03 连续整数区间与缺失范围    LC-0228  LC-0163

Level 1 · 02  双指针区间交集与多路合并      ← 多组区间之间的「公共部分」
                ├─ 01 两个有序区间序列求交集    LC-0986↗ LC-1229
                └─ 02 多人时间表与公共空闲区间  LC-0759

Level 1 · 03  不重叠区间与贪心调度          ← 从一堆区间里「选」或「扎」，答案是计数
                ├─ 01 冲突检测与最大兼容区间数量 LC-0252  LC-0435
                └─ 02 最少覆盖点与区间射击      LC-0452

Level 1 · 04  重叠计数、扫描线与资源分配    ← 视角转换：只关心「每个点被压了几次」
                ├─ 01 最少会议室与最大并发数    LC-0253  LC-2406
                ├─ 02 差分事件与容量约束        LC-1094  LC-2021  LC-1109
                └─ 03 单服务器时间线与流水线模拟 LC-1701✚ LC-3494✚

Level 1 · 05  离线区间查询与动态预订        ← 区间要反复被「问」或被「加」
                ├─ 01 最短覆盖区间的离线查询    LC-1851
                └─ 02 在线插入与区间冲突检测    LC-0729  LC-0731
```

↗️ = 实体在其他专题，本专题只放学习索引 · ✚ = 2026-11-11 从已清空的 `99-advanced (进阶专题)` 迁入

---

## 二、五个 Level 1 的学习目标

| Level 1 | 目标 | 排序键 | 输出形态 | 核心认识 |
|---|---|---|---|---|
| [**01** 合并、插入与范围整理](<./01 - 区间合并、插入与范围整理>) | 求**并集 / 差集**，把区间规范化 | **start ↑**（1288 加 end ↓） | 区间列表 | `cur_end = max(cur_end, e)` 不能省 |
| [**02** 双指针交集与多路合并](<./02 - 双指针区间交集与多路合并>) | 求**交集**（或并集的补） | 两边各自已有序 | 区间列表 | 弹掉 end 更小的那个 |
| [**03** 不重叠区间与贪心调度](<./03 - 不重叠区间与贪心调度>) | **最大兼容数 / 最少点数** | **end ↑** | 一个计数 | 排序键是 **end 不是 start** |
| [**04** 重叠计数与资源分配](<./04 - 重叠计数、扫描线与资源分配>) | **最大并发数**；以及**资源数固定时**的时间线推进 | start ↑ 或事件排序（Level 2 · 03 顺序由题目钦定） | 计数 / 一条数组 / 一个时刻 | 最少资源数 = 最大重叠数；资源数 = 1 且顺序固定 ⟹ 没有贪心空间，只剩 `max` 递推 |
| [**05** 离线查询与动态预订](<./05 - 离线区间查询与动态预订>) | 反复**查询 / 插入** | 查询 ↑ + 区间 start ↑ | 每次一个答案 | 懒删除只保证**堆顶**有效 |

**依赖顺序**：01 是地基（后面全都假设输入已规范化）→ 02 / 03 并列 → 04 → 05。

---

## 三、各 Level 2 的不变量

| Level 2 | 核心不变量 |
|---|---|
| 01 · 01 标准合并与插入 | `res` 内两两不相交且有序，`res[-1][1]` = 已处理区间的并集最右端点 |
| 01 · 02 包含与冗余消除 | `max_end` = 前 i-1 个区间 end 的最大值；start 已排序 ⟹ `end <= max_end` 就是「被覆盖」的充要条件 |
| 01 · 03 连续段与缺失范围 | 每段输出都落在原范围内 ⟹ 有序性与互不相交性从输入继承 |
| 02 · 01 两序列求交集 | `A[0..i-1]` 与 `B[0..j-1]` 之间的所有交集都已找到 |
| 02 · 02 公共空闲区间 | `prev_end` = 已处理忙碌区间的并集最右端点；`start > prev_end` ⟺ 该缝隙全员空闲 |
| 03 · 01 冲突检测与最大兼容数 | `last_end` 是「达到最大兼容数的所有方案中可能的最小值」⟹ 给后面留最多空间 |
| 03 · 02 最少覆盖点 | `arrow_x` 是最后一支箭的位置，且在不漏区间的前提下**尽可能靠右** |
| 04 · 01 最大并发数 | 堆里恰好是所有仍占用资源的区间的 end；堆的历史最大尺寸 = 答案 |
| 04 · 02 差分与容量约束 | 扫到坐标 `x` 时，`cur` 恰等于覆盖 `x` 的区间个数（或带权和） |
| 04 · 03 单服务器时间线与流水线 | 处理到第 `i` 个任务时，`free_at` 恰等于资源下一次空闲的时刻；已排好的占用区间**首尾相接、两两不重叠**（LC-3494 里是 n 条刚性连接的台阶整体右移） |
| 05 · 01 离线查询 | 清理后堆顶是所有覆盖当前查询点的区间中**最短**的那个（**不保证堆内其余元素有效**） |
| 05 · 02 在线预订 | 任意坐标的覆盖数 `<= LIMIT`；**被拒绝的调用不改变任何状态** |

---

## 四、全部题目（含真实相对路径）

| # | 题 | 优先级 | 端点 | 主模板 | 路径 |
|---|---|---|---|---|---|
| 1 | LC-0056 Merge Intervals | **P0** | 闭 | Sort + Merge | [→](<./01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>) |
| 2 | LC-0057 Insert Interval | **P0** | 闭 | 三段式 | [→](<./01 - 区间合并、插入与范围整理/01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>) |
| 3 | LC-1288 Remove Covered Intervals | P1 | 半开 | (start ↑, end ↓) | [→](<./01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/01 - LC-1288 - Remove Covered Intervals>) |
| 4 | LC-1272 Remove Interval ★ | P1+ | **半开** | 区间减法 | [→](<./01 - 区间合并、插入与范围整理/02 - 区间包含与冗余消除/02 - LC-1272 - Remove Interval>) |
| 5 | LC-0228 Summary Ranges | P2 | — | 连续段扫描 | [→](<./01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/01 - LC-0228 - Summary Ranges>) |
| 6 | LC-0163 Missing Ranges | P2 | 闭 | 连续段 + 哨兵 | [→](<./01 - 区间合并、插入与范围整理/03 - 连续整数区间与缺失范围/02 - LC-0163 - Missing Ranges>) |
| 7 | LC-0986 Interval List Intersections ↗️ | **P0** | 闭 | Two Pointers | [→](<./02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>) |
| 8 | LC-1229 Meeting Scheduler ★ | P1+ | 闭 | Two Pointers + 长度 | [→](<./02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/02 - LC-1229 - Meeting Scheduler>) |
| 9 | LC-0759 Employee Free Time | P1 | 闭 | Merge + Gap / K-way | [→](<./02 - 双指针区间交集与多路合并/02 - 多人时间表与公共空闲区间/01 - LC-0759 - Employee Free Time>) |
| 10 | LC-0252 Meeting Rooms | **P0** | 半开 | Conflict Detection | [→](<./03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/01 - LC-0252 - Meeting Rooms>) |
| 11 | LC-0435 Non-overlapping Intervals | **P0** | 半开 | End-time Greedy | [→](<./03 - 不重叠区间与贪心调度/01 - 冲突检测与最大兼容区间数量/02 - LC-0435 - Non-overlapping Intervals>) |
| 12 | LC-0452 Minimum Number of Arrows | P1 | **闭** | End-time Greedy | [→](<./03 - 不重叠区间与贪心调度/02 - 最少覆盖点与区间射击/01 - LC-0452 - Minimum Number of Arrows to Burst Balloons>) |
| 13 | LC-0253 Meeting Rooms II | **P0** | 半开 | Min Heap / Sweep | [→](<./04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>) |
| 14 | LC-2406 Divide Intervals Into Min Groups ★ | P1+ | **闭** | 双排序扫描 | [→](<./04 - 重叠计数、扫描线与资源分配/01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>) |
| 15 | LC-1094 Car Pooling | P1 | 半开 | Difference Array | [→](<./04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>) |
| 16 | LC-2021 Brightest Position on Street | P2 | 闭 | Difference Array | [→](<./04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/02 - LC-2021 - Brightest Position on Street>) |
| 17 | LC-1109 Corporate Flight Bookings ★ | P1+ | 闭（1-based） | Difference Array | [→](<./04 - 重叠计数、扫描线与资源分配/02 - 差分事件与容量约束/03 - LC-1109 - Corporate Flight Bookings>) |
| 18 | LC-1851 Min Interval to Include Each Query | **P0** | 闭 | Offline + 懒删除堆 | [→](<./05 - 离线区间查询与动态预订/01 - 最短覆盖区间的离线查询/01 - LC-1851 - Minimum Interval to Include Each Query>) |
| 19 | LC-0729 My Calendar I | P1 | **半开** | Dynamic Booking | [→](<./05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/01 - LC-0729 - My Calendar I>) |
| 20 | LC-0731 My Calendar II | P1+ | **半开** | Dynamic Booking + k | [→](<./05 - 离线区间查询与动态预订/02 - 在线插入与区间冲突检测/02 - LC-0731 - My Calendar II>) |
| 21 | LC-1701 Average Waiting Time ✚ | P1 | 闭（时刻） | 单服务器 `max` 递推 | [→](<./04 - 重叠计数、扫描线与资源分配/03 - 单服务器时间线与流水线模拟/01 - LC-1701 - Average Waiting Time>) |
| 22 | LC-3494 Min Time to Brew Potions ✚ | P2 | 闭（时刻） | 流水线台阶整体右推 | [→](<./04 - 重叠计数、扫描线与资源分配/03 - 单服务器时间线与流水线模拟/02 - LC-3494 - Find the Minimum Amount of Time to Brew Potions>) |

★ = 第二轮独立审核新增 · ↗️ = 实体在其他专题 · ✚ = 2026-11-11 从已清空的 `99-advanced` 迁入

**实体文件夹 21 个 + 跨专题学习索引 1 个 = 22 个条目，涉及 22 道不同题目。**

---

## 五、P0 / P1 / P2

| 等级 | 数量 | 题 |
|---|---|---|
| **P0**（核心模板，必须熟练） | **7** | 0056, 0057, 0986, 0252, 0253, 0435, 1851 |
| **P1**（标准面试覆盖面） | **5** | 0452, 1288, 1094, 0729, 0759 |
| **P1+**（第二轮新增 + 续篇） | **5** | 1229, 1272, 2406, 1109, 0731 |
| **P2**（存档与补充） | **3** | 0228, 0163, 2021 |

> P0/P1/P2 是**教学优先级**（学习依赖 + 模板覆盖面），
> **不代表任何公司的实际出题频次** —— 本仓库不编造频次数据。

详细路线见 [P0 / P1 / P2 Roadmap](<./_resources/p0-p1-p2-roadmap.md>)。

---

## 六、九个核心模板

> 这**不是**九套要分别背的代码。真正独立的只有四块骨架：
> **①排序扫描 ②双指针 ③堆 ④差分/前缀和**。其余都是换比较条件或换收尾。

### Template 1 — Sort + Merge Intervals

```python
intervals.sort(key=lambda x: x[0])              # ! start 升序
res = [intervals[0][:]]
for s, e in intervals[1:]:
    if s > res[-1][1]: res.append([s, e])       # ! 不相交 ⟹ 开新段
    else:              res[-1][1] = max(res[-1][1], e)   # ! max 不能省
```
**O(n log n)** / O(n)。📍 LC-0056、LC-0759

### Template 2 — Insert Interval（三段式）

```python
while i < n and intervals[i][1] < new[0]: res.append(intervals[i]); i += 1   # ① 左边
s, e = new
while i < n and intervals[i][0] <= e:                                        # ② 吃掉相交的
    s, e = min(s, intervals[i][0]), max(e, intervals[i][1]); i += 1
res.append([s, e]); res.extend(intervals[i:])                                # ③ 右边
```
**O(n)**（输入已排序，**不要 sort**）/ O(n)。📍 LC-0057、LC-1272（减法版）

### Template 3 — Two-pointer Interval Intersection

```python
while i < len(A) and j < len(B):
    left, right = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
    if left <= right: res.append([left, right])      # ! 闭区间 ⟹ <=（[2,2] 也算）
    if A[i][1] < B[j][1]: i += 1                     # ! 弹掉 end 更小的
    else:                 j += 1
```
**O(m + n)** / O(1)。📍 LC-0986、LC-1229

### Template 4 — End-time Greedy Scheduling

```python
intervals.sort(key=lambda x: x[1])              # ! end 升序 —— 不是 start！
take, last_end = 0, float('-inf')
for s, e in intervals:
    if s >= last_end:                           # ! LC-0452 闭区间改成 s > last_end
        take += 1; last_end = e
```
**O(n log n)** / O(1)。📍 LC-0435（`n - take`）、LC-0452（`take`）、LC-0252

### Template 5 — Meeting Rooms with Min Heap

```python
intervals.sort(key=lambda x: x[0])              # ! start 升序
heap = []
for s, e in intervals:
    if heap and heap[0] <= s: heapq.heapreplace(heap, e)   # ! 闭区间改成 heap[0] < s
    else:                     heapq.heappush(heap, e)
return len(heap)
```
**O(n log n)** / O(n)。📍 LC-0253、LC-2406

### Template 6 — Sweep Line / Event Sorting

```python
events = [(s, 1) for s, e in iv] + [(e, -1) for s, e in iv]
events.sort(key=lambda x: (x[0], x[1]))         # ! -1 先 ⟹ 半开语义
#          闭区间语义：key=lambda x: (x[0], -x[1])
cur = best = 0
for _, d in events: cur += d; best = max(best, cur)
```
**O(n log n)** / O(n)。**坐标可任意大 / 浮点**。📍 LC-0253、LC-2021、LC-0759

### Template 7 — Difference Array + Prefix Sum

```python
diff[l] += v
diff[r]     -= v        # ! 半开 [l, r)
diff[r + 1] -= v        # ! 闭   [l, r]
answer = list(itertools.accumulate(diff))
```
**O(n + V)** / O(V)。📍 LC-1094（峰值）、LC-1109（整条数组）、LC-2021（argmax）

### Template 8 — Offline Queries + Min Heap

```python
intervals.sort(key=lambda x: x[0])
for qi in sorted(range(len(queries)), key=lambda i: queries[i]):   # ! 查询排序
    q = queries[qi]
    while i < n and intervals[i][0] <= q:
        l, r = intervals[i]; heapq.heappush(heap, (r - l + 1, r)); i += 1
    while heap and heap[0][1] < q: heapq.heappop(heap)             # ! 懒删除：只清堆顶
    ans[qi] = heap[0][0] if heap else -1                           # ! 写回原始下标
```
**O((n + q) log n)** / O(n + q)。📍 LC-1851

### Template 9 — Dynamic Interval Booking

```python
def book(self, s, e):
    for bs, be in self.booked:
        if s < be and bs < e: return False     # ! 半开 ⟹ 严格小于；拒绝不改状态
    self.booked.append((s, e)); return True
```
单次 **O(n)**（平衡树可降到 O(log n)）/ O(n)。📍 LC-0729、LC-0731

---

## 七、哪些题共享模板，哪些题必须换目标

### 同一套代码，只改比较条件

| 组 | 题 | 唯一差别 |
|---|---|---|
| 合并 | LC-0056 / LC-0759 | 759 = 56 + 取相邻段的 Gap |
| 端点贪心 | LC-0435 / LC-0452 / LC-0252 | 252 问有没有；435 数个数；452 数点数 |
| 并发数 | LC-0253 / LC-2406 | **端点语义**：半开 `<=` vs 闭 `<` |
| 差分数组 | LC-1094 / LC-1109 / LC-2021 | 要峰值 / 要整条数组 / 要 argmax |
| 双指针交集 | LC-0986 / LC-1229 | 1229 多一个长度过滤 + 要先排序 |
| 在线预订 | LC-0729 / LC-0731 | 731 多维护一层 `overlaps` |
| 区间代数 | LC-0057 / LC-1272 | **加**（会合并）vs **减**（会裂开） |

### 必须更换优化目标（不能互相代入）

- **并集**（LC-0056）vs **最大并发数**（LC-0253）—— 都按 start 排序，但问的东西无关
- **最大化保留**（LC-0435）vs **最小化点数**（LC-0452）—— 数值相同，语义不同
- **区间的交集**（LC-0986）vs **空闲的交集**（LC-0759）—— 759 必须先反转成「忙碌的并集」

### 需要 Heap 的 / 只要 Sorting + Scan 的

| 必须 Heap | 可以不用 Heap | 只要 Sorting + Scan |
|---|---|---|
| LC-1851（取最短覆盖区间，本质用法） | LC-0253 / LC-2406（可换差分或扫描线） | 0056, 0057, 0435, 0452, 0252, 1288, 0228, 0163, 1272, 0986, 1229 |
| | LC-0759 解法 B（可换 Flatten + Sort） | |

**需要对 Query 离线排序的**：只有 LC-1851。
**应当用真正动态区间数据结构的**：LC-0729 / LC-0731 的升级版
（`sortedcontainers.SortedList` / 红黑树 / 动态开点线段树）—— 但本专题规模用 O(n) 就够。

---

## 八、区间端点对照表

| 场景 | 闭区间 `[a,b]` | 半开区间 `[a,b)` |
|---|---|---|
| 相交条件 | `s1 <= e2 and s2 <= e1` | `s1 < e2 and s2 < e1` |
| 交集非空 | `max(s) <= min(e)` | `max(s) < min(e)` |
| 资源可复用 | `prev_end < cur_start` | `prev_end <= cur_start` |
| 差分撤销位置 | `diff[right + 1] -= v` | `diff[end] -= v` |
| 堆顶弹出条件 | `heap[0] < cur_start` | `heap[0] <= cur_start` |
| 事件 tie-break | `(pos, -delta)`（`+1` 先） | `(pos, delta)`（`-1` 先） |
| `[1,2]` vs `[2,3]` | **重叠**（都含 2） | **不重叠** |
| 本专题的题 | 0986, 0452, 1851, 2406, 1229, 1109, 0163, 2021 | 0729, 0731, 1094, 1272, 1288, 0252, 0253, 0435 |

> **记忆法**：闭区间「多含一个点」⟹ 判重叠**更宽松**（`<=`）、释放资源**更严格**（`<`）、
> 差分撤销**往后挪一格**。半开区间全部相反。
>
> ⚠️ **不能仅因为输入写成 `[a,b]` 的数组就假定是闭区间 —— 必须读题干。**

完整版见 [Endpoint Semantics Cheat Sheet](<./_resources/endpoint-semantics-cheat-sheet.md>)。

---

## 九、跨专题索引

| 题 | 实体位置 | Primary Pattern | Secondary Patterns | Recommended / Alternative | 本专题的关系 |
|---|---|---|---|---|---|
| **LC-0986** Interval List Intersections | [`02-two-pointers`](<../02-two-pointers (双指针)/05 - 多序列同步扫描 (Two Sequences)/03 - 双序列归并与区间交集/02 - LC-0986 - Interval List Intersections>) | Two Pointers | Interval Intersection | 双指针 / — | 本专题 Level 02 的**模板题**，放学习索引 |
| **LC-1353** Max Events That Can Be Attended | [`13-greedy`](<../13-greedy (贪心)>) | Heap + Greedy Scheduling | Interval Scheduling | 排序 + 小顶堆 / 并查集 | 调度类亲戚，主归属在 Greedy |
| **LC-2402** Meeting Rooms III | [`09-heap`](<../09-heap (堆)>) | Two Heaps | Meeting Rooms | 双堆 + 懒释放 / — | LC-0253 的加强版，主归属在 Heap |
| **LC-0023** Merge k Sorted Lists | [`06-linked-list`](<../06-linked-list (链表)>) | K-way Merge | Min Heap | 堆 / 分治 | LC-0759 解法 B 的结构原型 |
| **LC-0480** Sliding Window Median | [`09-heap`](<../09-heap (堆)>) | Two Heaps + Lazy Deletion | — | 双堆 + 懒删除 / — | LC-1851 懒删除思想的同源题 |
| **LC-0045** Jump Game II | [`13-greedy`](<../13-greedy (贪心)>) | Greedy（维护可达边界） | Interval Coverage | 贪心 / BFS 分层 | LC-1326 的本质，所以 1326 不收进本专题 |

**跨专题去重规则**（本次执行遵循）：
1. 本专题已有原始学习成果 ⟹ **必须保留**，不动其他专题。
2. 本专题没有、其他专题已有 ⟹ **只建 README 相对路径引用**，不复制实体。
3. 一道题在仓库里**只能有一个实体文件夹** —— 否则 `review_due.py` 会重复叫号。

---

## 十、第二轮独立审核结果

第一轮（指令给定）新增 6 道：LC-0986↗️、LC-0452、LC-1288、LC-1094、LC-0729、LC-0759。

**第二轮自主新增 4 道**（上限 4，用满）：

| 题 | 填补的缺口（条件 A） | 面试代表性 / 可迁移性（B / C） |
|---|---|---|
| **LC-1229** Meeting Scheduler | 交集 **+ 长度约束**，且题目**不保证输入有序** | 常见的「找共同空档」变体；直接复用 986 骨架 |
| **LC-1272** Remove Interval | **区间差集（减法）** —— 本专题原本只有加法 | 补全「区间作为集合」的代数：并 / 含 / 差 |
| **LC-2406** Divide Intervals Into Min Groups | **闭区间版的 LC-0253** —— 端点语义的最佳对照 | 一道题把「`<` 还是 `<=`」这个最大坑钉死 |
| **LC-1109** Corporate Flight Bookings | 差分数组要**整条前缀和数组**（1094 只要峰值）+ **1-based 下标陷阱** | 差分数组最纯粹的一题，跨专题复用极广 |

**另加 LC-0731 My Calendar II**（指令第六节已点名为候选，作为 LC-0729 的直接续篇建立，
不占「自主新增 4 道」的名额）：把在线重叠上限从 1 推广到 k。

**未新增的候选（Future Candidates）及原因**：

| 题 | 原因 | 建议归属 |
|---|---|---|
| LC-0732 My Calendar III | 与 LC-0731 高度重复（违反 D）；真要 O(log n) 得上动态开点线段树（违反 E） | 本专题 05，待线段树学完 |
| LC-0352 Data Stream as Disjoint Intervals | 偏**数据结构设计**（违反 G） | `17-design` |
| LC-1326 Min Taps to Water a Garden | 本质是 Jump Game II 的区间版贪心（违反 G）；`13-greedy` 已有 LC-0045 完整教学 | `13-greedy` |
| LC-2276 Count Integers in Intervals | 需有序 map + 动态并集维护，记忆成本偏高（违反 E），且与 LC-0352 重复 | `17-design`（`99-advanced` 已于 2026-11-11 清空） |
| LC-0218 The Skyline Problem | Sweep Line + Heap 难题，学习成本远超本专题其他题（违反 E） | 将来**单独建专题** |
| LC-1353 / LC-2402 | **已在 `13-greedy` / `09-heap`**，有更合适的主归属（违反 G） | 见跨专题索引 |

判断标准（指令第六节 A–G）：
A 填补缺口 · B 面试代表性 · C 可迁移性 · D 不高度重复 · E 记忆成本合理 ·
F 能说明不变量 · G 无更合适的主归属。

---

## 十一、题面文件受限说明

以下 3 道是 **LeetCode Premium** 题目，本仓库无法合法抓取官方题面
⟹ **只有 `metadata.json` + `solution.py`，没有 `problem.pdf` / `problem_dark.pdf`**。
按指令要求：**不伪造题面、不生成空白 PDF、不拿别的题的 PDF 充数**。

| 题 | 缺失文件 | 原因 |
|---|---|---|
| LC-1229 Meeting Scheduler | problem.pdf, problem_dark.pdf | Premium |
| LC-1272 Remove Interval | problem.pdf, problem_dark.pdf | Premium |
| LC-0759 Employee Free Time | problem.pdf, problem_dark.pdf | Premium |

另有 4 道 Premium 题（LC-0252、LC-0253、LC-0163、LC-2021）**PDF 完整** ——
它们的题面在早先入库时已经抓到，本次完整保留。

详见 [_audit/post-migration-report.md](<./_audit/post-migration-report.md>)。

---

## 十二、Pattern Recognition 速查

| 题干关键词 | 模板 | 去哪 |
|---|---|---|
| merge / overlapping / union | Sort + Merge | Level 01 |
| insert / add one interval | 三段式 | Level 01 |
| remove covered / redundant | (start ↑, end ↓) | Level 01 |
| intersection / both available / common | Two Pointers | Level 02 |
| free time / everyone available | Merge + Gap | Level 02 |
| max non-overlapping / min removals | End-time Greedy | Level 03 |
| min arrows / points / taps | End-time Greedy | Level 03 |
| can attend all meetings | Conflict Detection | Level 03 |
| min rooms / min groups / max concurrent | Max Overlap | Level 04 |
| capacity / seats / passengers / brightness | Difference Array | Level 04 |
| for each query / smallest containing | Offline + Heap | Level 05 |
| book / calendar / double booking | Dynamic Booking | Level 05 |

完整决策树见 [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>)。

---

## 十三、最终建议学习顺序

```
【第一遍 · 7 道】把模板学完
  0056 → 0057 → 0986 → 0252 → 0435 → 0253 → 1851

【第二遍 · 12 道】标准面试覆盖面（P0 + P1）
  0056 → 0057 → 0986 → 0252 → 0435 → 0452 → 1288
       → 0253 → 1094 → 1851 → 0729 → 0759

【第三遍 · 20 道】按 Level 1 顺序，端点语义对照最完整
  L1 → 0056 0057 1288 1272 0228 0163
  L2 → 0986 1229 0759
  L3 → 0252 0435 0452
  L4 → 0253 2406 1094 1109 2021
  L5 → 1851 0729 0731
```

**配对练习**（一次打穿端点语义的坑）：

| 配对 | 对照的是什么 |
|---|---|
| `0253` → `2406` | 半开 vs **闭**，同一算法 |
| `0435` → `0452` | 同一贪心，**两种计数** |
| `0057` → `1272` | 区间的**加法** vs **减法** |
| `1094` → `1109` | 差分要**峰值** vs 要**整条数组** |
| `0729` → `0731` | 在线上限 **1** vs **2** |
| `0228` → `0163` | **有什么** vs **缺什么** |
| `0986` → `0759` | 零长度交集**要保留** vs **要丢弃** |

---

## 相关资料

| 文档 | 内容 |
|---|---|
| [Pattern Recognition Guide](<./_resources/pattern-recognition-guide.md>) | Q1–Q14 决策树 + 三秒速判表 + 排序键速查 |
| [Endpoint Semantics Cheat Sheet](<./_resources/endpoint-semantics-cheat-sheet.md>) | 闭 / 半开的全部不等号 + 差分撤销位置 + 六个必测边界 |
| [Interval Algorithm Comparison Table](<./_resources/interval-algorithm-comparison.md>) | 九个模板总索引 + 四个目标对照 + 复杂度速查 + 错误贪心反例 |
| [P0 / P1 / P2 Roadmap](<./_resources/p0-p1-p2-roadmap.md>) | 三条路线 + 配对练习 + Future Candidates |
| [_audit/post-migration-report.md](<./_audit/post-migration-report.md>) | 迁移映射、SHA-256 校验、NC 正式化、Premium 限制 |
