# Level 1 · 01 — 区间合并、插入与范围整理（Interval Merging / Insertion / Range Normalization）

> **本层的统一目标：把一堆区间整理成「规范形式」—— 排好序、互不相交。**
> 这是整个 Intervals 专题的地基：后面四层全都假设输入已经是规范形式。

---

## 核心定义

| 术语 | 定义 |
|---|---|
| **Normalized form（规范形式）** | 按 start 升序排列、且两两**互不相交**的区间列表 |
| **Union（并集）** | 把所有相交或相邻的区间融合成一段 → LC-0056 / LC-0057 |
| **Containment（包含）** | `[a,b] ⊆ [c,d] ⟺ c <= a and b <= d` → LC-1288 |
| **Difference（差集）** | 从每段里挖掉一个区间，可能把一段**裂成两段** → LC-1272 |
| **Consecutive run（连续段）** | 整数序列里 `a[i+1] == a[i] + 1` 的最长片段 → LC-0228 / LC-0163 |

---

## 三个决定性观察

### ① 排序后，判断相交只需要看「当前 start」和「已合并的 max end」

排序后 start 单调不减，所以**前面所有区间的 start 都 `<=` 当前的 start**。
于是「当前区间是否和前面的某一个相交」退化成一个标量比较：
```python
start <= cur_end          # 相交（闭区间或需要合并相邻时用 <=）
```
**不需要两两比较**，O(n²) 降到 O(n)。

### ② `cur_end` 必须用 `max`，不能直接赋值

```python
cur_end = max(cur_end, end)      # ! 不是 cur_end = end
```
反例 `[[1,10],[2,3]]`：直接赋值会把右界从 10 缩回 3，于是 `[4,5]` 被误判为新段。
**排序只保证 start 有序，end 完全可能回头。**

### ③ 「插入一个」和「减掉一个」是对称的两个操作，但代价不同

| | LC-0057 插入 | LC-1272 减去 |
|---|---|---|
| 可能导致 | 多段**合并成一段** | 一段**裂成两段** |
| 输出规模 | 最多 n 段（变少） | 最多 n+1 段（变多） |
| 要不要重新排序 | ❌ 不要（输入已排序，结果仍有序） | ❌ 不要（同理） |
| 复杂度 | **O(n)** | **O(n)** |

> 两题的输入都**已经是规范形式**，所以都是 **O(n)**。
> 在这里写 `intervals.sort()` 是白送一个 log n。

---

## 核心不变量

**Merge / Insert 的不变量**：
> 扫描到第 `i` 个区间时，`res` 里的区间**两两不相交且有序**，
> 且 `res[-1][1] == cur_end` 是「已处理过的所有区间的并集」的最右端点。

**Containment（LC-1288）的不变量**：
> 扫描到第 `i` 个区间时，`max_end` 是**前 i-1 个区间 end 的最大值**。
> 因为 start 已排序，`end <= max_end` 就是「被某个前面的区间完全覆盖」的充要条件。

**Difference（LC-1272）的不变量**：
> 每一段的输出都落在该段的原范围内，且段内先输出左残块再输出右残块
> ⟹ **有序性和互不相交性从输入继承下来**，不需要额外整理。

---

## 为什么用这种排序

| 题 | 排序键 | 为什么 |
|---|---|---|
| LC-0056 Merge | **start 升序**（end 随意） | 要的是并集。按 start 扫才能保证「相交的一定相邻」 |
| LC-0057 Insert | **不排序** | 输入已有序 |
| LC-1288 Covered | **start 升序，end 降序** | ⬇️ 见下 |
| LC-1272 Remove | **不排序** | 输入已有序 |
| LC-0228 / LC-0163 | **不排序** | 输入已是有序整数数组 |

### LC-1288 为什么 end 必须**降序**（全题唯一的坑）

反例 `[[1,4],[1,2]]`，答案应该是 **1**（`[1,2]` 被 `[1,4]` 覆盖）：

| tie-break | 排序结果 | 扫到 `[1,2]` 时 `max_end` | 结果 |
|---|---|---|---|
| end **降序** | `[1,4], [1,2]` | 4 ⟹ `2 <= 4` ⟹ 删 | ✅ 1 |
| end **升序** | `[1,2], [1,4]` | 0 ⟹ `2 > 0` ⟹ 保留 | ❌ 2 |

> **同起点时，长的必须排在前面，短的才会被判定为「被覆盖」。**
> 小样例（互不相交的输入）测不出这个 bug，必须专门造同起点的用例。

---

## 当前选择规则 + 简短正确性证明

### Merge Intervals（LC-0056）

**规则**：`start > cur_end` 开新段，否则 `cur_end = max(cur_end, end)`。

