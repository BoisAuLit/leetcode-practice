# Level 1 · 02 — 双指针区间交集与多路合并（Two Pointers / Intersection / K-way Merge）

> **本层的统一目标：两个（或 k 个）已排序的区间序列，求它们的「公共部分」。**
> Level 01 处理**一组**区间的内部整理；本层开始处理**多组**区间之间的关系。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Sorted Interval Stream** | 一个**已排序、内部互不相交**的区间序列，可以只持有「当前队头」 |
| **Intersection（交集）** | `[a1,b1] ∩ [a2,b2] = [max(a1,a2), min(b1,b2)]`，非空条件见下 |
| **K-way Merge** | k 条有序流用 Min Heap 同步推进，堆里永远只有 k 个队头 |
| **Free-time Detection** | 「所有人都空闲」= 忙碌区间**并集**的 Gap（德摩根律） |

---

## 两个决定性观察

### ① 交集公式只有一行，难点全在「非空条件的不等号」

```python
left  = max(a_start, b_start)
right = min(a_end,   b_end)
```

| 端点语义 | 非空条件 | 原因 |
|---|---|---|
| **闭区间** `[a,b]` | `left <= right` | `[1,2] ∩ [2,3] = [2,2]`，**单点区间是合法交集** |
| **半开区间** `[a,b)` | `left < right` | `[1,2) ∩ [2,3) = ∅`，零长度不算 |

LC-0986 和 LC-1229 都是**闭区间** ⟹ 用 `<=`。
写成 `<` 会漏掉所有「刚好共享一个端点」的交集。

### ② 「所有人的共同空闲」要先反转成「忙碌的并集」

这是 LC-0759 唯一的思维跳跃：

> 共同空闲 = `∩(每个人的空闲)` = `∩(每个人忙碌的补集)` = `(∪ 所有人的忙碌)的补集`

所以**不要**去求「k 个空闲列表的交集」（k 路求交很麻烦），
而是把**所有人的忙碌区间倒在一起合并**（Level 01 的 Merge Intervals），
然后取相邻段之间的 Gap。**员工是谁完全不重要。**

---

## 核心不变量

**双指针（LC-0986 / LC-1229）**：
> 任意时刻，`A[0..i-1]` 和 `B[0..j-1]` 之间的**所有**交集都已被找到，
> 且 `A[i]` 与 `B[j]` 是各自序列里**尚未排除**的最早区间。

**K-way Merge（LC-0759 解法 B）**：
> 堆里恰好包含每条非空流的**当前队头**，所以堆顶是全局最小的未处理区间起点。

**Free-time（LC-0759）**：
> 扫描到某处时，`prev_end` 是「已处理的所有忙碌区间的并集」的最右端点；
> 下一个区间的 `start > prev_end` ⟺ `(prev_end, start)` 内**无人**在忙。

---

## 为什么这样移动指针（交换论证）

**规则**：`A[i].end < B[j].end` 就 `i += 1`，否则 `j += 1`（**弹掉结束更早的那个**）。

**证明**：设 `A[i].end < B[j].end`。要证 `A[i]` 与 `B[j+1], B[j+2], …` 都不可能相交。
B 组内部**互不相交且有序** ⟹ `B[j+1].start > B[j].end`。
结合 `B[j].end > A[i].end` ⟹ `B[j+1].start > A[i].end`
⟹ `B[j+1]` 整个落在 `A[i]` 的右边，交集为空。
后续 B 区间的 start 更大，同理。
所以 `A[i]` 的全部交集都已经在前面找完了，`i += 1` **不会丢解**。∎

**为什么 LC-1229 的第一个命中就是最早的？**
两个指针都只右移 ⟹ `left = max(A[i].start, B[j].start)` 随扫描**单调不减**
⟹ 第一个满足长度约束的 `left` 就是最小的 `left`。∎

**为什么 LC-0759 的 Gap 一定是全员空闲？**
设并集排序后相邻两段是 `[.., a]` 和 `[b, ..]` 且 `a < b`。
若 `(a, b)` 内某点被某个忙碌区间覆盖，该区间在合并时会与左段或右段相连
（或自成一段落在中间）⟹ 与「两段在并集里相邻」矛盾。∎

**为什么零长度 Gap 不输出？**
`[1,2]` 和 `[2,3]` 之间的「空闲」是 `[2,2]`，**没有任何一个瞬间是空的**。
代码上是 `if prev_end < start`（**严格小于**）。写 `<=` 会吐出一堆 `[x,x]` 垃圾。

