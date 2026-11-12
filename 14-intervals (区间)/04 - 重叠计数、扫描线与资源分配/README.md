# Level 1 · 04 — 重叠计数、扫描线与资源分配（Max Overlap / Sweep Line / Difference Array）

> **本层的统一目标：不再关心「哪些区间」，只关心「每个坐标点上有多少个区间压着」。**
> 这是一次视角转换：从**区间**的世界转到**坐标轴上的事件流**。
>
> **Level 2 · 03 是这件事的另一端**：当资源数**固定为 1（或固定为 n 条流水线）**、
> 而且处理顺序由题目钦定时，「最大并发数」不再是问题 ——
> 问题变成「每个任务的占用区间落在时间轴的哪里」，答案是一行 `max` 递推。
> 先看它，再回头看 LC-0253，会更清楚「资源数是答案」和「资源数是约束」的区别。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Maximum Concurrent Overlap** | 某一时刻被覆盖的区间数的最大值 |
| **Single-server Timeline（单服务器时间线）** | 资源数固定为 1、顺序固定 ⟹ 占用区间**首尾相接**，`free_at = max(free_at, arrival) + duration` |
| **Flow Shop（流水线 / 同步时间线）** | n 个资源串联，一个任务必须**无间隔**依次穿过全部资源 ⟹ 它在时间轴上是一条**刚性台阶**，只能整体平移 |
| **Sweep Line（扫描线）** | 把每个区间拆成 `(start, +1)` 和 `(end, -1)` 两个**事件**，按坐标排序后扫过去 |
| **Coordinate Events** | 事件 = `(坐标, 增量)`；增量可以带权（人数、亮度） |
| **Difference Array（差分数组）** | `diff[l] += v`、`diff[r或r+1] -= v`，一次前缀和兑现所有区间加 |
| **Active Intervals** | 当前「还没结束」的区间集合（Heap 解法里就是堆的内容） |

---

## 三个决定性观察

### ① 「最少资源数」= 「最大并发数」

> **最少会议室数 / 最少分组数 = 任意时刻的最大重叠数。**

**下界**：若某时刻 `t` 有 `k` 个区间同时覆盖它，这 `k` 个区间两两相交
⟹ 必须分到 `k` 个不同的资源 ⟹ **至少 `k` 个**。
**上界**：按 start 排序 + 贪心（塞进任意一个已空出的资源）恰好用掉 `max_overlap` 个。
两边一夹 ⟹ 答案就是最大重叠数。∎

这把一个**调度问题**变成了一个**计数问题** —— 不用管「谁分到哪个房间」。

### ② 差分数组把「n 次区间加」从 O(n·len) 降到 O(n + V)

令 `diff[i] = a[i] - a[i-1]`（`a[-1] = 0`），则 `a[i] = Σ_{j<=i} diff[j]`。
对 `a` 的区间 `[l, r]` 整体加 `v`，只有**两个**差值发生变化
⟹ `diff[l] += v`、`diff[r+1] -= v`，**O(1) 完成一次区间加**。
最后一次前缀和把所有修改同时兑现。∎

### ③ 本层所有题的区别只在「要前缀和的什么」

| 题 | 要什么 | 代码差别 |
|---|---|---|
| [LC-0253](<./01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>) / [LC-2406](<./01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>) | 前缀和的**最大值** | `best = max(best, cur)` |
| [LC-1094](<./02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>) | 最大值**是否超限** | `if cur > capacity: return False` |
| [LC-1109](<./02 - 差分事件与容量约束/03 - LC-1109 - Corporate Flight Bookings>) | **整条前缀和数组** | `return list(accumulate(diff))` |
| [LC-2021](<./02 - 差分事件与容量约束/02 - LC-2021 - Brightest Position on Street>) | 最大值出现的**位置（argmax）** | 记下 `best_pos` |

> **一套代码，四种收尾。** 学会差分数组，本层这四道题就全通了。

**Level 2 · 03 的两道题不在这张表里**，因为它们问的不是「前缀和的什么」——
它们的区间不是给定的输入，而是**被递推算出来**的（见下面的专门小节）。

---

## 核心不变量

**扫描线 / 差分**：
> 扫描到坐标 `x` 时，`cur` 恰好等于「覆盖 `x` 的区间个数（或带权和）」。

**Min Heap（LC-0253 / LC-2406）**：
> 堆里恰好是**所有仍在占用资源的区间的结束时间**；
> 堆的尺寸 = 当前已分配的资源数；堆的历史最大尺寸 = 答案。

**贪心复用的正确性**：复用「结束最早」的资源永远不劣 ——
如果结束最早的那个都腾不出来，其他的更腾不出来。

---

## ⚠️ 端点语义：本层最大的坑