**证明（为什么只维护当前最右端点就够）**：
排序后 start 单调不减。设已处理的区间的并集最右端点是 `cur_end`。
对下一个区间 `[s, e]`：
- 若 `s > cur_end`，则 `[s, e]` 与**任何**已处理区间都不相交
  （它们的右端点都 `<= cur_end < s`）⟹ 必须开新段。
- 若 `s <= cur_end`，则它与当前段相交 ⟹ 并入，新的右端点是 `max(cur_end, e)`。

更远的历史信息（每个旧区间各自的端点）在后续判断中**永远用不到**，
因为 start 单调 ⟹ 后面的区间只可能和「最右端」发生关系。∎

### Remove Covered Intervals（LC-1288）

**规则**：按 `(start ↑, end ↓)` 排序，`end <= max_end` 就删。

**证明（为什么 start 升序 + end 降序足以判断覆盖）**：
覆盖条件是 `c <= a and b <= d`（`[a,b]` 被 `[c,d]` 覆盖）。
排序后所有在前面的区间都满足 `c <= a`（第一个条件**自动成立**）
⟹ 只需检查第二个条件 `b <= d`，而 `d` 能取到的最大值就是 `max_end`。
同起点时 end 降序保证了「同起点中最长的那个」先被扫到并写进 `max_end`。∎

---

## Python 模板

### Template 1：Sort + Merge

```python
def merge(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])          # ! start 升序
    res = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s > res[-1][1]:                      # ! 不相交 ⟹ 开新段
            res.append([s, e])
        else:                                   # ! 相交 ⟹ 并入
            res[-1][1] = max(res[-1][1], e)     # ! max 不能省
    return res
```
**O(n log n)** 时间（排序主导）、O(n) 输出空间。

### Template 2：Insert Interval（三段式）

```python
def insert(intervals, new):
    res, i, n = [], 0, len(intervals)
    # ① 左边：整段在 new 左侧，原样搬
    while i < n and intervals[i][1] < new[0]:
        res.append(intervals[i]); i += 1
    # ② 中间：和 new 相交的，全部吃进 new
    s, e = new
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    res.append([s, e])
    # ③ 右边：剩下的原样搬
    res.extend(intervals[i:])
    return res
```
**O(n)** 时间（输入已排序，**不要 sort**）、O(n) 输出空间。

### Template 2'：Remove Interval（区间减法，两行覆盖四种形态）

```python
def removeInterval(intervals, toBeRemoved):
    c, d = toBeRemoved
    res = []
    for a, b in intervals:
        if a < c: res.append([a, min(b, c)])    # ! 左残块
        if d < b: res.append([max(a, d), b])    # ! 右残块（可能和左残块一起出现 ⟹ 裂成两段）
    return res
```
**O(n)** 时间、O(n) 输出空间。

### Template 1'：Containment（LC-1288）

```python
def removeCoveredIntervals(intervals):
    intervals.sort(key=lambda x: (x[0], -x[1]))  # ! start ↑, end ↓
    kept, max_end = 0, 0
    for _, e in intervals:
        if e > max_end:                          # ! 没被覆盖
            kept += 1
            max_end = e
    return kept
```
**O(n log n)** 时间、O(1) 额外空间。

### 连续段扫描（LC-0228 / LC-0163）

```python
# LC-0228：输出存在的连续段
i, n, res = 0, len(nums), []
while i < n:
    j = i
    while j + 1 < n and nums[j + 1] == nums[j] + 1:
        j += 1
    res.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
    i = j + 1

# LC-0163：输出缺失的段 —— 加 lower-1 / upper+1 两个哨兵，然后看相邻差 >= 2
prev = lower - 1
for x in nums + [upper + 1]:
    if x - prev >= 2:
        res.append([prev + 1, x - 1])
    prev = x
```
两者都是 **O(n)** 时间。

---

## 代表题目

| # | 题 | 优先级 | 模板 | 端点 |
|---|---|---|---|---|
| 1 | [LC-0056 Merge Intervals](<./01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>) | **P0** | Sort + Merge | 闭（相邻要合并） |
| 2 | [LC-0057 Insert Interval](<./01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>) | **P0** | 三段式 | 闭 |
| 3 | [LC-1288 Remove Covered Intervals](<./02 - 区间包含与冗余消除/01 - LC-1288 - Remove Covered Intervals>) | P1 | (start ↑, end ↓) | 半开（按闭做答案相同） |
| 4 | [LC-1272 Remove Interval](<./02 - 区间包含与冗余消除/02 - LC-1272 - Remove Interval>) | P1+ | 区间减法 | **半开** |
| 5 | [LC-0228 Summary Ranges](<./03 - 连续整数区间与缺失范围/01 - LC-0228 - Summary Ranges>) | P2 | 连续段扫描 | — |
| 6 | [LC-0163 Missing Ranges](<./03 - 连续整数区间与缺失范围/02 - LC-0163 - Missing Ranges>) | P2 | 连续段扫描 + 哨兵 | 闭 |