**为什么不输出 `(-∞, 第一段)` 和 `(最后一段, +∞)`？**
题目要的是**有限（finite）**空闲区间；员工日程之外的时间不在讨论范围内。

---

## Python 模板

### Template 3：Two-pointer Interval Intersection

```python
def intervalIntersection(A, B):
    res, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        left  = max(A[i][0], B[j][0])
        right = min(A[i][1], B[j][1])
        if left <= right:                   # ! 闭区间 ⟹ <=（[2,2] 也算）
            res.append([left, right])
        if A[i][1] < B[j][1]:               # ! 弹掉 end 更小的
            i += 1
        else:
            j += 1
    return res
```
**O(m + n)** 时间（输入已排序）、O(1) 额外空间。

### Template 3'：加长度约束（LC-1229）

```python
def minAvailableDuration(slots1, slots2, duration):
    slots1.sort(); slots2.sort()             # ! 本题不保证有序！这两行不能省
    i = j = 0
    while i < len(slots1) and j < len(slots2):
        left  = max(slots1[i][0], slots2[j][0])
        right = min(slots1[i][1], slots2[j][1])
        if right - left >= duration:         # ! 唯一的新增条件（比长度，不是比非空）
            return [left, left + duration]
        if slots1[i][1] < slots2[j][1]: i += 1
        else:                               j += 1
    return []
```
**O(m log m + n log n)** 时间（排序主导）、O(1) 额外空间。

### Template：Flatten + Merge + Gap（LC-0759 解法 A）

```python
def employeeFreeTime(schedule):
    flat = sorted((iv.start, iv.end) for emp in schedule for iv in emp)
    if not flat: return []
    res, prev_end = [], flat[0][1]
    for s, e in flat[1:]:
        if s > prev_end:                     # ! 严格大于 ⟹ 正长度 Gap
            res.append(Interval(prev_end, s))
            prev_end = e
        else:
            prev_end = max(prev_end, e)      # ! 继续合并
    return res
```
**O(N log N)** 时间、O(N) 空间（`N` = 区间总数）。

### Template：K-way Merge + Min Heap（LC-0759 解法 B）

```python
def employeeFreeTime(schedule):
    heap = [(emp[0].start, emp[0].end, e, 0)
            for e, emp in enumerate(schedule) if emp]       # ! 只放 k 个队头
    if not heap: return []
    heapq.heapify(heap)
    res, prev_end = [], heap[0][1]
    while heap:
        s, e, who, idx = heapq.heappop(heap)
        if s > prev_end:
            res.append(Interval(prev_end, s)); prev_end = e
        else:
            prev_end = max(prev_end, e)
        if idx + 1 < len(schedule[who]):                     # ! 补上同一条流的下一个
            nxt = schedule[who][idx + 1]
            heapq.heappush(heap, (nxt.start, nxt.end, who, idx + 1))
    return res
```
**O(N log k)** 时间、**O(k)** 空间 —— 永远只持有 k 个区间，所以能处理**流式**输入。

---

## 复杂度对照

| 题 | 时间 | 空间 | 瓶颈 |
|---|---|---|---|
| LC-0986 | **O(m + n)** | O(1) 额外 | 双指针，输入已排序 |
| LC-1229 | O(m log m + n log n) | O(1) 额外 | **排序**（题目不保证有序） |
| LC-0759 解法 A | O(N log N) | O(N) | 排序 |
| LC-0759 解法 B | **O(N log k)** | **O(k)** | 堆操作；k 远小于 N 时更优 |

> ⚠️ **LC-0986 不是 O(n log n)** —— 输入已排序，双指针一次扫完就是 **O(m+n)**。
> 只有 LC-1229 因为题目不保证有序才需要排序。

---

## 代表题目

| # | 题 | 优先级 | 模板 | 端点 |
|---|---|---|---|---|
| 1 | [LC-0986 Interval List Intersections](<./01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>) ↗️ | **P0** | Two Pointers | 闭 |
| 2 | [LC-1229 Meeting Scheduler](<./01 - 两个有序区间序列求交集/02 - LC-1229 - Meeting Scheduler>) | P1+ | Two Pointers + 长度过滤 | 闭 |
| 3 | [LC-0759 Employee Free Time](<./02 - 多人时间表与公共空闲区间/01 - LC-0759 - Employee Free Time>) | P1 | Merge + Gap / K-way Heap | 闭 |

↗️ **LC-0986 的实体在 `02-two-pointers` 专题**（它更早入库，且 Two Pointers 是主归属）。
本层只放学习索引 + 完整模板和证明 —— 一道题在仓库里只能有一个实体文件夹，
否则 `review_due.py` 会重复叫号。