**LC-0253 和 LC-2406 是同一道题的两种端点语义版本。**

| | LC-0253 Meeting Rooms II | LC-2406 Divide Intervals |
|---|---|---|
| 区间 | **半开** `[start, end)` | **闭** `[left, right]` |
| `[1,2]` 和 `[2,3]` | **不冲突**（答案 1） | **冲突**（答案 **2**） |
| 复用条件 | `start >= 前一个 end` | `left > 前一个 right` |
| 堆弹出 | `heap[0] <= start` | `heap[0] < left` |
| 差分撤销 | `diff[end] -= 1` | `diff[right + 1] -= 1` |

> **把 253 的代码原封不动搬到 2406，会在 `[[1,2],[2,3]]` 上答 1（正确是 2）。**
> 闭区间的通用技巧：**把 `[l, r]` 平移成半开 `[l, r+1)`**，之后就是标准的 253。

**事件排序的 tie-break 同样由端点语义决定**：

| 想要 | 排序键 | 实例 |
|---|---|---|
| 端点相接**不**算重叠（半开） | `(pos, delta)` —— `-1` 先 | LC-1094（同站先下车再上车） |
| 端点相接**算**重叠（闭） | `(pos, -delta)` —— `+1` 先 | LC-2406、LC-0759 的扫描线解法 |

LC-1094 的具体后果：`[[2,1,5],[3,5,7]]`、`capacity=3`。
正确答案 **True**（5 这一站先下 2 人再上 3 人，峰值 3）。
tie-break 写反会在 5 处算出 5 人 ⟹ 误判 False。

---

## Python 模板

### Template 5：Min Heap（Meeting Rooms）

```python
def minMeetingRooms(intervals):                 # LC-0253，半开区间
    intervals.sort(key=lambda x: x[0])          # ! start 升序
    heap = []                                   # ! 堆里存各房间的结束时间
    for s, e in intervals:
        if heap and heap[0] <= s:               # ! 半开 ⟹ <=（结束即释放）
            heapq.heapreplace(heap, e)          # ! 复用结束最早的房间
        else:
            heapq.heappush(heap, e)             # ! 全占着 ⟹ 开新房间
    return len(heap)                            # ! 堆的尺寸就是答案
```
**O(n log n)** 时间、O(n) 空间。
LC-2406 把 `heap[0] <= s` 改成 `heap[0] < s` 即可（闭区间）。

### Template 6：Sweep Line（事件排序）

```python
def maxOverlap(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], x[1]))     # ! -1 在前 ⟹ 半开语义
    #          闭区间语义改成 key=lambda x: (x[0], -x[1])
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best
```
**O(n log n)** 时间、O(n) 空间。**坐标可以是任意大小/浮点数。**

### Template 7：Difference Array + 前缀和

```python
# 半开区间 [start, end)
diff = [0] * (V + 1)
for num, start, end in trips:
    diff[start] += num
    diff[end]   -= num                          # ! end 位置已不在区间内
# 闭区间 [left, right]
    diff[left]      += num
    diff[right + 1] -= num                      # ! right 还在区间内 ⟹ 往后挪一格

cur = 0
for d in diff:
    cur += d
    ...                                         # ! 收尾：取 max / 判超限 / 收集 / argmax
# 或者直接：answer = list(itertools.accumulate(diff))
```
**O(n + V)** 时间、O(V) 空间。**值域 V 小的时候比排序更快。**

### 双排序扫描（不吃值域的 O(n log n) 退路）

```python
def minGroups(intervals):                       # LC-2406
    starts = sorted(l for l, _ in intervals)
    ends   = sorted(r + 1 for _, r in intervals)    # ! 闭 ⟹ 平移成半开
    i = j = cur = best = 0
    while i < len(starts):
        if starts[i] < ends[j]:
            cur += 1; best = max(best, cur); i += 1
        else:
            cur -= 1; j += 1
    return best
```
**O(n log n)** 时间、O(n) 空间 —— 坐标巨大或是浮点数时的首选。

---

## 复杂度对照（不要一律写 O(n log n)）

| 题 | 差分解法 | 堆/排序解法 | 空间 | 本题该用哪个 |
|---|---|---|---|---|
| LC-0253 | O(n + V) | O(n log n) | O(V) / O(n) | 两者皆可 |
| LC-2406 | **O(n + V)**，V = 1e6 | O(n log n)，n ≤ 1e5 | O(V) / O(n) | **双排序扫描**（不吃值域更稳） |
| LC-1094 | **O(n + V)**，V = 1001 | O(n log n) | O(V) | **差分**（V 极小） |
| LC-1109 | **O(n + m)** | O(m log m + n) | O(n) | **差分**（下标本来就连续） |
| LC-2021 | **O(n + V)** | O(n log n) | O(n) | 看坐标范围 |
| LC-1701 | — | **O(n)**，一遍递推 | O(1) | 不需要排序（输入已按 arrival 有序） |
| LC-3494 | — | **O(n·m)**，n 巫师 × m 药水 | O(n) | 唯一解法；n, m ≤ 5000 ⟹ 2.5·10⁷ |