---

## 典型边界情况

| 边界 | 例子 | 期望 |
|---|---|---|
| 端点相接 | `merge([[1,2],[2,3]])` | `[[1,3]]`（**合并** —— 这里 `<=` 是对的） |
| 完全包含 | `merge([[1,10],[2,3]])` | `[[1,10]]`（`max` 生效） |
| 完全相同 | `removeCovered([[1,2],[1,2]])` | `1` |
| 同起点不同终点 | `removeCovered([[1,4],[1,2]])` | `1`（tie-break 的试金石） |
| 空输入 | `merge([])` | `[]` |
| 完全无重叠 | `merge([[1,2],[5,6]])` | 原样 |
| 减法裂成两段 | `removeInterval([[0,5]], [2,3])` | `[[0,2],[3,5]]` |
| 减法吃光整段 | `removeInterval([[1,2]], [0,5])` | `[]` |
| 半开端点相接 | `removeInterval([[1,2]], [2,3])` | `[[1,2]]`（**不重叠**） |
| 163 的哨兵 | `findMissing([], lower=1, upper=1)` | `[[1,1]]` |
| 插入到最左/最右 | `insert([[3,5]], [1,2])` / `[6,8]` | 不合并 |

> ⚠️ **注意 LC-0056 和 LC-1272 的不等号方向相反**：
> 56 要把 `[1,2]` 和 `[2,3]` **合并**（`s <= cur_end`），
> 1272 认为 `[1,2)` 和 `[2,3)` **不重叠**（`a < c`）。
> 不是哪个写错了 —— **是题意不同**。见
> [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>)。

---

## 错误策略反例

| 错误做法 | 反例 | 结果 |
|---|---|---|
| `cur_end = end`（不用 max） | `[[1,10],[2,3],[4,5]]` | 得 `[[1,10],[4,5]]`，正确是 `[[1,10]]` |
| LC-1288 用 `(start ↑, end ↑)` | `[[1,4],[1,2]]` | 得 2，正确 1 |
| LC-0057 先 `sort()` | — | 不出错但白付 O(n log n)，面试会被追问 |
| LC-0056 只比较相邻两个的 end | `[[1,10],[2,3],[4,5]]` | 同第一行，嵌套区间把右界缩回去 |
| LC-1272 用 `<=` 判残块 | `removeInterval([[1,2]], [1,2])` | 吐出 `[1,1]`/`[2,2]` 空区间，正确是 `[]` |
| LC-0163 不加哨兵 | `nums=[]` | 漏掉 `[lower, upper]` 整段 |
| 把 LC-0228 和 LC-0163 当同一题 | — | 228 问「有什么」，163 问「缺什么」，还多两个边界 |

---

## 相邻 Pattern 对比

| | 本层（01） | [Level 1 · 02](<../02 - 双指针区间交集与多路合并>) | [Level 1 · 03](<../03 - 不重叠区间与贪心调度>) | [Level 1 · 04](<../04 - 重叠计数、扫描线与资源分配>) |
|---|---|---|---|---|
| 目标 | **并集 / 差集 / 规范化** | **交集** | **最大兼容数 / 最少点数** | **最大并发数** |
| 排序键 | start ↑（1288 加 end ↓） | 两边各自已有序 | **end ↑** | start ↑ 或事件排序 |
| 输出 | 区间列表 | 区间列表 | 一个计数 | 一个计数 / 一条数组 |
| 要不要 Heap | ❌ | 只有 k 路合并要 | ❌ | ✅（或差分/扫描线） |
| 关键陷阱 | `max` + tie-break | `left <= right` | **排序键是 end 不是 start** | 端点语义决定不等号 |

> **本层是地基**：Level 02–05 的输入全都假设「已经是规范形式」。
> 如果一道题的输入**没有**排好序或**有**重叠，第一步永远是回到这一层先规范化。

---

## 相关资料

- [Pattern Recognition Guide](<../_resources/pattern-recognition-guide.md>) — Q1 / Q2 / Q13 / Q14
- [Endpoint Semantics Cheat Sheet](<../_resources/endpoint-semantics-cheat-sheet.md>)
- [Interval Algorithm Comparison Table](<../_resources/interval-algorithm-comparison.md>)
- [P0 / P1 / P2 Roadmap](<../_resources/p0-p1-p2-roadmap.md>)