⚠️ **LC-0759 是 LeetCode Premium 题目**，无法合法抓取官方题面
⟹ 该文件夹**没有 `problem.pdf` / `problem_dark.pdf`**（详见
[_audit/post-migration-report.md](<../_audit/post-migration-report.md>)）。
`solution.py` 里的题意描述为公开通行表述，解法与证明均自撰。

---

## 典型边界情况

| 边界 | 例子 | 期望 |
|---|---|---|
| 端点相等（零长度交集） | `[[1,2]] ∩ [[2,3]]` | `[[2,2]]`（**闭区间要保留**） |
| 完全包含 | `[[1,10]] ∩ [[2,3]]` | `[[2,3]]` |
| 完全相同 | `[[1,5]] ∩ [[1,5]]` | `[[1,5]]` |
| 空输入 | `[] ∩ [[1,2]]` | `[]` |
| 完全无重叠 | `[[1,2]] ∩ [[5,6]]` | `[]` |
| 长度**恰好**等于 duration | `slots1=[[0,10]], slots2=[[5,10]], d=5` | `[5,10]`（`>=` 不是 `>`） |
| **输入未排序**（LC-1229） | `[[60,120],[10,50]]` | 必须先 sort，否则漏解 |
| 零长度 Gap（LC-0759） | `[[[1,2]],[[2,3]]]` | `[]`（**不输出 `[2,2]`**） |
| 全员忙到底 | `[[[1,10]],[[2,3]]]` | `[]` |
| 单员工单区间 | `[[[1,2]]]` | `[]`（没有 Gap） |

> **注意 LC-0986 和 LC-0759 对「零长度」的处理完全相反**：
> 986 求**交集**，`[2,2]` 要保留；759 求**空闲**，`[2,2]` 要丢弃。
> 都对 —— 一个在问「有没有公共点」，一个在问「有没有公共时段」。

---

## 错误策略反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| LC-0986 用 `left < right` | `[[1,2]] ∩ [[2,3]]` | 漏掉 `[2,2]` |
| LC-0986 弹掉 **start 更小**的 | — | 会跳过未发现的交集 |
| LC-0986 双指针都自增 | `[[1,10]] ∩ [[2,3],[4,5]]` | 漏掉第二个交集 |
| LC-1229 不排序 | `[[60,120],[10,50]]` vs `[[60,70],[0,15]]` | 漏解或返回错误的「最早」 |
| LC-1229 用 `right - left > duration` | 长度恰好相等的情形 | 漏解 |
| LC-0759 去求「空闲列表的交集」 | — | 方向错了，应求忙碌的并集 |
| LC-0759 用 `prev_end <= start` | `[[[1,2]],[[2,3]]]` | 吐出零长度 `[2,2]` |
| LC-0759 输出两端无界区间 | — | 题目只要 finite 区间 |
| LC-0759 扫描线 tie-break 用 `(pos, delta)` | `[[[1,2]],[[2,3]]]` | 覆盖数短暂归零 ⟹ 假 Gap |

---

## 相邻 Pattern 对比

| | [Level 1 · 01](<../01 - 区间合并、插入与范围整理>) | **本层（02）** | [Level 1 · 03](<../03 - 不重叠区间与贪心调度>) |
|---|---|---|---|
| 输入 | **一组**区间 | **两/k 组**区间 | **一组**区间 |
| 目标 | 并集 / 差集 | **交集**（或并集的补） | 选出一个最优子集 |
| 核心操作 | `max(cur_end, e)` | `max(s)` / `min(e)` | 按 end 贪心取 |
| 指针 | 一个 | **两个（或 k 个 + 堆）** | 一个 |
| 输出 | 区间列表 | 区间列表 | 一个计数 |

**和 Level 01 的血缘关系**：
LC-0759 的内核**就是** LC-0056 Merge Intervals，只是把「合并结果」换成了「缝隙」。
**先把 Level 01 练熟，本层的一半就免费了。**

**跨专题血缘**：
- LC-0986 的主归属是 `02-two-pointers`（双序列同步扫描）
- LC-0759 解法 B 的堆结构 = `06-linked-list` 的 **LC-0023 Merge k Sorted Lists**
- k 路取最小值的套路 = `09-heap` 的 k-way merge 家族

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q3
- [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>) — 闭区间的 `<=`
- [Interval Algorithm Comparison Table](<../_resources/interval-algorithm-comparison.md>) — 模板 3
- [P0 / P1 / P2 Roadmap](<../_resources/p0-p1-p2-roadmap.md>)