> **差分 vs 排序的选择标准**：值域 `V` 比 `n log n` 小就用差分，否则用排序/堆。
> 坐标是浮点数或范围无界时**只能**用排序。

---

## 代表题目

| # | 题 | 优先级 | 端点 | 要什么 | 主模板 |
|---|---|---|---|---|---|
| 1 | [LC-0253 Meeting Rooms II](<./01 - 最少会议室与最大并发数/01 - LC-0253 - Meeting Rooms II>) | **P0** | 半开 | 最大值 | Min Heap / Sweep |
| 2 | [LC-2406 Divide Intervals Into Min Groups](<./01 - 最少会议室与最大并发数/02 - LC-2406 - Divide Intervals Into Minimum Number of Groups>) | P1+ | **闭** | 最大值 | 双排序扫描 |
| 3 | [LC-1094 Car Pooling](<./02 - 差分事件与容量约束/01 - LC-1094 - Car Pooling>) | P1 | 半开 | 最大值是否超限 | Difference Array |
| 4 | [LC-2021 Brightest Position on Street](<./02 - 差分事件与容量约束/02 - LC-2021 - Brightest Position on Street>) | P2 | 闭 | **argmax** | Difference Array |
| 5 | [LC-1109 Corporate Flight Bookings](<./02 - 差分事件与容量约束/03 - LC-1109 - Corporate Flight Bookings>) | P1+ | 闭（1-based） | **整条数组** | Difference Array |
| 6 | [LC-1701 Average Waiting Time](<./03 - 单服务器时间线与流水线模拟/01 - LC-1701 - Average Waiting Time>) ✚ | P1 | 闭（时刻） | 平均等待 | 单服务器 `max` 递推 |
| 7 | [LC-3494 Min Time to Brew Potions](<./03 - 单服务器时间线与流水线模拟/02 - LC-3494 - Find the Minimum Amount of Time to Brew Potions>) ✚ | P2 | 闭（时刻） | 最后完成时刻 | 台阶整体右推 |

⚠️ **LC-0253 和 LC-2021 是 LeetCode Premium 题目**；
LC-0253 的实体来自原 NeetCode 版本（已正式化为 LC-0253，所有原始文件保留），
LC-2021 原本就有完整的 `explanation.md` / `note.md` / PDF（全部保留）。

---

## 典型边界情况

| 边界 | 例子 | 期望 |
|---|---|---|
| 端点相等（半开） | `minMeetingRooms([[1,2],[2,3]])` | **`1`** |
| 端点相等（闭） | `minGroups([[1,2],[2,3]])` | **`2`** |
| 完全包含 | `minGroups([[1,10],[2,3],[4,5]])` | `2` |
| 完全相同 | `minGroups([[5,5],[5,5],[5,5]])` | `3` |
| 零长度区间（闭） | `minGroups([[1,1]])` | `1` |
| 空输入 | `minGroups([])` / `carPooling([], 1)` | `0` / `True` |
| 完全无重叠 | `minGroups([[1,2],[4,5]])` | `1` |
| 同站先下后上 | `carPooling([[2,1,5],[3,5,7]], 3)` | **`True`** |
| 峰值**恰好**等于容量 | `carPooling([[4,1,2]], 4)` | `True`（`<=` 不是 `<`） |
| 单次就超载 | `carPooling([[5,1,2]], 4)` | `False` |
| `last == n`（差分越界） | `corpFlightBookings([[5,5,9]], 5)` | `[0,0,0,0,9]`，数组要开 `n+1` |
| 整个范围 | `corpFlightBookings([[1,5,4]], 5)` | 全是 4 |

---

## 错误策略反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| 把 LC-0253 的 `<=` 搬到 LC-2406 | `[[1,2],[2,3]]` | 得 1，正确 **2** |
| LC-2406 差分写 `diff[right] -= 1` | `[[1,2],[2,3]]` | 同上 |
| LC-1094 事件排序不做 tie-break | `[[2,1,5],[3,5,7]]`, cap 3 | 得 False，正确 **True** |
| LC-1094 判 `cur >= capacity` | 峰值恰好等于容量 | 误判 False |
| LC-1109 差分数组只开 `n` 长 | `last == n` | `IndexError` |
| LC-1109 把 `-=` 的下标也减 1 | 任意用例 | 整条数组错位一格 |
| 对 start / end 分别排序后直接相减求并发数 | — | 必须双指针同步扫 |
| 用 O(n²) 逐对检查重叠 | n = 1e5 | TLE |
| 值域 1e9 还用差分数组 | — | MLE；该换事件排序 |

---

## Level 2 · 03 — 单服务器时间线与流水线模拟

> **这一层的两道题都不需要排序、不需要堆、不需要差分。**
> 它们是本层的**基线**：资源数固定、顺序固定 ⟹ 没有任何选择，
> 只剩「每个任务的占用区间落在时间轴的哪里」。

### 一行递推（LC-1701）

```python
free_at = max(free_at, arrival) + duration    # ! 资源下一次空闲的时刻
wait   += free_at - arrival                   # ! 这个任务等了多久
```

`max` 的两种情形就是全部分支：

| 情形 | 含义 | 开始时刻 |
|---|---|---|
| `free_at <= arrival` | 资源闲着等任务 | `arrival` |
| `free_at > arrival` | 任务排队等资源 | `free_at` |

> **这是 LC-0253 Meeting Rooms II 的「只有 1 个会议室」特例。**
> LC-0253 问「最少要几个资源」（资源数是**答案**）；
> 这里资源数固定为 1（资源数是**约束**），于是问题从「数重叠」变成「推时间线」。

### 从 1 个资源到 n 条流水线（LC-3494）

`n` 个资源**串联**，一个任务必须无间隔地依次穿过全部资源
⟹ 它在时间轴上是一条**形状固定的台阶**（级长 `skill[i] * mana[j]`），
**唯一的自由度是整体平移量 `s_j`**：

```
s_j = max_i ( finish_{j-1}[i] − mana[j] * pre[i] )      # ! 逐级量「撞深」，推到刚好不撞
finish_j[i] = s_j + mana[j] * pre[i+1]
```

**不能贪心地让每瓶药等上一瓶彻底离开流水线**（`s_j = finish_{j-1}[n-1]`）——
那会让前面的资源大量空转，答案偏大。
（LC-3494 的 `solution.py` 里把这个错误贪心写成了可运行的对照：
官方样例下它给 144，正确答案是 110。）

### 两层的对照

| | LC-1701 | LC-3494 |
|---|---|---|
| 资源 | **1** 个 | **n** 个，串成流水线 |
| 一个任务的形状 | 一段区间 `[s, s+d]` | 一条 n 级刚性台阶 |
| `max` 对什么取 | 对 1 个资源 | 对 n 个资源**逐级**取 |
| 复杂度 | O(n) | O(n·m) |

### 共同的坑

- **整数溢出（C++ / Java）**：LC-1701 的等待时间总和可达 `2·10^13`，
  LC-3494 的答案可达 `1.25·10^11` ⟹ 两题都**必须 `long long`**。Python 不受影响。
- **浮点**：LC-1701 要用**整数**累加总等待时间，**最后只除一次**；
  每项都除会累积 `10^5` 次舍入误差。
- **别去想贪心**：两题的处理顺序都由题目钦定。
  （顺带一个排队论事实：按 duration 升序重排能让平均等待更小 —— 但本题禁止重排。）

---

## 相邻 Pattern 对比

| | [Level 1 · 03](<../03 - 不重叠区间与贪心调度>) | **本层（04）** | [Level 1 · 05](<../05 - 离线区间查询与动态预订>) |
|---|---|---|---|
| 关心 | **选哪些区间** | **每个点被压了几次** | **某个查询点的最优区间** |
| 排序键 | **end ↑** | **start ↑** 或事件排序 | 查询点 ↑ + 区间 start ↑ |
| 数据结构 | 无（一个变量） | Heap / 差分数组 | **Heap + 懒删除** |
| 输出 | 一个计数 | 一个计数 / 一条数组 | 每个查询一个答案 |
| 本质 | 贪心 | **计数** | 离线 + 堆 |

**和 Level 03 的关键区别**：
Level 03 要「最多能选几个**互不相交**的」（end 排序 + 贪心）；
本层要「某一刻最多有几个**同时存在**的」（start 排序 + 计数）。
**两个问题的答案通常不同，排序键也不同。** 混用就全错。

**和 Level 05 的衔接**：
本层的 Heap 存「结束时间」用来**复用资源**；
Level 05 的 Heap 存「区间长度」用来**回答查询**，而且需要**懒删除**。
同一个数据结构，两种用法。

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q7 / Q8 / Q9
- [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>) — 差分撤销位置 + tie-break
- [Interval Algorithm Comparison Table](<../_resources/interval-algorithm-comparison.md>) — 模板 5 / 6 / 7
- [P0 / P1 / P2 Roadmap](<../_resources/p0-p1-p2-roadmap.md>)
